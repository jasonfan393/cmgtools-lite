from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.physicsobjects import _btagWPs as HiggsRecoTTHbtagwps

import ROOT, itertools
import numpy as np

class HiggsDiffRegressionTTH(Module):
    def __init__(self,label="_Recl", cut_BDT_rTT_score = 0.0, btagDeepCSVveto = 'M', doSystJEC=False):
        self.label = label
        self.cut_BDT_rTT_score = cut_BDT_rTT_score
        self.btagDeepCSVveto = btagDeepCSVveto
        self.branches = []
        self.systsJEC = {0:"", 1:"_jesTotalUp", -1:"_jesTotalDown"} if doSystJEC else {0:""}
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        # Independent on JES

        # Somehow dependent on JES

        for jesLabel in self.systsJEC.values():
            
            # Leptons
            for suffix in ["_pt", "_eta", "_phi", "_mass"]:
                # Leptons
                for iLep in range(3):
                    self.out.branch('%sLep%s%s%s'%(self.label,iLep,jesLabel,suffix)   , 'F') 
                self.out.branch('%sHadTop%s%s'%(self.label,jesLabel,suffix), 'F')
                # Jets
                self.out.branch('%sAll5_Jets%s%s'    %(self.label,jesLabel,suffix), 'F')
                self.out.branch('%sMore5_Jets%s%s'   %(self.label,jesLabel,suffix), 'F')
                self.out.branch('%sJets_plus_Lep%s%s'%(self.label,jesLabel,suffix), 'F')
            
            # Other variables    
            self.out.branch('%sTopScore%s'%(self.label,jesLabel)      , 'F')      
            self.out.branch('%smet%s'%(self.label,jesLabel)           , 'F')       
            self.out.branch('%smet_phi%s'%(self.label,jesLabel)       , 'F')
            self.out.branch('%sHTXS_Higgs%s_pt'%(self.label,jesLabel) , 'F')
            self.out.branch('%sHTXS_Higgs%s_y'%(self.label,jesLabel)  , 'F')
            self.out.branch('%sevt_tag%s'%(self.label,jesLabel)       , 'F')
            
    def analyze(self, event):

        # Some useful input parameters
        year=getattr(event,'year')
        btagvetoval=HiggsRecoTTHbtagwps['DeepFlav_%d_%s'%(year,self.btagDeepCSVveto)][1]

        nleps = getattr(event,"nLepGood")
        nFO = getattr(event,"nLepFO_Recl")
        ileps = getattr(event,"iLepFO_Recl")
        leps = Collection(event,"LepGood","nLepGood")
        lepsFO = [leps[ileps[i]] for i in xrange(nFO)]
        jets = [x for x in Collection(event,"JetSel_Recl","nJetSel_Recl")]
        (met, met_phi)  = event.MET_pt, event.MET_phi

        for jesLabel in self.systsJEC.values():
            score = getattr(event,"BDThttTT_eventReco_mvaValue%s"%jesLabel)
            
            # Hadronic top variables
            top1 = None
            j1top = None
            top2 = None
            j2top = None
            top3 = None
            j3top = None 
            HadTop = None

            if score>self.cut_BDT_rTT_score:

                j1top = int(getattr(event,"BDThttTT_eventReco_iJetSel1%s"%jesLabel))
                j2top = int(getattr(event,"BDThttTT_eventReco_iJetSel2%s"%jesLabel))
                j3top = int(getattr(event,"BDThttTT_eventReco_iJetSel3%s"%jesLabel))
                # make had top and fill
                top1 = ROOT.TLorentzVector(); top1.SetPtEtaPhiM(jets[j1top].p4().Pt(),jets[j1top].p4().Eta(), jets[j1top].p4().Phi(), jets[j1top].p4().M())
                top2 = ROOT.TLorentzVector(); top2.SetPtEtaPhiM(jets[j2top].p4().Pt(),jets[j2top].p4().Eta(), jets[j2top].p4().Phi(), jets[j2top].p4().M())
                top3 = ROOT.TLorentzVector(); top3.SetPtEtaPhiM(jets[j3top].p4().Pt(),jets[j3top].p4().Eta(), jets[j3top].p4().Phi(), jets[j3top].p4().M())
                HadTop = top1+top2+top3
                
            jetsNoTopNoB = [j for i,j in enumerate(jets) if i not in [j1top,j2top,j3top] and j.btagDeepB<btagvetoval]

            self.out.fillBranch('%sHadTop%s_pt'  %(self.label,jesLabel), HadTop.Pt()  if HadTop else -99.)
            self.out.fillBranch('%sHadTop%s_eta' %(self.label,jesLabel), HadTop.Eta() if HadTop else -99.)
            self.out.fillBranch('%sHadTop%s_phi' %(self.label,jesLabel), HadTop.Phi() if HadTop else -99.)
            self.out.fillBranch('%sHadTop%s_mass'%(self.label,jesLabel), HadTop.M()   if HadTop else -99.)
            self.out.fillBranch('%sTopScore%s'   %(self.label,jesLabel), score                          ) # else -99? Or not?

            evt_tag = 1

            # Lepton variables
            for iLep in range(3):
                if len(lepsFO) > iLep:
                    part = lepsFO[iLep].p4()
                    self.out.fillBranch('%sLep%s%s_pt'  %(self.label,iLep,jesLabel), part.Pt() )
                    self.out.fillBranch('%sLep%s%s_eta' %(self.label,iLep,jesLabel), part.Eta())
                    self.out.fillBranch('%sLep%s%s_phi' %(self.label,iLep,jesLabel), part.Phi())
                    self.out.fillBranch('%sLep%s%s_mass'%(self.label,iLep,jesLabel), part.M())
                else:
                    self.out.fillBranch('%sLep%s%s_pt'  %(self.label,iLep,jesLabel), -99 )
                    self.out.fillBranch('%sLep%s%s_eta' %(self.label,iLep,jesLabel), -99 )
                    self.out.fillBranch('%sLep%s%s_phi' %(self.label,iLep,jesLabel), -99 )
                    self.out.fillBranch('%sLep%s%s_mass'%(self.label,iLep,jesLabel), -99 )
 
            self.out.fillBranch('%sevt_tag%s'%(self.label,jesLabel), evt_tag)

            # Jet variables
            def my_sort(j):
                return getattr(j, "pt%s"%jesLabel)
            jets.sort(key=my_sort, reverse=True)

            all5_jets = ROOT.TLorentzVector()
            all5_jets.SetPtEtaPhiM(0,0,0,0)
            more5_jets = ROOT.TLorentzVector()
            more5_jets.SetPtEtaPhiM(0,0,0,0)
            Jets_plus_Lep = ROOT.TLorentzVector()
            Jets_plus_Lep.SetPtEtaPhiM(0,0,0,0)

            jets = [j for j in jets if getattr(j, "pt%s"%jesLabel) > 25]
            for i,j in enumerate(jets):
                jvec = ROOT.TLorentzVector(0,0,0,0)
                jvec.SetPtEtaPhiM(getattr(j, "pt%s"%jesLabel), j.eta, j.phi, j.mass)
                Jets_plus_Lep = Jets_plus_Lep + jvec
                if i<5 : all5_jets = all5_jets + jvec
                if i>=5: more5_jets = more5_jets + jvec
            for l in lepsFO:
                Jets_plus_Lep = Jets_plus_Lep + l.p4()

            self.out.fillBranch('%sAll5_Jets%s_pt'  %(self.label,jesLabel), all5_jets.Pt())
            self.out.fillBranch('%sAll5_Jets%s_eta' %(self.label,jesLabel), all5_jets.Eta())
            self.out.fillBranch('%sAll5_Jets%s_phi' %(self.label,jesLabel), all5_jets.Phi())
            self.out.fillBranch('%sAll5_Jets%s_mass'%(self.label,jesLabel), all5_jets.M())
            
            self.out.fillBranch('%sMore5_Jets%s_pt'  %(self.label,jesLabel), more5_jets.Pt()  if len(jets) > 5 else -99)
            self.out.fillBranch('%sMore5_Jets%s_eta' %(self.label,jesLabel), more5_jets.Eta() if len(jets) > 5 else -99)
            self.out.fillBranch('%sMore5_Jets%s_phi' %(self.label,jesLabel), more5_jets.Phi() if len(jets) > 5 else -99)
            self.out.fillBranch('%sMore5_Jets%s_mass'%(self.label,jesLabel), more5_jets.M()   if len(jets) > 5 else -99)
            
            self.out.fillBranch('%sJets_plus_Lep%s_pt'  %(self.label,jesLabel), Jets_plus_Lep.Pt())  
            self.out.fillBranch('%sJets_plus_Lep%s_eta' %(self.label,jesLabel), Jets_plus_Lep.Eta()) 
            self.out.fillBranch('%sJets_plus_Lep%s_phi' %(self.label,jesLabel), Jets_plus_Lep.Phi()) 
            self.out.fillBranch('%sJets_plus_Lep%s_mass'%(self.label,jesLabel), Jets_plus_Lep.M())   

            self.out.fillBranch('%smet%s'     %(self.label,jesLabel), met                                ) 
            self.out.fillBranch('%smet_phi%s' %(self.label,jesLabel), met_phi                            )
            self.out.fillBranch('%sHTXS_Higgs_pt%s'%(self.label,jesLabel), getattr(event,"HTXS_Higgs_pt"))
            self.out.fillBranch('%sHTXS_Higgs_y%s' %(self.label,jesLabel), getattr(event,"HTXS_Higgs_y") )
        return True

higgsDiffRegressionTTH = lambda : HiggsDiffRegressionTTH(label='Hreco_',
                                                         btagDeepCSVveto = 'M')
