import os 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 

from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import writeOutput
import keras 
import ROOT as r 
import numpy as np 
class ttH_kappa3(Module):
    def __init__(self):
        self.model = keras.models.load_model(os.environ['CMSSW_BASE']+'/src/CMGTools/TTHAnalysis/data/eft/reweighting/kappa3_model.h5' )

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        for out in ['weight', 'top_eta','atop_eta','higgs_eta','top_phi','atop_phi','top_pt','atop_pt','higgs_pt','sqrts']:
            self.wrappedOutputTree.branch('kappa3_'+out,'F')

    def analyze(self, event):
        lheParts = [l for l in Collection(event, 'LHEPart')]
        higgs   = [p for p in lheParts if  p.pdgId == 25][0]

        initialState   = [p for p in lheParts if  p.status < 0]

        if len(initialState) != 2:
            raise RuntimeError 

        #### Obtain information about the generated tops
        partobjs = [p for p in Collection(event, "GenPart")]
        candtops = []
        for i, part in enumerate(partobjs):
            if part.status != 22: 
                continue
            elif part.pdgId == 6:
                top = part.p4()
            elif part.pdgId == -6:
                atop = part.p4()
            
        
        higgs = higgs.p4()

        # input variables
        i1=r.TLorentzVector(); i1.SetPxPyPzE( 0, 0, initialState[0].incomingpz, abs(initialState[0].incomingpz))
        i2=r.TLorentzVector(); i2.SetPxPyPzE( 0, 0, initialState[1].incomingpz, abs(initialState[1].incomingpz))


        tth=(top+atop+higgs).BoostVector()

        top.Boost(-tth)
        atop.Boost(-tth)
        higgs.Boost(-tth)
        

        top_eta=top.Eta()
        atop_eta=atop.Eta()
        higgs_eta=higgs.Eta()
    
        top_phi=higgs.DeltaPhi(top)
        atop_phi=higgs.DeltaPhi(atop)
    
        top_pt=top.Pt()
        atop_pt=atop.Pt()
        higgs_pt=higgs.Pt()


        inputs=np.array([top_eta, atop_eta , higgs_eta, top_phi, atop_phi, top_pt, atop_pt, higgs_pt])
        inputs=inputs.reshape(1,8)

        self.wrappedOutputTree.fillBranch('kappa3_weight', self.model.predict(inputs))
        self.wrappedOutputTree.fillBranch('kappa3_top_eta'   ,top_eta   )
        self.wrappedOutputTree.fillBranch('kappa3_atop_eta'  ,atop_eta  )
        self.wrappedOutputTree.fillBranch('kappa3_higgs_eta' ,higgs_eta )
        self.wrappedOutputTree.fillBranch('kappa3_top_phi'   ,top_phi   )
        self.wrappedOutputTree.fillBranch('kappa3_atop_phi'  ,atop_phi  )
        self.wrappedOutputTree.fillBranch('kappa3_top_pt'    ,top_pt    )
        self.wrappedOutputTree.fillBranch('kappa3_atop_pt'   ,atop_pt   )
        self.wrappedOutputTree.fillBranch('kappa3_higgs_pt'  ,higgs_pt  )

        return True 

TTH_kappa3 = lambda : ttH_kappa3()
