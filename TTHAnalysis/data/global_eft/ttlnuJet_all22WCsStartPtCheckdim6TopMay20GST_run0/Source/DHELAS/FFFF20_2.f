C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     Gamma(-2,-6,-5)*Gamma(-2,-4,-3)*Gamma(-1,2,-4)*Gamma(-1,4,-6)*Pro
C     jP(-5,3)*ProjP(-3,1)
C     
      SUBROUTINE FFFF20_2(F1, F3, F4, COUP, M2, W2,F2)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 F2(6)
      REAL*8 P2(0:3)
      REAL*8 W2
      COMPLEX*16 F1(*)
      REAL*8 M2
      COMPLEX*16 DENOM
      COMPLEX*16 F3(*)
      COMPLEX*16 COUP
      COMPLEX*16 F4(*)
      F2(1) = +F1(1)+F3(1)+F4(1)
      F2(2) = +F1(2)+F3(2)+F4(2)
      P2(0) = -DBLE(F2(1))
      P2(1) = -DBLE(F2(2))
      P2(2) = -DIMAG(F2(2))
      P2(3) = -DIMAG(F2(1))
      DENOM = COUP/(P2(0)**2-P2(1)**2-P2(2)**2-P2(3)**2 - M2 * (M2 -CI
     $ * W2))
      F2(3)= DENOM*8D0 * CI*(F4(5)*(F1(5)*F3(6)*(P2(1)-CI*(P2(2)))
     $ +F1(6)*F3(5)*(+CI*(P2(2))-P2(1)))+F4(6)*(F1(5)*F3(6)*(P2(0)
     $ -P2(3))+F1(6)*F3(5)*(P2(3)-P2(0))))
      F2(4)= DENOM*8D0 * CI*(F4(5)*(F1(5)*-F3(6)*(P2(0)+P2(3))+F1(6)
     $ *F3(5)*(P2(0)+P2(3)))+F4(6)*(F1(5)*-F3(6)*(P2(1)+CI*(P2(2)))
     $ +F1(6)*F3(5)*(P2(1)+CI*(P2(2)))))
      F2(5)= DENOM*8D0 * CI * F4(6)*M2*(F1(5)*F3(6)-F1(6)*F3(5))
      F2(6)= DENOM*8D0 * CI * F4(5)*M2*(F1(6)*F3(5)-F1(5)*F3(6))
      END


