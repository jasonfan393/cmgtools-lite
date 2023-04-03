from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 

from copy import deepcopy
import ROOT
import os 
import numpy as np
import correctionlib

class btagSF(Module):
    def __init__(self, recllabel='Recl'):
        self.inputlabel = '_'+recllabel
        self.btvjson={}
        for year in '2016postVFP,2016preVFP,2017,2018'.split(','):
            self.btvjson[year]=correctionlib.CorrectionSet.from_file( os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/btag/btagging_%s_UL.json.gz'%year)
        self.year_btvjson=None

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
        self.all_variations=['%s_%s'%(var, sys) for var in ('down','up') for sys in 'cferr1,cferr2,hf,hfstats1,hfstats2,jes,lf,lfstats1,lfstats2,jesFlavorQCD,jesRelativeBal,jesHF,jesBBEC1,jesEC2,jesAbsolute,jesBBEC1_year,jesEC2_year,jesAbsolute_year,jesHF_year,jesRelativeSample_year'.split(',')]
        for what in ['']+self.all_variations:
            self.out.branch('btagSF%s'%what, 'F')
            self.out.branch('JetSel_Recl_btagSF%s'%what, 'F', lenVar="nJetSel_Recl")

    def computeSFforVar(self, var, flavors, etas, pts, discs, index):
        return np.prod( self.year_btvjson['deepJet_shape'].evaluate(var, flavors[index], etas[index], pts[index], discs[index]))

    def computePerJetForVar(self, var, flavors, etas, pts, discs):
        sfs=np.zeros_like( pts ) 
        if 'cferr' in var:
            sfs[flavors==4]= self.year_btvjson['deepJet_shape'].evaluate(var, flavors[flavors==4], etas[flavors==4], pts[flavors==4], discs[flavors==4])
            sfs[flavors!=4]= self.year_btvjson['deepJet_shape'].evaluate('central', flavors[flavors!=4], etas[flavors!=4], pts[flavors!=4], discs[flavors!=4])
        else:
            sfs[flavors==4]= self.year_btvjson['deepJet_shape'].evaluate('central', flavors[flavors==4], etas[flavors==4], pts[flavors==4], discs[flavors==4])
            sfs[flavors!=4]= self.year_btvjson['deepJet_shape'].evaluate(var, flavors[flavors!=4], etas[flavors!=4], pts[flavors!=4], discs[flavors!=4])

        return sfs

    def analyze(self, event):

        if self.year_btvjson is None:
            self.year='2018' if event.year == 2018 else '2017' if event.year == 2017 else '2016preVFP' if event.suberaId == 0 else '2016postVFP'
            self.year_btvjson=self.btvjson[self.year] 
            print(self.year)

        jets = [j for j in Collection(event, "JetSel"+self.inputlabel)]
        btagSF=1
        flavors= np.array([])
        pts    = np.array([])
        etas   = np.array([])
        discs  = np.array([])

        for jet in jets:
            if jet.pt > 25:
                flavors = np.append(flavors, self.getFlavorBTV(jet.hadronFlavour) ) 
                pts     = np.append(pts    , jet.pt ) 
                etas    = np.append(etas   , abs(jet.eta)) 
                discs   = np.append(discs  , jet.btagDeepFlavB ) 

        cjets =np.where(flavors == 4)
        blight=np.where(flavors != 4)

        cjets_central=self.computeSFforVar( 'central', flavors, etas, pts, discs, cjets ) 
        bjets_central=self.computeSFforVar( 'central', flavors, etas, pts, discs, blight ) 
        self.out.fillBranch( 'btagSF', cjets_central*bjets_central)

        to_store=self.computePerJetForVar('central' , flavors, etas, pts, discs ).tolist()
        self.out.fillBranch('JetSel_Recl_btagSF', to_store)


        for what in self.all_variations:
            if 'cferr' in what:
                cjets_var = self.computeSFforVar( what.replace('year',self.year[:4]) , flavors, etas, pts, discs, cjets ) 
                self.out.fillBranch( 'btagSF%s'%what, cjets_var*bjets_central)
            else:
                bjets_var = self.computeSFforVar( what.replace('year',self.year[:4]), flavors, etas, pts, discs, blight ) 
                self.out.fillBranch( 'btagSF%s'%what, cjets_central*bjets_var)
            to_store=self.computePerJetForVar(what.replace('year',self.year[:4]) , flavors, etas, pts, discs ).tolist()
            self.out.fillBranch('JetSel_Recl_btagSF%s'%what, to_store)

        return True
