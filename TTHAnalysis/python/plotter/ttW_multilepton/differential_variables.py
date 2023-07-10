class Observable:
    def __init__(self, FUNCTION_2L, FUNCTION_2Lreco,  CATBINS):
        self.FUNCTION_2L=FUNCTION_2L
        self.FUNCTION_2Lreco=FUNCTION_2Lreco
        self.CATBINS=CATBINS


        

all_vars={}
for OBSERVABLE in ["njets","nbjets","lep1_pt","lep2_pt","dR_ll","lep1_eta","max_eta","jet1_pt","deta_llss","dR_lbmedium","dR_lbloose","mindr_lep1_jet25","HT"]:
    if OBSERVABLE == "njets":
        FUNCTION_2L="nDressSelJet"
        FUNCTION_2Lreco="nJet25"
        CATBINS    ="[2.5,3.5,4.5,5.5,6.5,7.5]"
    
    elif OBSERVABLE == "nbjets":
        FUNCTION_2L="nDressBSelJet"
        FUNCTION_2Lreco="nBJetLoose25"
        CATBINS    ="[0.5,1.5,2.5,3.5]"
    
    elif OBSERVABLE == "lep1_pt":
        FUNCTION_2L="GenDressedLepton_pt[iDressSelLep[0]]"
        FUNCTION_2Lreco="LepGood1_conePt"
        CATBINS    ="[25,50,100,150,225,500]"
    
    elif OBSERVABLE == "lep2_pt":
        FUNCTION_2L="GenDressedLepton_pt[iDressSelLep[1]]"
        FUNCTION_2Lreco="LepGood2_conePt"
        CATBINS    ="[20,25,30,35,40,45,55,70,100]"
    
    elif OBSERVABLE == "dR_ll":
        FUNCTION_2L="deltaR(GenDressedLepton_eta[iDressSelLep[0]],GenDressedLepton_phi[iDressSelLep[0]],GenDressedLepton_eta[iDressSelLep[1]],GenDressedLepton_phi[iDressSelLep[1]])"
        FUNCTION_2Lreco="deltaR(LepGood1_eta,LepGood1_phi,LepGood2_eta,LepGood2_phi)"
        CATBINS    ="[0.0,1.5,2.5,3.5,5]"
    
    elif OBSERVABLE == "lep1_eta":
        FUNCTION_2L="abs(GenDressedLepton_eta[iDressSelLep[0]])"
        FUNCTION_2Lreco="abs(LepGood1_eta)"
        CATBINS    ="[0.,0.9,1.2,2.5]"
    
    elif OBSERVABLE == "max_eta":
        FUNCTION_2L="max(GenDressedLepton_eta[iDressSelLep[0]],GenDressedLepton_eta[iDressSelLep[1]])"
        FUNCTION_2Lreco="max(LepGood1_eta,LepGood2_eta)"
        CATBINS    ="[0.0,0.75,1.5,2.0,2.5]"
    
    elif OBSERVABLE == "jet1_pt":
        FUNCTION_2L="GenJet_pt[iDressSelJet[0]]"
        FUNCTION_2Lreco="JetSel_Recl_pt[0]"
        CATBINS    ="[25,50,100,150,225,500]"
    
    elif OBSERVABLE == "deta_llss":
        FUNCTION_2L="abs(GenDressedLepton_eta[iDressSelLep[0]]-GenDressedLepton_eta[iDressSelLep[1]])"
        FUNCTION_2Lreco="abs(LepGood1_eta-LepGood2_eta)"
        CATBINS    ="[0.0,0.4,0.8,1.2,1.6,2.0,2.4]"
    
    
    elif OBSERVABLE == "dR_lbmedium":
        FUNCTION_2L="dR_DressBSelJet_DressSelLep1"
        FUNCTION_2Lreco="dR_lbmedium"
        CATBINS    ="[0, 1.0, 1.5, 2.0, 3.0]"
    
    elif OBSERVABLE == "dR_lbloose":
        FUNCTION_2L="dR_DressBSelJet_DressSelLep1"
        FUNCTION_2Lreco="dR_lbloose"
        CATBINS    ="[0, 1.0, 1.5, 2.0, 3.0]"
    
    elif OBSERVABLE == "mindr_lep1_jet25":
        FUNCTION_2L="mindr_DressSelLep1_DressSelJet"
        FUNCTION_2Lreco="mindr_lep1_jet25"
        CATBINS    ="[0, 1.0, 1.5, 2.0, 3.0]"
    
    elif OBSERVABLE == "HT":
        FUNCTION_2L="Gen_HT"
        FUNCTION_2Lreco="htJet25j_Recl"
        CATBINS    ="[0.0,200.,400.,600.,1000.]"

    all_vars[OBSERVABLE]=Observable(FUNCTION_2L, FUNCTION_2Lreco,CATBINS)


