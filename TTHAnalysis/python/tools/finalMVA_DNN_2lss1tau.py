from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput, loadHisto
from CMGTools.TTHAnalysis.tools.tfTool import TFTool
import os 
from math import sqrt, cos, sin
from copy import deepcopy
import ROOT as r 


def mTauTauVis( ev, ind, hist): 
    #file = r.TFile("/home/ucl/cp3/atalier/final_tth/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/data/TauIDSFs/TauES_dm_DeepTau2017v2p1VSjet_UL2018.root")
    #hist = file.Get('tes')
    #    tes  = hist.GetBinContent(hist.GetXaxis().FindBin(dm))

    all_leps = [l for l in Collection(ev,"LepGood")]
    nFO = getattr(ev,"nLepFO_Recl")
    chosen = getattr(ev,"iLepFO_Recl")
    leps = [all_leps[chosen[i]] for i in xrange(nFO)]
    if len(leps) < 2: return -1
    
    if ev.Tau_tight2lss1tau_idx < 0: return -1
    taus = [ t for t in Collection(ev, 'TauSel_Recl')]
    dms = [ d for d in Collection(ev, 'TauSel_Recl_decayMode')]

    #dm = ev.TauSel_Recl_decayMode
    #tes  = hist.GetBinContent(hist.GetXaxis().FindBin(dm))
    #print("ciao ", tes)
    return (leps[ind].p4() + (taus[int(ev.Tau_tight2lss1tau_idx)].p4()*hist.GetBinContent(hist.GetXaxis().FindBin(dms[int(ev.Tau_tight2lss1tau_idx)])) )).M()  

def massL3( ev, var, hist): 
    if ev.Tau_tight2lss1tau_idx < 0: return -1
    all_leps = [l for l in Collection(ev,"LepGood")]
    nFO = getattr(ev,"nLepFO_Recl")
    chosen = getattr(ev,"iLepFO_Recl")
    leps = [all_leps[chosen[i]] for i in xrange(nFO)]
    if len(leps) < 2: return 0

    taus = [ t for t in Collection(ev, 'TauSel_Recl')]
    dms = [ d for d in Collection(ev, 'TauSel_Recl_decayMode')]
    l1=r.TLorentzVector();l2=r.TLorentzVector()
    l1.SetPtEtaPhiM(leps[0].conePt, leps[0].eta, leps[0].phi, 0)
    l2.SetPtEtaPhiM(leps[1].conePt, leps[1].eta, leps[1].phi, 0)
    part = l1 + l2 + taus[int(ev.Tau_tight2lss1tau_idx)].p4()*hist.GetBinContent(hist.GetXaxis().FindBin(dms[int(ev.Tau_tight2lss1tau_idx)]))
    
    met_pt  = getattr(ev,'MET_pt%s'%var) 
    met_phi = getattr(ev,'MET_phi%s'%var)

    return sqrt(part.Pt()*met_pt*(1-cos(part.Phi()-met_phi)))


class finalMVA_DNN_2lss1tau(Module):
    def __init__(self, tesYear = "2018", variations=[], doSystJEC=True, fillInputs=False):
        file = r.TFile("/home/ucl/cp3/atalier/final_tth/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/data/TauIDSFs/TauES_dm_DeepTau2017v2p1VSjet_UL{}.root".format(tesYear))
        self.tesHist = file.Get('tes')
        self.outVars = []
        self._MVAs   = []
        self.fillInputs = fillInputs
        cats_2lss1tau =  ["predictions_ttH",  "predictions_rest", "predictions_tH"]
        varorder = ["lep1_conePt", "lep1_eta", "lep1_phi", "mT_lep1", "mindr_lep1_jet", "lep2_conePt", "lep2_eta", "lep2_phi", "mT_lep2", "mindr_lep2_jet", "tau1_pt", "tau1_eta", "tau1_phi", "mindr_tau_jet", "avg_dr_jet", "mbb_loose", "min_dr_Lep", "mTauTauVis1", "mTauTauVis2", "res_HTT", "HadTop_pt", "massL3", "min_Deta_leadfwdJet_jet", "leadFwdJet_eta", "leadFwdJet_pt", "met_LD", "jet1_pt", "jet1_eta", "jet1_phi", "jet2_pt", "jet2_eta", "jet2_phi", "jet3_pt", "jet3_eta", "jet3_phi", "nJet", "nBJetLoose", "nBJetMedium", "nJetForward", "nElectron", "sum_Lep_charge"]
        self.systsJEC = {0:"",\
                         1:"_jesTotalCorrUp"  , -1:"_jesTotalCorrDown",\
                         2:"_jesTotalUnCorrUp", -2: "_jesTotalUnCorrDown",\
                         3:"_jerUp", -3: "_jerDown",\
                     } if doSystJEC else {0:""}
        if len(variations): 
            self.systsJEC = {0:""}
            for i,var in enumerate(variations):
                self.systsJEC[i+1]   ="_%sUp"%var
                self.systsJEC[-(i+1)]="_%sDown"%var

        if fillInputs:
            self.outVars.extend(varorder+[('nEvent','L')])
            self.outVars.extend(['frWeight','HTXS_Higgs_pt','HTXS_Higgs_y','genWeight'])
            self.inputHelper = self.getVarsForVariation('')
            self.inputHelper['nEvent'] = lambda ev : ev.event
            self.inputHelper['HTXS_Higgs_pt'] = lambda ev : ev.HTXS_Higgs_pt if hasattr(ev, 'HTXS_Higgs_pt') else 0
            self.inputHelper['HTXS_Higgs_y'] = lambda ev : ev.HTXS_Higgs_y  if hasattr(ev, 'HTXS_Higgs_pt') else 0
            self.inputHelper['genWeight'] = lambda ev : ev.genWeight
            self.fakerate={}
            for year in '2016APV_2016,2017,2018'.split(','):
                self.fakerate[year]={}
                self.fakerate[year][11]=loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/fakerate/fr_%s.root'%year, 'FR_mva090_el_TT')
                self.fakerate[year][13]=loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/fakerate/fr_%s.root'%year, 'FR_mva085_mu_TT')
                
        for var in self.systsJEC: 
            self._MVAs.append( TFTool('DNN_2lss1tau%s'%self.systsJEC[var], os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/2lss_1tau_DNN_legacy.pb',
                                      self.getVarsForVariation(self.systsJEC[var]), cats_2lss1tau, varorder, outputNodename='dense_40/Softmax'))

            self.outVars.extend( ['DNN_2lss1tau%s_'%self.systsJEC[var] + x for x in cats_2lss1tau])

        vars_2lss1tau_unclEnUp = deepcopy(self.getVarsForVariation(''))
        vars_2lss1tau_unclEnUp['met_LD'                 ] =  lambda ev : ev.MET_pt_unclustEnUp  *0.6 + ev.mhtJet25_Recl*0.4
        vars_2lss1tau_unclEnUp["mT_lep1"          ] =  lambda ev : ev.MT_met_lep1_unclustEnUp
        vars_2lss1tau_unclEnUp["mT_lep2"          ] =  lambda ev : ev.MT_met_lep2_unclustEnUp

        vars_2lss1tau_unclEnDown = deepcopy(self.getVarsForVariation(''))
        vars_2lss1tau_unclEnDown['met_LD'                 ] =  lambda ev : ev.MET_pt_unclustEnDown*0.6 + ev.mhtJet25_Recl*0.4
        vars_2lss1tau_unclEnDown["mT_lep1"          ] =  lambda ev : ev.MT_met_lep1_unclustEnDown
        vars_2lss1tau_unclEnDown["mT_lep2"          ] =  lambda ev : ev.MT_met_lep2_unclustEnDown

        worker_2lss1tau_unclUp   = TFTool("DNN_2lss1tau_unclUp", os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/2lss_1tau_DNN_legacy.pb', vars_2lss1tau_unclEnUp, cats_2lss1tau, varorder, outputNodename='dense_40/Softmax')
        worker_2lss1tau_unclDown = TFTool("DNN_2lss1tau_unclDown", os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/2lss_1tau_DNN_legacy.pb', vars_2lss1tau_unclEnDown,cats_2lss1tau,  varorder, outputNodename='dense_40/Softmax')

        self._MVAs.extend( [ worker_2lss1tau_unclUp, worker_2lss1tau_unclDown])
        self.outVars.extend( ['DNN_2lss1tau_unclUp_' + x for x in cats_2lss1tau] +  ['DNN_2lss1tau_unclDown_' + x for x in cats_2lss1tau])


    def getVarsForVariation(self, var):
        return {'avg_dr_jet'             : lambda ev : getattr(ev,'avg_dr_jet%s'%var),
                'min_dr_Lep'             : lambda ev : min([ev.drlep12, ev.drlep13, ev.drlep23]),
                'jet1_pt'                : lambda ev : getattr(ev,'JetSel_Recl_pt%s'%var)[0] if getattr(ev,'nJet25%s_Recl'%var) > 0 else 0,
                'lep1_conePt'            : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[0])], 
                'mindr_lep1_jet'         : lambda ev : getattr(ev,'mindr_lep1_jet%s'%var),
                'jet2_pt'                : lambda ev : getattr(ev,'JetSel_Recl_pt%s'%var)[1] if getattr(ev,'nJet25%s_Recl'%var) > 1 else 0,
                'leadFwdJet_pt'          : lambda ev : getattr(ev,'FwdJet1_pt%s_Recl'%var) if getattr(ev,'nFwdJet%s_Recl'%var) else 0,
                'mindr_lep2_jet'         : lambda ev : getattr(ev,'mindr_lep2_jet%s'%var),                   
                'nBJetMedium'            : lambda ev : getattr(ev,'nBJetMedium25%s_Recl'%var),
                'mbb_loose'              : lambda ev : getattr(ev,'mbb_loose%s'%var),
                'met_LD'                 : lambda ev : getattr(ev,'MET_pt%s'%var) *0.6 + getattr(ev,'mhtJet25%s_Recl'%var)*0.4,
                'lep2_conePt'            : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[1])],
                'jet1_eta'               : lambda ev : abs(ev.JetSel_Recl_eta[0]) if getattr(ev,'nJet25%s_Recl'%var) > 0 else 0,
                'jet3_pt'                : lambda ev : getattr(ev,'JetSel_Recl_pt%s'%var)[2] if getattr(ev,'nJet25%s_Recl'%var) > 2 else 0,
                'HadTop_pt'              : lambda ev : getattr(ev,'BDThttTT_eventReco_HadTop_pt%s'%var) if  getattr(ev,'BDThttTT_eventReco_mvaValue%s'%var) > 0 else 0,
                'sum_Lep_charge'         : lambda ev : (ev.LepGood_charge[int(ev.iLepFO_Recl[0])]+ev.LepGood_charge[int(ev.iLepFO_Recl[1])]+ev.LepGood_charge[int(ev.iLepFO_Recl[2])]) if ev.nLepFO_Recl >= 3 else 0,
                'nJet'                   : lambda ev : getattr(ev,'nJet25%s_Recl'%var),
                'res_HTT'                : lambda ev : getattr(ev,'BDThttTT_eventReco_mvaValue%s'%var) if getattr(ev,'BDThttTT_eventReco_mvaValue%s'%var) > 0 else 0,
                'lep1_eta'               : lambda ev : abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]) if ev.nLepFO_Recl >= 1 else 0,
                'lep2_eta'               : lambda ev : abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])]) if ev.nLepFO_Recl >= 2 else 0,
                'min_Deta_leadfwdJet_jet': lambda ev : getattr(ev,'min_Deta_leadfwdJet_jet%s'%var),
                'jet2_phi'               : lambda ev : ev.JetSel_Recl_phi[1] if getattr(ev,'nJet25%s_Recl'%var) >= 2 else 0,
                'jet1_phi'               : lambda ev : ev.JetSel_Recl_phi[0] if getattr(ev,'nJet25%s_Recl'%var) >= 1 else 0,
                'lep2_phi'               : lambda ev : (ev.LepGood_phi[int(ev.iLepFO_Recl[1])]) if ev.nLepFO_Recl >= 2 else 0,
                'leadFwdJet_eta'         : lambda ev : abs(getattr(ev,'FwdJet1_eta%s_Recl'%var)) if getattr(ev,'nFwdJet%s_Recl'%var) else 0,
                'jet3_eta'               : lambda ev : abs(ev.JetSel_Recl_eta[2]) if getattr(ev,'nJet25%s_Recl'%var) >= 3 else 0,
                'jet2_eta'               : lambda ev : abs(ev.JetSel_Recl_eta[1]) if getattr(ev,'nJet25%s_Recl'%var) >= 2 else 0,
                'nElectron'              : lambda ev : ((abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[0])]) == 11) + (abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[1])]) == 11) + (abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[2])]) == 11)) if ev.nLepFO_Recl >= 3 else 0,
                'lep1_phi'               : lambda ev : (ev.LepGood_phi[int(ev.iLepFO_Recl[0])]) if ev.nLepFO_Recl >= 1 else 0,
                'jet3_phi'               : lambda ev : ev.JetSel_Recl_phi[2] if getattr(ev,'nJet25%s_Recl'%var) >= 3 else 0,
                'nBJetLoose'             : lambda ev : getattr(ev,'nBJetLoose25%s_Recl'%var),
                'nJetForward'            : lambda ev : getattr(ev,'nFwdJet%s_Recl'%var),
                "mT_lep1"                : lambda ev : getattr(ev,'MT_met_lep1%s'%var),
                "mT_lep2"                : lambda ev : getattr(ev,'MT_met_lep2%s'%var),
                'tau1_pt'                : lambda ev : ev.TauSel_Recl_pt [int(ev.Tau_tight2lss1tau_idx)]*self.tesHist.GetBinContent(self.tesHist.GetXaxis().FindBin(ev.TauSel_Recl_decayMode[int(ev.Tau_tight2lss1tau_idx)])) if ev.Tau_tight2lss1tau_idx > -1 else 0, 
                'tau1_eta'               : lambda ev : ev.TauSel_Recl_eta[int(ev.Tau_tight2lss1tau_idx)] if ev.Tau_tight2lss1tau_idx > -1 else 0, 
                'tau1_phi'               : lambda ev : ev.TauSel_Recl_phi[int(ev.Tau_tight2lss1tau_idx)] if ev.Tau_tight2lss1tau_idx > -1 else 0, 
                'mindr_tau_jet'          : lambda ev : getattr(ev,'mindr_tau_jet%s'%var),
                'mTauTauVis1'            : lambda ev : mTauTauVis(ev, 0, self.tesHist),
                'mTauTauVis2'            : lambda ev : mTauTauVis(ev, 1, self.tesHist),
                'massL3'                 : lambda ev : massL3(ev, var, self.tesHist),

            }



    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        #print self.outVars
        declareOutput(self, wrappedOutputTree, self.outVars)
        
    def analyze(self,event):
        myvars = [event.iLepFO_Recl[0],event.iLepFO_Recl[1],event.iLepFO_Recl[2]]
        ret = []

        # if we want to train we wont take all the inputs
        if self.fillInputs:
            for var in self.inputHelper:
                ret.append( (var, self.inputHelper[var](event)))

            all_leps = [l for l in Collection(event,"LepGood")]
            nFO = getattr(event,"nLepFO_Recl")
            chosen = getattr(event,"iLepFO_Recl")
            leps = [all_leps[chosen[i]] for i in xrange(nFO)]

            if len(leps) < 2: return False
            if event.nJet25_Recl < 2: return False
            if event.nTauSel_Recl_2lss1tau_Tight < 1: return False

            # we scale fake leptons by the fake rate so we reproduce better the kinematics
            frWeight=1 
            year=str(event.year) if event.year in [2017,2018] else '2016APV_2016'
            for l in leps[:2]:
                if l.mcMatchId: continue # dont scale prompt or flips, we assume similar kinematics in FO and SR
                thebin=self.fakerate[year][abs(l.pdgId)].FindBin( l.conePt, abs(l.eta))
                frWeight*=self.fakerate[year][abs(l.pdgId)].GetBinContent(thebin)
            ret.append( ('frWeight', frWeight))


        for worker in self._MVAs:
            name = worker.name
            if not hasattr(event,"nJet25_jerUp_Recl") and ('_jes' in name or  '_jer' in name or '_uncl' in name): continue # using jer bc components wont change
            ret.extend( [(x,y) for x,y in worker(event).iteritems()])
            

            
        writeOutput(self, dict(ret))
        return True
