from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.tools.tfTool import TFTool
import os 
from copy import deepcopy
import ROOT as r

class finalMVA_DNN(Module):
    def __init__(self, variations=[], doSystJEC=True, fillInputs=False):
        self.outVars = []
        self._MVAs   = {}
        self.vars_2lss = {}
        self.fillInputs = fillInputs
        self.varorder = ["jet3_pt","jet3_eta","lep1_eta","jet2_pt","jet1_pt","jetFwd1_eta","mT_lep1","mT_lep2","jet4_phi","lep2_conePt","hadTop_BDT","jet1_phi","jet2_eta","n_presel_jetFwd","n_presel_jet","lep1_charge","avg_dr_jet","lep1_phi","Hj_tagger_hadTop","nBJetLoose","jet4_pt","mindr_lep1_jet","lep1_conePt","jetFwd1_pt","lep2_phi","jet2_phi","lep2_eta","mbb","mindr_lep2_jet","jet4_eta","nBJetMedium","Dilep_pdgId","metLD","jet3_phi","maxeta","jet1_eta"]
        self.cats_2lss = ['predictions_ttH_low_Higgs_pt', 'predictions_ttH_high_Higgs_pt', 'predictions_Rest','predictions_ttW','predictions_tHQ']

        if fillInputs:
            self.outVars.extend(self.varorder+['nEvent'])
            self.inputHelper = self.getVarsForVariation('')
            self.inputHelper['nEvent'] = lambda ev : ev.event

        self.systsJEC = {0:""}

        if len(variations) > 0:
            for i,var in enumerate(variations):
                self.systsJEC[i+1]   ="_%sUp"%var
                self.systsJEC[-(i+1)]="_%sDown"%var

        input_shapes = r.vector(r.vector('float'))()

        for var in self.systsJEC:
            input_names = r.vector('string')()
            input_names.push_back('input_1')
            output_names = r.vector('string')()
            output_names.push_back('Dense_output')
            self._MVAs['DNN_2lss%s'%self.systsJEC[var]] = r.ONNXInterface(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/2lss_MVADiscr_UL.onnx', input_shapes,
                                               input_names, output_names)

            self.vars_2lss['DNN_2lss%s'%self.systsJEC[var]] = self.getVarsForVariation(self.systsJEC[var])

            self.outVars.extend( ['DNN_2lss%s_'%self.systsJEC[var] + x for x in self.cats_2lss])

        if len(variations) > 0:
            vars_2lss_unclUp = deepcopy(self.getVarsForVariation(''))
            vars_2lss_unclUp["metLD"            ] =  lambda ev : (ev.MET_T1_pt_unclustEnUp ) *0.6 + ev.mhtJet25_Recl*0.4
            vars_2lss_unclUp["mT_lep1"          ] =  lambda ev : ev.MT_met_lep1_unclustEnUp
            vars_2lss_unclUp["mT_lep2"          ] =  lambda ev : ev.MT_met_lep2_unclustEnUp
            self.outVars.extend( ['DNN_2lss_unclUp_' + x for x in self.cats_2lss])

            vars_2lss_unclDown = deepcopy(self.getVarsForVariation(''))
            vars_2lss_unclDown["metLD"            ] =  lambda ev : (ev.MET_T1_pt_unclustEnDown) *0.6 + ev.mhtJet25_Recl*0.4
            vars_2lss_unclDown["mT_lep1"          ] =  lambda ev : ev.MT_met_lep1_unclustEnDown
            vars_2lss_unclDown["mT_lep2"          ] =  lambda ev : ev.MT_met_lep2_unclustEnDown
            self.outVars.extend( ['DNN_2lss_unclDown_' + x for x in self.cats_2lss])

            self._MVAs['DNN_2lss_unclUp'] = r.ONNXInterface(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/2lss_MVADiscr_UL.onnx', input_shapes,
                                                   input_names, output_names)
            self._MVAs['DNN_2lss_unclDown'] = r.ONNXInterface(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/2lss_MVADiscr_UL.onnx', input_shapes,
                                                   input_names, output_names)

            self.vars_2lss['DNN_2lss_unclUp'] = vars_2lss_unclUp
            self.vars_2lss['DNN_2lss_unclDown'] = vars_2lss_unclDown

        

    def getVarsForVariation(self, var ):
        return {"jet3_pt": lambda ev: getattr(ev, 'JetSel_Recl_pt%s' % var)[2] if getattr(ev,'nJet25%s_Recl' % var) > 2 else -9,
                "jet3_eta": lambda ev: abs(ev.JetSel_Recl_eta[2]) if getattr(ev, 'nJet25%s_Recl' % var) > 2 else 9,
                "lep1_eta": lambda ev: ev.LepGood_eta[int(ev.iLepFO_Recl[0])] if ev.nLepFO_Recl >= 1 else 0,
                "jet2_pt": lambda ev: getattr(ev, 'JetSel_Recl_pt%s' % var)[1] if getattr(ev,'nJet25%s_Recl' % var) > 1 else -9,
                "jet1_pt": lambda ev: getattr(ev, 'JetSel_Recl_pt%s' % var)[0] if getattr(ev,'nJet25%s_Recl' % var) > 0 else -9,
                "jetFwd1_eta": lambda ev: abs(getattr(ev, 'FwdJet1_eta%s_Recl' % var)) if getattr(ev,'nFwdJet%s_Recl' % var) else 9,
                "mT_lep1": lambda ev: getattr(ev, 'MT_met_lep1%s' % var),
                "mT_lep2": lambda ev: getattr(ev, 'MT_met_lep2%s' % var),
                "jet4_phi": lambda ev: ev.JetSel_Recl_phi[3] if getattr(ev, 'nJet25%s_Recl' % var) > 3 else -9,
                "lep2_conePt": lambda ev: ev.LepGood_conePt[int(ev.iLepFO_Recl[1])],
                "hadTop_BDT": lambda ev: getattr(ev, 'BDThttTT_eventReco_mvaValue%s' % (var)) if getattr(ev,'BDThttTT_eventReco_mvaValue%s' % (var)) > 0 else -9,
                "jet1_phi": lambda ev: ev.JetSel_Recl_phi[0] if getattr(ev, 'nJet25%s_Recl' % var) > 0 else -9,
                "jet2_eta": lambda ev: abs(ev.JetSel_Recl_eta[1]) if getattr(ev, 'nJet25%s_Recl' % var) > 1 else 9,
                "n_presel_jetFwd": lambda ev: getattr(ev, 'nFwdJet%s_Recl' % var),
                "n_presel_jet": lambda ev: getattr(ev, 'nJet25%s_Recl' % var),
                "lep1_charge": lambda ev: ev.LepGood_charge[int(ev.iLepFO_Recl[0])],
                "avg_dr_jet": lambda ev: getattr(ev, 'avg_dr_jet%s' % var) if getattr(ev,'avg_dr_jet%s' % var) > 0 else -9,
                "lep1_phi": lambda ev: (ev.LepGood_phi[int(ev.iLepFO_Recl[0])]) if ev.nLepFO_Recl >= 1 else -9,
                "Hj_tagger_hadTop": lambda ev: getattr(ev, 'BDThttTT_eventReco_Hj_score%s' % (var)) if getattr(ev,'BDThttTT_eventReco_Hj_score%s' % (var)) > 0 else -9,
                "nBJetLoose": lambda ev: getattr(ev, 'nBJetLoose25%s_Recl' % var),
                "jet4_pt": lambda ev: getattr(ev, 'JetSel_Recl_pt%s' % var)[3] if getattr(ev,'nJet25%s_Recl' % var) > 3 else -9,
                "mindr_lep1_jet": lambda ev: getattr(ev, 'mindr_lep1_jet%s' % var),
                "lep1_conePt": lambda ev: ev.LepGood_conePt[int(ev.iLepFO_Recl[0])],
                "jetFwd1_pt": lambda ev: getattr(ev, 'FwdJet1_pt%s_Recl' % var) if getattr(ev,'nFwdJet%s_Recl' % var) else -9,
                "lep2_phi": lambda ev: (ev.LepGood_phi[int(ev.iLepFO_Recl[1])]) if ev.nLepFO_Recl >= 2 else -9,
                "jet2_phi": lambda ev: ev.JetSel_Recl_phi[1] if getattr(ev, 'nJet25%s_Recl' % var) >= 2 else -9,
                "lep2_eta": lambda ev: ev.LepGood_eta[int(ev.iLepFO_Recl[1])] if ev.nLepFO_Recl >= 2 else -9,
                "mbb": lambda ev: getattr(ev, 'mbb_medium%s' % var) if getattr(ev, 'mbb_medium%s' % var) != 0 else -9,
                "mindr_lep2_jet": lambda ev: getattr(ev, 'mindr_lep2_jet%s' % var),
                "jet4_eta": lambda ev: abs(ev.JetSel_Recl_eta[3]) if getattr(ev, 'nJet25%s_Recl' % var) > 3 else 9,
                "nBJetMedium": lambda ev: getattr(ev, 'nBJetMedium25%s_Recl' % var),
                "Dilep_pdgId": lambda ev: (28 - abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[0])]) - abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[1])])) / 2,
                "metLD": lambda ev: (getattr(ev, 'MET_pt') if var == '' else getattr(ev,'MET_T1_pt%s' % var)) * 0.6 + getattr(ev, 'mhtJet25%s_Recl' % var) * 0.4,
                "jet3_phi": lambda ev: ev.JetSel_Recl_phi[2] if getattr(ev, 'nJet25%s_Recl' % var) >= 3 else -9,
                "maxeta": lambda ev: max([abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]), abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])])]),
                "jet1_eta": lambda ev: abs(ev.JetSel_Recl_eta[0]) if getattr(ev, 'nJet25%s_Recl' % var) > 0 else 9,
                }


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        # print(self.outVars)
        declareOutput(self, wrappedOutputTree, self.outVars)
        
    def analyze(self,event):
        myvars = [event.iLepFO_Recl[0],event.iLepFO_Recl[1],event.iLepFO_Recl[2]]
        ret = {}

        for name in self._MVAs.keys():

            # print(name)

            if len(self.vars_2lss.keys()) > 1:

                try:
                    _1 = hasattr(event, "nJet25_jerUp_Recl")
                except RuntimeError:
                    _1 = False

                try:
                    _2 = hasattr(event, "nJet25_jesBBEC1_yearDown_Recl")
                except RuntimeError:
                    _2 = False
                finally:
                    if ( not _1 and not _2) and ('_jes' in name or  '_jer' in name or '_uncl' in name): continue # using jer bc components wont change

            inputs = r.vector(r.vector('float'))()
            subinputs = r.vector('float')()
            for var in self.varorder:
                # print(f'  {var}')
                subinputs.push_back(self.vars_2lss[name][var](event))
                if self.fillInputs:
                    ret[var] = self.vars_2lss[name][var](event)
            inputs.push_back(subinputs)

            worker = self._MVAs[name]

            _output = worker.run(inputs)[0]
            del inputs
            del subinputs

            i = 0
            for output_name in self.cats_2lss:
                ret[f'{name}_{output_name}'] = _output[i]
                i += 1

        writeOutput(self, ret)
        return True
