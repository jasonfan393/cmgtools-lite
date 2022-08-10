int categories3l(float mZ, int nbjets, int charge_sum){

  if (abs(mZ-91.2) > 10){
    if (nbjets == 1){
      if (charge_sum < 0) return 1;
      else              return 2;
    }
    else{
      if (charge_sum < 0) return 3;
      else              return 4;
    }
  }
  else{
    if (nbjets == 1) return 5;
    else return 6;
  }


}


float categories2l( int charge1, int nbjets){
  
  if (charge1 < 0 && nbjets > 2){
    return 1;
  }
  else if (charge1 > 0 && nbjets > 2){
    return 2;
  }
  else if (charge1 < 0 && nbjets <= 2){
    return 3;
  }
  else if (charge1 > 0 && nbjets <= 2){
    return 4;
  }
  else return 0;

}
