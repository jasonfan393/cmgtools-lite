from __future__ import division
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.treeReAnalyzer import * 
from CMGTools.TTHAnalysis.tools.genParticleProducer import *
import ROOT, itertools
from math import *

#bTagCut = 0.3093 if year==2016 else 0.3033 if year==2017 else 0.2770
class HiggsRecoTTH(Module):
    #def __init__(self,label="_Recl",cut_BDT_rTT_score = 0.0, cuts_mW_had = (50.,110.), cuts_mH_vis = (90.,130.), btagDeepCSVveto = 0.4941, doSystJEC=True): #TODO update the values here
    def __init__(self,label="_Recl",cut_BDT_rTT_score = 0.0, cuts_mW_had = (50.,110.), cuts_mH_vis = (90.,130.), btagDeepCSVveto = 0.3093, doSystJEC=True): 
        self.label = label
        self.branches = []
        self.systsJEC = {0:"", 1:"_jesTotalUp", -1:"_jesTotalDown"} if doSystJEC else {0:""}
        for var in self.systsJEC: self.branches.extend(["Hreco_%s%s"%(x,self.systsJEC[var]) for x in ["minDRlj","visHmass","Wmass","lepIdx","j1Idx","j2Idx","pTHvis","matchedpartons","bothmatchedpartons","mismatchedtoptaggedjets","pTHgen","delR_H_partons","delR_H_j1j2","BDThttTT_eventReco_mvaValue"]]) # added new branches here
        self.cut_BDT_rTT_score = cut_BDT_rTT_score
        self.cuts_mW_had = cuts_mW_had
        self.cuts_mH_vis = cuts_mH_vis
        self.btagDeepCSVveto = btagDeepCSVveto
    
    # old interface
    def listBranches(self):
        return self.branches
    def __call__(self,event):
        return self.run(event,CMGCollection)

    # new interface
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self,wrappedOutputTree, self.branches)
    def analyze(self, event):
        writeOutput(self, self.run(event, NanoAODCollection))
        return True
    # code
    def run(self,event,Collection):
## TODO ##        
    # status flag for gen particles
    # ----------------------------- 
        statusFlagsMap={
        'isHardProcess' : 7,
        'isPrompt'      : 0
        }
    # define variables and gen collections
    # ------------------------------------   
        #HiggsDaughters = genHiggsDaughtersSelection(genpar) # that is how you define a collection from genproducer, i.e. apply the selection on your collection and it return a filtered collection
        genjet = Collection(event,"GenJet","nGenJet")
        genpar = Collection(event,"GenPart","nGenPart")
        QFromWFromH = []
        LFromWFromH = []
        QFromWFromT = []
        LFromWFromT = []
        #gengoodJets = []
        matchedpartons          = 0
        bothmatchedpartons      = 0 
        mismatchedtoptaggedjets = 0
        pTHgen = 0
        delR_H_partons = 0
        delR_H_j1j2    = 0
        

    #def isAncestor(a,p): #TODO need to modify this function for my purpose fitting the loop below
        #if a == p:
           #return True
        #for i in xrange(0,p.numberOfMothers()):
            #if isAncestor(a,p.mother(i)):
               #return True 
        #return False

    # loop over gen particles #TODO you can simplify the loop a bit but later, keep it explicit for now
    # -----------------------
        for part in genpar:
            if part.pdgId == 25:
               if part.statusFlags &(1 << statusFlagsMap['isHardProcess']):
                  pTHgen = part.p4().Pt()
            if abs(part.pdgId) in range (1,8):
               #print "it is a quark"
               if part.genPartIdxMother >= 0 and abs(genpar[part.genPartIdxMother].pdgId) == 24: 
                  #print "the mother of this quark is W+ or W-"
                  if abs(genpar[genpar[part.genPartIdxMother].genPartIdxMother].pdgId) == 25:
                     #print "the mother of this W is a Higgs"
                     QFromWFromH.append(part)
            if abs(part.pdgId) in range (11,18) and part.status == 1:
               #print "it is a lepton"
               if part.genPartIdxMother >= 0 and abs(genpar[part.genPartIdxMother].pdgId) == 24: 
                  #print "the mother of this lepton is W+ or W-"
                  if abs(genpar[genpar[part.genPartIdxMother].genPartIdxMother].pdgId) == 25:
                     #print "the mother of this W is a Higgs"
                     LFromWFromH.append(part)
            if abs(part.pdgId) in range (1,8):
               #print "it is a quark"
               if part.genPartIdxMother >= 0 and abs(genpar[part.genPartIdxMother].pdgId) == 24: 
                  #print "the mother of this quark is W+ or W-"
                  if abs(genpar[genpar[part.genPartIdxMother].genPartIdxMother].pdgId) == 6:
                     #print "the mother of this W is a Top"
                     QFromWFromT.append(part)
            if abs(part.pdgId) in range (11,18) and part.status == 1:
               #print "it is a lepton"
               if part.genPartIdxMother >= 0 and abs(genpar[part.genPartIdxMother].pdgId) == 24: 
                  #print "the mother of this lepton is W+ or W-"
                  if abs(genpar[genpar[part.genPartIdxMother].genPartIdxMother].pdgId) == 6:
                     #print "the mother of this W is a Top"
                     LFromWFromT.append(part)
    # loop over gen jets 
    # ------------------ 
        #for jet in genjet:
            #if not jet.partonFlavour == 5 and not jet.partonFlavour == -5: #TODO that excludes b-jets but it is not necessary
            #if jet.p4().Pt() > 30 and abs(jet.p4().Eta()) < 2.5:  # bit extreme cuts, I think supposed to be 24 and 2.4
               #gengoodJets.append(jet)
               #print "jet flavour = " + str(jet.partonFlavour) + " and mass = " + str(jet.p4().M()) + " GeV and pT = " + str(jet.p4().Pt())
        #MET_pt   = getattr(event,"MET_pt")
        #mhtJet25 = getattr(event,"mhtJet25_Recl")
        nleps    = getattr(event,"nLepGood")
        nFO      = getattr(event,"nLepFO"+self.label)
        ileps    = getattr(event,"iLepFO"+self.label)
        leps     = Collection(event,"LepGood","nLepGood")
        lepsFO   = [leps[ileps[i]] for i in xrange(nFO)]
        jets     = [x for x in Collection(event,"JetSel"+self.label,"nJetSel"+self.label)]
        ret      = {} 

        for var in self.systsJEC:
            score = getattr(event,"BDThttTT_eventReco_mvaValue%s"%self.systsJEC[var])
            #print score
            candidates=[]
            if score>self.cut_BDT_rTT_score:
                #if not len(jets) >= 4: continue 
                j1top = getattr(event,"BDThttTT_eventReco_iJetSel1%s"%self.systsJEC[var])
                j2top = getattr(event,"BDThttTT_eventReco_iJetSel2%s"%self.systsJEC[var])
                j3top = getattr(event,"BDThttTT_eventReco_iJetSel3%s"%self.systsJEC[var])
                jetsTopNoB   = [b for a,b in enumerate(jets) if a in [j1top,j2top,j3top] and b.btagDeepB<self.btagDeepCSVveto] #it is a jet coming from top and not a b-jet
                jetsNoTopNoB = [j for i,j in enumerate(jets) if i not in [j1top,j2top,j3top] and j.btagDeepB<self.btagDeepCSVveto]
                #if not len(lepsFO)==2: continue
                #if not lepsFO[0].charge==lepsFO[1].charge: continue
                #if not abs(lepsFO[0].pdgId)!=11 or abs(lepsFO[1].pdgId) != 11 or MET_pt*0.6 + mhtJet25*0.4 > 30: continue 
                #if not lepsFO[0].isLepTight and lepsFO[1].isLepTight: continue #TODO 
                for _lep,lep in [(ix,x.p4()) for ix,x in enumerate(lepsFO)]:
                    for _j1,_j2,j1,j2 in [(jets.index(x1),jets.index(x2),x1.p4(),x2.p4()) for x1,x2 in itertools.combinations(jetsNoTopNoB,2)]:
                        j1.SetPtEtaPhiM(getattr(jets[jets.index(x1)],'pt%s'%self.systsJEC[var]),j1.Eta(), j1.Phi(), j1.M())
                        j2.SetPtEtaPhiM(getattr(jets[jets.index(x2)],'pt%s'%self.systsJEC[var]),j2.Eta(), j2.Phi(), j2.M())
			W = j1+j2
			mW = W.M()
			if mW<self.cuts_mW_had[0] or mW>self.cuts_mW_had[1]: continue
			Wconstr = ROOT.TLorentzVector()
			Wconstr.SetPtEtaPhiM(W.Pt(),W.Eta(),W.Phi(),80.4)
			Hvisconstr = lep+Wconstr
			mHvisconstr = Hvisconstr.M()
			pTHvisconstr = Hvisconstr.Pt()
			if mHvisconstr<self.cuts_mH_vis[0] or mHvisconstr>self.cuts_mH_vis[1]: continue
			mindR = min(lep.DeltaR(j1),lep.DeltaR(j2))
                        delR_H_j1j2 = deltaR(j1.Eta(),j1.Phi(), j2.Eta(),j2.Phi())
		        candidates.append((mindR,mHvisconstr,mW,_lep,_j1,_j2,pTHvisconstr,delR_H_j1j2))
                        # need to remove #TODO
                        # --------------
                        #for jet in gengoodJets:
                            #if deltaR(jet.p4().Eta(),jet.p4().Phi(), j1.Eta(),j1.Phi()) < 0.3 or deltaR(jet.p4().Eta(),jet.p4().Phi(), j2.Eta(),j2.Phi()) < 0.3:
                               #print "at least one the detector-level jets matched with a true one --> counting it"
                               #matchedjets +=1
                            #elif deltaR(jet.p4().Eta(),jet.p4().Phi(), j1.Eta(),j1.Phi()) < 0.3 and deltaR(jet.p4().Eta(),jet.p4().Phi(), j2.Eta(),j2.Phi()) < 0.3:
                                 #print "both detector level jets match with both true ones --> counting it"
                                 #bothmatchedjets +=1
                for topjet in jetsTopNoB:
                    for gentopquark in QFromWFromT:
                        if deltaR(topjet.p4().Eta(),topjet.p4().Phi(), gentopquark.p4().Eta(),gentopquark.p4().Phi()) > 0.5:
                           #jets tagged as coming from top didn't match with true partons coming from top"
                           mismatchedtoptaggedjets +=1 #only with respect to the hadronic top where the W is going to qq and this is what I am matching here
            
                for q1,q2 in itertools.combinations(QFromWFromH,2):
                    delR_H_partons = deltaR(q1.p4().Eta(),q1.p4().Phi(), q2.p4().Eta(),q2.p4().Phi())
                    #print delR_H_partons

            best = min(candidates) if len(candidates) else None
            if best:
               jetmat1 = jets[best[4]] 
               jetmat2 = jets[best[5]]
	       for quark in QFromWFromH: 
	           if deltaR(quark.p4().Eta(),quark.p4().Phi(), jetmat1.p4().Eta(),jetmat1.p4().Phi()) < 0.3 or deltaR(quark.p4().Eta(),quark.p4().Phi(), jetmat2.p4().Eta(),jetmat2.p4().Phi()) < 0.3:
	              matchedpartons +=1
	           elif deltaR(quark.p4().Eta(),quark.p4().Phi(), jetmat1.p4().Eta(),jetmat1.p4().Phi()) < 0.3 and deltaR(quark.p4().Eta(),quark.p4().Phi(), jetmat2.p4().Eta(),jetmat2.p4().Phi()) < 0.3:
		        bothmatchedpartons +=1
            else: pass   
            ret["Hreco_minDRlj%s"                   %self.systsJEC[var]] = best[0 ] if best else -99
            ret["Hreco_visHmass%s"                  %self.systsJEC[var]] = best[1 ] if best else -99
            ret["Hreco_Wmass%s"                     %self.systsJEC[var]] = best[2 ] if best else -99
            ret["Hreco_lepIdx%s"                    %self.systsJEC[var]] = best[3 ] if best else -99
            ret["Hreco_j1Idx%s"                     %self.systsJEC[var]] = best[4 ] if best else -99
            ret["Hreco_j2Idx%s"                     %self.systsJEC[var]] = best[5 ] if best else -99
            ret["Hreco_pTHvis%s"                    %self.systsJEC[var]] = best[6 ] if best else -99
            ret["Hreco_delR_H_partons%s"            %self.systsJEC[var]] = delR_H_partons if best else -99 
            ret["Hreco_delR_H_j1j2%s"               %self.systsJEC[var]] = best[7 ] if best else -99
            ret["Hreco_matchedpartons%s"            %self.systsJEC[var]] = matchedpartons if best else -99 
            ret["Hreco_bothmatchedpartons%s"        %self.systsJEC[var]] = bothmatchedpartons if best else -99
            ret["Hreco_pTHgen%s"                    %self.systsJEC[var]] = pTHgen 
            ret["Hreco_mismatchedtoptaggedjets%s"   %self.systsJEC[var]] = mismatchedtoptaggedjets
            ret["Hreco_BDThttTT_eventReco_mvaValue%s" %self.systsJEC[var]] = score
        return ret
