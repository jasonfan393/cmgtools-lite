#include<iostream>
#include<map>
#include"TH1.h"
#include"TH2.h"
#include"TGraphAsymmErrors.h"
#include"TFile.h"
#include "TRandom3.h"
#include <vector>
#include <algorithm>
#include <numeric>
#include "TMath.h"
#include "TVector2.h"
#include "RooWorkspace.h"
#include "RooAbsPdf.h"
#include "RooRealVar.h"

using namespace std;

std::map<int,vector<TH2*>> hElec;
std::map<int,vector<TH2*>> hMuon;



TFile *elFile_2016_1, *elFile_2016_2, *elFile_2017_1, *elFile_2017_2, *elFile_2018_1, *elFile_2018_2, *muFile_2016_1, *muFile_2016_2, *muFile_2016_3, *muFile_2016_4, *muFile_2017_1, *muFile_2017_2, *muFile_2018_1, *muFile_2018_2;

bool setup = false;


void loadLeptonSF()
{
  setup = true;

  // electrons 

  // 2016
  elFile_2016_1 = TFile::Open("../../data/2016/ElectronScaleFactors_Run2016.root");
  hElec[2016].push_back( (TH2*)  elFile_2016_1->Get("Run2016_LeptonMvaVTIDEmuTightIP2DSIP3D8miniIso04") );
  hElec[2016].push_back( (TH2*)  elFile_2016_1->Get("Run2016_ConvIHit0") );

  elFile_2016_2 = TFile::Open("../../data/2016/EGM2D_BtoH_GT20GeV_RecoSF_Legacy2016.root");
  hElec[2016].push_back( (TH2*)  elFile_2016_2->Get("EGamma_SF2D") );

  // 2017

  elFile_2017_1 = TFile::Open("../../data/2017/leptonSF/ElectronScaleFactors_Run2017.root");
  hElec[2017].push_back( (TH2*)  elFile_2017_1->Get("Run2017_MVATightTightIP2D3D"));
  hElec[2017].push_back( (TH2*)  elFile_2017_1->Get("Run2017_MVAVLooseTightIP2DMini"));
  hElec[2017].push_back( (TH2*)  elFile_2017_1->Get("Run2017_ConvIHit0"));

  elFile_2017_2 = TFile::Open("../../data/2017/leptonSF/egammaEffi.txt_EGM2D_runBCDEF_passingRECO.root");
  hElec[2017].push_back( (TH2*)  elFile_2017_2->Get("EGamma_SF2D"));

  // 2018
  elFile_2018_1 = TFile::Open("../../data/2018/egammaEffi.txt_EGM2D_updatedAll.root");
  hElec[2018].push_back( (TH2*)  elFile_2018_1->Get("EGamma_SF2D"));
  
  elFile_2018_2 = TFile::Open("../../data/2018/ElectronScaleFactors_Run2018.root");
  hElec[2018].push_back( (TH2*)  elFile_2018_2->Get("Run2018_MVATightTightIP2D3D"));
  hElec[2018].push_back( (TH2*)  elFile_2018_2->Get("Run2018_Mini"));
  hElec[2018].push_back( (TH2*)  elFile_2018_2->Get("Run2018_ConvIHit0"));

  // Muons
  // 2016
  muFile_2016_1 = TFile::Open("../../data/2016/TnP_NUM_MediumID_DENOM_generalTracks_VAR_map_pt_eta.root");
  hMuon[2016].push_back( (TH2*)  muFile_2016_1->Get("SF"));
  muFile_2016_2 = TFile::Open("../../data/2016/TnP_NUM_MiniIsoLoose_DENOM_MediumID_VAR_map_pt_eta.root");
  hMuon[2016].push_back( (TH2*)  muFile_2016_2->Get("SF"));
  muFile_2016_3 = TFile::Open("../../data/2016/TnP_NUM_TightIP2D_DENOM_MediumID_VAR_map_pt_eta.root");
  hMuon[2016].push_back( (TH2*)  muFile_2016_3->Get("SF"));
  muFile_2016_4 = TFile::Open("../../data/2016/TnP_NUM_TightIP3D_DENOM_MediumID_VAR_map_pt_eta.root");
  hMuon[2016].push_back( (TH2*)  muFile_2016_4->Get("SF"));

  // 2017
  muFile_2017_1 = TFile::Open("../../data/2017/leptonSF/RunBCDEF_SF_ID.root");
  hMuon[2017].push_back( (TH2*)  muFile_2017_1->Get("NUM_MediumPromptID_DEN_genTracks_pt_abseta"));
  muFile_2017_2 = TFile::Open("../../data/2017/leptonSF/SF_num_miniiso_denmediumprompt.root");
  hMuon[2017].push_back( (TH2*)  muFile_2017_2->Get("TnP_MC_NUM_MiniIso02Cut_DEN_MediumCutidPromptCut_PAR_pt_eta"));

  // 2018
  muFile_2018_1 = TFile::Open("../../data/2018/RunABCD_SF_ID.root");
  hMuon[2018].push_back( (TH2*)  muFile_2018_1->Get("NUM_MediumPromptID_DEN_TrackerMuons_pt_abseta"));
  muFile_2018_2 = TFile::Open("../../data/2017/leptonSF/SF_num_miniiso_denmediumprompt.root");
  hMuon[2018].push_back( (TH2*)  muFile_2018_2->Get("TnP_MC_NUM_MiniIso02Cut_DEN_MediumCutidPromptCut_PAR_pt_eta"));
  

  

}

Double_t LepSF(Double_t pt, Double_t eta, Int_t pdgId, int year, TString sys="")
{
  if (!setup) loadLeptonSF();
  // sys can be 
  // "": nominal
  // "ElUp": obvious
  // "ElDn": obvious
  // "MuUp": obvious
  // "MuDn": obvious
  // cout << "[LepSF]" << pt << " " << eta << " " << pdgId << " " << sys << endl;

  vector<TH2*> hists = abs(pdgId)==11 ? hElec[year] : hMuon[year];
  float out = 1;
  int var = 0;

  if (sys.Contains("Up")) var = 1;
  else if (sys.Contains("Dn")) var = 1;
  else var = 0;

  for (auto hist : hists){
    int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
    out *=  hist->GetBinContent(ptbin,etabin)+var*hist->GetBinError(ptbin,etabin);
    if (abs(pdgId) == 13)
      out = out+var*out*0.03;
  }
  return out;
}


Double_t TriggerSF(int pdgid1, int pdgid2, int year)
{
  if (year == 2016){
    if (fabs(pdgid1*pdgid2) == 121) return 0.916/0.933;
    if (fabs(pdgid1*pdgid2) == 143) return 0.890/0.917;
    if (fabs(pdgid1*pdgid2) == 169) return 0.949/0.980;
  }
  if (year == 2017){
    if (fabs(pdgid1*pdgid2) == 121) return 0.906/0.955;
    if (fabs(pdgid1*pdgid2) == 143) return 0.858/0.928;
    if (fabs(pdgid1*pdgid2) == 169) return 0.873/0.947;
  }
  if (year == 2018){
    if (fabs(pdgid1*pdgid2) == 121) return 0.923/0.949;
    if (fabs(pdgid1*pdgid2) == 143) return 0.898/0.926;
    if (fabs(pdgid1*pdgid2) == 169) return 0.925/0.953;
  }

}



int njnb(int j, int b){
  if (j == 0 && b == 0) return 0;
  if (j == 1 && b == 0) return 1;
  if (j == 1 && b == 1) return 2;  
  if (j == 2 && b == 0) return 3;
  if (j == 2 && b == 1) return 4;
  if (j == 2 && b == 2) return 5;
  else return 6;
}




std::vector<int> boundaries_runPeriod2016 = {272007,275657,276315,276831,277772,278820,280919};
std::vector<int> boundaries_runPeriod2017 = {297020,299337,302030,303435,304911};
std::vector<int> boundaries_runPeriod2018 = {315252,316998,319313,320394};

std::vector<double> lumis_runPeriod2016 = {5.75, 2.573, 4.242, 4.025, 3.105, 7.576, 8.651};
std::vector<double> lumis_runPeriod2017 = {4.802,9.629,4.235,9.268,13.433};
std::vector<double> lumis_runPeriod2018 = {13.978 , 7.064 , 6.899 , 31.748};

bool cumul_lumis_isInit = false;
std::vector<float> cumul_lumis_runPeriod2016;
std::vector<float> cumul_lumis_runPeriod2017;
std::vector<float> cumul_lumis_runPeriod2018;

int runPeriod(int run, int year){
  std::vector<int> boundaries;
  if (year == 2016)
    boundaries = boundaries_runPeriod2016;
  else if (year == 2017)
    boundaries = boundaries_runPeriod2017;
  else if (year == 2018)
    boundaries = boundaries_runPeriod2018;
  else{
    std::cout << "Wrong year " << year << std::endl;
    return -99;
  }
  auto period = std::find_if(boundaries.begin(),boundaries.end(),[run](const int &y){return y>run;});
  return std::distance(boundaries.begin(),period)-1 + ( (year == 2017) ? 7 : 0 ) + ( (year == 2018) ? 12 : 0 ) ;
}

TRandom3 rand_generator_RunDependentMC(0);
int hashBasedRunPeriod2017(int isData, int run, int lumi, int event, int year){
  if (isData) return runPeriod(run,year);
  if (!cumul_lumis_isInit){
    cumul_lumis_runPeriod2016.push_back(0);
    cumul_lumis_runPeriod2017.push_back(0);
    cumul_lumis_runPeriod2018.push_back(0);
    float tot_lumi_2016 = std::accumulate(lumis_runPeriod2016.begin(),lumis_runPeriod2016.end(),float(0.0));
    float tot_lumi_2017 = std::accumulate(lumis_runPeriod2017.begin(),lumis_runPeriod2017.end(),float(0.0));
    float tot_lumi_2018 = std::accumulate(lumis_runPeriod2018.begin(),lumis_runPeriod2018.end(),float(0.0));

    for (uint i=0; i<lumis_runPeriod2016.size(); i++) cumul_lumis_runPeriod2016.push_back(cumul_lumis_runPeriod2016.back()+lumis_runPeriod2016[i]/tot_lumi_2016);
    for (uint i=0; i<lumis_runPeriod2017.size(); i++) cumul_lumis_runPeriod2017.push_back(cumul_lumis_runPeriod2017.back()+lumis_runPeriod2017[i]/tot_lumi_2017);
    for (uint i=0; i<lumis_runPeriod2018.size(); i++) cumul_lumis_runPeriod2018.push_back(cumul_lumis_runPeriod2018.back()+lumis_runPeriod2018[i]/tot_lumi_2018);
    cumul_lumis_isInit = true;
  }
  Int_t x = 161248*run+2136324*lumi+12781432*event;
  unsigned int hash = TString::Hash(&x,sizeof(Int_t));
  rand_generator_RunDependentMC.SetSeed(hash);
  float val = rand_generator_RunDependentMC.Uniform();
  
  vector<float> cumul;
  if (year == 2016) cumul = cumul_lumis_runPeriod2016;
  else if (year == 2017) cumul = cumul_lumis_runPeriod2017;
  else if (year == 2018) cumul = cumul_lumis_runPeriod2018;
  else{
    std::cout << "Wrong year " << year << std::endl;
    return -99;
  }
  auto period = std::find_if(cumul.begin(),cumul.end(),[val](const float &y){return y>val;});
  return std::distance(cumul.begin(),period)-1 + ( (year == 2017) ? 7 : 0 ) + ( (year == 2018) ? 12 : 0 );
}
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/lexical_cast.hpp>
#include <map>

bool init=false;
std::map<std::string,float> rmue_map2016,rmue_map2017,rmue_map2018;
std::map<std::string,float> rmue_map2016_mc,rmue_map2017_mc,rmue_map2018_mc;

float rmuecorrection(float pt1,float pt2,float eta1,float eta2,float pdgId1,float pdgId2, int year, int var=0, int isMC=0)
{

  // var code 
  // var = 0 => nominal
  // var = +/- 1 => up/down normalization variation
  // var = +/- 2 => up/down pt dependent variation
  // var = +/- 3 => up/down eta dependent variation
  // var = +/- 4 => RT variation (to-do) 


  if ( (abs(pdgId1)+abs(pdgId2)) != 24){
    return 0;
  }

  


  if (!init){
    init=true;
    boost::property_tree::ptree jsonTree2016, jsonTree2017, jsonTree2018;
    boost::property_tree::ptree jsonTree2016_mc, jsonTree2017_mc, jsonTree2018_mc;

    boost::property_tree::read_json("../../data/rmue/rMuE_correctionParameters_ZPeakControl_Run2016_36fb.json",jsonTree2016);
    boost::property_tree::read_json("../../data/rmue/rMuE_correctionParameters_ZPeakControl_Run2017_42fb.json",jsonTree2017);
    boost::property_tree::read_json("../../data/rmue/rMuE_correctionParameters_ZPeakControl_Run2018_60fb.json",jsonTree2018);

    boost::property_tree::read_json("../../data/rmue/rMuE_correctionParameters_ZPeakControl_Run2016_36fb_MC.json",jsonTree2016_mc);
    boost::property_tree::read_json("../../data/rmue/rMuE_correctionParameters_ZPeakControl_Run2017_42fb_MC.json",jsonTree2017_mc);
    boost::property_tree::read_json("../../data/rmue/rMuE_correctionParameters_ZPeakControl_Run2018_60fb_MC.json",jsonTree2018_mc);

    for (boost::property_tree::ptree::const_iterator it = jsonTree2016.begin(); it!=jsonTree2016.end(); ++it) {
      std::string field = boost::lexical_cast<std::string>( it->first);
      double value = boost::lexical_cast<double>( it->second.data() );
      rmue_map2016[field] = value;
    }
    for (boost::property_tree::ptree::const_iterator it = jsonTree2017.begin(); it!=jsonTree2017.end(); ++it) {
      std::string field = boost::lexical_cast<std::string>( it->first);
      double value = boost::lexical_cast<double>( it->second.data() );
      rmue_map2017[field] = value;
    }
    for (boost::property_tree::ptree::const_iterator it = jsonTree2018.begin(); it!=jsonTree2018.end(); ++it) {
      std::string field = boost::lexical_cast<std::string>( it->first);
      double value = boost::lexical_cast<double>( it->second.data() );
      rmue_map2018[field] = value;
    }

    for (boost::property_tree::ptree::const_iterator it = jsonTree2016_mc.begin(); it!=jsonTree2016_mc.end(); ++it) {
      std::string field = boost::lexical_cast<std::string>( it->first);
      double value = boost::lexical_cast<double>( it->second.data() );
      rmue_map2016_mc[field] = value;
    }
    for (boost::property_tree::ptree::const_iterator it = jsonTree2017_mc.begin(); it!=jsonTree2017_mc.end(); ++it) {
      std::string field = boost::lexical_cast<std::string>( it->first);
      double value = boost::lexical_cast<double>( it->second.data() );
      rmue_map2017_mc[field] = value;
    }
    for (boost::property_tree::ptree::const_iterator it = jsonTree2018_mc.begin(); it!=jsonTree2018_mc.end(); ++it) {
      std::string field = boost::lexical_cast<std::string>( it->first);
      double value = boost::lexical_cast<double>( it->second.data() );
      rmue_map2018_mc[field] = value;
    }

  }
  
  std::map<std::string,float> rmue_map = (isMC==0) ?  ((year == 2016) ? rmue_map2016 : (( year == 2017 ) ? rmue_map2017 : rmue_map2018)) : ((year == 2016) ? rmue_map2016_mc : (( year == 2017 ) ? rmue_map2017_mc : rmue_map2018_mc))  ;

  float rmue1 = rmue_map["norm"]*(rmue_map["ptOffset"] + rmue_map["ptFalling"]/pt1)*(rmue_map["etaParabolaBase"] + (eta1<-1.6)*rmue_map["etaParabolaMinus"]*pow(eta1+1.6, 2)+(eta1>1.6)*rmue_map["etaParabolaPlus"]*pow(eta1-1.6,2));
  float rmue2 = rmue_map["norm"]*(rmue_map["ptOffset"] + rmue_map["ptFalling"]/pt2)*(rmue_map["etaParabolaBase"] + (eta2<-1.6)*rmue_map["etaParabolaMinus"]*pow(eta2+1.6, 2)+(eta2>1.6)*rmue_map["etaParabolaPlus"]*pow(eta2-1.6,2));

  if (var == 1){
    rmue1*=1.05;
    rmue2*=1.05;
  }
  else if (var == -1){
    rmue1/=1.05;
    rmue2/=1.05;
  }
  else if (var == 2){
    rmue1 *= 1 + (0.05*(pt1-110)/90);
    rmue2 *= 1 + (0.05*(pt2-110)/90);
  }
  else if (var == -2){
    rmue1 /= 1 + (0.05*(pt1-110)/90);
    rmue2 /= 1 + (0.05*(pt2-110)/90);
  }
  else if (var == 3){
    rmue1 *= 1+ (0.05*(abs(eta1)-1.2)/1.2);
    rmue2 *= 1+ (0.05*(abs(eta2)-1.2)/1.2);
  }
  else if (var == -3){
    rmue1 /= 1+ (0.05*(abs(eta1)-1.2)/1.2);
    rmue2 /= 1+ (0.05*(abs(eta2)-1.2)/1.2);
  }


  float rt = 1; 
  if (year == 2016)
    rt = 1.049;
  else if (year == 2017)
    rt = 1.037;
  else
    rt = 1.029;
  
  
  if (abs(pdgId1) == 11){
    return rt*0.5*( rmue2 + 1/rmue1);
  }
  else{
    return rt*0.5*( rmue1 + 1/rmue2);
  }

}

float met_4l(float MET_pt_Edge, float  MET_phi_Edge,float  ptZ1_loose_Edge, float  phiZ1_loose_Edge){
  TVector2 met, z1;
  met.SetMagPhi( MET_pt_Edge, MET_phi_Edge);
  z1 .SetMagPhi( ptZ1_loose_Edge, phiZ1_loose_Edge);
  
  return (met+z1).Mod();
}

TFile* f_pdfs = 0; 
RooWorkspace*  f_w = 0;
RooAbsPdf* zptpdf = 0;
RooAbsPdf* metpdf = 0;
RooAbsPdf* ldppdf = 0;
RooAbsPdf* mlbpdf = 0;

float nll(float met, float zpt, float mlb, float ldp)
{
  if (!f_pdfs){
    f_pdfs = TFile::Open("../../data/pdfs_v4.root","READ");
    f_w = (RooWorkspace*) f_pdfs->Get("w");
  }

  f_w->var("lepsZPt_Edge")->setVal(zpt);
  float zptPdfVal = f_w->pdf("zpt_analyticalPDF_DA")->getVal(RooArgSet(*f_w->var("lepsZPt_Edge")));
  
  f_w->var("met_Edge")->setVal(met);
  float metPdfVal = f_w->pdf("met_analyticalPDF_DA")->getVal(RooArgSet(*f_w->var("met_Edge")));
  
  f_w->var("lepsDPhi_Edge")->setVal(ldp);
  float ldpPdfVal = f_w->pdf("ldp_analyticalPDF_DA")->getVal(RooArgSet(*f_w->var("lepsDPhi_Edge")));

  f_w->var("sum_mlb_Edge")->setVal(mlb);
  float mlbPdfVal = f_w->pdf("mlb_analyticalPDF_DA")->getVal(RooArgSet(*f_w->var("sum_mlb_Edge")));

  return -1.*TMath::Log(zptPdfVal*metPdfVal*ldpPdfVal*mlbPdfVal);
  
}


int strong_onz_category(int nJet25_Edge, int nBJetMedium25_Edge, float htJet25j, float mt2_Edge, float MET_pt_Edge)
{
  if (nJet25_Edge == 2 || nJet25_Edge == 3){
    if (nBJetMedium25_Edge == 0){ // SRA b-veto
      if (htJet25j < 500) return -1;
      if (mt2_Edge < 80) return -1;
      if (MET_pt_Edge < 50) return -1;
      return 1;
    }
    else{ // SRA b-tag
      if (htJet25j < 200) return -1;
      if (mt2_Edge < 100) return -1;
      if (MET_pt_Edge < 50) return -1;
      return 2;
    }
  }
  else if ( nJet25_Edge == 4 || nJet25_Edge == 5){
    if (nBJetMedium25_Edge == 0){ // SRB b-veto
      if (htJet25j < 500) return -1;
      if (mt2_Edge < 80) return -1;
      if (MET_pt_Edge < 50) return -1;
      return 3;
    }
    else{ // SRB b-tag
      if (htJet25j < 200) return -1;
      if (mt2_Edge < 100) return -1;
      if (MET_pt_Edge < 50) return -1;
      return 4;
    }
  }
  if (nJet25_Edge > 5){
    if (nBJetMedium25_Edge == 0){ // SRC b-veto
      if (mt2_Edge < 80) return -1;
      if (MET_pt_Edge < 50) return -1;
      return 5;
    }
    else{ // SRC b-tag
      if (mt2_Edge < 100) return -1;
      if (MET_pt_Edge < 50) return -1;
      return 6;
    }
  }
  return -1;
}
    

