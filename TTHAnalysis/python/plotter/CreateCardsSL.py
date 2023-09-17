import subprocess
import argparse
import os

parser = argparse.ArgumentParser()

training_specs = {}

parser.add_argument('--SR', type=str, default='', help='Signal Region')
parser.add_argument('--CR', type=str, default='', help='Control Region')
parser.add_argument('--y', type=str, default='2016,2016APV,2017,2018', help='Year')
parser.add_argument('--od', type=str, default='CardsSL', help='Output dir')
parser.add_argument('--combi', action='store_true', help='If true creates a combination of the selected years per signal region instead of individual cards per year')
parser.add_argument('--eft', action='store_true', help='If true creates eft cards')


FLAGS = parser.parse_args()

SRs = FLAGS.SR.split(',')
CRs = FLAGS.CR.split(',')
Years = FLAGS.y.split(',')
out_dir = FLAGS.od
combi = FLAGS.combi
eft = FLAGS.eft

list_SR = '2lss,2lss1tau,3l'.split(',')
list_CR = 'cr_3l,cr_4l'.split(',')

if 'all' in SRs:
    SRs=list_SR
if 'all' in CRs:
    CRs=list_CR

lumi = {
    '2016': '16.8',
    '2016APV': '19.5',
    '2017': '41.4',
    '2018': '59.7'
}

binning = {
    '2lss': '"catIndex_2lss_all_HiggsPt(LepGood1_pdgId, LepGood2_pdgId, DNN_2lss_predictions_ttH_low_Higgs_pt, DNN_2lss_predictions_ttH_high_Higgs_pt, DNN_2lss_predictions_ttW, DNN_2lss_predictions_tHQ, DNN_2lss_predictions_Rest, Hreco_dnn_prediction)" "121,-0.5,120.5"',
    '2lss1tau': '"catIndex_2lss1tau_all_HiggsPt(LepGood1_pdgId, LepGood2_pdgId, DNN_2lss1tau_predictions_ttH_low_Higgs_pt, DNN_2lss1tau_predictions_ttH_high_Higgs_pt, DNN_2lss1tau_predictions_tH, DNN_2lss1tau_predictions_rest, ttH_higgs_pt_2lss1tau_)" "21,-0.5,20.5"',
    '3l': '"catIndex_3l_all_HiggsPt(LepGood1_pdgId, LepGood2_pdgId, LepGood3_pdgId, DNN_3l_predictions_ttH_low_Higgs_pt, DNN_3l_predictions_ttH_high_Higgs_pt, DNN_3l_predictions_tH, DNN_3l_predictions_rest, Hreco_dnn_prediction_3l, nBJetMedium25_Recl)" "21,-0.5,20.5"',
}

classifier_list = {
    '2lss': '6_mva2lss_new',
    '2lss1tau': '6_mva2lss1tau',
    '3l': '6_mva3l',
}



for SR in SRs:
    if SR not in list_SR: continue

    print(SR)
    if combi:
        year_all = ','.join(Years)
        year_all_name = ''.join(Years)
        lumi_all = []

        bin = binning[SR]
        classifier = classifier_list[SR]

        for year in Years:
            lumi_all.append(lumi[year])
        lumi_all = ','.join(lumi_all)
        if SR == '2lss':
            command = 'python makeShapeCardsNew_unfolding.py ttH-multilepton/mca-2lss-mcdata-frdata-diff.txt ttH-multilepton/2lss_tight.txt {4} --unc ttH-multilepton/systsUnc.txt --amc --xu CMS_ttHl_TTZ_lnU,CMS_ttHl_TTW_lnU -P /pnfs/psi.ch/cms/trivcat/store/user/sesanche/NanoTrees_UL_v2_060422_newfts_skim2lss/ --FMCs {{P}}/0_jmeUnc_v1 --Fs {{P}}/1_recl --FMCs {{P}}/2_scalefactors_lep --FMCs {{P}}/2_btagSF --Fs {{P}}/3_tauCount --Fs {{P}}/4_evtVars --Fs {{P}}/5_BDThtt_reco --Fs {{P}}/{5} --Fs {{P}}/6_HiggsPtReg_2lss3l --xf GGHZZ4L_new,qqHZZ4L,WW_DPS,WpWpJJ,WWW_ll,T_sch_lep,GluGluToHHTo2V2Tau,WWTo2L2Nu_DPS,GluGluToHHTo4Tau,GluGluToHHTo4V,TTTW,ZGTo2LG --tree NanoAOD --s2v -j 16 -l {2} -f --WA prescaleFromSkim --split-factor=-1  --od {1} -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/lepchoice-ttH-FO.txt --mcc ttH-multilepton/mcc-METchoice-prefiring.txt --plotgroup data_fakes+=.*_promptsub --neg   --threshold 0.01 --asimov signal --filter ttH-multilepton/filter-processes.txt  -W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_2lss*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 2, year, suberaId)" --binname ttH_2lss_{3}_UL_SL --year {0} --tikhonov_unfolding pt_0_60,pt_60_120,pt_120_200,pt_200_300,pt_300_450,pt_450_inf rBin1,rBin2,rBin3,rBin4,rBin5,rBin6'.format(year_all, out_dir, lumi_all, year_all_name, bin, classifier)
        elif SR == '2lss1tau':
            command = 'python makeShapeCardsNew_unfolding.py ttH-multilepton/mca-2lss-mcdata-frdata-diff.txt ttH-multilepton/2lss_1tau.txt {4} --unc ttH-multilepton/systsUnc.txt --amc --xu CMS_ttHl_TTZ_lnU,CMS_ttHl_TTW_lnU -P /pnfs/psi.ch/cms/trivcat/store/user/sesanche/NanoTrees_UL_v2_060422_newfts_skim2lss/ --FMCs {{P}}/0_jmeUnc_v1 --Fs {{P}}/1_recl --FMCs {{P}}/2_scalefactors_lep --FMCs {{P}}/2_btagSF --Fs {{P}}/3_tauCount --Fs {{P}}/4_evtVars --Fs {{P}}/5_BDThtt_reco --Fs {{P}}/{5} --Fs {{P}}/6_HiggsPtReg_2lss1tau  --FMCs {{P}}/6_tauSF_new --xf GGHZZ4L_new,qqHZZ4L,WW_DPS,WpWpJJ,WWW_ll,T_sch_lep,GluGluToHHTo2V2Tau,WWTo2L2Nu_DPS,GluGluToHHTo4Tau,GluGluToHHTo4V,TTTW,ZGTo2LG --tree NanoAOD --s2v -j 16 -l {2} -f --WA prescaleFromSkim --split-factor=-1  --od {1} -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/lepchoice-ttH-FO.txt --mcc ttH-multilepton/mcc-METchoice-prefiring.txt --plotgroup data_fakes+=.*_promptsub --neg   --threshold 0.01 --asimov signal --filter ttH-multilepton/filter-processes.txt  -W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_2lss*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 2, year, suberaId)*TauSel_2lss1tau_SF" --binname ttH_2lss1tau_{3}_UL_SL --year {0} --tikhonov_unfolding pt_0_60,pt_60_120,pt_120_200,pt_200_300,pt_300_450,pt_450_inf rBin1,rBin2,rBin3,rBin4,rBin5,rBin6'.format(year_all, out_dir, lumi_all, year_all_name, bin, classifier)
        elif SR == '3l':
            command = 'python makeShapeCardsNew_unfolding.py ttH-multilepton/mca-3l-mcdata-frdata-diff.txt ttH-multilepton/3l_tight.txt {4} --unc ttH-multilepton/systsUnc.txt --amc --xu CMS_ttHl_TTZ_lnU,CMS_ttHl_TTW_lnU  -P /pnfs/psi.ch/cms/trivcat/store/user/sesanche/NanoTrees_UL_v2_060422_newfts_skim2lss/ --FMCs {{P}}/0_jmeUnc_v1 --Fs {{P}}/1_recl --FMCs {{P}}/2_scalefactors_lep --FMCs {{P}}/2_btagSF --Fs {{P}}/3_tauCount --Fs {{P}}/4_evtVars --Fs {{P}}/5_BDThtt_reco --Fs {{P}}/{5} --Fs {{P}}/6_HiggsPtReg_2lss3l --xf GGHZZ4L_new,qqHZZ4L,WW_DPS,WpWpJJ,WWW_ll,T_sch_lep,GluGluToHHTo2V2Tau,WWTo2L2Nu_DPS,GluGluToHHTo4Tau,GluGluToHHTo4V,TTTW,ZGTo2LG --tree NanoAOD --s2v -j 16 -l {2} -f --WA prescaleFromSkim --split-factor=-1  --od {1}  -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/lepchoice-ttH-FO.txt --mcc ttH-multilepton/mcc-METchoice-prefiring.txt --mcc ttH-multilepton/lepchoice-ttH-FO.txt --plotgroup data_fakes+=.*_promptsub --neg   --threshold 0.01 --asimov signal --filter ttH-multilepton/filter-processes.txt  -W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_3l*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 3, year, suberaId)" --binname ttH_3l_{3}_UL_SL --year {0} --tikhonov_unfolding pt_0_60,pt_60_120,pt_120_200,pt_200_300,pt_300_450,pt_450_inf rBin1,rBin2,rBin3,rBin4,rBin5,rBin6'.format(year_all, out_dir, lumi_all, year_all_name, bin, classifier)
        else:
            print(f'Unknown SR {SR}')
            exit()

        if eft:
            command = command.replace('frdata-diff', 'frdata-eft')
        
        print(command)

        output = subprocess.check_output(command, shell=True)
        print(output)
        with open('{}/{}_{}.out'.format(out_dir, SR, year), 'w') as f:
            f.write(f'{command}\n{output}')
        # os.system(command)

    else:

        bin = binning[SR]
        classifier = classifier_list[SR]

        for year in Years:
            if SR == '2lss':
                command = 'python makeShapeCardsNew_unfolding.py ttH-multilepton/mca-2lss-mcdata-frdata-diff.txt ttH-multilepton/2lss_tight.txt {3} --unc ttH-multilepton/systsUnc.txt --amc --xu CMS_ttHl_TTZ_lnU,CMS_ttHl_TTW_lnU -P /pnfs/psi.ch/cms/trivcat/store/user/sesanche/NanoTrees_UL_v2_060422_newfts_skim2lss/{0}/ --FMCs {{P}}/0_jmeUnc_v1 --Fs {{P}}/1_recl --FMCs {{P}}/2_scalefactors_lep --FMCs {{P}}/2_btagSF --Fs {{P}}/3_tauCount --Fs {{P}}/4_evtVars --Fs {{P}}/5_BDThtt_reco --Fs {{P}}/{4} --Fs {{P}}/6_HiggsPtReg_2lss3l --xf GGHZZ4L_new,qqHZZ4L,WW_DPS,WpWpJJ,WWW_ll,T_sch_lep,GluGluToHHTo2V2Tau,WWTo2L2Nu_DPS,GluGluToHHTo4Tau,GluGluToHHTo4V,TTTW,ZGTo2LG --tree NanoAOD --s2v -j 16 -l {2} -f --WA prescaleFromSkim --split-factor=-1  --od {1} -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/lepchoice-ttH-FO.txt --mcc ttH-multilepton/mcc-METchoice-prefiring.txt --plotgroup data_fakes+=.*_promptsub --neg   --threshold 0.01 --asimov signal --filter ttH-multilepton/filter-processes.txt  -W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_2lss*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 2, year, suberaId)" --binname ttH_2lss_{0}_UL_SL --year {0} --tikhonov_unfolding pt_0_60,pt_60_120,pt_120_200,pt_200_300,pt_300_450,pt_450_inf rBin1,rBin2,rBin3,rBin4,rBin5,rBin6'.format(year, out_dir, lumi[year], bin, classifier)
            elif SR == '2lss1tau':
                command = 'python makeShapeCardsNew_unfolding.py ttH-multilepton/mca-2lss-mcdata-frdata-diff.txt ttH-multilepton/2lss_1tau.txt {3} --unc ttH-multilepton/systsUnc.txt --amc --xu CMS_ttHl_TTZ_lnU,CMS_ttHl_TTW_lnU -P /pnfs/psi.ch/cms/trivcat/store/user/sesanche/NanoTrees_UL_v2_060422_newfts_skim2lss/{0}/ --FMCs {{P}}/0_jmeUnc_v1 --Fs {{P}}/1_recl --FMCs {{P}}/2_scalefactors_lep --FMCs {{P}}/2_btagSF --Fs {{P}}/3_tauCount --Fs {{P}}/4_evtVars --Fs {{P}}/5_BDThtt_reco --Fs {{P}}/{4} --Fs {{P}}/6_HiggsPtReg_2lss1tau --FMCs {{P}}/6_tauSF_new --xf GGHZZ4L_new,qqHZZ4L,WW_DPS,WpWpJJ,WWW_ll,T_sch_lep,GluGluToHHTo2V2Tau,WWTo2L2Nu_DPS,GluGluToHHTo4Tau,GluGluToHHTo4V,TTTW,ZGTo2LG --tree NanoAOD --s2v -j 16 -l {2} -f --WA prescaleFromSkim --split-factor=-1  --od {1} -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/lepchoice-ttH-FO.txt --mcc ttH-multilepton/mcc-METchoice-prefiring.txt --plotgroup data_fakes+=.*_promptsub --neg   --threshold 0.01 --asimov signal --filter ttH-multilepton/filter-processes.txt  -W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_2lss*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 2, year, suberaId)" --binname ttH_2lss1tau_{0}_UL_SL --year {0} --tikhonov_unfolding pt_0_60,pt_60_120,pt_120_200,pt_200_300,pt_300_450,pt_450_inf rBin1,rBin2,rBin3,rBin4,rBin5,rBin6'.format(year, out_dir, lumi[year], bin, classifier)
            elif SR == '3l':
                command = 'python makeShapeCardsNew_unfolding.py ttH-multilepton/mca-3l-mcdata-frdata-diff.txt ttH-multilepton/3l_tight.txt {3} --unc ttH-multilepton/systsUnc.txt --amc --xu CMS_ttHl_TTZ_lnU,CMS_ttHl_TTW_lnU  -P /pnfs/psi.ch/cms/trivcat/store/user/sesanche/NanoTrees_UL_v2_060422_newfts_skim2lss/{0}/ --FMCs {{P}}/0_jmeUnc_v1 --Fs {{P}}/1_recl --FMCs {{P}}/2_scalefactors_lep --FMCs {{P}}/2_btagSF --Fs {{P}}/3_tauCount --Fs {{P}}/4_evtVars --Fs {{P}}/5_BDThtt_reco --Fs {{P}}/{4} --Fs {{P}}/6_HiggsPtReg_2lss3l --xf GGHZZ4L_new,qqHZZ4L,WW_DPS,WpWpJJ,WWW_ll,T_sch_lep,GluGluToHHTo2V2Tau,WWTo2L2Nu_DPS,GluGluToHHTo4Tau,GluGluToHHTo4V,TTTW,ZGTo2LG --tree NanoAOD --s2v -j 16 -l {2} -f --WA prescaleFromSkim --split-factor=-1  --od {1}  -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/lepchoice-ttH-FO.txt --mcc ttH-multilepton/mcc-METchoice-prefiring.txt --mcc ttH-multilepton/lepchoice-ttH-FO.txt --plotgroup data_fakes+=.*_promptsub --neg   --threshold 0.01 --asimov signal --filter ttH-multilepton/filter-processes.txt  -W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_3l*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 3, year, suberaId)" --binname ttH_3l_{0}_UL_SL --year {0} --tikhonov_unfolding pt_0_60,pt_60_120,pt_120_200,pt_200_300,pt_300_450,pt_450_inf rBin1,rBin2,rBin3,rBin4,rBin5,rBin6'.format(year, out_dir, lumi[year], bin, classifier)
            else:
                print(f'Unknown SR {SR}')
                exit()

            if eft:
                command = command.replace('frdata-diff', 'frdata-eft')

            print(command)

            # output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = subprocess.check_output(command, shell=True)
            print(output)
            with open('{}/{}_{}.out'.format(out_dir, SR , year), 'w') as f:
                f.write(f'{command}\n{output}')

            # os.system(command)

for CR in CRs:
    if CR not in list_CR: continue
    print(CR)

    # os.system(command)

    for year in Years:
        command1 = 'python ttH-multilepton/make_cards_new.py CardsCR {} {}'.format(year, CR)
        command2 = subprocess.check_output(command1, shell=True)
        command2 = command2.decode().split('\n')[1]
        command2 = command2.replace('cards/CardsCR', '/work/sliechti/Differential/UL/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/python/plotter/{}/'.format(out_dir))
        if CR == 'cr_4l':
            command2 = command2.replace('/mca-4l-mcdata-frdata-splitdecays.txt', '/mca-4l-mcdata-frdata-diff.txt')
        if CR == 'cr_3l':
            command2 = command2.replace('/mca-3l-mcdata-frdata-splitdecays.txt', '/mca-3l-mcdata-frdata-diff.txt')

        # print(command2)

        os.system(command2)
        # output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # print(output)

            # os.system(command)