#!/usr/bin/env python
import sys
import re
import os

dowhat="plots"
#dowhat="yields"
#dowhat="dumps"
dowhat="cards"

ODIR=sys.argv[1]
YEAR=sys.argv[2]
TODO=sys.argv[3]

lumis = {
'2016': '35.9',
'2017': '41.4',
'2018': '59.7',
'all' : '35.92,41.53,59.74',
}
nCores = 32

#submit = '{command} --neglist ZZ_sub --plotgroup ZZ+=ZZ_sub' 
submit = 'sbatch -p  short  -c %d --wrap "{command}  --neglist ZZ_sub --plotgroup ZZ+=ZZ_sub "'%nCores
TREES = " -P /pool/ciencias/HeppyTrees/EdgeZ/Edge/Edge_260120/ --Fs {P}/1_trigger --FMCs {P}/2_btags --FMCs {P}/4_kfactor --FMCs {P}/6_flavsym  --obj Events --genWeightName genWeight_Edge "  #  --Fs {P}/5_massvars

command=""

if dowhat == "plots":
    command += "python mcPlots.py --pdir %s "%ODIR
elif dowhat == "yields":
    command += "python mcAnalysis.py " 
elif dowhat == "dumps":
    command += "python mcDump.py " 
elif dowhat == "cards": 
    command += "python makeShapeCardsNewScan.py --namedict susy-edge/namedict.txt " 


command += " -f -j {ncores} -l {lumi} --year {year} -L susy-edge/functions-edge.cc --tree nanoAODskim --split-factor=-1 ".format(ncores=nCores, lumi=lumis[YEAR], year=(YEAR if YEAR in '2016,2017,2018'.split(',') else '2016,2017,2018'))
command += TREES

if dowhat == "plots":
    command += " --maxRatioRange 0.6 1.99 --ratioYNDiv 210 --showRatio --attachRatioPanel --fixRatioRange --legendColumns 3 --legendWidth 0.52 --legendFontSize 0.042 --noCms --topSpamSize 1.1 --lspam '#scale[1.1]{#bf{CMS}} #scale[0.9]{#it{Preliminary}}' --showMCError "

if TODO.startswith("rsfof"):
    command += " susy-edge/mca-{year}-dd-data-offz.txt ".format(year = YEAR if YEAR != "all" else "{year}")
    command += " susy-edge/regions/rsfof_measurement.txt -E ^SF "
    command += " -W 'LepSF(Lep1_pt_Edge,Lep1_eta_Edge,Lep1_pdgId_Edge,year)*LepSF(Lep2_pt_Edge,Lep2_eta_Edge,Lep2_pdgId_Edge,year)' "
    command += " --xp TSleps.* "
    if dowhat == "plots": 
        command += " susy-edge/plots.txt  "


if TODO.startswith("sleptons"):
    command += " susy-edge/mca-{year}-dd-data-offz.txt ".format(year = YEAR if YEAR != "all" else "{year}")
    command += " susy-edge/regions/slepton.txt "
    command += " -W 'LepSF(Lep1_pt_Edge,Lep1_eta_Edge,Lep1_pdgId_Edge,year)*LepSF(Lep2_pt_Edge,Lep2_eta_Edge,Lep2_pdgId_Edge,year)' "
    command += "  --xp TSleps.* "  # --ap TSlepslep_550_275

    command += " -P /pool/ciencias/HeppyTrees/EdgeZ/Edge/Edge_260120/newfile/ -P /pool/ciencias/HeppyTrees/EdgeZ/Edge/Edge_260120/slepton_points/ " 

    binname = "slepton"
    if dowhat != 'cards':
        command += " --sP ^met_slepton "
    else:
        command = command.replace("--xp TSleps.*","")
    if dowhat == "plots": 
        command += " susy-edge/plots.txt --showIndivSigs --noStackSig "

    if '_onz' in TODO:
        command += " -I ^zveto " 
        binname = binname + '_onz'
    else:
        binname = binname + '_offz'

    if "withjet" in TODO:
        command += " -E ^sr_withjet "
        binname = binname + '_withjets'
    elif "withoutjet" in TODO:
        command += " -E ^sr_wojets "
        binname = binname + '_nojets'

    elif "domll" in TODO:
        command += " -U ^SF --xp DY -X ^zveto --sP ^mll --sP ^mll_inout"
        command = command.replace("--showRatio","")

    if "do_closure_inout" in TODO:
        command = command.replace("susy-edge/mca-{year}-dd-data-offz.txt".format(year = YEAR if YEAR != "all" else "{year}"), "susy-edge/mca-{year}-dy-inv.txt".format(year = YEAR if YEAR != "all" else "{year}"))
        command = command + ' --plotmode norm -X ^zveto --sP ^mll_inout ' 
        command = command + ' --ratioNums DY_extra4 --ratioDen DY_extra1 '
        command = command.replace("--legendColumns 3","")
    if binname == "slepton_onz_withjets":
        command += " --ap DY_onZ_withjet "
    if binname == "slepton_onz_nojets":
        command += " --ap DY_onZ_nojet "
    if binname == "slepton_offz_withjets":
        command += " --ap DY_offZ_withjet "
    if binname == "slepton_offz_nojets":
        command += " --ap DY_offZ_nojet "


    command = command + " --binname %s "%binname
    if dowhat == "cards":
        command += " --unc susy-edge/systUnc.txt --bbb mcstat --categorize MET_pt_Edge [100,150,225,300,14000] low,med,high,vhigh  --scanregex 'TSlepslep_(?P<m1>.*)_(?P<m2>.*)'  --params m1,m2 1 1,0.5,1.5  --ap TSlepslep_700_0 --outdir cards_apr1_v2 "

    if '_withz' in TODO:
        command += " -X ^zveto --sP ^mll"
    if '_relax' in TODO:
        command += " -X ^met -X ^mt2 -A ^alwaystrue extracut 'MET_pt_Edge > 50 && mt2_Edge >50 ' "
    command= submit.format(command=command)

if TODO.startswith('tchiwz_boosted'):
    command += " susy-edge/mca-{year}-dd-data.txt ".format(year = YEAR if YEAR != "all" else "{year}")
    command += " susy-edge/regions/tchiwz_boosted.txt "
    if dowhat == "plots": 
        command += " susy-edge/plots.txt --showIndivSigs --noStackSig --sP met_wzboosted "
    if 'dump_data_50_100' in TODO: 
        command +=  " -p data -A ^alwaystrue blind 'MET_pt_Edge > 50 && MET_pt_Edge < 100' {run_Edge}:{lumi_Edge}:{evt_Edge} > %s.txt"%(TODO)

if TODO.startswith('tchiwz_resolved'):
    command += " susy-edge/mca-{year}-dd-data.txt ".format(year = YEAR if YEAR != "all" else "{year}")
    command += " susy-edge/regions/tchiwz_resolved.txt "
    if dowhat == "plots": 
        command += " susy-edge/plots.txt --showIndivSigs --noStackSig --sP met_resolved "
    if 'dump_data_50_100' in TODO: 
        command +=  " -p data -A ^alwaystrue blind 'MET_pt_Edge > 50 && MET_pt_Edge < 100' {run_Edge}:{lumi_Edge}:{evt_Edge} > %s.txt"%(TODO)

if TODO.startswith('strong_onz'):
    command += " susy-edge/mca-{year}-dd-data.txt ".format(year = YEAR if YEAR != "all" else "{year}")
    command += " susy-edge/regions/strong-onz.txt "
    thecommand = '' 
    for subreg in 'SRA_btag,SRA_bveto,SRB_btag,SRB_bveto,SRC_btag,SRC_bveto'.split(','):
        subcommand = command + ' -E ^%s'%subreg
        subcommand = subcommand + ' --ap template_%s'%subreg
        if dowhat == "plots": 
            subcommand += " susy-edge/plots.txt --showIndivSigs --noStackSig --sP met_strong_%s "%subreg
        if 'dump_data_50_100' in TODO: 
            subcommand +=  " -p data -A ^alwaystrue blind 'MET_pt_Edge > 50 && MET_pt_Edge < 100' {run_Edge}:{lumi_Edge}:{evt_Edge} > %s_%s.txt"%(TODO,subreg)
            subcommand = subcommand.replace( '--ap template_%s'%subreg, '')
        thecommand += submit.format(command=subcommand) + '\n'
    command = thecommand

if TODO.startswith("cr_sleptons_3l"):
    command += " susy-edge/mca-{year}-mc-data.txt ".format(year = YEAR if YEAR != "all" else "{year}")
    command += " susy-edge/regions/slepton_3lcr.txt " 
    command += " -W 'LepSF(Lep1_pt_Edge,Lep1_eta_Edge,Lep1_pdgId_Edge,year)*LepSF(Lep2_pt_Edge,Lep2_eta_Edge,Lep2_pdgId_Edge,year)*LepSF(Lep3_pt_Edge,Lep3_eta_Edge,Lep3_pdgId_Edge,year)' " 
    if dowhat == "plots": 
        command += " susy-edge/plots.txt "

if TODO.startswith("cr_sleptons_4l"):
    command += " susy-edge/mca-{year}-mc-data.txt ".format(year = YEAR if YEAR != "all" else "{year}")
    command += " susy-edge/regions/slepton_4lcr.txt " 
    command += " -W 'LepSF(Lep1_pt_Edge,Lep1_eta_Edge,Lep1_pdgId_Edge,year)*LepSF(Lep2_pt_Edge,Lep2_eta_Edge,Lep2_pdgId_Edge,year)' " 
    if dowhat == "plots": 
        command += " susy-edge/plots.txt "

if TODO.startswith("cr_ttbar_analaysis"):
    command += " susy-edge/mca-{year}-mc-data.txt ".format(year = YEAR if YEAR != "all" else "{year}")
    command += " susy-edge/regions/dilep.txt -E ^em -E ^nj2 -E ^nb1 -X ^diLeptonPt " 
    command += " -W 'LepSF(Lep1_pt_Edge,Lep1_eta_Edge,Lep1_pdgId_Edge,year)*LepSF(Lep2_pt_Edge,Lep2_eta_Edge,Lep2_pdgId_Edge,year)*TriggerSF(Lep1_pdgId_Edge,Lep2_pdgId_Edge,year)' " 
    if dowhat == "plots": 
        command += " susy-edge/plots.txt "

if TODO.startswith("cr_dy"):
    command += " susy-edge/mca-{year}-mc-data.txt ".format(year = YEAR if YEAR != "all" else "{year}")
    command += " susy-edge/regions/dilep.txt -X ^diLeptonPt " 
    command += " -W 'LepSF(Lep1_pt_Edge,Lep1_eta_Edge,Lep1_pdgId_Edge,year)*LepSF(Lep2_pt_Edge,Lep2_eta_Edge,Lep2_pdgId_Edge,year)*TriggerSF(Lep1_pdgId_Edge,Lep2_pdgId_Edge,year)' " 
    command = command.replace('--maxRatioRange 0.6 1.99','--maxRatioRange 0.9 1.3')
    if dowhat == "plots": 
        command += " susy-edge/plots.txt --sP year --sP njet25 --sP njet35 "
    if '_dynamicveto' in TODO: 
        command += " -E ^nj1 "
        command = command.replace("--sP year --sP njet25 --sP njet35", "--sP  lep2_over_jet1 " ) 
    command = submit.format(command=command)
    thecommand = '' 
#    for subreg in 'ee,mm'.split(','):
#        subcommand = command + ' -E %s'%subreg
#        subcommand = subcommand.replace(ODIR, ODIR+'_%s'%subreg)
#        thecommand += subcommand + '\n'
#    command= thecommand

print command
