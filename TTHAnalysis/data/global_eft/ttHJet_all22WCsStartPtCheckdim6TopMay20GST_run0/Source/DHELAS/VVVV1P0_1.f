C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     Metric(1,4)*Metric(2,3) - Metric(1,3)*Metric(2,4)
C     
      SUBROUTINE VVVV1P0_1(V2, V3, V4, COUP, M1, W1,V1)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 V2(*)
      COMPLEX*16 V3(*)
      REAL*8 P1(0:3)
      COMPLEX*16 TMP44
      REAL*8 W1
      COMPLEX*16 TMP30
      COMPLEX*16 V4(*)
      COMPLEX*16 DENOM
      REAL*8 M1
      COMPLEX*16 COUP
      COMPLEX*16 V1(6)
      V1(1) = +V2(1)+V3(1)+V4(1)
      V1(2) = +V2(2)+V3(2)+V4(2)
      P1(0) = -DBLE(V1(1))
      P1(1) = -DBLE(V1(2))
      P1(2) = -DIMAG(V1(2))
      P1(3) = -DIMAG(V1(1))
      TMP30 = (V3(3)*V2(3)-V3(4)*V2(4)-V3(5)*V2(5)-V3(6)*V2(6))
      TMP44 = (V4(3)*V2(3)-V4(4)*V2(4)-V4(5)*V2(5)-V4(6)*V2(6))
      DENOM = COUP/(P1(0)**2-P1(1)**2-P1(2)**2-P1(3)**2 - M1 * (M1 -CI
     $ * W1))
      V1(3)= DENOM*(-CI*(V4(3)*TMP30)+CI*(V3(3)*TMP44))
      V1(4)= DENOM*(-CI*(V4(4)*TMP30)+CI*(V3(4)*TMP44))
      V1(5)= DENOM*(-CI*(V4(5)*TMP30)+CI*(V3(5)*TMP44))
      V1(6)= DENOM*(-CI*(V4(6)*TMP30)+CI*(V3(6)*TMP44))
      END


