C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     ProjM(2,3)*ProjM(4,1)
C     
      SUBROUTINE FFFF1_4(F1, F2, F3, COUP, M4, W4,F4)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 DENOM
      REAL*8 W4
      COMPLEX*16 TMP37
      COMPLEX*16 F1(*)
      COMPLEX*16 F2(*)
      COMPLEX*16 F3(*)
      REAL*8 M4
      REAL*8 P4(0:3)
      COMPLEX*16 COUP
      COMPLEX*16 F4(6)
      F4(1) = +F1(1)+F2(1)+F3(1)
      F4(2) = +F1(2)+F2(2)+F3(2)
      P4(0) = -DBLE(F4(1))
      P4(1) = -DBLE(F4(2))
      P4(2) = -DIMAG(F4(2))
      P4(3) = -DIMAG(F4(1))
      TMP37 = (F2(3)*F3(3)+F2(4)*F3(4))
      DENOM = COUP/(P4(0)**2-P4(1)**2-P4(2)**2-P4(3)**2 - M4 * (M4 -CI
     $ * W4))
      F4(3)= DENOM*CI * TMP37*F1(3)*M4
      F4(4)= DENOM*CI * TMP37*F1(4)*M4
      F4(5)= DENOM*(-CI )* TMP37*(F1(3)*(-1D0)*(P4(0)+P4(3))+F1(4)*(
     $ +CI*(P4(2))-P4(1)))
      F4(6)= DENOM*CI * TMP37*(F1(3)*(P4(1)+CI*(P4(2)))+F1(4)*(P4(0)
     $ -P4(3)))
      END


C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     ProjM(2,3)*ProjM(4,1)
C     
      SUBROUTINE FFFF1_15_16_17_5_9_4(F1, F2, F3, COUP1, COUP2, COUP3,
     $  COUP4, COUP5, COUP6, M4, W4,F4)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 DENOM
      REAL*8 W4
      COMPLEX*16 FTMP(6)
      COMPLEX*16 COUP2
      COMPLEX*16 COUP4
      COMPLEX*16 F1(*)
      COMPLEX*16 COUP1
      COMPLEX*16 F2(*)
      COMPLEX*16 F3(*)
      REAL*8 M4
      REAL*8 P4(0:3)
      COMPLEX*16 COUP3
      COMPLEX*16 COUP6
      INTEGER*4 I
      COMPLEX*16 COUP5
      COMPLEX*16 F4(6)
      CALL FFFF1_4(F1,F2,F3,COUP1,M4,W4,F4)
      CALL FFFF15_4(F1,F2,F3,COUP2,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      CALL FFFF16_4(F1,F2,F3,COUP3,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      CALL FFFF17_4(F1,F2,F3,COUP4,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      CALL FFFF5_4(F1,F2,F3,COUP5,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      CALL FFFF9_4(F1,F2,F3,COUP6,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      END


C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     ProjM(2,3)*ProjM(4,1)
C     
      SUBROUTINE FFFF1_15_16_17_9_4(F1, F2, F3, COUP1, COUP2, COUP3,
     $  COUP4, COUP5, M4, W4,F4)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 DENOM
      REAL*8 W4
      COMPLEX*16 FTMP(6)
      COMPLEX*16 COUP2
      COMPLEX*16 COUP4
      COMPLEX*16 F1(*)
      COMPLEX*16 COUP1
      COMPLEX*16 F2(*)
      COMPLEX*16 F3(*)
      REAL*8 M4
      REAL*8 P4(0:3)
      COMPLEX*16 COUP3
      COMPLEX*16 COUP6
      INTEGER*4 I
      COMPLEX*16 COUP5
      COMPLEX*16 F4(6)
      CALL FFFF1_4(F1,F2,F3,COUP1,M4,W4,F4)
      CALL FFFF15_4(F1,F2,F3,COUP2,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      CALL FFFF16_4(F1,F2,F3,COUP3,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      CALL FFFF17_4(F1,F2,F3,COUP4,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      CALL FFFF9_4(F1,F2,F3,COUP5,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      END


