class Observable:
    def __init__(self, FUNCTION_2L, FUNCTION_2Lreco,  CATBINS):
        self.FUNCTION_2L=FUNCTION_2L
        self.FUNCTION_2Lreco=FUNCTION_2Lreco
        self.CATBINS=CATBINS
        self.CATBINS_Gen=CATBINS_Gen


        

all_vars={}
for OBSERVABLE in ["njets","nbjets","lep1_pt","lep2_pt","dR_ll","lep1_eta","max_eta","jet1_pt","deta_llss","dR_lbmedium","dR_lbloose","mindr_lep1_jet25","HT"]:
    if OBSERVABLE == "njets":
        FUNCTION_2L="nDressSelJet"
        FUNCTION_2Lreco="nJet25"
        CATBINS      ="[2.5,3.5,4.5,5.5,6.5]"
        CATBINS_Gen  = CATBINS
    
    elif OBSERVABLE == "nbjets":
        FUNCTION_2L="nDressBSelJet"
        FUNCTION_2Lreco="nBJetLoose25"
        CATBINS    ="[0.5,1.5,2.5,3.5]"
        CATBINS_Gen  = CATBINS
    
    elif OBSERVABLE == "lep1_pt":
        FUNCTION_2L="GenDressedLepton_pt[iDressSelLep[0]]"
        FUNCTION_2Lreco="LepGood1_conePt"
        CATBINS    = "[25,50,70,85,100,120,150,200,300]"
        CATBINS_Gen  ="[25,70,100,150,300]"
    
    elif OBSERVABLE == "lep2_pt":
        FUNCTION_2L="GenDressedLepton_pt[iDressSelLep[1]]"
        FUNCTION_2Lreco="LepGood2_conePt"
        CATBINS    ="[15,30,45,70,100,200]"
        CATBINS_Gen    ="[15,45,100,200]"
    
    elif OBSERVABLE == "dR_ll":
        FUNCTION_2L="deltaR(GenDressedLepton_eta[iDressSelLep[0]],GenDressedLepton_phi[iDressSelLep[0]],GenDressedLepton_eta[iDressSelLep[1]],GenDressedLepton_phi[iDressSelLep[1]])"
        FUNCTION_2Lreco="deltaR(LepGood1_eta,LepGood1_phi,LepGood2_eta,LepGood2_phi)"
        CATBINS    ="[0.0,1.5,2.5,3.5,5]"
        CATBINS_Gen    ="[0.0,1.5,2.5,3.5,5]"
    
    elif OBSERVABLE == "lep1_eta":
        FUNCTION_2L="abs(GenDressedLepton_eta[iDressSelLep[0]])"
        FUNCTION_2Lreco="abs(LepGood1_eta)"
        CATBINS    ="[0.0,0.2,0.4,0.6,0.8,1.0,1.3,1.8,2.5]"
        CATBINS_Gen    ="[0.0,0.4,0.8,1.3,2.5]"
    
    elif OBSERVABLE == "max_eta":
        FUNCTION_2L="max(GenDressedLepton_eta[iDressSelLep[0]],GenDressedLepton_eta[iDressSelLep[1]])"
        FUNCTION_2Lreco="max(LepGood1_eta,LepGood2_eta)"
        CATBINS    ="[0.0,0.2,0.4,0.6,0.8,1.0,1.3,1.8,2.5]"
        CATBINS_Gen    ="[0.0,0.4,0.8,1.3,2.5]"
    
    elif OBSERVABLE == "jet1_pt":
        FUNCTION_2L="GenJet_pt[iDressSelJet[0]]"
        FUNCTION_2Lreco="JetSel_Recl_pt[0]"
        CATBINS        ="[25,95,150,200,300,450]"
        CATBINS_Gen    ="[25,150,300,450]"
    
    elif OBSERVABLE == "deta_llss":
        FUNCTION_2L="abs(GenDressedLepton_eta[iDressSelLep[0]]-GenDressedLepton_eta[iDressSelLep[1]])"
        FUNCTION_2Lreco="abs(LepGood1_eta-LepGood2_eta)"
        CATBINS    =" [0,0.25,0.5,0.75,1.10,1.5,2.1,2.5]"
        CATBINS_Gen    =" [0,0.5,1.10,2.1,2.5]"
    
    
    elif OBSERVABLE == "dR_lbmedium":
        FUNCTION_2L="dR_DressBSelJet_DressSelLep1"
        FUNCTION_2Lreco="dR_lbmedium"
        CATBINS    ="[0, 1.0, 1.5, 2.0, 3.0]"
        CATBINS_Gen    ="[0, 1.0, 1.5, 2.0, 3.0]"
    
    elif OBSERVABLE == "dR_lbloose":
        FUNCTION_2L="dR_DressBSelJet_DressSelLep1"
        FUNCTION_2Lreco="dR_lbloose"
        CATBINS    ="[0, 1.0, 1.5, 2.0, 3.0]"
        CATBINS_Gen    ="[0, 1.0, 1.5, 2.0, 3.0]"
    
    elif OBSERVABLE == "mindr_lep1_jet25":
        FUNCTION_2L="mindr_DressSelLep1_DressSelJet"
        FUNCTION_2Lreco="mindr_lep1_jet25"
        CATBINS    ="[0, 1.0, 1.5, 2.0, 3.0]"
        CATBINS_Gen    ="[0, 1.0, 1.5, 2.0, 3.0]"
    
    elif OBSERVABLE == "HT":
        FUNCTION_2L="Gen_HT"
        FUNCTION_2Lreco="htJet25j_Recl"
        CATBINS    ="[0.0,200.,400.,600.,1000.]"
        CATBINS_Gen    ="[0.0,200.,400.,600.,1000.]"

    all_vars[OBSERVABLE]=Observable(FUNCTION_2L, FUNCTION_2Lreco,CATBINS)


