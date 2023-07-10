from differential_variables import all_vars

def do_mca_for_var( OBSERVABLE ):

    binning = eval(all_vars[OBSERVABLE].CATBINS)

    full_mca_template='''incl_sig : + ; IncludeMca="ttW_multilepton/mca-includes/mca-2lss-sigprompt-{OBSERVABLE}.txt"
incl_bkg : + ; IncludeMca="ttW_multilepton/mca-includes/mca-2lss-bkgprompt.txt"
incl_convs     : + ; IncludeMca="ttW_multilepton/mca-includes/mca-2lss-convs.txt"
incl_datafakes  : + ; IncludeMca="ttW_multilepton/mca-includes/mca-data.txt", FakeRate="ttW_multilepton/fakeRate-2lss-frdata.txt", Label="Non-prompt", FillColor=ROOT.kBlack, FillStyle=3005, PostFix='_fakes'
incl_promptsub : + ; IncludeMca="ttW_multilepton/mca-includes/mca-2lss-sigprompt-inclusive.txt", FakeRate="ttW_multilepton/fakeRate-2lss-frdata.txt", PostFix='_promptsub', AddWeight="-1"
incl_promptsub : + ; IncludeMca="ttW_multilepton/mca-includes/mca-2lss-bkgprompt.txt", FakeRate="ttW_multilepton/fakeRate-2lss-frdata.txt", PostFix='_promptsub', AddWeight="-1"
incl_dataflips  : + ; IncludeMca="ttW_multilepton/mca-includes/mca-data-forFlips.txt", FakeRate="ttW_multilepton/flipRate-2lss-frdata.txt", Label="Charge mis-m.", FillColor=ROOT.kBlack, FillStyle=3006, PostFix='_flips'

incl_data : + ; IncludeMca="ttW_multilepton/mca-includes/mca-data.txt"'''

    outf1=open("ttW_multilepton/mca-2lss-mcdata-frdata-{OBSERVABLE}.txt".format(OBSERVABLE=OBSERVABLE),'w')
    outf1.write( full_mca_template.format(OBSERVABLE=OBSERVABLE))
    outf1.close()

    template='''TTW_{OBSERVABLE}_bin{binno}+     : TTWToLNu_fxfx_withGen : 0.2357*1.44 : LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge && ({FUNCTION_2L} > {cutlow}) && ({FUNCTION_2L} < {cuthigh}) && (nDressSelLep > 1) && (GenDressedLepton_pdgId[iDressSelLep[1]]*GenDressedLepton_pdgId[iDressSelLep[1]]>0) && (GenDressedLepton_pt[iDressSelLep[1]] > 25 && GenDressedLepton_pt[iDressSelLep[1]] >  20) && (nDressSelJet >= 3) && (nDressBSelJet >=1) ; FillColor=ROOT.kGreen-5   , Label="{cutlow} < ttW {OBSERVABLE} < {cuthigh}", FillStyle=3022,  FriendsSimple="{{P}}/A_ttW_diff_info_extended_25gev/"
TTW_{OBSERVABLE}_bin{binno}+     : TTWJetsToLNu_EWK_5f_NLO_withGen : xsec*1.44 : LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge && ({FUNCTION_2L} > {cutlow}) && ({FUNCTION_2L} < {cuthigh}) && (nDressSelLep > 1) && (GenDressedLepton_pdgId[iDressSelLep[1]]*GenDressedLepton_pdgId[iDressSelLep[1]]>0) && (GenDressedLepton_pt[iDressSelLep[1]] > 25 && GenDressedLepton_pt[iDressSelLep[1]] >  20) && (nDressSelJet >= 3) && (nDressBSelJet >=1) ; FillColor=ROOT.kGreen-5   , Label="{cutlow} < ttW {OBSERVABLE}  < {cuthigh}", FillStyle=3022,  FriendsSimple="{{P}}/A_ttW_diff_info_extended_25gev/"\n'''
    
    signal_mca=""

    for i,(binlow,binhigh) in enumerate(zip(binning, binning[1:])):
        signal_mca += template.format(binno=i, cutlow=binlow, cuthigh=binhigh, OBSERVABLE=OBSERVABLE, FUNCTION_2L=all_vars[OBSERVABLE].FUNCTION_2L)

        signal_mca+='''TTW_ooa+     : TTWToLNu_fxfx_withGen : 0.2357: LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge && !((nDressSelLep > 1) && (GenDressedLepton_pdgId[iDressSelLep[0]]*GenDressedLepton_pdgId[iDressSelLep[1]]>0) && (GenDressedLepton_pt[iDressSelLep[0]] > 25 && GenDressedLepton_pt[iDressSelLep[1]] >  20) && (nDressSelJet >= 3) && (nDressBSelJet >=1)) ;  FillColor=ROOT.kGreen-5, Label="ttW (<2 leps)", FriendsSimple="{P}/A_ttW_diff_info_extended/"  
    TTW_ooa+     : TTWJetsToLNu_EWK_5f_NLO_withGen : xsec : LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge && !((nDressSelLep > 1) && (GenDressedLepton_pdgId[iDressSelLep[0]]*GenDressedLepton_pdgId[iDressSelLep[1]]>0) && (GenDressedLepton_pt[iDressSelLep[0]] > 25 && GenDressedLepton_pt[iDressSelLep[1]] >  20) && (nDressSelJet >= 3) && (nDressBSelJet >=1)) ; FillColor=ROOT.kGreen-5, Label="ttW (<2 leps)", FriendsSimple="{P}/A_ttW_diff_info_extended/" \n'''

    outf2=open("ttW_multilepton/mca-includes/mca-2lss-sigprompt-{OBSERVABLE}.txt".format(OBSERVABLE=OBSERVABLE),'w')
    outf2.write( signal_mca )
    outf2.close()


for obs in all_vars:
    do_mca_for_var(obs)
