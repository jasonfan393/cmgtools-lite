C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     Gamma(-1,2,-2)*Gamma(-1,4,-3)*ProjM(-2,3)*ProjP(-3,1)
C     
      SUBROUTINE FFFF15_0(F1, F2, F3, F4, COUP,VERTEX)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 TMP20
      COMPLEX*16 F1(*)
      COMPLEX*16 F2(*)
      COMPLEX*16 F3(*)
      COMPLEX*16 VERTEX
      COMPLEX*16 COUP
      COMPLEX*16 F4(*)
      TMP20 = (F1(5)*F2(5)*(F4(3)*F3(3)+F4(4)*F3(4))+F1(6)*F2(6)*(F4(3)
     $ *F3(3)+F4(4)*F3(4)))
      VERTEX = COUP*(-2D0 * CI * TMP20)
      END

