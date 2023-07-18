class Observable:
    def __init__(self, FUNCTION_2L, FUNCTION_2Lreco,  CATBINS, CATBINS_Gen, REGION = "2lss"):
        self.FUNCTION_2L=FUNCTION_2L
        self.FUNCTION_2Lreco=FUNCTION_2Lreco
        self.CATBINS=CATBINS
        self.CATBINS_Gen=CATBINS_Gen
        self.REGION = REGION



all_vars={}
for REGION in ["2lss", "3l"]:
    for OBSERVABLE in ["njets","nbjets","lep1_pt","lep2_pt","dR_ll","lep1_eta","max_eta","jet1_pt","deta_llss","dR_lbmedium","dR_lbloose","mindr_lep1_jet25","HT"]:
        if OBSERVABLE == "njets":
            FUNCTION_2L="nDressSelJet"
            FUNCTION_2Lreco="nJet25"
            if REGION == "2lss":
                CATBINS      ="[2.5,3.5,4.5,5.5]"
                CATBINS_Gen  = CATBINS
            elif REGION == "3l":
                CATBINS      ="[2.5,3.5,4.5,5.5]"
                CATBINS_Gen  = CATBINS
                
        elif OBSERVABLE == "nbjets":
            FUNCTION_2L="nDressBSelJet"
            FUNCTION_2Lreco="nBJetLoose25"
            if REGION == "2lss":
                CATBINS    ="[1.5,2.5,3.5]"
                CATBINS_Gen  = CATBINS
            elif REGION == "3l":
                CATBINS    ="[1.5,2.5,3.5]"
                CATBINS_Gen  = CATBINS
                
        elif OBSERVABLE == "lep1_pt":
            FUNCTION_2L="GenDressedLepton_pt[iDressSelLep[0]]"
            FUNCTION_2Lreco="LepGood1_conePt"
            if REGION == "2lss":
                CATBINS    = "[25,50,70,85,100,120,150,200,300]"
                CATBINS_Gen  ="[25,70,100,150,300]"
            elif REGION == "3l":
                CATBINS    = "[25,50,70,85,100,120,150,200,300]"
                CATBINS_Gen  ="[25,70,100,150,300]" 
                               
        elif OBSERVABLE == "lep2_pt":
            FUNCTION_2L="GenDressedLepton_pt[iDressSelLep[1]]"
            FUNCTION_2Lreco="LepGood2_conePt"
            if REGION == "2lss":
                CATBINS    = "[25,50,70,85,100,120,150,200,300]"
                CATBINS_Gen  ="[25,70,100,150,300]"
            elif REGION == "3l":
                CATBINS    = "[25,50,70,85,100,120,150,200,300]"
                CATBINS_Gen  ="[25,70,100,150,300]"
                
        elif OBSERVABLE == "dR_ll":
            FUNCTION_2L="deltaR(GenDressedLepton_eta[iDressSelLep[0]],GenDressedLepton_phi[iDressSelLep[0]],GenDressedLepton_eta[iDressSelLep[1]],GenDressedLepton_phi[iDressSelLep[1]])"
            FUNCTION_2Lreco="deltaR(LepGood1_eta,LepGood1_phi,LepGood2_eta,LepGood2_phi)"
            if REGION == "2lss":
                CATBINS    = "[0,0.5, 1.0, 1.25, 1.5,1.75, 2.0,2.25,2.5,2.75,3.0,3.25,3.5,3.75,10.0]"
                CATBINS_Gen    ="[0, 1.0, 1.5, 2.0, 2.5, 3.0,3.5,10.0]"
            elif REGION == "3l":
                continue # Not implemented
            
        elif OBSERVABLE == "lep1_eta":
            FUNCTION_2L="abs(GenDressedLepton_eta[iDressSelLep[0]])"
            FUNCTION_2Lreco="abs(LepGood1_eta)"
            if REGION == "2lss":
                CATBINS    ="[0.0,0.2,0.4,0.6,0.8,1.0,1.3,1.8,2.5]"
                CATBINS_Gen    ="[0.0,0.4,0.8,1.3,2.5]"
            elif REGION == "3l":
                CATBINS    ="[0.0,0.2,0.4,0.6,0.8,1.0,1.3,1.8,2.5]"
                CATBINS_Gen    ="[0.0,0.4,0.8,1.3,2.5]"
                
        elif OBSERVABLE == "max_eta":
            FUNCTION_2L="max(GenDressedLepton_eta[iDressSelLep[0]],GenDressedLepton_eta[iDressSelLep[1]])"
            FUNCTION_2Lreco="max(LepGood1_eta,LepGood2_eta)"
            if REGION == "2lss":
                CATBINS    ="[0.0,0.2,0.4,0.6,0.8,1.0,1.3,1.8,2.5]"
                CATBINS_Gen    ="[0.0,0.4,0.8,1.3,2.5]"
            elif REGION == "3l":
                continue # Not implemented

        elif OBSERVABLE == "jet1_pt":
            FUNCTION_2L="GenJet_pt[iDressSelJet[0]]"
            FUNCTION_2Lreco="JetSel_Recl_pt[0]"
            if REGION == "2lss":
                CATBINS        ="[25,95,150,200,300,450]"
                CATBINS_Gen    ="[25,150,300,450]"
            elif REGION == "3l":
                CATBINS        ="[25,95,150,200,300,450]"
                CATBINS_Gen    ="[25,150,300,450]"
                
        elif OBSERVABLE == "deta_llss":
            FUNCTION_2L="abs(GenDressedLepton_eta[iDressSelLep[0]]-GenDressedLepton_eta[iDressSelLep[1]])"
            FUNCTION_2Lreco="abs(LepGood1_eta-LepGood2_eta)"
            if REGION == "2lss":
                CATBINS    ="[0,0.25,0.5,0.75,1.10,1.5,2.1,2.5]"
                CATBINS_Gen    ="[0,0.5,1.10,2.1,2.5]"
            elif REGION == "3l":
                continue # Not implemented
       
        elif OBSERVABLE == "dR_lbmedium":
            FUNCTION_2L="dR_DressBSelJet_DressSelLep1"
            FUNCTION_2Lreco="dR_lbmedium"
            if REGION == "2lss":
                CATBINS    ="[0, 0.5,1.0,1.25, 1.5,1.75, 2.0,2.25, 2.5,2.75, 3.0,3.25,3.5,3.75,4.0]"
                CATBINS_Gen    ="[0, 1.0, 1.5, 2.0, 2.5, 3.0,3.5,4.0]"
            elif REGION == "3l":
                continue # Not implemented

        elif OBSERVABLE == "dR_lbloose":
            FUNCTION_2L="dR_DressBSelJet_DressSelLep1"
            FUNCTION_2Lreco="dR_lbloose"
            if REGION == "2lss":
                CATBINS    ="[0, 0.5,1.0,1.25, 1.5,1.75, 2.0,2.25, 2.5,2.75, 3.0,3.25,3.5,3.75,4.0]"
                CATBINS_Gen    ="[0, 1.0, 1.5, 2.0, 2.5, 3.0,3.5,4.0]"
            elif REGION == "3l":
                continue # Not implemented

        elif OBSERVABLE == "mindr_lep1_jet25":
            FUNCTION_2L="mindr_DressSelLep1_DressSelJet"
            FUNCTION_2Lreco="mindr_lep1_jet25"
            if REGION == "2lss":
                CATBINS    ="[0,0.375,0.75,0.875,1.0,1.125,1.25,1.375,1.5,1.625,1.75,1.875,2.0,2.25,2.5,2.75,3.0]"
                CATBINS_Gen    ="[0, 0.75,1.0,1.25, 1.5,1.75, 2.0,2.5, 3.0]"
            elif REGION == "3l":
                continue # Not implemented

        elif OBSERVABLE == "HT":
            FUNCTION_2L="Gen_HT"
            FUNCTION_2Lreco="htJet25j_Recl"
            if REGION == "2lss":
                CATBINS    ="[0.0,100,200,250,300.,337.50,375.,412.50,450,487.5,525,562.5,600.,700,800,900,2000.]"
                CATBINS_Gen    ="[0.0,200,300.,375.,450,525,600.,800,2000.]"
            elif REGION == "3l":
                CATBINS    ="[0.0,100,200,250,300.,337.50,375.,412.50,450,487.5,525,562.5,600.,700,800,900,2000.]"
                CATBINS_Gen    ="[0.0,200,300.,375.,450,525,600.,800,2000.]"
        
        elif OBSERVABLE == "m3l":
            FUNCTION_2L="mass_3_cheap(GenDressedLepton_pt[iDressSelLep[0]],GenDressedLepton_eta[iDressSelLep[0]],GenDressedLepton_pt[iDressSelLep[1]],GenDressedLepton_eta[iDressSelLep[1]],GenDressedLepton_phi[iDressSelLep[1]]-GenDressedLepton_phi[iDressSelLep[0]],GenDressedLepton_pt[iDressSelLep[2]],GenDressedLepton_eta[iDressSelLep[2]],GenDressedLepton_phi[iDressSelLep[2]]-GenDressedLepton_phi[iDressSelLep[0]])"
            FUNCTION_2Lreco="mass_3_cheap(LepGood1_pt,LepGood1_eta,LepGood2_pt,LepGood2_eta,LepGood2_phi-LepGood1_phi,LepGood3_pt,LepGood3_eta,LepGood3_phi-LepGood1_phi)"
            if REGION == "2lss":
                continue # Not implemented
            elif REGION == "3l":
                CATBINS    ="[0., 50., 150., 250., 350., 600.]"
                
        elif OBSERVABLE == "pt3l":
            FUNCTION_2L="GenDressedLepton_pt[iDressSelLep[0]] + GenDressedLepton_pt[iDressSelLep[1]] + GenDressedLepton_pt[iDressSelLep[2]]"
            FUNCTION_2Lreco="LepGood1_pt+LepGood2_pt+LepGood3_pt"
            if REGION == "2lss":
                continue # Not implemented
            elif REGION == "3l":
                CATBINS    ="[0.0, 150., 250., 350., 800.]"
        
        all_vars[OBSERVABLE+"_%s"%REGION]=Observable(FUNCTION_2L, FUNCTION_2Lreco, CATBINS, CATBINS_Gen, REGION)


