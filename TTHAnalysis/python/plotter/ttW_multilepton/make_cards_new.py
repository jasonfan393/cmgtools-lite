import os, sys, re
from differential_variables import all_vars
nCores=16


if 'psi' in os.environ['HOSTNAME']:       
    ORIGIN="/pnfs/psi.ch/cms/trivcat/store/user/sesanche/NanoTrees_UL_v2_060422_newfts_skim2lss"; 
    queue ="standard"
elif 'fanae' in os.environ['HOSTNAME']:
    ORIGIN     = "/beegfs/data/nanoAODv9/ttH_differential/NanoTrees_UL_v2_060422_skim2lss_newfts"
    queue ="batch"
elif 'gae' in os.environ['HOSTNAME']: 
    ORIGIN    = "/beegfs/data/nanoAODv9/ttH_differential/NanoTrees_UL_v2_060422_skim2lss_newfts"
    queue ="batch"

else: 
    raise RuntimeError("You need ntuples to run the analysis :)")

#submit = '{command}' 
submit = '''sbatch -c %d -p %s  --wrap '{command}' '''%(nCores, queue)

if len(sys.argv) < 4: 
    print 'Sytaxis is %s [outputdir] [year] [region] [observable] [other]'%sys.argv[0]
    raise RuntimeError 
OUTNAME=sys.argv[1]
YEAR=sys.argv[2]
REGION=sys.argv[3]
OBSERVABLE=sys.argv[4]
OTHER=sys.argv[5:] if len(sys.argv) > 5 else ''

if   YEAR == '2016'   : LUMI="16.8"
elif   YEAR == '2016APV': LUMI="19.5"
elif YEAR in '2017': LUMI="41.4"
elif YEAR in '2018': LUMI="59.7"
else:
    raise RuntimeError("Wrong year %s"%YEAR)


#print "Normalizing to {LUMI}/fb".format(LUMI=LUMI);
OPTIONS=" --tree NanoAOD  -j {J} -l {LUMI}  --s2v -f --WA prescaleFromSkim --split-factor=-1 ".format(LUMI=LUMI,J=nCores)
os.system("test -d cards/{OUTNAME} || mkdir -p cards/{OUTNAME}".format(OUTNAME=OUTNAME))
OPTIONS="{OPTIONS} --od cards/{OUTNAME} ".format(OPTIONS=OPTIONS, OUTNAME=OUTNAME)
if "gen" in OTHER:
   OPTIONS = OPTIONS.replace("--WA prescaleFromSkim","")
   ltext = "-l {LUMI}".format(LUMI=LUMI)


T2L="-P {ORIGIN}/{YEAR} --FMCs {{P}}/0_jmeUnc_v1  --FMCs {{P}}/2_btagSF_fixedWP/ --FMCs {{P}}/2_scalefactors_lep/ --Fs {{P}}/4_evtVars --FMCs {{P}}/6_ttWforlepton --Fs {{P}}/7_Vars_forttWDiff_25 --Fs {{P}}/1_recl   --xf GGHZZ4L_new,qqHZZ4L,tWll,WW_DPS,WpWpJJ,WWW_ll,T_sch_lep,GluGluToHHTo2V2Tau,TGJets_lep,WWTo2L2Nu_DPS,GluGluToHHTo4Tau,ZGTo2LG,GluGluToHHTo4V,TTTW ".format(ORIGIN=ORIGIN, YEAR=YEAR)

if "gen" in OTHER:
   T2L= "-P {ORIGIN}/NanoTrees_UL_v2_gennoskim/{YEAR} ".format(ORIGIN = re.sub("NanoTrees_UL_v2_060422_.*","",ORIGIN), YEAR=YEAR)


T3L=T2L
T4L=T2L

SYSTS="--unc ttW_multilepton/systsUnc.txt --amc --xu CMS_ttWl_WZ_lnU,CMS_ttWl_ZZ_lnU,QCDscale_ttW,CMS_ttHl_TTW_lnU,CMS_ttHl_TTZ_lnU"
MCAOPTION=""
MCAOPTION=""
ASIMOV="--asimov signal"
SCRIPT= "makeShapeCardsNew.py"
PROMPTSUB="--plotgroup data_fakes+=.*_promptsub"

if 'unblind' in OTHER:
    ASIMOV=""

print "We are using the asimov dataset"
OPTIONS="{OPTIONS} -L ttH-multilepton/functionsTTH.cc --mcc ttW_multilepton/lepchoice-ttW-FO.txt --mcc ttW_multilepton/mcc-METchoice-prefiring.txt {PROMPTSUB} --neg   --threshold 0.01 {ASIMOV} ".format(OPTIONS=OPTIONS,PROMPTSUB=PROMPTSUB,ASIMOV=ASIMOV) # neg necessary for subsequent rebin #
CATPOSTFIX=""
MCASUFFIX="mcdata-frdata"

DOFILE = ""

GENN = ""

if OBSERVABLE == "inclusive":
    FUNCTION_2L="0"
    CATBINS    ="[-0.5,0.5]"

elif OBSERVABLE == "asymmetry":
    FUNCTION_3L="ttW_charge_asymmetry_v4(hasOSSF,nJet30, abs(positive_lepton_eta)-abs(negative_lepton_eta),nBJetMedium30, mZ_OSSF)"
    CATBINS    ="[-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,23.5,24.5,25.5,26.5,27.5,28.5,29.5,30.5,31.5]"
    CATPOSTFIX=" -E ^met "
else:
    if "gen" in OTHER:
        GENN = "Gen_"
        FUNCTION_2L=all_vars[(OBSERVABLE,REGION)].FUNCTION_2L
        CATBINS=all_vars[(OBSERVABLE,REGION)].CATBINS_Gen

    else:
        FUNCTION_2L=all_vars[(OBSERVABLE,REGION)].FUNCTION_2Lreco
        CATBINS=all_vars[(OBSERVABLE,REGION)].CATBINS

if "gen" in OTHER:
    SYSTS=""


if REGION == "2lss":
    OPT_2L='{T2L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_2lss*triggerSF_2lss"'.format(T2L=T2L, OPTIONS=OPTIONS, YEAR=YEAR)
    if "gen" in OTHER:
        OPT_2L = OPT_2L.replace('-W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_2lss*triggerSF_2lss"','')
    CATPOSTFIX=""
    CHARGE = ""
    if "chargesplit" in OTHER:
       CHARGE = "chargebiname"

    TORUN='''python {SCRIPT} {DOFILE} ttW_multilepton/mca-2lss-{MCASUFFIX}{MCAOPTION}{OBSERVABLE}.txt ttW_multilepton/2lss_tight.txt "{FUNCTION_2L}" "{CATBINS}" {SYSTS} {OPT_2L} --binname ttW_2lss_0tau_{GEN}{OBS}_{YEAR}{CHARGE} --year {YEAR}  '''.format(SCRIPT=SCRIPT, DOFILE=DOFILE, MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, OBSERVABLE="-"+OBSERVABLE, FUNCTION_2L=FUNCTION_2L, CATBINS=CATBINS, SYSTS=SYSTS, OPT_2L=OPT_2L, YEAR=YEAR, GEN=GENN,OBS=OBSERVABLE,CHARGE = CHARGE)
    if "gen" in OTHER:
        MCA = '''ttW_multilepton/mca-2lss-{MCASUFFIX}{MCAOPTION}{OBSERVABLE}.txt'''.format(MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, OBSERVABLE="-"+OBSERVABLE)
        TORUN = TORUN.replace(MCA,"ttW_multilepton/mca-includes/mca-2lss-sigprompt-gen.txt")
        TORUN = TORUN.replace("ttW_multilepton/2lss_tight.txt","ttW_multilepton/2lss_fiducial.txt")
    if "chargesplit" in OTHER:
        print( submit.format(command=TORUN.replace("chargebiname","_positive")+ " -E ^plusplus")) #tra-tra
        print( submit.format(command=TORUN.replace("chargebiname","_negative")+ " -E ^minusminus")) #malamente
        os.system(submit.format(command=TORUN.replace("chargebiname","_positive")+ " -E ^plusplus"))
        os.system(submit.format(command=TORUN.replace("chargebiname","_negative")+ " -E ^minusminus"))

    else:
        #os.system( submit.format(command=TORUN))
        print( submit.format(command=TORUN))

if REGION == "3l" and "diff" in OTHER:
    OPT_2L='{T2L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_3l*triggerSF_3l"'.format(T2L=T2L, OPTIONS=OPTIONS, YEAR=YEAR)
    if "gen" in OTHER:
        OPT_2L = OPT_2L.replace('-W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_3l*triggerSF_3l"','')
    CATPOSTFIX=""

    TORUN='''python {SCRIPT} {DOFILE} ttW_multilepton/mca-3l-{MCASUFFIX}{MCAOPTION}{OBSERVABLE}.txt ttW_multilepton/3l_tight.txt "{FUNCTION_2L}" "{CATBINS}" {SYSTS} {OPT_2L} --binname ttW_3l_0tau_{GEN}{OBS}_{YEAR} --year {YEAR}  '''.format(SCRIPT=SCRIPT, DOFILE=DOFILE, MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, OBSERVABLE="-"+OBSERVABLE, FUNCTION_2L=FUNCTION_2L, CATBINS=CATBINS, SYSTS=SYSTS, OPT_2L=OPT_2L, YEAR=YEAR, GEN=GENN,OBS=OBSERVABLE)
    if "gen" in OTHER:
        MCA = '''ttW_multilepton/mca-3l-{MCASUFFIX}{MCAOPTION}{OBSERVABLE}.txt'''.format(MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, OBSERVABLE="-"+OBSERVABLE)
        TORUN = TORUN.replace(MCA,"ttW_multilepton/mca-includes/mca-3l-sigprompt-gen.txt")
        TORUN = TORUN.replace("ttW_multilepton/3l_tight.txt","ttW_multilepton/3l_fiducial.txt")
    #os.system( submit.format(command=TORUN))
    print( submit.format(command=TORUN))

if REGION == "3l" and not("diff" in OTHER):
    OPT_3L='{T2L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_3l*triggerSF_3l"'.format(T2L=T2L, OPTIONS=OPTIONS, YEAR=YEAR)
    TORUN='''python {SCRIPT} {DOFILE} ttW_multilepton/mca-3l-mcdata-frdata-leptoncharge.txt ttW_multilepton/3l_tight.txt "{FUNCTION_3L}" "{CATBINS}" {SYSTS} {OPT_3L} --binname ttW_3l_{OBS}_{YEAR} --year {YEAR}{CATPOSTFIX} '''.format(SCRIPT=SCRIPT, DOFILE=DOFILE, MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, FUNCTION_3L=FUNCTION_3L, CATBINS=CATBINS, SYSTS=SYSTS, OPT_3L=OPT_3L, YEAR=YEAR, OBS=OBSERVABLE, CATPOSTFIX=CATPOSTFIX)
    print( submit.format(command=TORUN))
