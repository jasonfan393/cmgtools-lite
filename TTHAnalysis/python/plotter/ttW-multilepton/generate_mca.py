

def do_mca_for_var( OBSERVABLE ):

    if OBSERVABLE == "njets":
        FUNCTION_2L="nDressSelJet"
        CATBINS    ="[2.5,3.5,4.5,5.5,6.5,7.5]"
    
    elif OBSERVABLE == "nbjets":
        FUNCTION_2L="nDressBSelJet"
        CATBINS    ="[0.5,1.5,2.5,3.5]"
    
    elif OBSERVABLE == "lep1_pt":
        FUNCTION_2L="GenDressedLepton_pt[iDressSelLep[0]]"
        CATBINS    ="[25,50,100,150,225,500]"
    
    elif OBSERVABLE == "lep2_pt":
        FUNCTION_2L="GenDressedLepton_pt[iDressSelLep[1]]"
        CATBINS    ="[20,25,30,35,40,45,55,70,100]"
    
    elif OBSERVABLE == "dR_ll":
        FUNCTION_2L="deltaR(GenDressedLepton_eta[iDressSelLep[0]],GenDressedLepton_phi[iDressSelLep[0]],GenDressedLepton_eta[iDressSelLep[1]],GenDressedLepton_phi[iDressSelLep[1]])"
        CATBINS    ="[0.0,1.5,2.5,3.5,5]"
    
    elif OBSERVABLE == "lep1_eta":
        FUNCTION_2L="abs(GenDressedLepton_eta[iDressSelLep[0]])"
        CATBINS    ="[0.,0.9,1.2,2.5]"
    
    elif OBSERVABLE == "max_eta":
        FUNCTION_2L="max(GenDressedLepton_eta[iDressSelLep[0]],GenDressedLepton_eta[iDressSelLep[1]])"
        CATBINS    ="[0.0,0.75,1.5,2.0,2.5]"
    
    
    elif OBSERVABLE == "jet1_pt":
        FUNCTION_2L="GenJet_pt[iDressSelJet[0]]"
        CATBINS    ="[25,50,100,150,225,500]"
    
    elif OBSERVABLE == "deta_llss":
        FUNCTION_2L="abs(GenDressedLepton_eta[iDressSelLep[0]]-GenDressedLepton_eta[iDressSelLep[1]])"
        CATBINS    ="[0.0,0.4,0.8,1.2,1.6,2.0,2.4]"
    
    
    elif OBSERVABLE == "dR_lbmedium":
        FUNCTION_2L="dR_DressBSelJet_DressSelLep1"
        CATBINS    ="[0, 1.0, 1.5, 2.0, 3.0]"
    
    elif OBSERVABLE == "dR_lbloose":
        FUNCTION_2L="dR_DressBSelJet_DressSelLep1"
        CATBINS    ="[0, 1.0, 1.5, 2.0, 3.0]"
    
    elif OBSERVABLE == "mindr_lep1_jet25":
        FUNCTION_2L="mindr_DressSelLep1_DressSelJet"
        CATBINS    ="[0, 1.0, 1.5, 2.0, 3.0]"
    
    elif OBSERVABLE == "HT":
        FUNCTION_2L="Gen_HT"
        CATBINS    ="[0.0,200.,400.,600.,1000.]"
    binning = eval(CATBINS)

    full_mca_template='''incl_sig : + ; IncludeMca="ttW-multilepton/mca-includes/mca-2lss-sigprompt-{OBSERVABLE}.txt"
incl_bkg : + ; IncludeMca="ttW-multilepton/mca-includes/mca-2lss-bkgprompt.txt"
incl_convs     : + ; IncludeMca="ttW-multilepton/mca-includes/mca-2lss-convs.txt"
incl_datafakes  : + ; IncludeMca="ttW-multilepton/mca-includes/mca-data.txt", FakeRate="ttW-multilepton/fakeRate-2lss-frdata.txt", Label="Non-prompt", FillColor=ROOT.kBlack, FillStyle=3005, PostFix='_fakes'
incl_promptsub : + ; IncludeMca="ttW-multilepton/mca-includes/mca-2lss-sigprompt-inclusive.txt", FakeRate="ttW-multilepton/fakeRate-2lss-frdata.txt", PostFix='_promptsub', AddWeight="-1"
incl_promptsub : + ; IncludeMca="ttW-multilepton/mca-includes/mca-2lss-bkgprompt.txt", FakeRate="ttW-multilepton/fakeRate-2lss-frdata.txt", PostFix='_promptsub', AddWeight="-1"
incl_dataflips  : + ; IncludeMca="ttW-multilepton/mca-includes/mca-data-forFlips.txt", FakeRate="ttW-multilepton/flipRate-2lss-frdata.txt", Label="Charge mis-m.", FillColor=ROOT.kBlack, FillStyle=3006, PostFix='_flips'

incl_data : + ; IncludeMca="ttW-multilepton/mca-includes/mca-data.txt"'''

    outf1=open("ttW-multilepton/mca-2lss-mcdata-frdata-{OBSERVABLE}.txt".format(OBSERVABLE=OBSERVABLE),'w')
    outf1.write( full_mca_template.format(OBSERVABLE=OBSERVABLE))
    outf1.close()

    template='''TTW_{OBSERVABLE}_bin{binno}+     : TTWToLNu_fxfx_withGen : 0.2357*1.44 : LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge && ({FUNCTION_2L} > {cutlow}) && ({FUNCTION_2L} < {cuthigh}) && (nDressSelLep > 1) && (GenDressedLepton_pdgId[iDressSelLep[1]]*GenDressedLepton_pdgId[iDressSelLep[1]]>0) && (GenDressedLepton_pt[iDressSelLep[1]] > 25 && GenDressedLepton_pt[iDressSelLep[1]] >  20) && (nDressSelJet >= 3) && (nDressBSelJet >=1) ; FillColor=ROOT.kGreen-5   , Label="{cutlow} < ttW {OBSERVABLE} < {cuthigh}", FillStyle=3022,  FriendsSimple="{{P}}/A_ttW_diff_info_extended/"
TTW_{OBSERVABLE}_bin{binno}+     : TTWJetsToLNu_EWK_5f_NLO_withGen : xsec*1.44 : LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge && ({FUNCTION_2L} > {cutlow}) && ({FUNCTION_2L} < {cuthigh}) && (nDressSelLep > 1) && (GenDressedLepton_pdgId[iDressSelLep[1]]*GenDressedLepton_pdgId[iDressSelLep[1]]>0) && (GenDressedLepton_pt[iDressSelLep[1]] > 25 && GenDressedLepton_pt[iDressSelLep[1]] >  20) && (nDressSelJet >= 3) && (nDressBSelJet >=1) ; FillColor=ROOT.kGreen-5   , Label="{cutlow} < ttW {OBSERVABLE}  < {cuthigh}", FillStyle=3022,  FriendsSimple="{{P}}/A_ttW_diff_info_extended/"\n'''
    
    signal_mca=""

    for i,(binlow,binhigh) in enumerate(zip(binning, binning[1:])):
        signal_mca += template.format(binno=i, cutlow=binlow, cuthigh=binhigh, OBSERVABLE=OBSERVABLE, FUNCTION_2L=FUNCTION_2L)

    outf2=open("ttW-multilepton/mca-includes/mca-2lss-sigprompt-{OBSERVABLE}.txt".format(OBSERVABLE=OBSERVABLE),'w')
    outf2.write( signal_mca )
    outf2.close()


for obs in ["njets","nbjets","lep1_pt","lep2_pt","dR_ll","lep1_eta","max_eta","jet1_pt","deta_llss","dR_lbmedium","dR_lbloose","mindr_lep1_jet25","HT"]:
    do_mca_for_var(obs)
