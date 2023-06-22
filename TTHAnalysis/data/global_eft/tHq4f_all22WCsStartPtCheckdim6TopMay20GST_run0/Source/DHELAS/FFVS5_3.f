C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     -(P(-1,3)*Gamma(-1,2,-3)*Gamma(3,-3,-2)*ProjP(-2,1)) +
C      P(-1,3)*Gamma(-1,-3,-2)*Gamma(3,2,-3)*ProjP(-2,1)
C     
      SUBROUTINE FFVS5_3(F1, F2, S4, COUP, M3, W3,V3)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 DENOM
      COMPLEX*16 V3(6)
      REAL*8 W3
      REAL*8 P3(0:3)
      REAL*8 M3
      COMPLEX*16 F1(*)
      COMPLEX*16 TMP16
      COMPLEX*16 F2(*)
      COMPLEX*16 COUP
      COMPLEX*16 S4(*)
      V3(1) = +F1(1)+F2(1)+S4(1)
      V3(2) = +F1(2)+F2(2)+S4(2)
      P3(0) = -DBLE(V3(1))
      P3(1) = -DBLE(V3(2))
      P3(2) = -DIMAG(V3(2))
      P3(3) = -DIMAG(V3(1))
      TMP16 = (F1(5)*-F2(5)*(P3(1)*P3(1)+P3(2)*P3(2)+P3(3)*P3(3)-P3(0)
     $ *P3(0))-F1(6)*F2(6)*(P3(1)*P3(1)+P3(2)*P3(2)+P3(3)*P3(3)-P3(0)
     $ *P3(0)))
      DENOM = COUP/(P3(0)**2-P3(1)**2-P3(2)**2-P3(3)**2 - M3 * (M3 -CI
     $ * W3))
      V3(3)= DENOM*2D0 * CI * S4(3)*(F1(5)*(F2(6)*(P3(1)+CI*(P3(2)))
     $ +P3(3)*F2(5))+F1(6)*(F2(5)*(P3(1)-CI*(P3(2)))-P3(3)*F2(6)))
      V3(4)= DENOM*2D0 * CI * S4(3)*(F1(5)*(F2(6)*(P3(0)-P3(3))-CI
     $ *(P3(2)*F2(5)))+F1(6)*(F2(5)*(P3(0)+P3(3))+CI*(P3(2)*F2(6))))
      V3(5)= DENOM*(-2D0 )* CI * S4(3)*(F1(5)*(F2(6)*(-CI*(P3(0))+CI
     $ *(P3(3)))-CI*(P3(1)*F2(5)))+F1(6)*(F2(5)*(+CI*(P3(0)+P3(3)))+CI
     $ *(P3(1)*F2(6))))
      V3(6)= DENOM*2D0 * CI * S4(3)*(F1(5)*(F2(6)*(P3(1)+CI*(P3(2)))
     $ +P3(0)*F2(5))+F1(6)*(F2(5)*(+CI*(P3(2))-P3(1))-P3(0)*F2(6)))
      END


