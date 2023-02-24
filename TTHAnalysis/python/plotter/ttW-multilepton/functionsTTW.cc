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


float ttH_2lss_ifflav(int LepGood1_pdgId, int LepGood2_pdgId, float ret_ee, float ret_em, float ret_mm){
  if (abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11) return ret_ee;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)))       return ret_em;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13) return ret_mm;
  std::cerr << "ERROR: invalid input " << abs(LepGood1_pdgId) << ", " << abs(LepGood1_pdgId) << std::endl;
  assert(0);
  return 0; // avoid warning
}
