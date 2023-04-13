import os, sys
nCores=32
submit = '''sbatch -c %d -p batch  --wrap '{command}' '''%nCores
#submit = '{command}' 


if 'psi' in os.environ['HOSTNAME']:       ORIGIN="/pnfs/psi.ch/cms/trivcat/store/user/sesanche/"; 
elif 'fanae' in os.environ['HOSTNAME']:
    ORIGIN     = "/beegfs/data/nanoAODv9/ttH_differential/"
elif 'gae' in os.environ['HOSTNAME']: 
    ORIGIN    = "/beegfs/data/nanoAODv9/ttH_differential/"


else: 
    raise RuntimeError("You need ntuples to run the analysis :)")

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
OPTIONS=" --tree NanoAOD --s2v -j {J} -l {LUMI} -f --WA prescaleFromSkim --split-factor=-1 ".format(LUMI=LUMI,J=nCores)
os.system("test -d cards/{OUTNAME} || mkdir -p cards/{OUTNAME}".format(OUTNAME=OUTNAME))
OPTIONS="{OPTIONS} --od cards/{OUTNAME} ".format(OPTIONS=OPTIONS, OUTNAME=OUTNAME)
if "gen" in OTHER:
   OPTIONS = OPTIONS.replace("--WA prescaleFromSkim","")
   ltext = "-l {LUMI}".format(LUMI=LUMI)

   OPTIONS = OPTIONS.replace(ltext,"-l 1.")

T2L="-P {ORIGIN}/NanoTrees_UL_v2_060422_skim2lss_newfts/{YEAR} --FMCs {{P}}/0_jmeUnc_v1  --FMCs {{P}}/2_btagSF_fixedWP/ --FMCs {{P}}/2_scalefactors_lep/ --Fs {{P}}/1_recl   --xf GGHZZ4L_new,qqHZZ4L,tWll,WW_DPS,WpWpJJ,WWW_ll,T_sch_lep,GluGluToHHTo2V2Tau,TGJets_lep,WWTo2L2Nu_DPS,GluGluToHHTo4Tau,ZGTo2LG,GluGluToHHTo4V,TTTW ".format(ORIGIN=ORIGIN, YEAR=YEAR)

if "gen" in OTHER:
   T2L= "-P {ORIGIN}/NanoTrees_UL_v2_gennoskim/".format(ORIGIN=ORIGIN)

T3L=T2L
T4L=T2L

SYSTS="--unc ttW-multilepton/systsUnc.txt --amc --xu CMS_ttWl_WZ_lnU,CMS_ttWl_ZZ_lnU,QCDscale_ttW"
MCAOPTION=""
MCAOPTION=""
ASIMOV="--asimov signal"
SCRIPT= "makeShapeCardsNew.py"
PROMPTSUB="--plotgroup data_fakes+=.*_promptsub"

if 'unblind' in OTHER:
    ASIMOV=""

print "We are using the asimov dataset"
OPTIONS="{OPTIONS} -L ttW-multilepton/functionsTTW.cc --mcc ttW-multilepton/lepchoice-ttW-FO.txt --mcc ttW-multilepton/mcc-METchoice-prefiring.txt {PROMPTSUB} --neg   --threshold 0.01 {ASIMOV} ".format(OPTIONS=OPTIONS,PROMPTSUB=PROMPTSUB,ASIMOV=ASIMOV) # neg necessary for subsequent rebin #
CATPOSTFIX=""
MCASUFFIX="mcdata-frdata"

DOFILE = ""

availableObservables = ['inclusive', 'njets','nbjets','lep1_pt','jet1_pt','deta_llss']

if OBSERVABLE == "inclusive":
    FUNCTION_2L="0"
    CATBINS    ="[-0.5,0.5]"
    

elif OBSERVABLE == "njets":
    FUNCTION_2L="nJet30"
    if "gen" in OTHER:
        FUNCTION_2L="nDressSelJet"
        SYSTS = ""
    CATBINS    ="[2.5,3.5,4.5,5.5,6.5,7.5]"

elif OBSERVABLE == "nbjets":
    FUNCTION_2L="nBJetLoose30"
    if "gen" in OTHER:
        FUNCTION_2L="nDressBSelJet"
        SYSTS = ""
    CATBINS    ="[0.5,1.5,2.5,3.5]"

elif OBSERVABLE == "lep1_pt":
    FUNCTION_2L="LepGood1_conePt"
    CATBINS    = "[25,40,50,75,100,125,150,187,225,350,500]"
    if "gen" in OTHER:
        FUNCTION_2L="GenDressedLepton_pt[iDressSelLep[0]]"
        CATBINS    ="[25,50,100,150,225,500]"
        SYSTS = ""


elif OBSERVABLE == "jet1_pt":
    FUNCTION_2L="JetSel_Recl_pt[0]"
    CATBINS    ="[30,40,50,75,100,125,150,187,225,350,500]"
    if "gen" in OTHER:
        FUNCTION_2L="GenJet_pt[iDressSelJet[0]]"
        CATBINS    ="[30,50,100,150,225,500]"
        SYSTS = ""

elif OBSERVABLE == "deta_llss":
    FUNCTION_2L="abs(LepGood1_eta-LepGood2_eta)"
    CATBINS    ="[0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4]"
    if "gen" in OTHER:
        FUNCTION_2L="abs(GenDressedLepton_eta[iDressSelLep[0]]-GenDressedLepton_eta[iDressSelLep[1]])"
        CATBINS    ="[0.0,0.4,0.8,1.2,1.6,2.0,2.4]"
        SYSTS = ""


if "gen" in OTHER:
   signals_remove = []

else:
   signals_remove = [ 'TTW_%s.*'%s for s in availableObservables if s!= OBSERVABLE]     
GENN = ""
if "gen" in OTHER:
   GENN = "Gen_"

if REGION == "2lss":
    OPT_2L='{T2L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_2lss*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 2, year, suberaId)"'.format(T2L=T2L, OPTIONS=OPTIONS, YEAR=YEAR)
    OPT_2L = OPT_2L.replace('-W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_2lss*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 2, year, suberaId)"','')
    CATPOSTFIX=""


    TORUN='''python {SCRIPT} {DOFILE} ttW-multilepton/mca-2lss-{MCASUFFIX}{MCAOPTION}.txt ttW-multilepton/2lss_tight.txt "{FUNCTION_2L}" "{CATBINS}" {SYSTS} {OPT_2L} --binname ttW_2lss_0tau_{GEN}{OBS}_{YEAR} --year {YEAR} --xp {signals_remove} '''.format(SCRIPT=SCRIPT, DOFILE=DOFILE, MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, FUNCTION_2L=FUNCTION_2L, CATBINS=CATBINS, SYSTS=SYSTS, OPT_2L=OPT_2L, signals_remove=','.join(signals_remove), YEAR=YEAR, GEN=GENN,OBS=OBSERVABLE)
    if "gen" in OTHER:
        TORUN = TORUN.replace("_"+YEAR,"")
        TORUN = TORUN.replace("--xp","")
        TORUN = TORUN.replace("ttW-multilepton/mca-2lss-mcdata-frdata.txt","ttW-multilepton/mca-includes/mca-2lss-sigprompt-gen.txt")
        TORUN = TORUN.replace("ttW-multilepton/2lss_tight.txt","ttW-multilepton/2lss_fiducial.txt")
    #os.system( submit.format(command=TORUN))
    print( submit.format(command=TORUN))

