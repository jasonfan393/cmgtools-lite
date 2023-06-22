C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     ProjM(2,1)*ProjP(4,3)
C     
      SUBROUTINE FFFF10_2(F1, F3, F4, COUP, M2, W2,F2)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 TMP12
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
      TMP12 = (F4(5)*F3(5)+F4(6)*F3(6))
      DENOM = COUP/(P2(0)**2-P2(1)**2-P2(2)**2-P2(3)**2 - M2 * (M2 -CI
     $ * W2))
      F2(3)= DENOM*CI * TMP12*F1(3)*M2
      F2(4)= DENOM*CI * TMP12*F1(4)*M2
      F2(5)= DENOM*(-CI )* TMP12*(F1(3)*(-1D0)*(P2(0)+P2(3))+F1(4)*(
     $ +CI*(P2(2))-P2(1)))
      F2(6)= DENOM*CI * TMP12*(F1(3)*(P2(1)+CI*(P2(2)))+F1(4)*(P2(0)
     $ -P2(3)))
      END


C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     ProjM(2,1)*ProjP(4,3)
C     
      SUBROUTINE FFFF10_14_18_19_6_8_2(F1, F3, F4, COUP1, COUP2, COUP3
     $ , COUP4, COUP5, COUP6, M2, W2,F2)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 F2(6)
      COMPLEX*16 FTMP(6)
      COMPLEX*16 COUP2
      COMPLEX*16 COUP5
      REAL*8 P2(0:3)
      REAL*8 W2
      COMPLEX*16 F1(*)
      REAL*8 M2
      COMPLEX*16 DENOM
      COMPLEX*16 COUP1
      COMPLEX*16 F3(*)
      COMPLEX*16 COUP4
      COMPLEX*16 COUP3
      COMPLEX*16 COUP6
      INTEGER*4 I
      COMPLEX*16 F4(*)
      CALL FFFF10_2(F1,F3,F4,COUP1,M2,W2,F2)
      CALL FFFF14_2(F1,F3,F4,COUP2,M2,W2,FTMP)
      DO I = 3, 6
        F2(I) = F2(I) + FTMP(I)
      ENDDO
      CALL FFFF18_2(F1,F3,F4,COUP3,M2,W2,FTMP)
      DO I = 3, 6
        F2(I) = F2(I) + FTMP(I)
      ENDDO
      CALL FFFF19_2(F1,F3,F4,COUP4,M2,W2,FTMP)
      DO I = 3, 6
        F2(I) = F2(I) + FTMP(I)
      ENDDO
      CALL FFFF6_2(F1,F3,F4,COUP5,M2,W2,FTMP)
      DO I = 3, 6
        F2(I) = F2(I) + FTMP(I)
      ENDDO
      CALL FFFF8_2(F1,F3,F4,COUP6,M2,W2,FTMP)
      DO I = 3, 6
        F2(I) = F2(I) + FTMP(I)
      ENDDO
      END


C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     ProjM(2,1)*ProjP(4,3)
C     
      SUBROUTINE FFFF10_11_20_6_110_2(F1, F3, F4, COUP1, COUP2, COUP3,
     $  COUP4, COUP5, M2, W2,F2)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 F2(6)
      COMPLEX*16 FTMP(6)
      COMPLEX*16 COUP2
      COMPLEX*16 COUP5
      REAL*8 P2(0:3)
      REAL*8 W2
      COMPLEX*16 F1(*)
      REAL*8 M2
      COMPLEX*16 DENOM
      COMPLEX*16 COUP1
      COMPLEX*16 F3(*)
      COMPLEX*16 COUP4
      COMPLEX*16 COUP3
      COMPLEX*16 COUP6
      INTEGER*4 I
      COMPLEX*16 F4(*)
      CALL FFFF10_2(F1,F3,F4,COUP1,M2,W2,F2)
      CALL FFFF11_2(F1,F3,F4,COUP2,M2,W2,FTMP)
      DO I = 3, 6
        F2(I) = F2(I) + FTMP(I)
      ENDDO
      CALL FFFF20_2(F1,F3,F4,COUP3,M2,W2,FTMP)
      DO I = 3, 6
        F2(I) = F2(I) + FTMP(I)
      ENDDO
      CALL FFFF6_2(F1,F3,F4,COUP4,M2,W2,FTMP)
      DO I = 3, 6
        F2(I) = F2(I) + FTMP(I)
      ENDDO
      CALL FFFF110_2(F1,F3,F4,COUP5,M2,W2,FTMP)
      DO I = 3, 6
        F2(I) = F2(I) + FTMP(I)
      ENDDO
      END


C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     ProjM(2,1)*ProjP(4,3)
C     
      SUBROUTINE FFFF10_11_19_2_20_6_7_8_21_110_2(F1, F3, F4, COUP1,
     $  COUP2, COUP3, COUP4, COUP5, COUP6, COUP7, COUP8, COUP9, COUP10
     $ , M2, W2,F2)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 COUP6
      COMPLEX*16 FTMP(6)
      COMPLEX*16 COUP2
      COMPLEX*16 COUP5
      REAL*8 P2(0:3)
      REAL*8 W2
      COMPLEX*16 COUP1
      COMPLEX*16 F3(*)
      COMPLEX*16 COUP4
      COMPLEX*16 COUP9
      REAL*8 M2
      COMPLEX*16 F2(6)
      INTEGER*4 I
      COMPLEX*16 COUP10
      COMPLEX*16 DENOM
      COMPLEX*16 COUP8
      COMPLEX*16 COUP7
      COMPLEX*16 F1(*)
      COMPLEX*16 COUP3
      COMPLEX*16 F4(*)
      CALL FFFF10_2(F1,F3,F4,COUP1,M2,W2,F2)
      CALL FFFF11_2(F1,F3,F4,COUP2,M2,W2,FTMP)
      DO I = 3, 6
        F2(I) = F2(I) + FTMP(I)
      ENDDO
      CALL FFFF19_2(F1,F3,F4,COUP3,M2,W2,FTMP)
      DO I = 3, 6
        F2(I) = F2(I) + FTMP(I)
      ENDDO
      CALL FFFF2_2(F1,F3,F4,COUP4,M2,W2,FTMP)
      DO I = 3, 6
        F2(I) = F2(I) + FTMP(I)
      ENDDO
      CALL FFFF20_2(F1,F3,F4,COUP5,M2,W2,FTMP)
      DO I = 3, 6
        F2(I) = F2(I) + FTMP(I)
      ENDDO
      CALL FFFF6_2(F1,F3,F4,COUP6,M2,W2,FTMP)
      DO I = 3, 6
        F2(I) = F2(I) + FTMP(I)
      ENDDO
      CALL FFFF7_2(F1,F3,F4,COUP7,M2,W2,FTMP)
      DO I = 3, 6
        F2(I) = F2(I) + FTMP(I)
      ENDDO
      CALL FFFF8_2(F1,F3,F4,COUP8,M2,W2,FTMP)
      DO I = 3, 6
        F2(I) = F2(I) + FTMP(I)
      ENDDO
      CALL FFFF21_2(F1,F3,F4,COUP9,M2,W2,FTMP)
      DO I = 3, 6
        F2(I) = F2(I) + FTMP(I)
      ENDDO
      CALL FFFF110_2(F1,F3,F4,COUP10,M2,W2,FTMP)
      DO I = 3, 6
        F2(I) = F2(I) + FTMP(I)
      ENDDO
      END


