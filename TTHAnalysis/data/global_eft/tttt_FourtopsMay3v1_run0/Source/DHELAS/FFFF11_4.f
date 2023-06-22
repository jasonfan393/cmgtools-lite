C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     ProjP(2,1)*ProjP(4,3)
C     
      SUBROUTINE FFFF11_4(F1, F2, F3, COUP, M4, W4,F4)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 TMP12
      REAL*8 W4
      COMPLEX*16 F1(*)
      COMPLEX*16 F2(*)
      COMPLEX*16 F3(*)
      COMPLEX*16 DENOM
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
      TMP12 = (F1(5)*F2(5)+F1(6)*F2(6))
      DENOM = COUP/(P4(0)**2-P4(1)**2-P4(2)**2-P4(3)**2 - M4 * (M4 -CI
     $ * W4))
      F4(3)= DENOM*CI * TMP12*(F3(5)*(P4(0)-P4(3))+F3(6)*(+CI*(P4(2))
     $ -P4(1)))
      F4(4)= DENOM*(-CI )* TMP12*(F3(5)*(P4(1)+CI*(P4(2)))-F3(6)*(P4(0)
     $ +P4(3)))
      F4(5)= DENOM*CI * F3(5)*TMP12*M4
      F4(6)= DENOM*CI * F3(6)*TMP12*M4
      END


C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     ProjP(2,1)*ProjP(4,3)
C     
      SUBROUTINE FFFF11_14_18_19_2_20_6_7_21_110_4(F1, F2, F3, COUP1,
     $  COUP2, COUP3, COUP4, COUP5, COUP6, COUP7, COUP8, COUP9, COUP10
     $ , M4, W4,F4)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 COUP6
      COMPLEX*16 FTMP(6)
      COMPLEX*16 COUP2
      REAL*8 M4
      COMPLEX*16 COUP5
      COMPLEX*16 COUP1
      COMPLEX*16 F3(*)
      COMPLEX*16 COUP4
      COMPLEX*16 COUP9
      COMPLEX*16 F2(*)
      INTEGER*4 I
      COMPLEX*16 COUP10
      REAL*8 P4(0:3)
      COMPLEX*16 DENOM
      COMPLEX*16 COUP8
      COMPLEX*16 COUP7
      COMPLEX*16 F1(*)
      COMPLEX*16 COUP3
      REAL*8 W4
      COMPLEX*16 F4(6)
      CALL FFFF11_4(F1,F2,F3,COUP1,M4,W4,F4)
      CALL FFFF14_4(F1,F2,F3,COUP2,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      CALL FFFF18_4(F1,F2,F3,COUP3,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      CALL FFFF19_4(F1,F2,F3,COUP4,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      CALL FFFF2_4(F1,F2,F3,COUP5,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      CALL FFFF20_4(F1,F2,F3,COUP6,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      CALL FFFF6_4(F1,F2,F3,COUP7,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      CALL FFFF7_4(F1,F2,F3,COUP8,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      CALL FFFF21_4(F1,F2,F3,COUP9,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      CALL FFFF110_4(F1,F2,F3,COUP10,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      END


C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     ProjP(2,1)*ProjP(4,3)
C     
      SUBROUTINE FFFF11_2_4(F1, F2, F3, COUP1, COUP2, M4, W4,F4)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 COUP6
      COMPLEX*16 FTMP(6)
      COMPLEX*16 COUP2
      REAL*8 M4
      COMPLEX*16 COUP5
      COMPLEX*16 COUP1
      COMPLEX*16 F3(*)
      COMPLEX*16 COUP4
      COMPLEX*16 COUP9
      COMPLEX*16 F2(*)
      INTEGER*4 I
      COMPLEX*16 COUP10
      REAL*8 P4(0:3)
      COMPLEX*16 DENOM
      COMPLEX*16 COUP8
      COMPLEX*16 COUP7
      COMPLEX*16 F1(*)
      COMPLEX*16 COUP3
      REAL*8 W4
      COMPLEX*16 F4(6)
      CALL FFFF11_4(F1,F2,F3,COUP1,M4,W4,F4)
      CALL FFFF2_4(F1,F2,F3,COUP2,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      END


C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     ProjP(2,1)*ProjP(4,3)
C     
      SUBROUTINE FFFF11_2_6_4(F1, F2, F3, COUP1, COUP2, COUP3, M4, W4
     $ ,F4)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 COUP6
      COMPLEX*16 FTMP(6)
      COMPLEX*16 COUP2
      REAL*8 M4
      COMPLEX*16 COUP5
      COMPLEX*16 COUP1
      COMPLEX*16 F3(*)
      COMPLEX*16 COUP4
      COMPLEX*16 COUP9
      COMPLEX*16 F2(*)
      INTEGER*4 I
      COMPLEX*16 COUP10
      REAL*8 P4(0:3)
      COMPLEX*16 DENOM
      COMPLEX*16 COUP8
      COMPLEX*16 COUP7
      COMPLEX*16 F1(*)
      COMPLEX*16 COUP3
      REAL*8 W4
      COMPLEX*16 F4(6)
      CALL FFFF11_4(F1,F2,F3,COUP1,M4,W4,F4)
      CALL FFFF2_4(F1,F2,F3,COUP2,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      CALL FFFF6_4(F1,F2,F3,COUP3,M4,W4,FTMP)
      DO I = 3, 6
        F4(I) = F4(I) + FTMP(I)
      ENDDO
      END


