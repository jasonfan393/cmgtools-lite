from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput

from math import sqrt, cos
from copy import copy, deepcopy
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR, deltaPhi
from CMGTools.TTHAnalysis.tools.physicsobjects import _btagWPs
import ROOT as r 

class ttWLepSelector_eval(Module):
    def __init__(self, recllabel='Recl' ):
        self.inputlabel = '_'+recllabel
        self.branches   = [
            'even_lepton_1_score','even_lepton_1_index',
            'even_lepton_2_score','even_lepton_2_index',
            'positive_lepton_eta',
            'negative_lepton_eta',
            "hasOSSF",
            "mZ_OSSF",
        ]
        self.passing=0; self.total=0
        input_names = r.vector('string')(); 
        input_names.push_back('inputs')
        
        input_shapes=r.vector(r.vector('int'))()

        output_names = r.vector('string')(); output_names.push_back('output')
        self.inter=r.ONNXInterface("/work/sesanche/ttH/UL/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/macros/leptonselector.onnx",input_shapes, input_names, output_names)
        self.input_list=['lep_pt', 'lep_eta', 'lep_phi', 'm_lb1', 'm_lb2', 'dr_lb1', 'dr_lb2']

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self, wrappedOutputTree, self.branches)

    def analyze(self, event):
        if event.event in [7239721,7239767,7239853,7239896,7239929]:
            print("CheckAAAAA")

        all_leps = [l for l in Collection(event,"LepGood")]
        nFO = getattr(event,"nLepFO"+self.inputlabel)
        chosen = getattr(event,"iLepFO"+self.inputlabel)
        leps = [all_leps[chosen[i]] for i in range(nFO)]

        all_ret={}

        for var in self.branches:
            all_ret[var]=-99


        if len(leps) < 3:  # we only care about events with three leptons anyway
            writeOutput( self, all_ret)
            return True  

        # we keep also the right charge only :) 
        all_charge = leps[0].charge + leps[1].charge + leps[2].charge
        if abs(all_charge) != 1: 
            writeOutput( self, all_ret)
            return True  

        # we select the even leptons now 
        even_leps = []; odd_leps = []
        for il in range(3):
            if leps[il].charge == all_charge: 
                even_leps.append( leps[il] ) 
            else:
                odd_leps.append( leps[il] )


        jets = [j for j in Collection(event,"JetSel"+self.inputlabel)]
        jetptcut = 25
        jets = list(filter(lambda x : x.pt > jetptcut, jets))
        bloose = list(filter(lambda x : x.btagDeepFlavB > _btagWPs["DeepFlav_%d_%s"%(event.year,"L")][1], jets) )
        if len(jets) < 2 or len(bloose) == 0: 
            writeOutput( self, all_ret)
            return True # at least two jets and at least one b-jet

        if len(even_leps) != 2:
            raise RuntimeError("Theres something wrong in the logic, there should be only 2 event leptons")

        maxScore=-1;
        maxLeptonIndex=-1
        minScore=-1;
        minLeptonIndex=-1

        for lep in even_leps:
            inputvars={}
            inputvars['lep_pt'] = lep.pt
            inputvars['lep_phi'] = lep.phi
            inputvars['lep_eta'] = lep.eta

            if len(bloose) > 1:
                bjets = bloose[:2]
            else:
                bjets = [bloose[0]]
                mindr=99; thejet=None
                for j in jets:
                    if mindr > deltaR(j,lep) and j not in bjets:
                        mindr = deltaR(j,lep)
                        thejet=j
                bjets.append( thejet )
            
                    
            inputvars['m_lb1'] = (lep.p4()+bjets[0].p4()).M()
            inputvars['m_lb2'] = (lep.p4()+bjets[1].p4()).M()
            inputvars['dr_lb1'] = deltaR(lep,bjets[0])
            inputvars['dr_lb2'] = deltaR(lep,bjets[1])
            
            inputs=r.vector(r.vector('float'))()
            subinputs=r.vector('float')()
            for var in self.input_list:
                subinputs.push_back( inputvars[var] ) 
            inputs.push_back(subinputs)


            score = self.inter.run( inputs )[0][0]
            if score > maxScore:
                minScore = maxScore
                minLeptonIndex = maxLeptonIndex
                maxScore = score
                maxLeptonIndex = all_leps.index(lep)

            else:
                minScore = score
                minLeptonIndex = all_leps.index(lep)
                
        all_ret['even_lepton_1_score']=maxScore
        all_ret['even_lepton_1_index']=maxLeptonIndex # index of the lepton that is more likely coming from a top 
        all_ret['even_lepton_2_score']=minScore
        all_ret['even_lepton_2_index']=minLeptonIndex 
        
        if odd_leps[0].charge > 0:
            all_ret['positive_lepton_eta'] = odd_leps[0].eta
            all_ret['negative_lepton_eta'] = all_leps[maxLeptonIndex].eta
        else:
            all_ret['positive_lepton_eta'] = all_leps[maxLeptonIndex].eta
            all_ret['negative_lepton_eta'] = odd_leps[0].eta


        if event.event in [7239721,7239767,7239853,7239896,7239929]:
            print("Check B")
            print(leps[0].pdgId, leps[1].pdgId, leps[2].pdgId)

        # lets do some stuff with the leptons
        hasOSSF=0; mZ_OSSF=-99
        for i1,l1 in enumerate(leps[:3]):
            for i2,l2 in enumerate(leps[:3]):
                if i2 <= i1: 
                    continue
                    
                if abs(l1.pdgId)!=abs(l2.pdgId): continue
                if l1.pdgId*l2.pdgId > 0: continue
                hasOSSF=1
                mass = (l1.p4()+l2.p4()).M()
                if abs(mZ_OSSF - 91) > abs(mass-91):
                    mZ_OSSF = mass 
        self.passing = self.passing + hasOSSF
        self.total = self.total + 1
        if event.event in [7239721,7239767,7239853,7239896,7239929]:
            print("Check B")
            print(hasOSSF)

        all_ret['hasOSSF'] = hasOSSF

        all_ret['mZ_OSSF'] = mZ_OSSF
        if event.event in [7239721,7239767,7239853,7239896,7239929]:
            print("Check C")
            print(all_ret['hasOSSF'])

        writeOutput(self, all_ret)

        return True

ttWlepselector = lambda : ttWLepSelector_eval()
