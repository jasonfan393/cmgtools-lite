C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     Gamma(-1,2,-2)*Gamma(-1,4,-3)*ProjM(-2,3)*ProjP(-3,1)
C     
      SUBROUTINE FFFF15_3(F1, F2, F4, COUP, M3, W3,F3)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 F2(*)
      REAL*8 W3
      REAL*8 P3(0:3)
      REAL*8 M3
      COMPLEX*16 F1(*)
      COMPLEX*16 DENOM
      COMPLEX*16 F3(6)
      COMPLEX*16 COUP
      COMPLEX*16 F4(*)
      F3(1) = +F1(1)+F2(1)+F4(1)
      F3(2) = +F1(2)+F2(2)+F4(2)
      P3(0) = -DBLE(F3(1))
      P3(1) = -DBLE(F3(2))
      P3(2) = -DIMAG(F3(2))
      P3(3) = -DIMAG(F3(1))
      DENOM = COUP/(P3(0)**2-P3(1)**2-P3(2)**2-P3(3)**2 - M3 * (M3 -CI
     $ * W3))
      F3(3)= DENOM*2D0 * CI * F4(3)*M3*(F1(5)*F2(5)+F1(6)*F2(6))
      F3(4)= DENOM*2D0 * CI * F4(4)*M3*(F1(5)*F2(5)+F1(6)*F2(6))
      F3(5)= DENOM*2D0 * CI*(F4(3)*(F1(5)*F2(5)*(P3(3)-P3(0))+F1(6)
     $ *F2(6)*(P3(3)-P3(0)))+F4(4)*(F1(5)*F2(5)*(P3(1)+CI*(P3(2)))
     $ +F1(6)*F2(6)*(P3(1)+CI*(P3(2)))))
      F3(6)= DENOM*(-2D0 * CI)*(F4(3)*(F1(5)*F2(5)*(+CI*(P3(2))-P3(1))
     $ +F1(6)*F2(6)*(+CI*(P3(2))-P3(1)))+F4(4)*(F1(5)*F2(5)*(P3(0)
     $ +P3(3))+F1(6)*F2(6)*(P3(0)+P3(3))))
      END


