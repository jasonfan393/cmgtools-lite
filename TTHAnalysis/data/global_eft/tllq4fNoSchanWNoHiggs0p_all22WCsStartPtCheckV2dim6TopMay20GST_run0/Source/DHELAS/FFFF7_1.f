C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     Gamma(-2,-6,-5)*Gamma(-2,-4,-3)*Gamma(-1,2,-4)*Gamma(-1,4,-6)*Pro
C     jM(-5,3)*ProjM(-3,1)
C     
      SUBROUTINE FFFF7_1(F2, F3, F4, COUP, M1, W1,F1)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 F2(*)
      REAL*8 P1(0:3)
      REAL*8 M1
      REAL*8 W1
      COMPLEX*16 F1(6)
      COMPLEX*16 DENOM
      COMPLEX*16 F3(*)
      COMPLEX*16 COUP
      COMPLEX*16 F4(*)
      F1(1) = +F2(1)+F3(1)+F4(1)
      F1(2) = +F2(2)+F3(2)+F4(2)
      P1(0) = -DBLE(F1(1))
      P1(1) = -DBLE(F1(2))
      P1(2) = -DIMAG(F1(2))
      P1(3) = -DIMAG(F1(1))
      DENOM = COUP/(P1(0)**2-P1(1)**2-P1(2)**2-P1(3)**2 - M1 * (M1 -CI
     $ * W1))
      F1(3)= DENOM*8D0 * CI * F3(4)*M1*(F2(3)*F4(4)-F2(4)*F4(3))
      F1(4)= DENOM*8D0 * CI * F3(3)*M1*(F2(4)*F4(3)-F2(3)*F4(4))
      F1(5)= DENOM*(-8D0 * CI)*(F3(3)*(F2(3)*F4(4)*(P1(1)+CI*(P1(2)))
     $ -F2(4)*F4(3)*(P1(1)+CI*(P1(2))))+F3(4)*(F2(3)*F4(4)*(P1(0)-P1(3)
     $ )+F2(4)*F4(3)*(P1(3)-P1(0))))
      F1(6)= DENOM*(-8D0 * CI)*(F3(3)*(F2(3)*-F4(4)*(P1(0)+P1(3))+F2(4)
     $ *F4(3)*(P1(0)+P1(3)))+F3(4)*(F2(3)*F4(4)*(+CI*(P1(2))-P1(1))
     $ +F2(4)*F4(3)*(P1(1)-CI*(P1(2)))))
      END


