ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      written by the UFO converter
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      SUBROUTINE COUP1()

      IMPLICIT NONE
      INCLUDE 'model_functions.inc'

      DOUBLE PRECISION PI, ZERO
      PARAMETER  (PI=3.141592653589793D0)
      PARAMETER  (ZERO=0D0)
      INCLUDE 'input.inc'
      INCLUDE 'coupl.inc'
      GC_1 = -(MDL_EE*MDL_COMPLEXI)/3.000000D+00
      GC_2 = (2.000000D+00*MDL_EE*MDL_COMPLEXI)/3.000000D+00
      GC_3 = -(MDL_EE*MDL_COMPLEXI)
      GC_4 = MDL_EE*MDL_COMPLEXI
      GC_649 = (MDL_EE*MDL_COMPLEXI)/(MDL_SW*MDL_SQRT__2)
      GC_650 = -(MDL_CW*MDL_EE*MDL_COMPLEXI)/(2.000000D+00*MDL_SW)
      GC_651 = (MDL_CW*MDL_EE*MDL_COMPLEXI)/(2.000000D+00*MDL_SW)
      GC_653 = (MDL_CW*MDL_EE*MDL_COMPLEXI)/MDL_SW
      GC_660 = -(MDL_EE*MDL_COMPLEXI*MDL_SW)/(6.000000D+00*MDL_CW)
      GC_661 = (MDL_EE*MDL_COMPLEXI*MDL_SW)/(2.000000D+00*MDL_CW)
      GC_664 = (MDL_CW*MDL_EE*MDL_COMPLEXI)/(2.000000D+00*MDL_SW)
     $ +(MDL_EE*MDL_COMPLEXI*MDL_SW)/(2.000000D+00*MDL_CW)
      GC_730 = (MDL_EE__EXP__2*MDL_COMPLEXI*MDL_VEV)/(2.000000D+00
     $ *MDL_SW__EXP__2)
      GC_734 = (MDL_CTW*MDL_EE*MDL_COMPLEXI*MDL_VEV)
     $ /(MDL_LAMBDA__EXP__2*MDL_SW*MDL_SQRT__2)
      GC_735 = (MDL_CTWI*MDL_EE*MDL_VEV)/(MDL_LAMBDA__EXP__2*MDL_SW
     $ *MDL_SQRT__2)
      GC_740 = (MDL_CPQ3*MDL_EE*MDL_COMPLEXI*MDL_VEV__EXP__2)
     $ /(MDL_LAMBDA__EXP__2*MDL_SW*MDL_SQRT__2)
      GC_813 = (MDL_CTW*MDL_COMPLEXI*MDL_VEV)/(MDL_LAMBDA__EXP__2
     $ *MDL_SW*MDL_SQRT__2)-(MDL_CTZ*MDL_CW*MDL_COMPLEXI*MDL_VEV)
     $ /(MDL_LAMBDA__EXP__2*MDL_SW*MDL_SQRT__2)
      GC_814 = (MDL_CTWI*MDL_VEV)/(MDL_LAMBDA__EXP__2*MDL_SW
     $ *MDL_SQRT__2)-(MDL_CTZI*MDL_CW*MDL_VEV)/(MDL_LAMBDA__EXP__2
     $ *MDL_SW*MDL_SQRT__2)
      GC_923 = -(MDL_CPTBI*MDL_EE*MDL_VEV__EXP__2)/(2.000000D+00
     $ *MDL_LAMBDA__EXP__2*MDL_SW*MDL_SQRT__2)-(MDL_CPTB*MDL_EE
     $ *MDL_COMPLEXI*MDL_VEV__EXP__2)/(2.000000D+00*MDL_LAMBDA__EXP__2
     $ *MDL_SW*MDL_SQRT__2)
      GC_924 = (MDL_CPTBI*MDL_EE*MDL_VEV__EXP__2)/(2.000000D+00
     $ *MDL_LAMBDA__EXP__2*MDL_SW*MDL_SQRT__2)-(MDL_CPTB*MDL_EE
     $ *MDL_COMPLEXI*MDL_VEV__EXP__2)/(2.000000D+00*MDL_LAMBDA__EXP__2
     $ *MDL_SW*MDL_SQRT__2)
      GC_938 = -(MDL_CPQM*MDL_CW*MDL_EE*MDL_COMPLEXI*MDL_VEV__EXP__2)
     $ /(2.000000D+00*MDL_LAMBDA__EXP__2*MDL_SW)-(MDL_CPQM*MDL_EE
     $ *MDL_COMPLEXI*MDL_SW*MDL_VEV__EXP__2)/(2.000000D+00*MDL_CW
     $ *MDL_LAMBDA__EXP__2)
      GC_948 = -(MDL_CPT*MDL_CW*MDL_EE*MDL_COMPLEXI*MDL_VEV__EXP__2)
     $ /(2.000000D+00*MDL_LAMBDA__EXP__2*MDL_SW)-(MDL_CPT*MDL_EE
     $ *MDL_COMPLEXI*MDL_SW*MDL_VEV__EXP__2)/(2.000000D+00*MDL_CW
     $ *MDL_LAMBDA__EXP__2)
      GC_10 = -(MDL_CBLSI1/MDL_LAMBDA__EXP__2)+(MDL_CBLS1*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_11 = MDL_CBLSI1/MDL_LAMBDA__EXP__2+(MDL_CBLS1*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_12 = -(MDL_CBLSI2/MDL_LAMBDA__EXP__2)+(MDL_CBLS2*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_13 = MDL_CBLSI2/MDL_LAMBDA__EXP__2+(MDL_CBLS2*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      END