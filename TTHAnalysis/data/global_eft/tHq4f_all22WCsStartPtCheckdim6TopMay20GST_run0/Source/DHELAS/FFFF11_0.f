C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     ProjP(2,1)*ProjP(4,3)
C     
      SUBROUTINE FFFF11_0(F1, F2, F3, F4, COUP,VERTEX)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 TMP12
      COMPLEX*16 TMP11
      COMPLEX*16 F1(*)
      COMPLEX*16 F2(*)
      COMPLEX*16 F3(*)
      COMPLEX*16 VERTEX
      COMPLEX*16 COUP
      COMPLEX*16 F4(*)
      TMP11 = (F4(5)*F3(5)+F4(6)*F3(6))
      TMP12 = (F2(5)*F1(5)+F2(6)*F1(6))
      VERTEX = COUP*(-CI * TMP11*TMP12)
      END


