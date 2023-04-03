from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 

from copy import deepcopy
import ROOT
import os 
import numpy as np
import correctionlib
from CMGTools.TTHAnalysis.tools.nanoAOD.constants import _btagWPs

class btagSF_fixedWP(Module):
    def __init__(self, recllabel='Recl'):
        self.inputlabel = '_'+recllabel
        self.btvjson={}
        self.effhist={}
        self.effhist_loose={}
        for year in '2016postVFP,2016preVFP,2017,2018'.split(','):
            self.btvjson[year]=correctionlib.CorrectionSet.from_file( os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/btag/btagging_%s_UL.json.gz'%year)
            self.effhist[year]={}
            self.effhist_loose[year]={}
            for what in 'B,C,L'.split(','):
                if year == '2016preVFP' : theyear="2016apv"
                elif year == '2016postVFP': theyear="2016"
                else : theyear=year
                self.effhist[year][what]  =self.loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/btag/btagEffs_TopEFT_2022_05_16.root', 'BtagSF%s_DeepFlavM_%s'%(what,theyear))
                self.effhist_loose[year][what]  =self.loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/btag/btagEffs_TopEFT_2022_05_16_loose.root', 'BtagSF%s_DeepFlavM_%s'%(what,theyear))
        self.year_btvjson=None

        self.allUnct = "central,light_up_correlated,light_down_correlated,heavy_up_correlated,heavy_down_correlated,light_up_uncorrelated,light_down_uncorrelated,heavy_up_uncorrelated,heavy_down_uncorrelated".split(",")

    def loadHisto(self, fil, histname):
        tf = ROOT.TFile.Open(fil)
        if not tf: raise RuntimeError("No such file %s"%fil)
        hist = tf.Get(histname)
        if not hist: raise RuntimeError("No such object %s in %s"%(histname,fil))
        ret = deepcopy(hist)
        tf.Close()
        return ret


    def getFlavorBTV(self, flavor):
        '''                                                                                              
            Maps hadronFlavor to BTV flavor:                                                             
            Note the flavor convention: hadronFlavor is b = 5, c = 4, f = 0                              
            Convert them to the btagging group convention of 0, 1, 2                                     
        '''
        flavor_btv = None
        if abs(flavor) == 5:
            flavor_btv = 5
        elif abs(flavor) == 4:
            flavor_btv = 4
        elif abs(flavor) in [0, 1, 2, 3, 21]:
            flavor_btv = 0
        else:
            if self.verbose > 0:
                print((
                    "WARNING: Unknown flavor '%s', setting b-tagging SF to -1!" % repr(flavor)))
            return -1.
        return flavor_btv

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for syst in self.allUnct:
            outsyst = "" if syst == 'central' else "_" + syst
            self.out.branch( 'btagSF%s'%outsyst,'F')


    def computeSFforVar(self, var, what, flavors, etas, pts, discs, index, wp):
        sfs= self.year_btvjson[what].evaluate(var, wp, flavors[index], etas[index], pts[index])
        return sfs

    def getEff( self, pt, eta, flavor, wp='medium'):
        if wp == 'medium':
            thehist = self.year_eff['B' if flavor == 5 else 'C' if flavor == 4 else 'L']
        if wp == 'loose':
            thehist = self.year_looseeff['B' if flavor == 5 else 'C' if flavor == 4 else 'L']
        return thehist.GetBinContent( thehist.FindBin( min(149,pt), abs(eta) )) 


    def analyze(self, event):
        if self.year_btvjson is None:
            year='2018' if event.year == 2018 else '2017' if event.year == 2017 else '2016preVFP' if event.suberaId == 0 else '2016postVFP'
            self.year_btvjson  = self.btvjson[year] 
            self.year_eff      = self.effhist[year]
            self.year_looseeff = self.effhist_loose[year]

        jets = [j for j in Collection(event, "JetSel"+self.inputlabel)]
        btagSF=1
        flavors= np.array([])
        pts    = np.array([])
        etas   = np.array([])
        discs  = np.array([])
        effs_m   = np.array([])
        effs_l   = np.array([])

        for jet in jets:
            if jet.pt > 30:
                flavors  = np.append(flavors, self.getFlavorBTV(jet.hadronFlavour) ) 
                pts      = np.append(pts    , jet.pt ) 
                etas     = np.append(etas   , abs(jet.eta)) 
                discs    = np.append(discs  , jet.btagDeepFlavB ) 
                effs_m   = np.append(effs_m , self.getEff( jet.pt, jet.eta, self.getFlavorBTV(jet.hadronFlavour),wp='medium'))
                effs_l   = np.append(effs_l , self.getEff( jet.pt, jet.eta, self.getFlavorBTV(jet.hadronFlavour),wp='loose'))

        heavy = np.where(flavors != 0)
        light = np.where(flavors == 0)


        for syst in self.allUnct:
            syst_for_light = syst.replace("light_","") if 'light' in syst else 'central'
            syst_for_heavy = syst.replace("heavy_","") if 'heavy' in syst else 'central'
            
            heavy_medium=self.computeSFforVar( syst_for_heavy, 'deepJet_comb', flavors, etas, pts, discs, heavy , 'M') 
            light_medium=self.computeSFforVar( syst_for_light, 'deepJet_incl', flavors, etas, pts, discs, light , 'M')

            heavy_loose=self.computeSFforVar( syst_for_heavy, 'deepJet_comb', flavors, etas, pts, discs, heavy , 'L') 
            light_loose=self.computeSFforVar( syst_for_light, 'deepJet_incl', flavors, etas, pts, discs, light , 'L')


            p_data=1; p_mc=1
            suberastring='APV' if (hasattr(event, 'suberaId') and event.suberaId) == 1 else ''

            wpM = _btagWPs["DeepFlav_UL%d%s_%s"%(event.year, suberastring,"M")][1]
            wpL = _btagWPs["DeepFlav_UL%d%s_%s"%(event.year, suberastring,"L")][1]

            for mask,sf_med, sf_los in zip([heavy, light], [heavy_medium, light_medium], [heavy_loose, light_loose]):
                pass_m =np.where(discs[mask] >= wpM)
                pass_l_not_m=np.where((discs[mask] < wpM) &  (discs[mask] >= wpL))
                fail_l = np.where(discs[mask] < wpL)
                
                eff_m_mask=effs_m[mask]
                eff_l_mask=effs_l[mask]
                
                p_data*=np.prod(eff_m_mask[pass_m]*sf_med[pass_m])
                p_data*=np.prod((eff_l_mask[pass_l_not_m]*sf_los[pass_l_not_m]-eff_m_mask[pass_l_not_m]*sf_med[pass_l_not_m]))
                p_data*=np.prod((1-eff_l_mask[fail_l]*sf_los[fail_l]))
                p_mc*=np.prod(eff_m_mask[pass_m])
                p_mc*=np.prod(eff_l_mask[pass_l_not_m]-eff_m_mask[pass_l_not_m])
                p_mc*=np.prod(1-eff_l_mask[fail_l])
            
        

            outsyst = "" if syst == 'central' else "_" + syst
            self.out.fillBranch( 'btagSF%s'%outsyst, p_data/p_mc)

        
        return True

btagSF = lambda : btagSF_fixedWP()
