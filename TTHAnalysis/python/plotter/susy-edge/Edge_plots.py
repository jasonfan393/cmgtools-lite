#!/usr/bin/env python
import sys
import re
import os

#dowhat="plots"
dowhat="yields"


ODIR=sys.argv[1]
YEAR=sys.argv[2]
TODO=sys.argv[3]

lumis = {
'2016': '35.9',
'2017': '41.4',
'2018': '59.7',
'all' : '35.9,41.4,59.7',
}

submit = '{command}' 
nCores = 32
TREES = " -P /pool/ciencias/HeppyTrees/EdgeZ/Edge/Edge_190120/ --Fs {P}/1_trigger --FMCs {P}/2_btags --FMCs {P}/4_kfactor --Fs {P}/5_massvars  --obj Events --genWeightName genWeight_Edge " 

command=""

if dowhat == "plots":
    command += "python mcPlots.py --pdir %s "%ODIR
elif dowhat == "yields":
    command += "python mcAnalysis.py " 


command += " -f -j {ncores} -l {lumi} --year {year} -L susy-edge/functions-edge.cc --tree nanoAODskim --split-factor=-1 ".format(ncores=nCores, lumi=lumis[YEAR], year=(YEAR if YEAR in '2016,2017,2018'.split(',') else '2016,2017,2018'))
command += TREES

if dowhat == "plots":
    command += " --maxRatioRange 0.6 1.99 --ratioYNDiv 210 --showRatio --attachRatioPanel --fixRatioRange --legendColumns 3 --legendWidth 0.52 --legendFontSize 0.042 --noCms --topSpamSize 1.1 --lspam '#scale[1.1]{#bf{CMS}} #scale[0.9]{#it{Preliminary}}' --showMCError "


if TODO.startswith("sleptons"):
    command += " susy-edge/mca-{year}-dd-data-offz.txt ".format(year = YEAR if YEAR != "all" else "{year}")
    command += " susy-edge/regions/slepton.txt "
    command += " -W 'LepSF(Lep1_pt_Edge,Lep1_eta_Edge,Lep1_pdgId_Edge,year)*LepSF(Lep2_pt_Edge,Lep2_eta_Edge,Lep2_pdgId_Edge,year)' "
    command += " --ap TSlepslep_550_275 --xp TSleps.* " 

    if dowhat == "plots": 
        command += " susy-edge/plots.txt --showIndivSigs --noStackSig "

    if "withjet" in TODO:
        command += " -E ^sr_withjet "
    elif "withoutjet" in TODO:
        command += " -E ^sr_wojets "

if TODO.startswith('tchiwz_boosted'):
    command += " susy-edge/mca-{year}-dd-data.txt ".format(year = YEAR if YEAR != "all" else "{year}")
    command += " susy-edge/regions/tchiwz_boosted.txt "
    if dowhat == "plots": 
        command += " susy-edge/plots.txt --showIndivSigs --noStackSig --sP met_wzboosted "

if TODO.startswith('tchiwz_resolved'):
    command += " susy-edge/mca-{year}-dd-data.txt ".format(year = YEAR if YEAR != "all" else "{year}")
    command += " susy-edge/regions/tchiwz_resolved.txt "
    command += " --ap template_SRWZ_resolved"
    if dowhat == "plots": 
        command += " susy-edge/plots.txt --showIndivSigs --noStackSig --sP met_wzresolved "

if TODO.startswith('strong_onz'):
    command += " susy-edge/mca-{year}-dd-data.txt ".format(year = YEAR if YEAR != "all" else "{year}")
    command += " susy-edge/regions/strong-onz.txt "
    thecommand = '' 
    for subreg in 'SRA_btag,SRA_bveto,SRB_btag,SRB_bveto,SRC_btag,SRC_bveto'.split(','):
        subcommand = command + ' -E ^%s'%subreg
        subcommand = subcommand + ' --ap template_%s'%subreg
        if dowhat == "plots": 
            subcommand += " susy-edge/plots.txt --showIndivSigs --noStackSig --sP met_strong_%s "%subreg

        thecommand += subcommand + '\n'
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
        command += " susy-edge/plots.txt --sP year "
    thecommand = '' 
    for subreg in 'ee,mm'.split(','):
        subcommand = command + ' -E %s'%subreg
        subcommand = subcommand.replace(ODIR, ODIR+'_%s'%subreg)
        thecommand += subcommand + '\n'
    command= thecommand

print command
