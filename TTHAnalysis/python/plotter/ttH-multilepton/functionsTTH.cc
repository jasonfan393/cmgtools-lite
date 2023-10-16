#include "TFile.h"
#include "TH2.h"
#include "TF1.h"
#include "TH2Poly.h"
#include "TGraphAsymmErrors.h"
#include "TRandom3.h"

#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <map>

float ttH_MVAto1D_6_2lss_Marco (float kinMVA_2lss_ttbar, float kinMVA_2lss_ttV){

  return 2*((kinMVA_2lss_ttbar>=-0.2)+(kinMVA_2lss_ttbar>=0.3))+(kinMVA_2lss_ttV>=-0.1)+1;

}
float ttH_MVAto1D_3_3l_Marco (float kinMVA_3l_ttbar, float kinMVA_3l_ttV){

  if (kinMVA_3l_ttbar<0.3 && kinMVA_3l_ttV<-0.1) return 1;
  else if (kinMVA_3l_ttbar>=0.3 && kinMVA_3l_ttV>=-0.1) return 3;
  else return 2;

}

#include "binning_2d_thresholds.h"
float ttH_MVAto1D_7_2lss_Marco (float kinMVA_2lss_ttbar, float kinMVA_2lss_ttV){

//________________
//|   |   |   | 7 |
//|   |   | 4 |___|
//| 1 | 2 |___| 6 |
//|   |   |   |___|
//|   |   | 3 | 5 |
//|___|___|___|___|
//

  if (kinMVA_2lss_ttbar<cuts_2lss_ttbar0) return 1;
  else if (kinMVA_2lss_ttbar<cuts_2lss_ttbar1) return 2;
  else if (kinMVA_2lss_ttbar<cuts_2lss_ttbar2) return 3+(kinMVA_2lss_ttV>=cuts_2lss_ttV0);
  else return 5+(kinMVA_2lss_ttV>=cuts_2lss_ttV1)+(kinMVA_2lss_ttV>=cuts_2lss_ttV2);

}
float ttH_MVAto1D_5_3l_Marco (float kinMVA_3l_ttbar, float kinMVA_3l_ttV){

  int reg = 2*((kinMVA_3l_ttbar>=cuts_3l_ttbar1)+(kinMVA_3l_ttbar>=cuts_3l_ttbar2))+(kinMVA_3l_ttV>=cuts_3l_ttV1)+1;
  if (reg==2) reg=1;
  if (reg>2) reg = reg-1;
  return reg;

}


float newBinning(float x, float y){
  float r =  4*((y>-0.16)+(y>0.28))+(x>-0.22)+(x>0.09)+(x>0.42)+1;
  if (r==9) r-=4;
  if (r>9) r-=1;
  return r;
}

//#include "GetBinning.C"


float ttH_MVAto1D_6_flex (float kinMVA_2lss_ttbar, float kinMVA_2lss_ttV, int pdg1, int pdg2, float ttVcut, float ttcut1, float ttcut2){

  return 2*((kinMVA_2lss_ttbar>=ttcut1)+(kinMVA_2lss_ttbar>=ttcut2)) + (kinMVA_2lss_ttV>=ttVcut)+1;

}

float returnInputX(float x, float y) {return x;}

float mvaCat(float ttH, float rest, float ttW, float thq){
  float ret = 0; 
  if (ttH > rest && ttH > ttW && ttH > thq){
    ret =  ttH;
  }
  if (ttW > ttH && ttW > rest && ttW > thq){
    ret= ttW+1;
  }
  if (thq > ttH && thq > ttW && thq > rest){
    ret= thq+2;
  }
  if (rest > ttH && rest > thq && rest > ttW){
    ret= rest+3;
  }
  return ret;

}

int ttH_catIndex_2lss(int LepGood1_pdgId, int LepGood2_pdgId, float tth, float ttw, float thq, float rest)
{

//2lss_ee_ttH
//2lss_ee_rest
//2lss_ee_ttw
//2lss_ee_thq
//2lss_em_ttH
//2lss_em_rest
//2lss_em_ttw
//2lss_em_thq
//2lss_mm_ttH
//2lss_mm_rest
//2lss_mm_ttw
//2lss_mm_thq  
  int flch = 0;
  int procch = 0;

  if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 22)
    flch = 0;
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 24)
    flch = 1;
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 26)
    flch = 2;
  else
    cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

  if (tth >= ttw && tth >= thq && tth >= rest)
    procch = 0;
  else if (rest >= tth && rest >= ttw && rest >= thq)
    procch = 1;
  else if (ttw >= tth && ttw >= rest && ttw >= thq)
    procch = 2;
  else if (thq >= tth && thq >= rest && thq >= ttw)
    procch = 3;
  else 
    cout << "[2lss]: It shouldnt be here. DNN scores are " << tth << " " << rest << " " << ttw << " " << thq << endl;
      
  return flch*4+procch+1;

}


std::vector<TString> bin2lsslabels = {
  "ee_ttHnode","ee_Restnode","ee_ttWnode","ee_tHQnode",
  "em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode",
  "mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"
};
TFile* f2lssBins;

std::map<TString,int> bins2lss = {{"ee_ttHnode",5},{"ee_Restnode",8},{"ee_ttWnode",6},{"ee_tHQnode",4},
				  {"em_ttHnode",13},{"em_Restnode",8},{"em_ttWnode",19},{"em_tHQnode",11},
				  {"mm_ttHnode",13},{"mm_Restnode",11},{"mm_ttWnode",15},{"mm_tHQnode",7}};
std::map<TString, TH1F*> binHistos2lss;
std::map<TString, int> bins2lsscumul;


std::map<TString, int> bins2lsscumul_cp;
std::map<TString,int> bins2lss_withcp = {{"ee_ttHnode",5*2},{"ee_Restnode",8},{"ee_ttWnode",6},{"ee_tHQnode",4},
					 {"em_ttHnode",13*4},{"em_Restnode",8},{"em_ttWnode",19},{"em_tHQnode",11},
					 {"mm_ttHnode",13*4},{"mm_Restnode",11},{"mm_ttWnode",15},{"mm_tHQnode",7}};


int ttH_catIndex_2lss_MVA_CP(int LepGood1_pdgId, int LepGood2_pdgId, float tth, float ttw, float thq, float rest, float cp)
{
  if (!f2lssBins){
    int offset = 0;
    f2lssBins = TFile::Open("../../data/kinMVA/DNNBin_v3_xmas.root");
    for (auto & la : bin2lsslabels){
      int bins = bins2lss[la];
      binHistos2lss[la] = (TH1F*) f2lssBins->Get(Form("%s_2018_Map_nBin%d", la.Data(), bins));
      bins2lsscumul_cp[la] = offset;
      offset += bins2lss_withcp[la];
    }
  }
  
  int idx = ttH_catIndex_2lss(LepGood1_pdgId, LepGood2_pdgId, tth,ttw, thq,rest); 
  TString binLabel = bin2lsslabels[idx-1];
  float mvavar = 0;
  int cpidx=0; int cpbins=1;
  if (tth >= ttw && tth >= thq && tth >= rest){
    mvavar = tth;
    if (abs(LepGood1_pdgId) + abs(LepGood2_pdgId) == 22){
      cpbins=2;
      if (cp < 0.165208) cpidx=0;
      else cpidx=1;
    }
    else{
      cpbins=4;
      if      (cp < 0.128845)  cpidx = 0;
      else if (cp < 0.165208)  cpidx = 1;
      else if (cp < 0.2208)    cpidx = 2;
      else                     cpidx = 3;
    }
  }
  else if (rest >= tth && rest >= ttw && rest >= thq)
    mvavar =rest;
  else if (ttw >= tth && ttw >= rest && ttw >= thq)
    mvavar = ttw;
  else if (thq >= tth && thq >= rest && thq >= ttw)
    mvavar = thq;
  else 
    cout << "It shouldnt be here" << endl;
  return binHistos2lss[binLabel]->FindBin( mvavar ) + binHistos2lss[binLabel]->GetNbinsX()*cpidx + bins2lsscumul_cp[binLabel];

}

int ttH_catIndex_2lss_MVA_CP_ttH(int LepGood1_pdgId, int LepGood2_pdgId, float tth, float ttw, float thq, float rest, float cp)
{
  int b;
  b = -99;
  int bin = ttH_catIndex_2lss_MVA_CP(LepGood1_pdgId, LepGood2_pdgId, tth,  ttw, thq, rest, cp);
  if (bin <=10) b = bin;
  else if (bin>=29 && bin<=80) b =bin-18;
  else if (bin>=119 && bin<=170) b = bin-(18+38);
  else 
    b=-99;
  return b;
}

int ttH_catIndex_2lss_MVA_CP_Rest(int LepGood1_pdgId, int LepGood2_pdgId, float tth, float ttw, float thq, float rest, float cp)
{
  int b;
  b = -99;
  int bin = ttH_catIndex_2lss_MVA_CP(LepGood1_pdgId, LepGood2_pdgId, tth,  ttw, thq, rest, cp);
  if (bin >10 && bin <=18) b = bin-10;
  else if (bin>80 && bin<=88) b =bin-62-10;
  else if (bin>170 && bin<=181) b = bin-(62+82+10);
  else 
    b=-99;
  return b;
}
//fixme
int ttH_catIndex_2lss_MVA_CP_ttW(int LepGood1_pdgId, int LepGood2_pdgId, float tth, float ttw, float thq, float rest, float cp)
{
  int b;
  b = -99;
  int bin = ttH_catIndex_2lss_MVA_CP(LepGood1_pdgId, LepGood2_pdgId, tth,  ttw, thq, rest, cp);
  if (bin >=19 && bin <25) b = bin-10-8;
  else if (bin>88 && bin<=107) b =bin-64-10-8;
  else if (bin>=181 && bin<=196) b = bin-(74+64+10+8);
  else 
    b=-99;
  return b;
}
int ttH_catIndex_2lss_MVA_CP_tH(int LepGood1_pdgId, int LepGood2_pdgId, float tth, float ttw, float thq, float rest, float cp)
{
  int b;
  b = -99;
  int bin = ttH_catIndex_2lss_MVA_CP(LepGood1_pdgId, LepGood2_pdgId, tth,  ttw, thq, rest, cp);
  if (bin >=25 && bin <29) b = bin-10-8-6;
  else if (bin>107 && bin<=119) b =bin-79-10-8-6;
  else if (bin>196 && bin<=203) b = bin-(78+79+10+8+6);
  else 
    b=-99;
  return b;
}



int ttH_catIndex_2lss_MVA(int LepGood1_pdgId, int LepGood2_pdgId, float tth, float ttw, float thq, float rest)
{
  if (!f2lssBins){
    int offset = 0;
    f2lssBins = TFile::Open("../../data/kinMVA/DNNBin_v3_xmas.root");
    for (auto & la : bin2lsslabels){
      int bins = bins2lss[la];
      binHistos2lss[la] = (TH1F*) f2lssBins->Get(Form("%s_2018_Map_nBin%d", la.Data(), bins));
      bins2lsscumul[la] = offset;
      offset += bins;
    }
  }
  int idx = ttH_catIndex_2lss(LepGood1_pdgId, LepGood2_pdgId, tth,ttw, thq,rest); 
  TString binLabel = bin2lsslabels[idx-1];
  float mvavar = 0;
  if (tth >= ttw && tth >= thq && tth >= rest)
    mvavar = tth;
  else if (rest >= tth && rest >= ttw && rest >= thq)
    mvavar =rest;
  else if (ttw >= tth && ttw >= rest && ttw >= thq)
    mvavar = ttw;
  else if (thq >= tth && thq >= rest && thq >= ttw)
    mvavar = thq;
  else 
    cout << "It shouldnt be here" << endl;

  return binHistos2lss[binLabel]->FindBin( mvavar ) + bins2lsscumul[binLabel];

}


// for plots

int ttH_2lss_node( float tth, float ttw, float thq, float rest ){

  int procch = 0;
  if (tth >= ttw && tth >= thq && tth >= rest)
    procch = 0;
  else if (rest >= tth && rest >= ttw && rest >= thq)
    procch = 1;
  else if (ttw >= tth && ttw >= rest && ttw >= thq)
    procch = 2;
  else if (thq >= tth && thq >= rest && thq >= ttw)
    procch = 3;
  else 
    cout << "[2lss]: It shouldnt be here. DNN scores are " << tth << " " << rest << " " << ttw << " " << thq << endl;

  return procch;
}


std::vector<TString> bin2lsslabels_plots = {
  "ee_ttHnode" , "em_ttHnode" ,  "mm_ttHnode", 
  "ee_Restnode", "em_Restnode",  "mm_Restnode",
  "ee_ttWnode" , "em_ttWnode" ,  "mm_ttWnode",
  "ee_tHQnode" , "em_tHQnode" ,  "mm_tHQnode",

};

std::map<TString, TH1F*> binHistos2lss_plots;
TFile* f2lssBins_plots;


int ttH_catIndex_2lss_plots(int LepGood1_pdgId, int LepGood2_pdgId, float tth, float ttw, float thq, float rest)
{

  if (!f2lssBins_plots){
    f2lssBins_plots = TFile::Open("../../data/kinMVA/DNNBin_v3_xmas.root");
    for (auto & la : bin2lsslabels_plots){
      int bins = bins2lss[la];
      binHistos2lss_plots[la] = (TH1F*) f2lssBins_plots->Get(Form("%s_2018_Map_nBin%d", la.Data(), bins));
    }
  }

  int idx = ttH_catIndex_2lss(LepGood1_pdgId, LepGood2_pdgId, tth,ttw, thq,rest); 
  TString binLabel = bin2lsslabels[idx-1];
  int offset=0;
  int node = ttH_2lss_node(tth, ttw,thq, rest);
  if (abs(LepGood1_pdgId*LepGood2_pdgId) == 143){
    if (node == 0) offset = 5;
    else if (node == 1) offset = 8;
    else if (node == 2) offset = 6;
    else offset = 4;
  }
  if (abs(LepGood1_pdgId*LepGood2_pdgId) == 169){
    if (node == 0) offset = 5+13;
    else if (node == 1) offset = 8+8;
    else if (node == 2) offset = 6+19;
    else offset = 4+11;
  }

  float mvavar = 0;
  if (tth >= ttw && tth >= thq && tth >= rest)
    mvavar = tth;
  else if (rest >= tth && rest >= ttw && rest >= thq)
    mvavar =rest;
  else if (ttw >= tth && ttw >= rest && ttw >= thq)
    mvavar = ttw;
  else if (thq >= tth && thq >= rest && thq >= ttw)
    mvavar = thq;
  else 
    cout << "It shouldnt be here" << endl;


  return binHistos2lss_plots[binLabel]->FindBin( mvavar ) + offset;
    

}

float ttH_ClassifierCut_3l(float tth_low, float tth_high, float thq, float bkg)
{
  if ((bkg > 0.28) && (thq < 0.7) && (tth_high < 0.5)){
	if (bkg < 0.45)       return 0;
    else                  return 1;
  }
  else if ((thq > 0.7)){
	return 2;
  }
  else if ((tth_high > 0.5) && (tth_low < 0.3) && (bkg < 0.3)){
	if (tth_high < 0.7)       return 3;
    else                  return 4;
  }
  else{
	if ((tth_low < 0.25) && (bkg > 0.1)) return 5;
	else if (tth_low < 0.5)  return 6;
    else                  return 7;
  }
  
}


float ttH_ClassifierCut_3l_test(float tth_low, float tth_high, float thq, float bkg)
{
  if ((bkg > 0.28) && (thq < 0.7) && (tth_high < 0.5)){
	if (bkg < 0.45)       return 0;
    else                  return 1;
  }
    else if ((thq > 0.7)){
	return 2;
  }
    else if ((tth_high + tth_low < 0.3)){
	return 1;
  }
  else if ((tth_high > 0.5) && (tth_low < 0.3) && (bkg < 0.3)){
	if (tth_high < 0.7)       return 3;
    else                  return 4;
  }
  else{
	if ((tth_low < 0.25) && (bkg > 0.1)) return 1;
	else if (tth_low < 0.5)  return 5;
    else                  return 6;
  }
  
}



float ttH_catIndex_2lss1tau( float tth, float thq, float bkg)
{

  if ((tth > thq)  && (tth > bkg)){
    if (tth < 0.49)       return 0;
    else if (tth < 0.57)  return 1;
    else if (tth < 0.64)  return 2;
    else if (tth < 0.74)  return 3;
    else if (tth < 0.85)  return 4;
    else                  return 5;
  }
  else if ((thq > tth) && (thq > bkg)){
    if      (thq < 0.49) return 6;
    else if (thq < 0.57) return 7;
    else if (thq < 0.70) return 8;
    else                 return 9;
  }
  else{
    if (bkg < 0.5)         return 10;
    else if ( bkg < 0.56 ) return 11;
    else if ( bkg < 0.62 ) return 12;
    else if ( bkg < 0.71 ) return 13;
    else                   return 14;

  }
  
}

float ttH_catIndex_2lss1tau_CP( float tth, float thq, float bkg, float cp)
{
  int cpIndx=0;
  if      ( cp < 0.139074) cpIndx=0;
  else if ( cp < 0.181274) cpIndx=1;
  else if ( cp < 0.243589) cpIndx=2;
  else                       cpIndx=3;

  if ((tth > thq)  && (tth > bkg)){
    if (tth < 0.49)       return 0 + cpIndx*6;
    else if (tth < 0.57)  return 1 + cpIndx*6;
    else if (tth < 0.64)  return 2 + cpIndx*6;
    else if (tth < 0.74)  return 3 + cpIndx*6;
    else if (tth < 0.85)  return 4 + cpIndx*6;
    else                  return 5 + cpIndx*6;
  }
  else if ((thq > tth) && (thq > bkg)){
    if      (thq < 0.49) return 24;
    else if (thq < 0.57) return 25;
    else if (thq < 0.70) return 26;
    else                 return 27;
  }
  else{
    if (bkg < 0.5)         return 28;
    else if ( bkg < 0.56 ) return 29;
    else if ( bkg < 0.62 ) return 30;
    else if ( bkg < 0.71 ) return 31;
    else                   return 32;

  }
  
}

// 2lss                                                                                                                   
std::vector<float> tth_bounds_2lss = {0.50};
std::vector<float> ttw_bounds_2lss = {0.475};
std::vector<float> th_bounds_2lss  = {0.465};
std::vector<float> bkg_bounds_2lss = {0.405};
std::vector<float> hpt_bounds_2lss = {60,120,200,300,450};

// 3l                                                                                                                     
std::vector<float> tth_bounds_3l = {0.7};
std::vector<float> th_bounds_3l  = {0.535};
std::vector<float> bkg_bounds_3l = {0.505};
std::vector<float> hpt_bounds_3l = {40,60,120,200,233,300,450};

// 2lss1t                                                                                                                 
std::vector<float> tth_bounds_2lss1t = {0.8};
std::vector<float> th_bounds_2lss1t  = {0.565};
std::vector<float> bkg_bounds_2lss1t = {0.52};
std::vector<float> hpt_bounds_2lss1t = {60,100,120,173,200,233,300,450};

float ttH_catIndex_diff_higgspt_varthresh_generic( float tth, std::vector<float> tth_bounds, float ttw, std::vector<float> ttw_bounds, float th, std::vector<float> th_bounds, float bkg, std::vector<float> bkg_bounds, float hpt, std::vector<float> hpt_bounds)
{
  if (tth_bounds.size() != 0) tth_bounds.push_back(0.00);
  if (ttw_bounds.size() != 0) ttw_bounds.push_back(0.00);
  if (th_bounds.size() != 0) th_bounds.push_back(0.00);
  if (bkg_bounds.size() != 0) bkg_bounds.push_back(0.00);
  if (hpt_bounds.size() != 0) hpt_bounds.push_back(10000);
  float catIndex = 0;
  if        (tth_bounds.size() != 0 && tth > ttw && tth > th && tth > bkg) {
    for (int i=0; i<tth_bounds.size(); i++) {
      catIndex += (tth < tth_bounds[i]);
    }
    catIndex *= hpt_bounds.size();
    for (int i=0; i<hpt_bounds.size(); i++) {
      catIndex += (hpt > hpt_bounds[i]);
    }
  } else if (ttw_bounds.size() != 0 && ttw > th && ttw > bkg) {
    catIndex += tth_bounds.size()*hpt_bounds.size();
    for (int i=0; i<ttw_bounds.size(); i++) {
      catIndex += (ttw < ttw_bounds[i]);
    }
  } else if (th_bounds.size() != 0 && th > bkg) {
    catIndex += tth_bounds.size()*hpt_bounds.size() + ttw_bounds.size();
    for (int i=0; i<th_bounds.size(); i++) {
      catIndex += (th < th_bounds[i]);
    }
  } else {
    catIndex += tth_bounds.size()*hpt_bounds.size() + ttw_bounds.size() + th_bounds.size();
    for (int i=0; i<bkg_bounds.size(); i++) {
      catIndex += (bkg < bkg_bounds[i]);
    }
  }
  return catIndex;
}

float ttH_catIndex_diff_higgspt_varthresh_2lss( float tth, float ttw, float th, float bkg, float hpt){
  return ttH_catIndex_diff_higgspt_varthresh_generic( tth, tth_bounds_2lss, ttw, ttw_bounds_2lss, th, th_bounds_2lss, bkg, bkg_bounds_2lss, hpt, hpt_bounds_2lss);
}

float ttH_catIndex_diff_higgspt_varthresh_3l( float tth, float th, float bkg, float hpt){
  return ttH_catIndex_diff_higgspt_varthresh_generic( tth, tth_bounds_3l, 0.0, std::vector<float>(), th, th_bounds_3l, bkg, bkg_bounds_3l, hpt, hpt_bounds_3l);
}

float ttH_catIndex_diff_higgspt_varthresh_2lss1t( float tth, float th, float bkg, float hpt){
  return ttH_catIndex_diff_higgspt_varthresh_generic( tth, tth_bounds_2lss1t, 0.0, std::vector<float>(), th, th_bounds_2lss1t, bkg, bkg_bounds_2lss1t, hpt, hpt_bounds_2lss1t);
}


TF1* fTauSFs[4][3];
TFile* fTauSFFiles[4];

TF1* fTauFRs[4][2][5]; // year, eta range, (nom, par1Down, par1Up, par2Down, par2Up)
TFile* fTauFRFiles[4];

bool isTauSFInit=false;
float tauSF( float taupt, float taueta, int year, int suberaid, int isMatch, int var=0, int varFRNorm=0, int varFRShape=0, int varFRAdd=0){  // var is -1,0,1

  assert( (abs(var)+abs(varFRShape)+abs(varFRNorm)+abs(varFRAdd) != 0 && abs(var)+abs(varFRShape)+abs(varFRNorm)+abs(varFRAdd) != 1) );

  // to add the fr uncertainty
  if (!isTauSFInit){
    isTauSFInit=true;
    fTauSFFiles[0]=TFile::Open("$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/tauSF/TauID_SF_pt_DeepTau2017v2p1VSjet_UL2016_preVFP.root");
    fTauSFFiles[1]=TFile::Open("$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/tauSF/TauID_SF_pt_DeepTau2017v2p1VSjet_UL2016_postVFP.root");
    fTauSFFiles[2]=TFile::Open("$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/tauSF/TauID_SF_pt_DeepTau2017v2p1VSjet_UL2017.root");
    fTauSFFiles[3]=TFile::Open("$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/tauSF/TauID_SF_pt_DeepTau2017v2p1VSjet_UL2018.root");
    for (int i =0; i < 4; ++i){
      fTauSFs[i][0]=(TF1*) fTauSFFiles[i]->Get("VLoose_down");
      fTauSFs[i][1]=(TF1*) fTauSFFiles[i]->Get("VLoose_cent");
      fTauSFs[i][2]=(TF1*) fTauSFFiles[i]->Get("VLoose_up");
    }
    fTauFRFiles[0]=TFile::Open("$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/tauSF/TauSF_2016APV_fit.root");
    fTauFRFiles[1]=TFile::Open("$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/tauSF/TauSF_2016_fit.root");
    fTauFRFiles[2]=TFile::Open("$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/tauSF/TauSF_2017_fit.root");
    fTauFRFiles[3]=TFile::Open("$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/tauSF/TauSF_2018_fit.root ");
    for (int i =0; i < 4; ++i){
      fTauFRs[i][0][0]=(TF1*) fTauFRFiles[i]->Get("nominal_central");
      fTauFRs[i][1][0]=(TF1*) fTauFRFiles[i]->Get("nominal_fwd");
      fTauFRs[i][0][1]=(TF1*) fTauFRFiles[i]->Get("down_1st_central");
      fTauFRs[i][1][1]=(TF1*) fTauFRFiles[i]->Get("down_1st_fwd");
      fTauFRs[i][0][2]=(TF1*) fTauFRFiles[i]->Get("up_1st_central");
      fTauFRs[i][1][2]=(TF1*) fTauFRFiles[i]->Get("up_1st_fwd");
      fTauFRs[i][0][3]=(TF1*) fTauFRFiles[i]->Get("down_2nd_central");
      fTauFRs[i][1][3]=(TF1*) fTauFRFiles[i]->Get("down_2nd_fwd");
      fTauFRs[i][0][4]=(TF1*) fTauFRFiles[i]->Get("up_2nd_central");
      fTauFRs[i][1][4]=(TF1*) fTauFRFiles[i]->Get("down_2nd_fwd");
    }
  }
  
  int yearIdx = 0;
  if (year == 2016)  yearIdx = suberaid;  // suberaid == 0 for 2016APV and 1 for 2016
  if (year != 2016)  yearIdx = (year-2016)+1;

  if (isMatch){
    float varSF=fTauSFs[yearIdx][var+1]->Eval(taupt);
    float nomSF=fTauSFs[yearIdx][1]->Eval(taupt);
    return  (1 + var*std::sqrt( (varSF/nomSF-1)*(varSF/nomSF-1) + 0.03*0.03))*nomSF;
  }


  else{
    int etaindx = (abs(taueta)<1.5) ? 0 : 1;
    int varIdx  = 0;
    if (varFRNorm==1) varIdx=2;
    if (varFRNorm==-1) varIdx=1;
    if (varFRShape==1) varIdx=4;
    if (varFRShape==-1) varIdx=3;
    if (varFRAdd==1) varIdx=5;
    if (varFRAdd==-1) varIdx=6;
    if (varIdx < 5)
       return fTauFRs[yearIdx][etaindx][varIdx]->Eval(taupt);
    else if  (varIdx == 5)
       return 1.3*fTauFRs[yearIdx][etaindx][0]->Eval(taupt);
    else if (varIdx == 6)
       return 0.7*fTauFRs[yearIdx][etaindx][0]->Eval(taupt);
}
  

}


int ttH_catIndex_2lss_nosign(int LepGood1_pdgId, int LepGood2_pdgId, int nBJetMedium25){

  if (abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11) return 1;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && nBJetMedium25 < 2) return 2;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && nBJetMedium25 >= 2) return 3;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && nBJetMedium25 < 2) return 4;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && nBJetMedium25 >= 2) return 5;

 return -1;

}

int ttH_catIndex_2lss_SVA(int LepGood1_pdgId, int LepGood2_pdgId, int LepGood1_charge, int nJet25){

  int res = -2;

  if (abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11) res = 1;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && LepGood1_charge<0) res = 3;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && LepGood1_charge>0) res = 5;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && LepGood1_charge<0) res = 7;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && LepGood1_charge>0) res = 9;
  if (nJet25>=6) res+=1;

  return res; // 1-10
}


int ttH_catIndex_2lss_SVA_forPlots1(int LepGood1_pdgId, int LepGood2_pdgId, int nJet25){

  int res = -2;

  if (abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11) res = 1;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId))) res = 3;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13) res = 5;
  if (nJet25>=6) res+=1;

  return res; // 1-6
}

int ttH_catIndex_2lss_SVA_forPlots2(int nJet25){

  int res = 1;
  if (nJet25>=6) res+=1;
  return res; // 1-6
}

int ttH_catIndex_2lss_SVA_soft(int LepGood1_pdgId, int LepGood2_pdgId, int LepGood1_charge, int nJet25){

  int res = -2;

  if (abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11) res = 1;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && LepGood1_charge<0) res = 3;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && LepGood1_charge>0) res = 5;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && LepGood1_charge<0) res = 7;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && LepGood1_charge>0) res = 9;
  if (nJet25>3) res+=1;

  return res; // 1-10
}


int ttH_catIndex_3l(float ttH, float tH, float rest, int lep1_pdgId, int lep2_pdgId, int lep3_pdgId, int nBMedium )
{

  int sumpdgId = abs(lep1_pdgId)+abs(lep2_pdgId)+abs(lep3_pdgId);
  
  if (ttH >= rest && ttH >= tH){
    if (nBMedium < 2)
      return 1; // ttH_bl
    else
      return 2; // ttH_bt
  }
  else if (tH >= ttH && tH >= rest){
    if (nBMedium < 2){
      return 3; // tH_bl
    }
    else{
      return 4; // tH_bt
    }
  }
  else if (rest >= ttH && rest >= tH){
    if ( sumpdgId == 33){ // rest_eee
      return 5;
    }
    else if (sumpdgId == 35){ 
      if (nBMedium < 2)
	return 6; // rest_eem_bl
      else
	return 7; // rest_eem_bt
    }
    else if (sumpdgId == 37){ // emm
      if (nBMedium < 2)
	return 8; // rest_emm_bl
      else
	return 9; // rest_emm_bt
    }
    else if (sumpdgId == 39){ // mmm
      if (nBMedium < 2)
	return 10; // rest_mmm_bl
      else
	return 11; // rest_mmm_bt
    }
  }

  
  cout << "[ttH_catIndex_3l]: It should not be here" << endl;
  return -1;

}


std::vector<TString> bin3llabels = {"ttH_bl",  "ttH_bt",  "tH_bl",  "tH_bt",  "rest_eee",  "rest_eem_bl",  "rest_eem_bt",  "rest_emm_bl",  "rest_emm_bt",  "rest_mmm_bl",  "rest_mmm_bt"};

std::map<TString, TH1F*> binHistos3l;
std::map<TString, int> bins3lcumul;
std::map<TString, int> bins3lcumul_cp;
TFile* f3lBins;



int ttH_catIndex_3l_MVA(float ttH, float tH, float rest, int lep1_pdgId, int lep2_pdgId, int lep3_pdgId, int nBMedium )
{

  if (!f3lBins){
    f3lBins=TFile::Open("../../data/kinMVA/binning_3l.root");
    int count=0;
    for (auto label : bin3llabels){
      binHistos3l[label] = (TH1F*) f3lBins->Get(label);
      bins3lcumul[label] = count;
      count += binHistos3l[label]->GetNbinsX();
    }
  }
  TString binLabel = bin3llabels[ttH_catIndex_3l(ttH,tH,rest,lep1_pdgId,lep2_pdgId,lep3_pdgId,nBMedium)-1];
  float mvas[] = { ttH, tH, rest };
  float mvavar = *std::max_element( mvas, mvas+3 );
  return binHistos3l[binLabel]->FindBin( mvavar ) + bins3lcumul[binLabel];

  
  cout << "[ttH_catIndex_3l_MVA]: It should not be here "<< ttH << " " << tH << " " << rest << endl;
  return -1;

}

int ttH_catIndex_3l_MVA_CP(float ttH, float tH, float rest, int lep1_pdgId, int lep2_pdgId, int lep3_pdgId, int nBMedium, float cp )
{

  if (!f3lBins){
    f3lBins=TFile::Open("../../data/kinMVA/binning_3l.root");
    int count=0;
    for (auto label : bin3llabels){
      binHistos3l[label] = (TH1F*) f3lBins->Get(label);
      bins3lcumul_cp[label] = count;
      int ncpbins=1;
      if (label.Contains("ttH")) ncpbins=4;
      count += binHistos3l[label]->GetNbinsX()*ncpbins;
    }
  }
  TString binLabel = bin3llabels[ttH_catIndex_3l(ttH,tH,rest,lep1_pdgId,lep2_pdgId,lep3_pdgId,nBMedium)-1];
  float mvas[] = { ttH, tH, rest };
  float mvavar = 0;
  int cpIdx=0;
  if (ttH > tH && ttH > rest){
    mvavar=ttH;
    if (cp < 0.44861784) cpIdx= 0;
    else if (cp < 0.51305674) cpIdx= 1;
    else if (cp < 0.59185324) cpIdx= 2;
    else                      cpIdx= 3;
  }
  else if (tH > rest && tH > ttH)
    mvavar=tH;
  else
    mvavar=rest;

  return binHistos3l[binLabel]->FindBin( mvavar ) + binHistos3l[binLabel]->GetNbinsX()*cpIdx + bins3lcumul_cp[binLabel];

  
  cout << "[ttH_catIndex_3l_MVA]: It should not be here "<< ttH << " " << tH << " " << rest << endl;
  return -1;

}

int ttH_catIndex_3l_node(float ttH, float tH, float rest){
  if (ttH >= tH && ttH >= rest){
    return 0;
  }
  else if (tH >= ttH && tH >= rest){
    return 1;
  }
  else if (rest >= ttH && rest >= tH){
    return 2;
  }
}


int ttH_catIndex_3l_plots(float ttH, float tH, float rest, int lep1_pdgId, int lep2_pdgId, int lep3_pdgId, int nBMedium )
{
  if (!f3lBins){
    f3lBins=TFile::Open("../../data/kinMVA/binning_3l.root");
    int count=0;
    for (auto label : bin3llabels){
      binHistos3l[label] = (TH1F*) f3lBins->Get(label);
      bins3lcumul[label] = count;
      count += binHistos3l[label]->GetNbinsX();
    }
  }

  int offset =0;
  int pdgSum = abs(lep1_pdgId) + abs(lep2_pdgId) + abs(lep3_pdgId);

  if (ttH_catIndex_3l_node(ttH,tH,rest) == 0){
    if (nBMedium >= 2) offset=5;
  }
  else if (ttH_catIndex_3l_node(ttH,tH,rest) == 1){
    if (nBMedium >= 2) offset=7;
  }
  else{
    if (nBMedium  < 2){
      if (pdgSum == 35) offset = 1;
      else if (pdgSum == 37) offset=1+4;
      else if (pdgSum == 39) offset=1+4+4;
    }
    else{
      if (pdgSum == 35) offset = 1+4+4+3;
      if (pdgSum == 37) offset = 1+4+4+3+1;
      if (pdgSum == 39) offset = 1+4+4+3+1+1;
    }
  }
  TString binLabel = bin3llabels[ttH_catIndex_3l(ttH,tH,rest,lep1_pdgId,lep2_pdgId,lep3_pdgId,nBMedium)-1];
  float mvas[] = { ttH, tH, rest };
  float mvavar = *std::max_element( mvas, mvas+3 );
  return binHistos3l[binLabel]->FindBin( mvavar ) + offset;

}

float ttH_mva_4l(float score)
{
  return 1. / (1. + std::sqrt((1. - score) / (1. + score)));

}

int ttH_catIndex_4l(float bdt, float cut=0.85)
{
  if (ttH_mva_4l(bdt) < cut) return 1;
  else return 2;
}

int ttH_catIndex_3l_SVA(int LepGood1_charge, int LepGood2_charge, int LepGood3_charge, int nJet25){

  if ((LepGood1_charge+LepGood2_charge+LepGood3_charge)<0 && nJet25 < 4) return 11;
  if ((LepGood1_charge+LepGood2_charge+LepGood3_charge)>0 && nJet25 < 4) return 12;
  if ((LepGood1_charge+LepGood2_charge+LepGood3_charge)<0 && nJet25 >= 4) return 13;
  if ((LepGood1_charge+LepGood2_charge+LepGood3_charge)>0 && nJet25 >= 4) return 14;

  return -1;

}

int ttH_catIndex_3l_SVAforPlots(int nJet25){

  if (nJet25 < 4) return 1;
  if (nJet25 >= 4) return 2;

  return -1;

}

int ttH_catIndex_3l_SVA_soft(int LepGood1_charge, int LepGood2_charge, int LepGood3_charge, int nJet25){

  if ((LepGood1_charge+LepGood2_charge+LepGood3_charge)<0 && nJet25 <= 3) return 11;
  if ((LepGood1_charge+LepGood2_charge+LepGood3_charge)>0 && nJet25 <= 3) return 12;
  if ((LepGood1_charge+LepGood2_charge+LepGood3_charge)<0 && nJet25 > 3) return 13;
  if ((LepGood1_charge+LepGood2_charge+LepGood3_charge)>0 && nJet25 > 3) return 14;

  return -1;

}




std::map<TString, TFile*> fRecoToLoose;
std::map<TString, TH1*> hRecoToLoose;

float _get_looseToTight_leptonSF_ttH(int pdgid, float pt, float eta, int nlep, int year, int suberaid){
  
  if (!fRecoToLoose.size()){
    for (auto& theyear : {"2016","2016APV", "2017", "2018"}){
      fRecoToLoose[TString::Format("%s_el_2lss",theyear)]=TFile::Open(TString::Format("../../data/leptonSF/elecNEWmva/egammaEffi%s_2lss_EGM2D.root",theyear));
      fRecoToLoose[TString::Format("%s_el_3l",theyear)]=TFile::Open(TString::Format("../../data/leptonSF/elecNEWmva/egammaEffi%s_3l_EGM2D.root",theyear));
      fRecoToLoose[TString::Format("%s_mu_3l",theyear)]=TFile::Open(TString::Format("../../data/leptonSF/muon/egammaEffi%s_EGM2D.root",theyear));
    }

    for (auto const & x : fRecoToLoose){
      hRecoToLoose[x.first]=(TH1*) x.second->Get("EGamma_SF2D");
    }

  }

  TString yearString= TString::Format("%d",year) + (( year == 2016 && suberaid == 0) ? "APV" : "");
  TString pdgstring  = (abs(pdgid) == 11) ? "el" : "mu";
  TString lepstring = (nlep == 2 && abs(pdgid) == 11 ) ? "2lss" : "3l";

  auto h = hRecoToLoose.at( yearString + "_" + pdgstring + "_" + lepstring);
  int bin = h->FindBin( std::abs(eta) ,std::min(std::max(pt,10.1f),119.f));

  return h->GetBinContent(bin);

}


float ttH_2lss_ifflav(int LepGood1_pdgId, int LepGood2_pdgId, float ret_ee, float ret_em, float ret_mm){
  if (abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11) return ret_ee;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)))       return ret_em;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13) return ret_mm;
  std::cerr << "ERROR: invalid input " << abs(LepGood1_pdgId) << ", " << abs(LepGood1_pdgId) << std::endl;
  assert(0);
  return 0; // avoid warning
}
float ttH_2lss_ifflavnb(int LepGood1_pdgId, int LepGood2_pdgId, int nBJetMedium25, float ret_ee, float ret_em_bl, float ret_em_bt, float ret_mm_bl, float ret_mm_bt){
  if (abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11) return ret_ee;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && nBJetMedium25 < 2) return ret_em_bl;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && nBJetMedium25 >= 2) return ret_em_bt;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && nBJetMedium25 < 2) return ret_mm_bl;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && nBJetMedium25 >= 2) return ret_mm_bt;
  std::cerr << "ERROR: invalid input " << abs(LepGood1_pdgId) << ", " << abs(LepGood1_pdgId) <<  ", " << nBJetMedium25 << std::endl;
  assert(0);
  return 0; // avoid warning
}

float ttH_3l_ifflav(int LepGood1_pdgId, int LepGood2_pdgId, int LepGood3_pdgId){
  if (abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11 && abs(LepGood3_pdgId)==11) return 1;
  if ((abs(LepGood1_pdgId) + abs(LepGood2_pdgId) + abs(LepGood3_pdgId)) == 35)       return 2;
  if ((abs(LepGood1_pdgId) + abs(LepGood2_pdgId) + abs(LepGood3_pdgId)) == 37)       return 3;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && abs(LepGood3_pdgId)==13) return 4;
  return -1;
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


float wploose[3][2]  = {{0.0508, 0.0480}, {0.0532,-99}, {0.0490,-99}};
float wpmedium[3][2] = {{0.2598,0.2489} , {0.3040,-99}, {0.2783,-99}};

float deepFlavB_WPLoose(int year, int subera) {
    return wploose[year-2016][subera];
}
float deepFlavB_WPMedium(int year, int subera) {
    return wpmedium[year-2016][subera];
}
// float deepFlavB_WPTight(int year, int subera) {
//     float wp[3]  = { 0.7221, 0.7489, 0.7264 };
//     return wp[year-2016];
// }

float smoothBFlav(float jetpt, float ptmin, float ptmax, int year, int subera, float scale_loose=1.0) {

  float the_wploose =wploose[year-2016][subera];
  float the_wpmedium=wpmedium[year-2016][subera];
  float x = std::min(std::max(0.f, jetpt - ptmin)/(ptmax-ptmin), 1.f); 
  return x*the_wploose*scale_loose + (1-x)*the_wpmedium;
}

float ttH_4l_clasifier(float nJet25,float nBJetMedium25,float mZ2){
 
  if ( abs(mZ2 -91.2)<10) return 1;
  if ((abs(mZ2-91.2) > 10) && nJet25==0) return 2;
  if ( (abs(mZ2-91.2) > 10) && nJet25>=0 && nBJetMedium25==1) return 3;
  if ( (abs(mZ2-91.2) > 10) && nJet25>=1 && nBJetMedium25>1) return 4;

  else return -1;
}

//float ttH_3l_clasifier(float nJet25,float nBJetMedium25){
//
//  if (nJet25 == 0) return 0;
//  if ((nJet25 == 1)*(nBJetMedium25 == 0)) return 1;
//  if ((nJet25 == 2)*(nBJetMedium25 == 0)) return 2;
//  if ((nJet25 == 3)*(nBJetMedium25 == 0)) return 3;
//  if ((nJet25>3)*(nBJetMedium25 == 0))    return 4;
//  if ((nJet25 == 1)*(nBJetMedium25 == 1)) return 5;
//  if ((nJet25 == 2)*(nBJetMedium25 == 1)) return 6;
//  if ((nJet25 == 3)*(nBJetMedium25 == 1)) return 7;
//  if ((nJet25 == 4)*(nBJetMedium25 == 1)) return 8;
//  if ((nJet25>4)*(nBJetMedium25 == 1))    return 9;
//  if ((nJet25 == 2)*(nBJetMedium25>1))    return 10;
//  if ((nJet25 == 3)*(nBJetMedium25>1))    return 11;
//  if ((nJet25 == 4)*(nBJetMedium25>1))    return 12;
//  if ((nJet25>4)*(nBJetMedium25>1))       return 13;
//  else return -1;
//}

float ttH_3l_clasifier(float nJet25,float nBJetMedium25){

  if ((nJet25 == 1)*(nBJetMedium25 == 0)) return 1;
  if ((nJet25 == 2)*(nBJetMedium25 == 0)) return 2;
  if ((nJet25 == 3)*(nBJetMedium25 == 0)) return 3;
  if ((nJet25>3)*(nBJetMedium25 == 0))    return 4;
  if ((nJet25 == 2)*(nBJetMedium25 == 1)) return 5;
  if ((nJet25 == 3)*(nBJetMedium25 == 1)) return 6;
  if ((nJet25 == 4)*(nBJetMedium25 == 1)) return 7;
  if ((nJet25>4)*(nBJetMedium25 == 1))    return 8;
  if ((nJet25 == 2)*(nBJetMedium25>1))    return 9;
  if ((nJet25 == 3)*(nBJetMedium25>1))    return 10;
  if ((nJet25 == 4)*(nBJetMedium25>1))    return 11;
  if ((nJet25>4)*(nBJetMedium25>1))       return 12;
  else return -1;
}

float triggerSF_ttH(int pdgid1, float pt1, int pdgid2, float pt2, int nlep, int year, int suberaid, int var=0){

  TString yearString= TString::Format("%d",year) + (( year == 2016 && suberaid == 0) ? "APV" : "");

  if (nlep == 2){
    if (abs(pdgid1*pdgid2) == 121){

      if (yearString == "2016APV"){
        if (pt2 < 20){
          return 0.96*(1 + var*0.02);
        }
        else if (pt2 > 20 && pt2 < 55){
          return 0.99*(1 + var*0.01);
        }
        else return 1.*(1 + var*0.01);
      }

      if (yearString == "2016"){
        if (pt2 < 40){
          return 0.98*(1 + var*0.02);
        }
        else return 0.99*(1 + var*0.01);
      }

      if (yearString == "2017"){
        if (pt2<25) return 0.96*(1 + var*0.02);
	else return 0.985*(1 + var*0.01);
      }

      if (yearString == "2018"){
        if (pt2<20){
	  return 0.98*(1 + var*0.01);
        }
        else if (pt2 > 20 && pt2 < 70){
          return 1.*(1 + var*0.01);
        }
        else return 1.01*(1 + var*0.005);
      }
    }

    else if ( abs(pdgid1*pdgid2) == 143){

      if (yearString == "2016APV"){
        if (pt2 < 25){
          return 0.98*(1 + var*0.01);
        }
        else if (pt2 > 25 && pt2 < 70){
          return 0.99*(1 + var*0.005);
        }
        else return 1.*(1 + var*0.005);
      }

      if (yearString == "2016"){
        if (pt2 < 20){
          return 0.98*(1 + var*0.02);
        }
        else return 0.99*(1 + var*0.01);
      }

      if (yearString == "2017"){
	if (pt2<20) return 0.99*(1 + var*0.01);
        else if (pt2 > 20 && pt2 < 40){
          return 0.98*(1 + var*0.01);
        }
        else return 0.995*(1 + var*0.005);
      }

      if (yearString == "2018"){
        if (pt2<20) return 0.98*(1 + var*0.01);
        else if (pt2 > 20 && pt2 < 55){
          return 0.99*(1 + var*0.005);
        }
        else  return 1.*(1 + var*0.005);
      }
    }

    else{
      if (yearString == "2016APV"){
        if (pt2 < 25){
          return 0.98*(1 + var*0.01);
        }
        else return 0.99*(1 + var*0.01);
      }

      if (yearString == "2016"){
        if (pt2 < 20){
          return 0.97*(1 + var*0.01);
        }
        else return 0.99*(1 + var*0.01);
      }

      if (yearString == "2017"){
        if (pt2 < 25){
          return 0.97*(1 + var*0.01);
        }
        else return 0.99*(1 + var*0.01);
      }

      if (yearString == "2018"){
        return 0.99*(1 + var*0.01);
      }
    }

  }
  else {
    
    if (yearString == "2016APV" || yearString == "2016"){
      return 1.*(1 + var*0.02);
    }
    if (yearString == "2017" || yearString == "2018"){
      return 1.*(1 + var*0.01);
    }

  }

}


int ttH_catIndex_2lss(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float ttw, float thq, float rest)
{
  int flch = 0;
  int idx = 0;
	
  if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 22) {
	  //ee
	  flch = 0;
	  if (tth_high > 0.60) idx = 2;
	  else if (thq > 0.5) idx = 3;
	  else if (ttw > 0.35) idx = 4;
	  else if (rest > 0.3) idx = 5;
	  else if (tth_low > 0.4) idx = 1;
	  else if (tth_low > 0.2) idx = 0;
	  else idx = 5;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 24) {
	  //em
      flch = 1;
	  if (tth_high > 0.60) idx = 2;
	  else if (thq > 0.5) idx = 3;
	  else if (ttw > 0.35) idx = 4;
	  else if (rest > 0.3) idx = 5;
	  else if (tth_low > 0.4) idx = 1;
	  else if (tth_low > 0.2) idx = 0;
	  else idx = 5;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 26) {
	  //mm
      flch = 2;
	  if (tth_high > 0.60) idx = 2;
	  else if (thq > 0.5) idx = 3;
	  else if (ttw > 0.35) idx = 4;
	  else if (rest > 0.3) idx = 5;
	  else if (tth_low > 0.4) idx = 1;
	  else if (tth_low > 0.2) idx = 0;
	  else idx = 5;
  }
  else
    cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return flch*6 + idx;
 
}

float ttH_max_2lss_tth_low(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float ttw, float thq, float rest)
{
  
  //cout << tth_low << "\n";
  if (!((tth_low > ttw && tth_low > rest && tth_low > tth_high && tth_low > thq) || (tth_high > ttw && tth_high > rest && tth_high > tth_low && tth_high > thq && tth_high < 0.5))) {
	  //cout << "Dropped \n\n";
	  return -99;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 22) {
	  //ee 
	  //cout << "ee \n\n";
	  return tth_low;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 24) {
	  //em
	  //cout << "em \n\n";
	  return tth_low + 1.;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 26) {
	  //mm
	  //cout << "mm \n\n";
	  return tth_low + 2.;
  }
  else
    cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return -99;
 
}

float ttH_max_2lss_tth_high(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float ttw, float thq, float rest)
{
  
  if (tth_high < tth_low || tth_high < ttw || tth_high < thq || tth_high < rest || tth_high < 0.5) return -99;
	
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 22) {
	  //ee
	  return tth_high;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 24) {
	  //em
	  return tth_high + 1.;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 26) {
	  //mm
	  return tth_high + 2.;
  }
  else
    cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return -99;
 
}

float ttH_max_2lss_ttw(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float ttw, float thq, float rest)
{
  
  if (ttw < tth_low || ttw < tth_high || ttw < thq || ttw < rest) return -99;
	
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 22) {
	  //ee
	  return ttw;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 24) {
	  //em
	  return ttw + 1;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 26) {
	  //mm
	  return ttw + 2;
  }
  else
    cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return false;
 
}

float ttH_max_2lss_thq(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float ttw, float thq, float rest)
{
  
  if (thq < tth_low || thq < tth_high || thq < ttw || thq < rest) return -99;
	
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 22) {
	  //ee
	  return thq;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 24) {
	  //em
	  return thq + 1;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 26) {
	  //mm
	  return thq + 2;
  }
  else
    cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return false;
 
}

float ttH_max_2lss_rest(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float ttw, float thq, float rest)
{
  
  if (rest < tth_low || rest < tth_high || rest < ttw || rest < thq) return -99;
	
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 22) {
	  //ee
	  return rest;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 24) {
	  //em
	  return rest + 1;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 26) {
	  //mm
	  return rest + 2;
  }
  else
    cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return false;
 
}


float ttH_catIndex_2lss_ttH_low_test(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float ttw, float thq, float rest)
{
  int flch = 0;
  int idx = 0;
	
  if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 22) {
	  //ee
	  flch = 0;
	  if (tth_low > 0.5) idx = 0;
	  else idx = 1;
	  return idx;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 24) {
	  //em
      flch = 1;
	  if (tth_low > 0.60) idx = 0;
	  else if (tth_low > 0.5) idx = 1;
	  else if (tth_low > 0.4) idx = 2;
	  else if (tth_low > 0.35) idx = 3;
	  else if (tth_low > 0.3) idx = 4;
	  else idx = 5;
	  return 2 + idx;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 26) {
	  //mm
      flch = 2;
	  if (tth_low > 0.60) idx = 0;
	  else if (tth_low > 0.5) idx = 1;
	  else if (tth_low > 0.4) idx = 2;
	  else if (tth_low > 0.35) idx = 3;
	  else if (tth_low > 0.3) idx = 4;
	  else idx = 5;
	  
	  return 2 + 6 + idx;
  }
  else
    cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return false;
 
}

float ttH_catIndex_2lss1tau(float tth_low, float tth_high, float thq, float bkg)
{

  if (tth_high > 0.6)  return 3;
  else if (thq > 0.7) return 4;
  else if (bkg > 0.5) return 8;
  else if (tth_low > 0.49) return 2;
  else if (tth_low > 0.345) return 1;
  else if (tth_low > 0.2) return 0;
  else if (bkg > 0.36) return 7;
  else if (bkg > 0.255) return 6;
  else return 5;
  
}

// 2lss

int class_max_p_2lss_tth_low(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float ttw, float thq, float rest)
{
  std::vector<float> PrecentileCuts = {0.0, 0.2363853227182694, 0.3368149797051845, 0.3901109848733349, 0.4506187899733912, 0.5248424485833131};
  
  //cout << tth_low << "\n";
  if (!((tth_low > ttw && tth_low > rest && tth_low > tth_high && tth_low > thq) || (tth_high > ttw && tth_high > rest && tth_high > tth_low && tth_high > thq && tth_high < 0.5))) {
	  //cout << "Dropped \n\n";
	  return -99;
  }


  int bin_counter = PrecentileCuts.size()-1;
  while (bin_counter >= 0) {
	  if (tth_low > PrecentileCuts[bin_counter]) return bin_counter;
	  bin_counter = bin_counter - 1;
  }
  
  cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return -99;
 
}

int class_max_p_2lss_tth_high(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float ttw, float thq, float rest)
{
  std::vector<float> PrecentileCuts = {0.0, 0.6276702917791234};
  
  //cout << tth_low << "\n";
  if (tth_high < tth_low || tth_high < ttw || tth_high < thq || tth_high < rest || tth_high < 0.5) {
	  //cout << "Dropped \n\n";
	  return -99;
  }
  
  int bin_counter = PrecentileCuts.size()-1;
  while (bin_counter >= 0) {
	  if (tth_high > PrecentileCuts[bin_counter]) return bin_counter;
	  bin_counter = bin_counter - 1;
  }

  cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return -99;
 
}

int class_max_p_2lss_thq(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float ttw, float thq, float rest)
{
  std::vector<float> PrecentileCuts_ee = {0.0, 0.354085349458666, 0.4159274794765929, 0.5146309676033994};
  std::vector<float> PrecentileCuts_em = {0.0, 0.30232072396170684, 0.3245198619455962, 0.3514758403887882, 0.37825277692173975, 0.4018283951125225, 0.42793959660908976, 0.45400140447258974, 0.48978830344359003, 0.5269570440242298, 0.581569164294888};
  std::vector<float> PrecentileCuts_mm = {0.0, 0.3147166177053606, 0.35773857931831554, 0.4030518141514902, 0.45022165678166953, 0.4961459045036706, 0.5600289980746318};
  
  //cout << tth_low << "\n";
  if (thq < tth_low || thq < ttw || thq < tth_high || thq < rest) {
	  //cout << "Dropped \n\n";
	  return -99;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 22) {
	  //ee 
	  //cout << "ee \n\n";
	  int bin_counter = PrecentileCuts_ee.size()-1;
	  while (bin_counter >= 0) {
		  if (thq > PrecentileCuts_ee[bin_counter]) return bin_counter;
		  bin_counter = bin_counter - 1;
	  }
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 24) {
	  //em
	  //cout << "em \n\n";
	  int bin_counter = PrecentileCuts_em.size()-1;
	  while (bin_counter >= 0) {
		  if (thq > PrecentileCuts_em[bin_counter]) return 4 + bin_counter;
		  bin_counter = bin_counter - 1;
	  }
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 26) {
	  //mm
	  //cout << "mm \n\n";
	  int bin_counter = PrecentileCuts_mm.size()-1;
	  while (bin_counter >= 0) {
		  if (thq > PrecentileCuts_mm[bin_counter]) return 15 + bin_counter;
		  bin_counter = bin_counter - 1;
	  }
  }
  else
    cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return -99;
 
}

int class_max_p_2lss_rest(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float ttw, float thq, float rest)
{
  std::vector<float> PrecentileCuts_ee = {0.0, 0.35589085145899546, 0.39473021424996413, 0.42038832283012506, 0.4458440784977981, 0.47524492874678287, 0.507630610350954, 0.5508479071234978};
  std::vector<float> PrecentileCuts_em = {0.0, 0.34106179945631143, 0.37537384347166464, 0.40115793767147, 0.42503565936487436, 0.4506482339902208, 0.4810122285022193, 0.5210433090893043};
  std::vector<float> PrecentileCuts_mm = {0.0, 0.3134678090024507, 0.33836150459882647, 0.35769439175065626, 0.3754963107740153, 0.39030317708146983, 0.40510413817838403, 0.4228129819708819, 0.44071421879577927, 0.46686285529431115, 0.5048887507440911};
  
  //cout << tth_low << "\n";
  if (rest < tth_low || rest < ttw || rest < tth_high || rest < thq) {
	  //cout << "Dropped \n\n";
	  return -99;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 22) {
	  //ee 
	  //cout << "ee \n\n";
	  int bin_counter = PrecentileCuts_ee.size()-1;
	  while (bin_counter >= 0) {
		  if (rest > PrecentileCuts_ee[bin_counter]) return bin_counter;
		  bin_counter = bin_counter - 1;
	  }
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 24) {
	  //em
	  //cout << "em \n\n";
	  int bin_counter = PrecentileCuts_em.size()-1;
	  while (bin_counter >= 0) {
		  if (rest > PrecentileCuts_em[bin_counter]) return 8 + bin_counter;
		  bin_counter = bin_counter - 1;
	  }
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 26) {
	  //mm
	  //cout << "mm \n\n";
	  int bin_counter = PrecentileCuts_mm.size()-1;
	  while (bin_counter >= 0) {
		  if (rest > PrecentileCuts_mm[bin_counter]) return 16 + bin_counter;
		  bin_counter = bin_counter - 1;
	  }
  }
  else
    cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return -99;
 
}

int class_max_p_2lss_ttw(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float ttw, float thq, float rest)
{
  std::vector<float> PrecentileCuts_ee = {0.0, 0.2996266728846854, 0.34408099834539285, 0.39052886380707674, 0.43193612762413575, 0.4845194241684518};
  std::vector<float> PrecentileCuts_em = {0.0, 0.28687050899838823, 0.30416659060707585, 0.31662333873108667, 0.3295696565150568, 0.3390085122116467, 0.3496005760153689, 0.35928485684103334, 0.371812376313478, 0.38516495819060187, 0.39708568375176445, 0.4090171644549572, 0.4230154079938128, 0.43540545537103004, 0.4506397658058679, 0.4662733560022563, 0.4878304469053573, 0.5142451041074271, 0.5743363552359685};
  std::vector<float> PrecentileCuts_mm = {0.0, 0.29260021687919296, 0.3147691482703262, 0.33120834411664923, 0.345197362204061, 0.3602847510177273, 0.3765950698152387, 0.3896580597302101, 0.40235956066633594, 0.41460333674441985, 0.4311239016212267, 0.4472832633374457, 0.4672440702434247, 0.49300905979589926, 0.5453891629375588};
  
  //cout << tth_low << "\n";
  if (ttw < tth_low || ttw < rest || ttw < tth_high || ttw < thq) {
	  //cout << "Dropped \n\n";
	  return -99;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 22) {
	  //ee 
	  //cout << "ee \n\n";
	  int bin_counter = PrecentileCuts_ee.size()-1;
	  while (bin_counter >= 0) {
		  if (ttw > PrecentileCuts_ee[bin_counter]) return bin_counter;
		  bin_counter = bin_counter - 1;
	  }
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 24) {
	  //em
	  //cout << "em \n\n";
	  int bin_counter = PrecentileCuts_em.size()-1;
	  while (bin_counter >= 0) {
		  if (ttw > PrecentileCuts_em[bin_counter]) return 6 + bin_counter;
		  bin_counter = bin_counter - 1;
	  }
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 26) {
	  //mm
	  //cout << "mm \n\n";
	  int bin_counter = PrecentileCuts_mm.size()-1;
	  while (bin_counter >= 0) {
		  if (ttw > PrecentileCuts_mm[bin_counter]) return 25 + bin_counter;
		  bin_counter = bin_counter - 1;
	  }
  }
  else
    cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return -99;
 
}

int class_max_p_2lss_tth_to_HiggsPt(int bin_idx, float Higgs_pt)
{
  std::vector<float> Pt_cuts_low = {0.0, 60, 120, 200};
  std::vector<float> Pt_cuts_high = {0.0, 200, 300, 450};
  
  if (bin_idx < 6) {
  
	  int nr_tth_bins = Pt_cuts_low.size();
	  int bin_counter = Pt_cuts_low.size()-1;
	  
	  while (bin_counter >= 0) {
		  if (Higgs_pt > Pt_cuts_low[bin_counter]) return nr_tth_bins*bin_idx + bin_counter;
		  bin_counter = bin_counter - 1;
	  }
  }
  else {
	  	  int nr_tth_bins = Pt_cuts_high.size();
	  int bin_counter = Pt_cuts_high.size()-1;
	  
	  while (bin_counter >= 0) {
		  if (Higgs_pt > Pt_cuts_high[bin_counter]) return nr_tth_bins*bin_idx + bin_counter;
		  bin_counter = bin_counter - 1;
	  }
  }
 return -99;
 
}

int catIndex_2lss_all_HiggsPt(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float ttw, float thq, float rest, float Higgs_pt)
{
  // 121 bins [0,120]
  int ttH_idx = 0;
  
  if ((tth_low > ttw && tth_low > rest && tth_low > tth_high && tth_low > thq) || (tth_high > ttw && tth_high > rest && tth_high > tth_low && tth_high > thq && tth_high < 0.5)) {
	  ttH_idx = class_max_p_2lss_tth_low(LepGood1_pdgId, LepGood2_pdgId, tth_low, tth_high, ttw, thq, rest);
	  return class_max_p_2lss_tth_to_HiggsPt(ttH_idx, Higgs_pt);
  }
  
  else if (tth_high > ttw && tth_high > rest && tth_high > tth_low && tth_high > thq && tth_high > 0.5) {
	  ttH_idx = 6 + class_max_p_2lss_tth_high(LepGood1_pdgId, LepGood2_pdgId, tth_low, tth_high, ttw, thq, rest);
	  return class_max_p_2lss_tth_to_HiggsPt(ttH_idx, Higgs_pt);
  }
  
  else if (thq > ttw && thq > rest && thq > tth_low && thq > tth_high) {
	  return 32 + class_max_p_2lss_thq(LepGood1_pdgId, LepGood2_pdgId, tth_low, tth_high, ttw, thq, rest);
  }
  
  else if (ttw > tth_high && ttw > rest && ttw > tth_low && ttw > thq) {
	  return 54 + class_max_p_2lss_ttw(LepGood1_pdgId, LepGood2_pdgId, tth_low, tth_high, ttw, thq, rest);
  }
  
  else if (rest > tth_low && rest > ttw && rest > tth_high && rest > thq) {
	  return 94 + class_max_p_2lss_rest(LepGood1_pdgId, LepGood2_pdgId, tth_low, tth_high, ttw, thq, rest);
  }
	else cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;
 return -99;
 
}


// 2lss1tau

float ttH_max_2lss1tau_tth_low(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float thq, float rest)
{
  
  //cout << tth_low << "\n";
  if (!((tth_low > rest && tth_low > tth_high && tth_low > thq) || (tth_high > rest && tth_high > tth_low && tth_high > thq && tth_high < 0.5))) {
	  //cout << "Dropped \n\n";
	  return -99;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 22) {
	  //ee 
	  //cout << "ee \n\n";
	  return tth_low;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 24) {
	  //em
	  //cout << "em \n\n";
	  return tth_low + 1.;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 26) {
	  //mm
	  //cout << "mm \n\n";
	  return tth_low + 2.;
  }
  else
    cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return -99;
 
}

float ttH_max_2lss1tau_tth_high(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float thq, float rest)
{
  
  if (tth_high < tth_low || tth_high < thq || tth_high < rest || tth_high < 0.5) return -99;
	
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 22) {
	  //ee
	  return tth_high;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 24) {
	  //em
	  return tth_high + 1.;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 26) {
	  //mm
	  return tth_high + 2.;
  }
  else
    cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return -99;
 
}

float ttH_max_2lss1tau_thq(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float thq, float rest)
{
  
  if (thq < tth_low || thq < tth_high || thq < rest) return -99;
	
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 22) {
	  //ee
	  return thq;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 24) {
	  //em
	  return thq + 1;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 26) {
	  //mm
	  return thq + 2;
  }
  else
    cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return false;
 
}

float ttH_max_2lss1tau_rest(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float thq, float rest)
{
  
  if (rest < tth_low || rest < tth_high || rest < thq) return -99;
	
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 22) {
	  //ee
	  return rest;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 24) {
	  //em
	  return rest + 1;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 26) {
	  //mm
	  return rest + 2;
  }
  else
    cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return false;
 
}

int class_max_p_2lss1tau_tth_low(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float thq, float rest)
{
  std::vector<float> PrecentileCuts = {0.0, 0.46820808094240446};
  
  //cout << tth_low << "\n";
  if (!(tth_low > rest && tth_low > tth_high && tth_low > thq)) {
	  //cout << "Dropped \n\n";
	  return -99;
  }
  
  int bin_counter = PrecentileCuts.size()-1;
  while (bin_counter >= 0) {
	  if (tth_low > PrecentileCuts[bin_counter]) return bin_counter;
	  bin_counter = bin_counter - 1;
  }
  
  cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return -99;
 
}


int class_max_p_2lss1tau_thq(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float thq, float rest)
{
  std::vector<float> PrecentileCuts = {0.0, 0.45035608910694963, 0.5154428669859836, 0.6468995910968893};
  
  //cout << tth_low << "\n";
  if (thq < tth_low || thq < tth_high || thq < rest) {
	  //cout << "Dropped \n\n";
	  return -99;
  }
  
  int bin_counter = PrecentileCuts.size()-1;
  while (bin_counter >= 0) {
	  if (thq > PrecentileCuts[bin_counter]) return bin_counter;
	  bin_counter = bin_counter - 1;
  }


  cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return -99;
 
}

int class_max_p_2lss1tau_rest(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float thq, float rest)
{
  std::vector<float> PrecentileCuts = {0.0, 0.3871003602105856, 0.4414829001841132, 0.498805189523118, 0.5766101702746904};
  
  //cout << tth_low << "\n";
  if (rest < tth_low || rest < tth_high || rest < thq) {
	  //cout << "Dropped \n\n";
	  return -99;
  }
  
  int bin_counter = PrecentileCuts.size()-1;
  while (bin_counter >= 0) {
	  if (rest > PrecentileCuts[bin_counter]) return bin_counter;
	  bin_counter = bin_counter - 1;
  }
  
  cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return -99;
 
}

int class_max_p_2lss1tau_tth_to_HiggsPt(int bin_idx, float Higgs_pt)
{
  std::vector<float> Pt_cuts_low = {0.0, 60, 120, 200};
  std::vector<float> Pt_cuts_high = {0.0, 200, 300, 450};
  
  if (bin_idx < 2) {
  
	  int nr_tth_bins = Pt_cuts_low.size();
	  int bin_counter = Pt_cuts_low.size()-1;
	  
	  while (bin_counter >= 0) {
		  if (Higgs_pt > Pt_cuts_low[bin_counter]) return nr_tth_bins*bin_idx + bin_counter;
		  bin_counter = bin_counter - 1;
	  }
  }
  else {
	  	  int nr_tth_bins = Pt_cuts_high.size();
	  int bin_counter = Pt_cuts_high.size()-1;
	  
	  while (bin_counter >= 0) {
		  if (Higgs_pt > Pt_cuts_high[bin_counter]) return nr_tth_bins*bin_idx + bin_counter;
		  bin_counter = bin_counter - 1;
	  }
  }
 return -99;
 
}

int catIndex_2lss1tau_all_HiggsPt(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float thq, float rest, float Higgs_pt)
{
  // 21 bins [0,20]
  int ttH_idx = 0;
  
  if (((tth_low > rest && tth_low > tth_high && tth_low > thq) || (tth_high > rest && tth_high > tth_low && tth_high > thq && tth_high < 0.5))) {
	  ttH_idx = class_max_p_2lss1tau_tth_low(LepGood1_pdgId, LepGood2_pdgId, tth_low, tth_high, thq, rest);
	  return class_max_p_2lss1tau_tth_to_HiggsPt(ttH_idx, Higgs_pt);
  }
  
  else if (tth_high > rest && tth_high > tth_low && tth_high > thq && tth_high > 0.5) {
	  return class_max_p_2lss1tau_tth_to_HiggsPt(2, Higgs_pt);
  }
  
  else if (thq > rest && thq > tth_low && thq > tth_high) {
	  return 12 + class_max_p_2lss1tau_thq(LepGood1_pdgId, LepGood2_pdgId, tth_low, tth_high, thq, rest);
  }
  
  else if (rest > tth_low && rest > tth_high && rest > thq) {
	  return 16 + class_max_p_2lss1tau_rest(LepGood1_pdgId, LepGood2_pdgId, tth_low, tth_high, thq, rest);
  }
	else cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;
 return -99;
}


// 3l


float ttH_max_3l_tth_low(int LepGood1_pdgId, int LepGood2_pdgId, int LepGood3_pdgId, float tth_low, float tth_high, float thq, float rest)
{
  
  //cout << tth_low << "\n";
  if (!((tth_low > rest && tth_low > tth_high && tth_low > thq) || (tth_high > rest && tth_high > tth_low && tth_high > thq && tth_high < 0.5))) {
	  //cout << "Dropped \n\n";
	  return -99;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId)+abs(LepGood3_pdgId) == 33) {
	  //eee
	  return tth_low;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId)+abs(LepGood3_pdgId) == 35) {
	  //eem
	  return tth_low + 1;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId)+abs(LepGood3_pdgId) == 37) {
	  //emm
      return tth_low + 2;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId)+abs(LepGood3_pdgId) == 39) {
	  //mmm
	  return tth_low + 3;
  }
  else
    cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return -99;
 
}

float ttH_max_3l_tth_high(int LepGood1_pdgId, int LepGood2_pdgId, int LepGood3_pdgId, float tth_low, float tth_high, float thq, float rest)
{
  
  if (tth_high < tth_low || tth_high < thq || tth_high < rest || tth_high < 0.5) return -99;
	
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId)+abs(LepGood3_pdgId) == 33) {
	  //eee
	  return tth_high;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId)+abs(LepGood3_pdgId) == 35) {
	  //eem
	  return tth_high + 1;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId)+abs(LepGood3_pdgId) == 37) {
	  //emm
      return tth_high + 2;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId)+abs(LepGood3_pdgId) == 39) {
	  //mmm
	  return tth_high + 3;
  }
  else
    cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return -99;
 
}

float ttH_max_3l_thq(int LepGood1_pdgId, int LepGood2_pdgId, int LepGood3_pdgId, float tth_low, float tth_high, float thq, float rest)
{
  
  if (thq < tth_low || thq < tth_high || thq < rest) return -99;
	
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId)+abs(LepGood3_pdgId) == 33) {
	  //eee
	  return thq;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId)+abs(LepGood3_pdgId) == 35) {
	  //eem
	  return thq + 1;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId)+abs(LepGood3_pdgId) == 37) {
	  //emm
      return thq + 2;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId)+abs(LepGood3_pdgId) == 39) {
	  //mmm
	  return thq + 3;
  }
  else
    cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return false;
 
}

float ttH_max_3l_rest(int LepGood1_pdgId, int LepGood2_pdgId, int LepGood3_pdgId, float tth_low, float tth_high, float thq, float rest)
{
  
  if (rest < tth_low || rest < tth_high || rest < thq) return -99;
	
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId)+abs(LepGood3_pdgId) == 33) {
	  //eee
	  return rest;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId)+abs(LepGood3_pdgId) == 35) {
	  //eem
	  return rest + 1;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId)+abs(LepGood3_pdgId) == 37) {
	  //emm
	  return rest + 2;
  }
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId)+abs(LepGood3_pdgId) == 39) {
	  //mmm
	  return rest + 3;
  }
  else
    cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return false;
 
}

int class_max_p_3l_tth_low(int LepGood1_pdgId, int LepGood2_pdgId, int LepGood3_pdgId, float tth_low, float tth_high, float thq, float rest)
{
  std::vector<float> PrecentileCuts = {0.0, 0.46820808094240446};
  
  //cout << tth_low << "\n";
  if (!(tth_low > rest && tth_low > tth_high && tth_low > thq)) {
	  //cout << "Dropped \n\n";
	  return -99;
  }
  
  int bin_counter = PrecentileCuts.size()-1;
  while (bin_counter >= 0) {
	  if (tth_low > PrecentileCuts[bin_counter]) return bin_counter;
	  bin_counter = bin_counter - 1;
  }
  
  cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return -99;
 
}


int class_max_p_3l_thq(int LepGood1_pdgId, int LepGood2_pdgId, int LepGood3_pdgId, float tth_low, float tth_high, float thq, float rest)
{
  std::vector<float> PrecentileCuts = {0.0, 0.45035608910694963, 0.5154428669859836, 0.6468995910968893};
  
  //cout << tth_low << "\n";
  if (thq < tth_low || thq < tth_high || thq < rest) {
	  //cout << "Dropped \n\n";
	  return -99;
  }
  
  int bin_counter = PrecentileCuts.size()-1;
  while (bin_counter >= 0) {
	  if (thq > PrecentileCuts[bin_counter]) return bin_counter;
	  bin_counter = bin_counter - 1;
  }


  cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return -99;
 
}

int class_max_p_3l_rest(int LepGood1_pdgId, int LepGood2_pdgId, int LepGood3_pdgId, float tth_low, float tth_high, float thq, float rest)
{
  std::vector<float> PrecentileCuts = {0.0, 0.410866806016376, 0.46782556287241234, 0.5318078974624368, 0.6110519619335995};
  
  //cout << tth_low << "\n";
  if (rest < tth_low || rest < tth_high || rest < thq) {
	  //cout << "Dropped \n\n";
	  return -99;
  }
  
  int bin_counter = PrecentileCuts.size()-1;
  while (bin_counter >= 0) {
	  if (rest > PrecentileCuts[bin_counter]) return bin_counter;
	  bin_counter = bin_counter - 1;
  }
  
  cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

 return -99;
 
}

int class_max_p_3l_tth_to_HiggsPt(int bin_idx, float Higgs_pt)
{
  std::vector<float> Pt_cuts_low = {0.0, 60, 120, 200};
  std::vector<float> Pt_cuts_high = {0.0, 200, 300, 450};
  
  if (bin_idx < 2) {
  
	  int nr_tth_bins = Pt_cuts_low.size();
	  int bin_counter = Pt_cuts_low.size()-1;
	  
	  while (bin_counter >= 0) {
		  if (Higgs_pt > Pt_cuts_low[bin_counter]) return nr_tth_bins*bin_idx + bin_counter;
		  bin_counter = bin_counter - 1;
	  }
  }
  else {
	  	  int nr_tth_bins = Pt_cuts_high.size();
	  int bin_counter = Pt_cuts_high.size()-1;
	  
	  while (bin_counter >= 0) {
		  if (Higgs_pt > Pt_cuts_high[bin_counter]) return nr_tth_bins*bin_idx + bin_counter;
		  bin_counter = bin_counter - 1;
	  }
  }
 return -99;
 
}

int catIndex_3l_all_HiggsPt(int LepGood1_pdgId, int LepGood2_pdgId, int LepGood3_pdgId, float tth_low, float tth_high, float thq, float rest, float Higgs_pt, int nBMedium )
{
  // 21 bins [0,20]
  int ttH_idx = 0;
  
  if ((tth_low > rest && tth_low > tth_high && tth_low > thq)) {
    if (nBMedium < 2)
      ttH_idx = 0; // ttH_bl
    else
      ttH_idx = 1; // ttH_bt
    return class_max_p_3l_tth_to_HiggsPt(ttH_idx, Higgs_pt);
  }
  
  else if (tth_high > rest && tth_high > tth_low && tth_high > thq) {
	  return class_max_p_3l_tth_to_HiggsPt(2, Higgs_pt);
  }
  
  else if (thq > rest && thq > tth_low && thq > tth_high) {
    if (nBMedium < 2){
      return 12; // tH_bl
    }
    else{
      return 13; // tH_bt
    }}
  
  else if (rest > tth_low && rest > tth_high && rest > thq) {
    int sumpdgId = abs(LepGood1_pdgId)+abs(LepGood2_pdgId)+abs(LepGood3_pdgId);
    if ( sumpdgId == 33){ // rest_eee
      return 14;
    }
    else if (sumpdgId == 35){ 
      if (nBMedium < 2)
	return 15; // rest_eem_bl
      else
	return 16; // rest_eem_bt
    }
    else if (sumpdgId == 37){ // emm
      if (nBMedium < 2)
	return 17; // rest_emm_bl
      else
	return 18; // rest_emm_bt
    }
    else if (sumpdgId == 39){ // mmm
      if (nBMedium < 2)
	return 19; // rest_mmm_bl
      else
	return 20; // rest_mmm_bt
    }
  }
	else cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;
 return -99;
}


// mttH binning

// 2lss

int class_2lss_tth_mttH_binning(float mttH)
{
	// 46 bins in total
    std::vector<float> mttH_cuts = {0.0,     400.0,  425.0,  450.0,  475.0,  500.0,  525.0,  550.0,  575.0,  600.0,
	                                625.0,   650.0,  675.0,  700.0,  725.0,  750.0,  775.0,  800.0,  825.0,  850.0, 
									875.0,   900.0,  933.0,  967.0, 1000.0, 1033.0, 1067.0, 1100.0, 1150.0, 1200.0, 
									1250.0, 1300.0, 1350.0, 1400.0, 1450.0, 1500.0, 1550.0, 1600.0, 1650.0, 1700.0, 
									1775.0, 1875.0, 2000.0, 2150.0, 2300.0, 2550.0};
    int bin_counter = mttH_cuts.size()-1;
	
	while (bin_counter >= 0) {
			  if (mttH > mttH_cuts[bin_counter]) return bin_counter;
			  bin_counter = bin_counter - 1;
		  }
	
	
	return -99;
	
  }
  
  
int catIndex_2lss_all_mttH(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float ttw, float thq, float rest, float mttH)
{
  // 135 bins [0,134]
  
  // Merge ttH_low and ttH_high classes into one ttH class (46 bins)
  if ((tth_low > ttw && tth_low > rest && tth_low > thq) || (tth_high > ttw && tth_high > rest && tth_high > thq)) {
      return class_2lss_tth_mttH_binning(mttH);
  }
  
  // 22 thq bins
  else if (thq > ttw && thq > rest && thq > tth_low && thq > tth_high) {
      return 46 + class_max_p_2lss_thq(LepGood1_pdgId, LepGood2_pdgId, tth_low, tth_high, ttw, thq, rest);
  }
  
  // 40 ttW bins
  else if (ttw > tth_high && ttw > rest && ttw > tth_low && ttw > thq) {
      return 68 + class_max_p_2lss_ttw(LepGood1_pdgId, LepGood2_pdgId, tth_low, tth_high, ttw, thq, rest);
  }
  
  // 27 rest bins
  else if (rest > tth_low && rest > ttw && rest > tth_high && rest > thq) {
      return 108 + class_max_p_2lss_rest(LepGood1_pdgId, LepGood2_pdgId, tth_low, tth_high, ttw, thq, rest);
  }
    else cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;
 return -99;
}


// 2lss1tau

int class_2lss1tau_tth_mttH_binning(float mttH)
{
	// 10 bins in total
    std::vector<float> mttH_cuts = {0.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1200.0, 1500.0};
    int bin_counter = mttH_cuts.size()-1;
	
	while (bin_counter >= 0) {
			  if (mttH > mttH_cuts[bin_counter]) return bin_counter;
			  bin_counter = bin_counter - 1;
		  }
	
	
	return -99;
	
  }

int catIndex_2lss1tau_all_mttH(int LepGood1_pdgId, int LepGood2_pdgId, float tth_low, float tth_high, float thq, float rest, float mttH)
{
  // 19 bins [0,18]
  
  // Merge ttH_low and ttH_high classes into one ttH class (10 bins)
  if ((tth_low > rest && tth_low > thq) || (tth_high > rest && tth_high > thq)) {
	  return class_2lss1tau_tth_mttH_binning(mttH);
  }
  
  // 4 thq bins
  else if (thq > rest && thq > tth_low && thq > tth_high) {
	  return 10 + class_max_p_2lss1tau_thq(LepGood1_pdgId, LepGood2_pdgId, tth_low, tth_high, thq, rest);
  }
  
  // 5 rest bins
  else if (rest > tth_low && rest > tth_high && rest > thq) {
	  return 14 + class_max_p_2lss1tau_rest(LepGood1_pdgId, LepGood2_pdgId, tth_low, tth_high, thq, rest);
  }
	else cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;
 return -99;
}

// 3l

int class_3l_tth_mttH_binning(float mttH)
{
	// 10 bins in total
    std::vector<float> mttH_cuts = {0.0, 450.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1100.0, 1250.0, 1500.0};
    int bin_counter = mttH_cuts.size()-1;
	
	while (bin_counter >= 0) {
			  if (mttH > mttH_cuts[bin_counter]) return bin_counter;
			  bin_counter = bin_counter - 1;
		  }
	
	
	return -99;
	
  }

int catIndex_3l_all_mttH(int LepGood1_pdgId, int LepGood2_pdgId, int LepGood3_pdgId, float tth_low, float tth_high, float thq, float rest, float mttH, int nBMedium )
{
  // 28 bins [0,27]
  int ttH_idx = 0;
  
  // 20 ttH bins
  if ((tth_low > rest && tth_low > thq) || (tth_high > rest && tth_high > thq)) {
    if (nBMedium < 2)
      return class_3l_tth_mttH_binning(mttH); // ttH_bl
    else
      return 10+class_3l_tth_mttH_binning(mttH); // ttH_bt
  }
  
  else if (thq > rest && thq > tth_low && thq > tth_high) {
    if (nBMedium < 2){
      return 20; // tH_bl
    }
    else{
      return 21; // tH_bt
    }}
  
  else if (rest > tth_low && rest > tth_high && rest > thq) {
    int sumpdgId = abs(LepGood1_pdgId)+abs(LepGood2_pdgId)+abs(LepGood3_pdgId);
    if ( sumpdgId == 33){ // rest_eee
      return 22;
    }
    else if (sumpdgId == 35){ 
      if (nBMedium < 2)
	return 23; // rest_eem_bl
      else
	return 24; // rest_eem_bt
    }
    else if (sumpdgId == 37){ // emm
      if (nBMedium < 2)
	return 25; // rest_emm_bl
      else
	return 26; // rest_emm_bt
    }
    else if (sumpdgId == 39){ // mmm
      if (nBMedium < 2)
	return 27; // rest_mmm_bl
      else
	return 28; // rest_mmm_bt
    }
  }
	else cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;
 return -99;
}