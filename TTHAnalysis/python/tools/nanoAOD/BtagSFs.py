from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
import ROOT 
import os, copy

class BtagSFs( Module ):
    def __init__(self, jetcoll="JetSel_Edge", suffix=""):
        self.jetcoll = jetcoll
        self.suffix  = suffix

        self.h_btag_eff_b    = {}
        self.h_btag_eff_c    = {}
        self.h_btag_eff_udsg = {}
        self.btagcut = {
            2016 : 0.6321,
            2017 : 0.4941,
            2018 : 0.4184
        }
        self.f_btag_eff      = ROOT.TFile(os.environ['CMSSW_BASE'] + "/src/CMGTools/TTHAnalysis/data/btag/btagEffs_Nanov4.root")
        for year in [2016,2017,2018]:
            self.h_btag_eff_b   [year] = copy.deepcopy(self.f_btag_eff.Get("h2_Eff_%d_btagDeepB_med_b"   %year))
            self.h_btag_eff_c   [year] = copy.deepcopy(self.f_btag_eff.Get("h2_Eff_%d_btagDeepB_med_c"   %year))
            self.h_btag_eff_udsg[year] = copy.deepcopy(self.f_btag_eff.Get("h2_Eff_%d_btagDeepB_med_udsg"%year))
        self.f_btag_eff.Close() 

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch('btagSF%s'%(self.suffix),'F')
        self.out.branch('btagSF%s_heavyUp'%(self.suffix),'F')
        self.out.branch('btagSF%s_lightUp'%(self.suffix),'F')
        self.out.branch('btagSF%s_heavyDown'%(self.suffix),'F')
        self.out.branch('btagSF%s_lightDown'%(self.suffix),'F')

    def getBtagEffFromFile(self, pt, eta, mcFlavour, year):

       pt_cutoff = max(20.,min(399., pt))
       if (abs(mcFlavour) == 5):
           h = self.h_btag_eff_b[year]
           #use pt bins up to 600 GeV for b
           pt_cutoff = max(20.,min(599., pt))
       elif (abs(mcFlavour) == 4):
           h = self.h_btag_eff_c[year]
       else:
           h = self.h_btag_eff_udsg[year]

       binx = h.GetXaxis().FindBin(pt_cutoff)
       biny = h.GetYaxis().FindBin(abs(eta))

       return h.GetBinContent(binx,biny)

    def analyze(self, event):
        jets = [ j for j in Collection(event, self.jetcoll)] 

        mcTag     = 1.
        mcNoTag   = 1.
        dataTag   = 1.
        dataNoTag = 1.

        dataTag_Hup     = 1.
        dataNoTag_Hup   = 1.
        dataTag_Hdown     = 1.
        dataNoTag_Hdown   = 1.

        dataTag_Lup     = 1.
        dataNoTag_Lup   = 1.
        dataTag_Ldown     = 1.
        dataNoTag_Ldown   = 1.

        for jet in jets:
            SF    = getattr(jet,'btagSF%s'%(self.suffix))
            SF_up = getattr(jet,'btagSF%s_up'%(self.suffix))
            SF_dn = getattr(jet,'btagSF%s_down'%(self.suffix))


            istag=False 
            if jet.pt < 35 or abs(jet.eta) > 2.4: continue
            mcFlavor = jet.hadronFlavour
            eff = self.getBtagEffFromFile(jet.pt, jet.eta, jet.hadronFlavour, event.year)
            
            if (jet.btagDeepB > self.btagcut[event.year]): 
                istag=True

            if(istag):
                mcTag = mcTag * eff
                dataTag = dataTag * eff * SF
                if(mcFlavor == 5 or mcFlavor ==4):
                    dataTag_Hup = dataTag_Hup*eff*SF_up
                    dataTag_Hdown = dataTag_Hdown*eff*SF_dn
                    dataTag_Lup = dataTag_Lup*eff*SF
                    dataTag_Ldown = dataTag_Ldown*eff*SF

                else:
                    dataTag_Hup = dataTag_Hup*eff*SF
                    dataTag_Hdown = dataTag_Hdown*eff*SF
                    dataTag_Lup = dataTag_Lup*eff*SF_up
                    dataTag_Ldown = dataTag_Ldown*eff*SF_dn


            else:
                mcNoTag = mcNoTag * (1 - eff)
                dataNoTag = dataNoTag * (1 - eff*SF)
                if mcFlavor==5 or mcFlavor==4:
                    dataNoTag_Hup   = dataNoTag_Hup * (1 - eff*SF_up)
                    dataNoTag_Hdown = dataNoTag_Hdown * (1 - eff*SF_dn)
                    dataNoTag_Lup   = dataNoTag_Lup * (1 - eff*SF)
                    dataNoTag_Ldown = dataNoTag_Ldown * (1 - eff*SF)
                else:
                    dataNoTag_Hup   = dataNoTag_Hup * (1 - eff*SF)
                    dataNoTag_Hdown = dataNoTag_Hdown * (1 - eff*SF)
                    dataNoTag_Lup   = dataNoTag_Lup * (1 - eff*SF_up)
                    dataNoTag_Ldown = dataNoTag_Ldown * (1 - eff*SF_dn)

            wtbtag           = (dataNoTag * dataTag ) / ( mcNoTag * mcTag )
            wtbtagUp_heavy   = (dataNoTag_Hup * dataTag_Hup ) / ( mcNoTag * mcTag )
            wtbtagUp_light   = (dataNoTag_Lup * dataTag_Lup ) / ( mcNoTag * mcTag )
            wtbtagDown_heavy = (dataNoTag_Hdown * dataTag_Hdown ) / ( mcNoTag * mcTag )
            wtbtagDown_light = (dataNoTag_Ldown * dataTag_Ldown ) / ( mcNoTag * mcTag )


            self.out.fillBranch('btagSF%s'%(self.suffix),wtbtag) 
            self.out.fillBranch('btagSF%s_heavyUp'%(self.suffix),wtbtagUp_heavy) 
            self.out.fillBranch('btagSF%s_lightUp'%(self.suffix),wtbtagUp_light) 
            self.out.fillBranch('btagSF%s_heavyDown'%(self.suffix),wtbtagDown_heavy) 
            self.out.fillBranch('btagSF%s_lightDown'%(self.suffix),wtbtagDown_light) 
        return True
