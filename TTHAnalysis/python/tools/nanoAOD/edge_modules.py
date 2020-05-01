MODULES = []
from CMGTools.TTHAnalysis.tools.nanoAOD.Edge_triggers import Triggers
triggers =  lambda : Triggers('Trigger','Filters')

# python prepareEventVariablesFriendTree.py -t NanoAOD /pool/ciencias/HeppyTrees/EdgeZ/Edge/Edge_260120/ /pool/ciencias/HeppyTrees/EdgeZ/Edge/Edge_260120/1_trigger  -I CMGTools.TTHAnalysis.tools.nanoAOD.edge_modules triggers -q all --env oviedo

from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import btagSFProducer
from CMGTools.TTHAnalysis.tools.nanoAOD.BtagSFs import BtagSFs

btags2016 =  lambda : btagSFProducer('2016','deepcsv')
btags2017 =  lambda : btagSFProducer('2017','deepcsv')
btags2018 =  lambda : btagSFProducer('2018','deepcsv')
btagSum = lambda : BtagSFs()

btagSF2016 = [btags2016, btagSum]
btagSF2017 = [btags2017, btagSum]
btagSF2018 = [btags2018, btagSum]

btags2016_fs =  lambda : btagSFProducer('2016_fastsim','deepcsv', suffix="fastsim")
btags2017_fs =  lambda : btagSFProducer('2017_fastsim','deepcsv', suffix="fastsim")
btags2018_fs =  lambda : btagSFProducer('2018_fastsim','deepcsv', suffix="fastsim")
btagSum_fs = lambda : BtagSFs(suffix="fastsim")

btagSF2016_fs = [btags2016, btagSum, btags2016_fs, btagSum_fs]
btagSF2017_fs = [btags2017, btagSum, btags2017_fs, btagSum_fs]
btagSF2018_fs = [btags2018, btagSum, btags2018_fs, btagSum_fs]


# python prepareEventVariablesFriendTree.py -t NanoAOD /pool/ciencias/HeppyTrees/EdgeZ/Edge/Edge_260120/ /pool/ciencias/HeppyTrees/EdgeZ/Edge/Edge_260120//2_btags  -I CMGTools.TTHAnalysis.tools.nanoAOD.edge_modules btagSF{year} -d ZZZ_2016 -c 0 -N 1000
# python prepareEventVariablesFriendTree.py -t NanoAOD /pool/ciencias/HeppyTrees/EdgeZ/Edge/Edge_260120/ /pool/ciencias/HeppyTrees/EdgeZ/Edge/Edge_260120//2_btags  -I CMGTools.TTHAnalysis.tools.nanoAOD.edge_modules btagSF{year}_fs --dm TSlep.*  -N 1000

from CMGTools.TTHAnalysis.tools.objTagger import ObjTagger

goodFatJets2016 = lambda : ObjTagger("isGood","FatJetSel_Edge",[lambda x : (x.msoftdrop > 65 and x.msoftdrop  < 105 and x.tau2/x.tau1 < 0.4 and x.pt > 200) ], makelinks=True)
goodFatJets2017 = lambda : ObjTagger("isGood","FatJetSel_Edge",[lambda x : (x.msoftdrop > 65 and x.msoftdrop  < 105 and x.tau2/x.tau1 < 0.45 and x.pt > 200) ], makelinks=True)
goodFatJets2018 = lambda : ObjTagger("isGood","FatJetSel_Edge",[lambda x : (x.msoftdrop > 65 and x.msoftdrop  < 105 and x.tau2/x.tau1 < 0.45 and x.pt > 200) ], makelinks=True)

# python prepareEventVariablesFriendTree.py -t NanoAOD /pool/ciencias/HeppyTrees/EdgeZ/Edge/Edge_260120/ /pool/ciencias/HeppyTrees/EdgeZ/Edge/Edge_260120//3_fatjetcounter  -I CMGTools.TTHAnalysis.tools.nanoAOD.edge_modules goodFatJets -d ZZZ_2016 -c 0 -N 1000

from CMGTools.TTHAnalysis.tools.nanoAOD.Edge_ZZkfactor import ZZkfactor

from CMGTools.TTHAnalysis.tools.nanoAOD.Edge_massVariables import massVariables
#from CMGTools.TTHAnalysis.tools.nanoAOD.edge_isr_reweight import Edge_isr_reweight
#from CMGTools.TTHAnalysis.tools.nanoAOD.helperVariables import helperVariables

#from CMGTools.TTHAnalysis.tools.nanoAOD.flavSym import FlavSym
