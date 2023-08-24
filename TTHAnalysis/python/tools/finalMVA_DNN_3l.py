from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.tools.tfTool import TFTool
import os 
from math import sqrt, cos, sin
from copy import deepcopy
import ROOT as r 



class finalMVA_DNN_3l(Module):
    def __init__(self, variations=[], fillInputs=False, doSystJEC=True):
        self.outVars = []
        self._MVAs   = {}
        self.vars_3l = {}
        self.fillInputs = fillInputs
        self.cats_3l =  ['predictions_ttH_low_Higgs_pt', 'predictions_ttH_high_Higgs_pt', "predictions_tH", "predictions_rest"]
        self.varorder = ['lep1_conePt', 'lep1_eta', 'lep1_phi', 'lep2_conePt', 'lep2_eta', 'lep2_phi', 'lep3_conePt', 'lep3_eta', 'lep3_phi',
                         'mindr_lep1_jet', 'mindr_lep2_jet', 'mindr_lep3_jet', 'min_dr_Lep', 'avg_dr_jet', 'met_LD', 'mbb_loose',
                         'leadFwdJet_eta', 'leadFwdJet_pt', 'min_Deta_leadfwdJet_jet', 'jet1_pt', 'jet1_eta', 'jet1_phi', 'jet2_pt', 'jet2_eta',
                         'jet2_phi', 'jet3_pt', 'jet3_eta', 'jet3_phi', 'sum_Lep_charge', 'HadTop_pt', 'res_HTT', 'nJet', 'nBJetLoose',
                         'nBJetMedium', 'nJetForward', 'nElectron', 'has_SFOS']

        if fillInputs:
            self.outVars.extend(self.varorder+['nEvent'])
            self.inputHelper = self.getVarsForVariation('')
            self.inputHelper['nEvent'] = lambda ev : ev.event

        self.systsJEC = {0:""}
        if len(variations): 
            self.systsJEC = {0:""}
            if len(variations) > 0:
                for i, var in enumerate(variations):
                    self.systsJEC[i + 1] = "_%sUp" % var
                    self.systsJEC[-(i + 1)] = "_%sDown" % var
                
        input_shapes = r.vector(r.vector('float'))()

        for var in self.systsJEC:
            input_names = r.vector('string')()
            input_names.push_back('input_1')
            output_names = r.vector('string')()
            output_names.push_back('Dense_output')
            self._MVAs['DNN_3l%s'%self.systsJEC[var]] = r.ONNXInterface(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/3l_MVADiscr_UL.onnx',
                                                                        input_shapes, input_names, output_names)

            self.vars_3l['DNN_3l%s'%self.systsJEC[var]] = self.getVarsForVariation(self.systsJEC[var])

            self.outVars.extend( ['DNN_3l%s_'%self.systsJEC[var] + x for x in self.cats_3l])


        if len(variations) > 0:
            vars_3l_unclEnUp = deepcopy(self.getVarsForVariation(''))
            vars_3l_unclEnUp['met_LD'                 ] =  lambda ev : ev.MET_pt_unclustEnUp*0.6 + ev.mhtJet25_Recl*0.4
            self.outVars.extend(['DNN_3l_unclUp_' + x for x in self.cats_3l])

            vars_3l_unclEnDown = deepcopy(self.getVarsForVariation(''))
            vars_3l_unclEnDown['met_LD'                 ] =  lambda ev : ev.MET_pt_unclustEnDown*0.6 + ev.mhtJet25_Recl*0.4
            self.outVars.extend(['DNN_3l_unclDown_' + x for x in self.cats_3l])

            self._MVAs['DNN_3l_unclUp'] = r.ONNXInterface(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/3l_MVADiscr_UL.onnx', input_shapes,
                                                          self.varorder, self.cats_3l)
            self._MVAs['DNN_3l_unclDown'] = r.ONNXInterface(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/3l_MVADiscr_UL.onnx', input_shapes,
                                                            self.varorder, self.cats_3l)

            self.vars_3l['DNN_3l_unclUp'] = vars_3l_unclEnUp
            self.vars_3l['DNN_3l_unclDown'] = vars_3l_unclEnDown


    def getVarsForVariation(self, var):
        return {'avg_dr_jet'             : lambda ev : getattr(ev,'avg_dr_jet%s'%var),
                'min_dr_Lep'             : lambda ev : min([ev.drlep12, ev.drlep13, ev.drlep23]),
                'jet1_pt'                : lambda ev : getattr(ev,'JetSel_Recl_pt%s'%var)[0] if getattr(ev,'nJet25%s_Recl'%var) > 0 else 0,
                'lep1_conePt'            : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[0])], 
                'mindr_lep1_jet'         : lambda ev : getattr(ev,'mindr_lep1_jet%s'%var),
                'jet2_pt'                : lambda ev : getattr(ev,'JetSel_Recl_pt%s'%var)[1] if getattr(ev,'nJet25%s_Recl'%var) > 1 else 0,
                'leadFwdJet_pt'          : lambda ev : getattr(ev,'FwdJet1_pt%s_Recl'%var) if getattr(ev,'nFwdJet%s_Recl'%var) else 0,
                'lep3_conePt'            : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[2])],
                'mindr_lep2_jet'         : lambda ev : getattr(ev,'mindr_lep2_jet%s'%var),                   
                'nBJetMedium'            : lambda ev : getattr(ev,'nBJetMedium25%s_Recl'%var),
                'mindr_lep3_jet'         : lambda ev : getattr(ev,'mindr_lep3_jet%s'%var), #### 
                'mbb_loose'              : lambda ev : getattr(ev,'mbb_loose%s'%var),
                'met_LD'                 : lambda ev : getattr(ev,'MET_pt%s'%var)*0.6 + getattr(ev,'mhtJet25%s_Recl'%var)*0.4,
                'lep2_conePt'            : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[1])],
                'jet1_eta'               : lambda ev : abs(ev.JetSel_Recl_eta[0]) if getattr(ev,'nJet25%s_Recl'%var) > 0 else 0,
                'jet3_pt'                : lambda ev : getattr(ev,'JetSel_Recl_pt%s'%var)[2] if getattr(ev,'nJet25%s_Recl'%var) > 2 else 0,
                'HadTop_pt'              : lambda ev : getattr(ev,'BDThttTT_eventReco_HadTop_pt%s'%var) if  getattr(ev,'BDThttTT_eventReco_mvaValue%s'%var) > 0 else 0,
                'has_SFOS'               : lambda ev : ev.hasOSSF3l,
                'sum_Lep_charge'         : lambda ev : (ev.LepGood_charge[int(ev.iLepFO_Recl[0])]+ev.LepGood_charge[int(ev.iLepFO_Recl[1])]+ev.LepGood_charge[int(ev.iLepFO_Recl[2])]) if ev.nLepFO_Recl >= 3 else 0,
                'nJet'                   : lambda ev : getattr(ev,'nJet25%s_Recl'%var),
                'lep3_eta'               : lambda ev : abs(ev.LepGood_eta[int(ev.iLepFO_Recl[2])]) if ev.nLepFO_Recl >= 3 else 0,
                'res_HTT'                : lambda ev : getattr(ev,'BDThttTT_eventReco_mvaValue%s'%var) if getattr(ev,'BDThttTT_eventReco_mvaValue%s'%var) > 0 else 0,
                'lep1_eta'               : lambda ev : abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]) if ev.nLepFO_Recl >= 1 else 0,
                'lep2_eta'               : lambda ev : abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])]) if ev.nLepFO_Recl >= 2 else 0,
                'lep3_eta'               : lambda ev : abs(ev.LepGood_eta[int(ev.iLepFO_Recl[2])]) if ev.nLepFO_Recl >= 3 else 0,
                'min_Deta_leadfwdJet_jet': lambda ev : getattr(ev,'min_Deta_leadfwdJet_jet%s'%var),
                'jet2_phi'               : lambda ev : ev.JetSel_Recl_phi[1] if getattr(ev,'nJet25%s_Recl'%var) >= 2 else 0,
                'jet1_phi'               : lambda ev : ev.JetSel_Recl_phi[0] if getattr(ev,'nJet25%s_Recl'%var) >= 1 else 0,
                'lep3_phi'               : lambda ev : (ev.LepGood_phi[int(ev.iLepFO_Recl[2])]) if ev.nLepFO_Recl >= 3 else 0,
                'lep2_phi'               : lambda ev : (ev.LepGood_phi[int(ev.iLepFO_Recl[1])]) if ev.nLepFO_Recl >= 2 else 0,
                'leadFwdJet_eta'         : lambda ev : abs(getattr(ev,'FwdJet1_eta%s_Recl'%var)) if getattr(ev,'nFwdJet%s_Recl'%var) else 0,
                'jet3_eta'               : lambda ev : abs(ev.JetSel_Recl_eta[2]) if getattr(ev,'nJet25%s_Recl'%var) >= 3 else 0,
                'jet2_eta'               : lambda ev : abs(ev.JetSel_Recl_eta[1]) if getattr(ev,'nJet25%s_Recl'%var) >= 2 else 0,
                'nElectron'              : lambda ev : ((abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[0])]) == 11) + (abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[1])]) == 11) + (abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[2])]) == 11)) if ev.nLepFO_Recl >= 3 else 0,
                'lep1_phi'               : lambda ev : (ev.LepGood_phi[int(ev.iLepFO_Recl[0])]) if ev.nLepFO_Recl >= 1 else 0,
                'jet3_phi'               : lambda ev : ev.JetSel_Recl_phi[2] if getattr(ev,'nJet25%s_Recl'%var) >= 3 else 0,
                'nBJetLoose'             : lambda ev : getattr(ev,'nBJetLoose25%s_Recl'%var),
                'nJetForward'            : lambda ev : getattr(ev,'nFwdJet%s_Recl'%var),
            }



    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self, wrappedOutputTree, self.outVars)
        
    def analyze(self,event):
        myvars = [event.iLepFO_Recl[0],event.iLepFO_Recl[1],event.iLepFO_Recl[2]]
        ret = {}

        for name in self._MVAs.keys():
            # print(name)

            if len(self.vars_3l.keys()) > 1:
                try:
                    _1 = hasattr(event, "nJet25_jerUp_Recl")
                except RuntimeError:
                    _1 = False
                finally:
                    if not _1 and ('_jes' in name or '_jer' in name or '_uncl' in name): continue  # using jer bc components wont change
            #
            # if self.fillInputs:
            #     all_leps = [l for l in Collection(event,"LepGood")]
            #     nFO = getattr(event,"nLepFO_Recl")
            #     chosen = getattr(event,"iLepFO_Recl")
            #     leps = [all_leps[chosen[i]] for i in range(nFO)]
            #
            #     if event.nJet25_Recl < 4 and event.MET_pt*0.6 + event.mhtJet25_Recl*0.4 < 30 + 15*(event.mZ1_Recl > 0): return False #met LD
            #     if len(leps) < 3: return False #trilep
            #     if abs(leps[0].charge + leps[1].charge + leps[2].charge) != 1: return False #q1
            #     # print(leps[0].isLepTight_Recl) # Could be used for tight cut TTT
            #     if event.nLepTight_Recl > 3: return False # exclusive
            #     if leps[0].conePt < 25 or leps[1].conePt < 15 or leps[2].conePt < 10: return False #pt251515
            #     if abs(event.mZ1_Recl-91.2) < 10: return False #ZVeto
            #     if event.minMllAFAS_Recl <= 12: return False #cleanup
            #     if event.nBJetLoose25_Recl < 2 or event.nBJetMedium25_Recl <1: return False #2b1B
            #     if event.mZ2_Recl > 0 and event.m4l < 140: return False #vetottHZZ
            #     if event.nTauSel_Recl_Tight != 0: return False #tauveto
            #     if event.nJet25_Recl < 2: return False #2j

            inputs = r.vector(r.vector('float'))()
            subinputs = r.vector('float')()
            for var in self.varorder:
                # print(f'  {var}')
                subinputs.push_back(self.vars_3l[name][var](event))
                if self.fillInputs:
                    ret[var] = self.vars_3l[name][var](event)
            inputs.push_back(subinputs)

            worker = self._MVAs[name]

            _output = worker.run(inputs)[0]
            del inputs
            del subinputs

            i = 0
            for output_name in self.cats_3l:
                ret[f'{name}_{output_name}'] = _output[i]
                i += 1

        writeOutput(self, ret)

        return True

