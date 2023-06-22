      SUBROUTINE M2_SMATRIXHEL(P,HEL,ANS)
      IMPLICIT NONE
C     
C     CONSTANT
C     
      INTEGER    NEXTERNAL
      PARAMETER (NEXTERNAL=6)
      INTEGER                 NCOMB
      PARAMETER (             NCOMB=32)
CF2PY INTENT(OUT) :: ANS
CF2PY INTENT(IN) :: HEL
CF2PY INTENT(IN) :: P(0:3,NEXTERNAL)

C     
C     ARGUMENTS 
C     
      REAL*8 P(0:3,NEXTERNAL),ANS
      INTEGER HEL
C     
C     GLOBAL VARIABLES
C     
      INTEGER USERHEL
      COMMON/M2_HELUSERCHOICE/USERHEL
C     ----------
C     BEGIN CODE
C     ----------
      USERHEL=HEL
      CALL M2_SMATRIX(P,ANS)
      USERHEL=-1

      END

      SUBROUTINE M2_SMATRIX(P,ANS)
C     
C     Generated by MadGraph5_aMC@NLO v. 2.6.5, 2018-02-03
C     By the MadGraph5_aMC@NLO Development Team
C     Visit launchpad.net/madgraph5 and amcatnlo.web.cern.ch
C     
C     MadGraph5_aMC@NLO StandAlone Version
C     
C     Returns amplitude squared summed/avg over colors
C     and helicities
C     for the point in phase space P(0:3,NEXTERNAL)
C     
C     Process: u d~ > t b~ g h DIM6<=1 FCNC=0
C     Process: c s~ > t b~ g h DIM6<=1 FCNC=0
C     
      IMPLICIT NONE
C     
C     CONSTANTS
C     
      INTEGER    NEXTERNAL
      PARAMETER (NEXTERNAL=6)
      INTEGER    NINITIAL
      PARAMETER (NINITIAL=2)
      INTEGER NPOLENTRIES
      PARAMETER (NPOLENTRIES=(NEXTERNAL+1)*6)
      INTEGER                 NCOMB
      PARAMETER (             NCOMB=32)
      INTEGER HELAVGFACTOR
      PARAMETER (HELAVGFACTOR=4)
C     
C     ARGUMENTS 
C     
      REAL*8 P(0:3,NEXTERNAL),ANS
CF2PY INTENT(OUT) :: ANS
CF2PY INTENT(IN) :: P(0:3,NEXTERNAL)
C     
C     LOCAL VARIABLES 
C     
      INTEGER NHEL(NEXTERNAL,NCOMB),NTRY
C     put in common block to expose this variable to python interface
      COMMON/M2_PROCESS_NHEL/NHEL
      REAL*8 T
      REAL*8 M2_MATRIX
      INTEGER IHEL,IDEN, I, J
C     For a 1>N process, them BEAMTWO_HELAVGFACTOR would be set to 1.
      INTEGER BEAMS_HELAVGFACTOR(2)
      DATA (BEAMS_HELAVGFACTOR(I),I=1,2)/2,2/
      INTEGER JC(NEXTERNAL)
      LOGICAL GOODHEL(NCOMB)
      DATA NTRY/0/
      DATA GOODHEL/NCOMB*.FALSE./

C     
C     GLOBAL VARIABLES
C     
      INTEGER USERHEL
      COMMON/M2_HELUSERCHOICE/USERHEL
      DATA USERHEL/-1/

      DATA (NHEL(I,   1),I=1,6) / 1,-1,-1, 1,-1, 0/
      DATA (NHEL(I,   2),I=1,6) / 1,-1,-1, 1, 1, 0/
      DATA (NHEL(I,   3),I=1,6) / 1,-1,-1,-1,-1, 0/
      DATA (NHEL(I,   4),I=1,6) / 1,-1,-1,-1, 1, 0/
      DATA (NHEL(I,   5),I=1,6) / 1,-1, 1, 1,-1, 0/
      DATA (NHEL(I,   6),I=1,6) / 1,-1, 1, 1, 1, 0/
      DATA (NHEL(I,   7),I=1,6) / 1,-1, 1,-1,-1, 0/
      DATA (NHEL(I,   8),I=1,6) / 1,-1, 1,-1, 1, 0/
      DATA (NHEL(I,   9),I=1,6) / 1, 1,-1, 1,-1, 0/
      DATA (NHEL(I,  10),I=1,6) / 1, 1,-1, 1, 1, 0/
      DATA (NHEL(I,  11),I=1,6) / 1, 1,-1,-1,-1, 0/
      DATA (NHEL(I,  12),I=1,6) / 1, 1,-1,-1, 1, 0/
      DATA (NHEL(I,  13),I=1,6) / 1, 1, 1, 1,-1, 0/
      DATA (NHEL(I,  14),I=1,6) / 1, 1, 1, 1, 1, 0/
      DATA (NHEL(I,  15),I=1,6) / 1, 1, 1,-1,-1, 0/
      DATA (NHEL(I,  16),I=1,6) / 1, 1, 1,-1, 1, 0/
      DATA (NHEL(I,  17),I=1,6) /-1,-1,-1, 1,-1, 0/
      DATA (NHEL(I,  18),I=1,6) /-1,-1,-1, 1, 1, 0/
      DATA (NHEL(I,  19),I=1,6) /-1,-1,-1,-1,-1, 0/
      DATA (NHEL(I,  20),I=1,6) /-1,-1,-1,-1, 1, 0/
      DATA (NHEL(I,  21),I=1,6) /-1,-1, 1, 1,-1, 0/
      DATA (NHEL(I,  22),I=1,6) /-1,-1, 1, 1, 1, 0/
      DATA (NHEL(I,  23),I=1,6) /-1,-1, 1,-1,-1, 0/
      DATA (NHEL(I,  24),I=1,6) /-1,-1, 1,-1, 1, 0/
      DATA (NHEL(I,  25),I=1,6) /-1, 1,-1, 1,-1, 0/
      DATA (NHEL(I,  26),I=1,6) /-1, 1,-1, 1, 1, 0/
      DATA (NHEL(I,  27),I=1,6) /-1, 1,-1,-1,-1, 0/
      DATA (NHEL(I,  28),I=1,6) /-1, 1,-1,-1, 1, 0/
      DATA (NHEL(I,  29),I=1,6) /-1, 1, 1, 1,-1, 0/
      DATA (NHEL(I,  30),I=1,6) /-1, 1, 1, 1, 1, 0/
      DATA (NHEL(I,  31),I=1,6) /-1, 1, 1,-1,-1, 0/
      DATA (NHEL(I,  32),I=1,6) /-1, 1, 1,-1, 1, 0/
      DATA IDEN/36/

      INTEGER POLARIZATIONS(0:NEXTERNAL,0:5)
      COMMON/M2_BORN_BEAM_POL/POLARIZATIONS
      DATA ((POLARIZATIONS(I,J),I=0,NEXTERNAL),J=0,5)/NPOLENTRIES*-1/

C     
C     FUNCTIONS
C     
      LOGICAL M2_IS_BORN_HEL_SELECTED

C     ----------
C     BEGIN CODE
C     ----------
      IF(USERHEL.EQ.-1) NTRY=NTRY+1
      DO IHEL=1,NEXTERNAL
        JC(IHEL) = +1
      ENDDO
C     When spin-2 particles are involved, the Helicity filtering is
C      dangerous for the 2->1 topology.
C     This is because depending on the MC setup the initial PS points
C      have back-to-back initial states
C     for which some of the spin-2 helicity configurations are zero.
C      But they are no longer zero
C     if the point is boosted on the z-axis. Remember that HELAS
C      helicity amplitudes are no longer
C     lorentz invariant with expternal spin-2 particles (only the
C      helicity sum is).
C     For this reason, we simply remove the filterin when there is
C      only three external particles.
      IF (NEXTERNAL.LE.3) THEN
        DO IHEL=1,NCOMB
          GOODHEL(IHEL)=.TRUE.
        ENDDO
      ENDIF
      ANS = 0D0
      DO IHEL=1,NCOMB
        IF (USERHEL.EQ.-1.OR.USERHEL.EQ.IHEL) THEN
          IF (GOODHEL(IHEL) .OR. NTRY .LT. 20.OR.USERHEL.NE.-1) THEN
            IF(NTRY.GE.2.AND.POLARIZATIONS(0,0).NE.
     $       -1.AND.(.NOT.M2_IS_BORN_HEL_SELECTED(IHEL))) THEN
              CYCLE
            ENDIF
            T=M2_MATRIX(P ,NHEL(1,IHEL),JC(1))
            IF(POLARIZATIONS(0,0).EQ.-1.OR.M2_IS_BORN_HEL_SELECTED(IHEL)
     $       ) THEN
              ANS=ANS+T
            ENDIF
            IF (T .NE. 0D0 .AND. .NOT.    GOODHEL(IHEL)) THEN
              GOODHEL(IHEL)=.TRUE.
            ENDIF
          ENDIF
        ENDIF
      ENDDO
      ANS=ANS/DBLE(IDEN)
      IF(USERHEL.NE.-1) THEN
        ANS=ANS*HELAVGFACTOR
      ELSE
        DO J=1,NINITIAL
          IF (POLARIZATIONS(J,0).NE.-1) THEN
            ANS=ANS*BEAMS_HELAVGFACTOR(J)
            ANS=ANS/POLARIZATIONS(J,0)
          ENDIF
        ENDDO
      ENDIF
      END


      REAL*8 FUNCTION M2_MATRIX(P,NHEL,IC)
C     
C     Generated by MadGraph5_aMC@NLO v. 2.6.5, 2018-02-03
C     By the MadGraph5_aMC@NLO Development Team
C     Visit launchpad.net/madgraph5 and amcatnlo.web.cern.ch
C     
C     Returns amplitude squared summed/avg over colors
C     for the point with external lines W(0:6,NEXTERNAL)
C     
C     Process: u d~ > t b~ g h DIM6<=1 FCNC=0
C     Process: c s~ > t b~ g h DIM6<=1 FCNC=0
C     
      IMPLICIT NONE
C     
C     CONSTANTS
C     
      INTEGER    NGRAPHS
      PARAMETER (NGRAPHS=94)
      INTEGER    NEXTERNAL
      PARAMETER (NEXTERNAL=6)
      INTEGER    NWAVEFUNCS, NCOLOR
      PARAMETER (NWAVEFUNCS=21, NCOLOR=4)
      REAL*8     ZERO
      PARAMETER (ZERO=0D0)
      COMPLEX*16 IMAG1
      PARAMETER (IMAG1=(0D0,1D0))
C     
C     ARGUMENTS 
C     
      REAL*8 P(0:3,NEXTERNAL)
      INTEGER NHEL(NEXTERNAL), IC(NEXTERNAL)
C     
C     LOCAL VARIABLES 
C     
      INTEGER I,J
      COMPLEX*16 ZTEMP
      REAL*8 DENOM(NCOLOR), CF(NCOLOR,NCOLOR)
      COMPLEX*16 AMP(NGRAPHS), JAMP(NCOLOR)
      COMPLEX*16 W(20,NWAVEFUNCS)
      COMPLEX*16 DUM0,DUM1
      DATA DUM0, DUM1/(0D0, 0D0), (1D0, 0D0)/
C     
C     GLOBAL VARIABLES
C     
      INCLUDE 'coupl.inc'

C     
C     COLOR DATA
C     
      DATA DENOM(1)/1/
      DATA (CF(I,  1),I=  1,  4) /   12,    4,    4,    0/
C     1 T(2,1) T(5,3,4)
      DATA DENOM(2)/1/
      DATA (CF(I,  2),I=  1,  4) /    4,   12,    0,    4/
C     1 T(2,4) T(5,3,1)
      DATA DENOM(3)/1/
      DATA (CF(I,  3),I=  1,  4) /    4,    0,   12,    4/
C     1 T(3,1) T(5,2,4)
      DATA DENOM(4)/1/
      DATA (CF(I,  4),I=  1,  4) /    0,    4,    4,   12/
C     1 T(3,4) T(5,2,1)
C     ----------
C     BEGIN CODE
C     ----------
      CALL IXXXXX(P(0,1),ZERO,NHEL(1),+1*IC(1),W(1,1))
      CALL OXXXXX(P(0,2),ZERO,NHEL(2),-1*IC(2),W(1,2))
      CALL OXXXXX(P(0,3),MDL_MT,NHEL(3),+1*IC(3),W(1,3))
      CALL IXXXXX(P(0,4),MDL_MB,NHEL(4),-1*IC(4),W(1,4))
      CALL VXXXXX(P(0,5),ZERO,NHEL(5),+1*IC(5),W(1,5))
      CALL SXXXXX(P(0,6),+1*IC(6),W(1,6))
      CALL FFV1_2(W(1,1),W(1,5),GC_7,ZERO,ZERO,W(1,7))
      CALL FFV2_3(W(1,4),W(1,3),GC_649,MDL_MW,MDL_WW,W(1,8))
      CALL FFV2_3(W(1,7),W(1,2),GC_649,MDL_MW,MDL_WW,W(1,9))
C     Amplitude(s) for diagram number 1
      CALL VVS1_0(W(1,9),W(1,8),W(1,6),GC_730,AMP(1))
      CALL FFV4_3(W(1,4),W(1,3),GC_924,MDL_MW,MDL_WW,W(1,10))
C     Amplitude(s) for diagram number 2
      CALL VVS1_0(W(1,9),W(1,10),W(1,6),GC_730,AMP(2))
      CALL FFV10_3_3(W(1,4),W(1,3),GC_741,GC_768,MDL_MW,MDL_WW,W(1,11))
C     Amplitude(s) for diagram number 3
      CALL VVS1_0(W(1,9),W(1,11),W(1,6),GC_730,AMP(3))
      CALL FFV2_3(W(1,4),W(1,3),GC_740,MDL_MW,MDL_WW,W(1,12))
C     Amplitude(s) for diagram number 4
      CALL VVS1_0(W(1,9),W(1,12),W(1,6),GC_730,AMP(4))
      CALL FFS2_4_1(W(1,3),W(1,6),GC_739,GC_738,MDL_MT,MDL_WT,W(1,13))
C     Amplitude(s) for diagram number 5
      CALL FFV2_0(W(1,4),W(1,13),W(1,9),GC_649,AMP(5))
      CALL FFS4_1(W(1,3),W(1,6),GC_954,MDL_MT,MDL_WT,W(1,14))
C     Amplitude(s) for diagram number 6
      CALL FFFF10_11_19_2_20_6_7_8_21_110_0(W(1,7),W(1,2),W(1,4),W(1
     $ ,14),GC_41,GC_59,GC_45,GC_206,GC_61,GC_570,GC_204,GC_471,GC_201
     $ ,GC_62,AMP(6))
      CALL FFFF10_11_19_2_20_6_7_8_21_110_0(W(1,7),W(1,2),W(1,4),W(1
     $ ,14),GC_43,GC_67,GC_47,GC_214,GC_69,GC_572,GC_212,GC_473,GC_209
     $ ,GC_70,AMP(7))
C     Amplitude(s) for diagram number 7
      CALL FFV2_0(W(1,4),W(1,14),W(1,9),GC_649,AMP(8))
C     Amplitude(s) for diagram number 8
      CALL FFV4_0(W(1,4),W(1,14),W(1,9),GC_924,AMP(9))
C     Amplitude(s) for diagram number 9
      CALL FFV10_3_0(W(1,4),W(1,14),W(1,9),GC_741,GC_768,AMP(10))
C     Amplitude(s) for diagram number 10
      CALL FFV2_0(W(1,4),W(1,14),W(1,9),GC_740,AMP(11))
      CALL FFS4_2(W(1,4),W(1,6),GC_953,MDL_MB,ZERO,W(1,15))
C     Amplitude(s) for diagram number 11
      CALL FFFF10_11_19_2_20_6_7_8_21_110_0(W(1,7),W(1,2),W(1,15),W(1
     $ ,3),GC_41,GC_59,GC_45,GC_206,GC_61,GC_570,GC_204,GC_471,GC_201
     $ ,GC_62,AMP(12))
      CALL FFFF10_11_19_2_20_6_7_8_21_110_0(W(1,7),W(1,2),W(1,15),W(1
     $ ,3),GC_43,GC_67,GC_47,GC_214,GC_69,GC_572,GC_212,GC_473,GC_209
     $ ,GC_70,AMP(13))
C     Amplitude(s) for diagram number 12
      CALL FFV2_0(W(1,15),W(1,3),W(1,9),GC_649,AMP(14))
C     Amplitude(s) for diagram number 13
      CALL FFV4_0(W(1,15),W(1,3),W(1,9),GC_924,AMP(15))
C     Amplitude(s) for diagram number 14
      CALL FFV10_3_0(W(1,15),W(1,3),W(1,9),GC_741,GC_768,AMP(16))
C     Amplitude(s) for diagram number 15
      CALL FFV2_0(W(1,15),W(1,3),W(1,9),GC_740,AMP(17))
      CALL FFVS2_5_3(W(1,4),W(1,3),W(1,6),GC_476,GC_48,MDL_MW,MDL_WW
     $ ,W(1,9))
C     Amplitude(s) for diagram number 16
      CALL FFV2_0(W(1,7),W(1,2),W(1,9),GC_649,AMP(18))
      CALL FFVS1_3_3(W(1,4),W(1,3),W(1,6),GC_733,GC_828,MDL_MW,MDL_WW
     $ ,W(1,16))
C     Amplitude(s) for diagram number 17
      CALL FFV2_0(W(1,7),W(1,2),W(1,16),GC_649,AMP(19))
      CALL FFV6_1(W(1,3),W(1,5),GC_7,MDL_MT,MDL_WT,W(1,7))
      CALL FFV2_3(W(1,1),W(1,2),GC_649,MDL_MW,MDL_WW,W(1,17))
C     Amplitude(s) for diagram number 18
      CALL FFVS2_5_0(W(1,4),W(1,7),W(1,17),W(1,6),GC_476,GC_48,AMP(20))
C     Amplitude(s) for diagram number 19
      CALL FFVS1_3_0(W(1,4),W(1,7),W(1,17),W(1,6),GC_733,GC_828,AMP(21)
     $ )
      CALL FFV2_3(W(1,4),W(1,7),GC_649,MDL_MW,MDL_WW,W(1,18))
C     Amplitude(s) for diagram number 20
      CALL VVS1_0(W(1,17),W(1,18),W(1,6),GC_730,AMP(22))
      CALL FFV4_3(W(1,4),W(1,7),GC_924,MDL_MW,MDL_WW,W(1,18))
C     Amplitude(s) for diagram number 21
      CALL VVS1_0(W(1,17),W(1,18),W(1,6),GC_730,AMP(23))
      CALL FFV10_3_3(W(1,4),W(1,7),GC_741,GC_768,MDL_MW,MDL_WW,W(1,18))
C     Amplitude(s) for diagram number 22
      CALL VVS1_0(W(1,17),W(1,18),W(1,6),GC_730,AMP(24))
      CALL FFV2_3(W(1,4),W(1,7),GC_740,MDL_MW,MDL_WW,W(1,18))
C     Amplitude(s) for diagram number 23
      CALL VVS1_0(W(1,17),W(1,18),W(1,6),GC_730,AMP(25))
      CALL FFS2_4_1(W(1,7),W(1,6),GC_739,GC_738,MDL_MT,MDL_WT,W(1,18))
C     Amplitude(s) for diagram number 24
      CALL FFV2_0(W(1,4),W(1,18),W(1,17),GC_649,AMP(26))
      CALL FFS4_1(W(1,7),W(1,6),GC_954,MDL_MT,MDL_WT,W(1,18))
C     Amplitude(s) for diagram number 25
      CALL FFV2_0(W(1,4),W(1,18),W(1,17),GC_649,AMP(27))
C     Amplitude(s) for diagram number 26
      CALL FFV4_0(W(1,4),W(1,18),W(1,17),GC_924,AMP(28))
C     Amplitude(s) for diagram number 27
      CALL FFV10_3_0(W(1,4),W(1,18),W(1,17),GC_741,GC_768,AMP(29))
C     Amplitude(s) for diagram number 28
      CALL FFV2_0(W(1,4),W(1,18),W(1,17),GC_740,AMP(30))
      CALL FFV11_9_1(W(1,3),W(1,5),GC_725,GC_726,MDL_MT,MDL_WT,W(1,18))
      CALL FFV2_3(W(1,4),W(1,18),GC_649,MDL_MW,MDL_WW,W(1,19))
C     Amplitude(s) for diagram number 29
      CALL VVS1_0(W(1,17),W(1,19),W(1,6),GC_730,AMP(31))
      CALL FFS4_1(W(1,18),W(1,6),GC_954,MDL_MT,MDL_WT,W(1,19))
C     Amplitude(s) for diagram number 30
      CALL FFV2_0(W(1,4),W(1,19),W(1,17),GC_649,AMP(32))
C     Amplitude(s) for diagram number 31
      CALL FFV2_0(W(1,15),W(1,7),W(1,17),GC_649,AMP(33))
C     Amplitude(s) for diagram number 32
      CALL FFV4_0(W(1,15),W(1,7),W(1,17),GC_924,AMP(34))
C     Amplitude(s) for diagram number 33
      CALL FFV10_3_0(W(1,15),W(1,7),W(1,17),GC_741,GC_768,AMP(35))
C     Amplitude(s) for diagram number 34
      CALL FFV2_0(W(1,15),W(1,7),W(1,17),GC_740,AMP(36))
C     Amplitude(s) for diagram number 35
      CALL FFV2_0(W(1,15),W(1,18),W(1,17),GC_649,AMP(37))
C     Amplitude(s) for diagram number 36
      CALL FFFF10_11_19_2_20_6_7_8_21_110_0(W(1,1),W(1,2),W(1,15),W(1
     $ ,7),GC_41,GC_59,GC_45,GC_206,GC_61,GC_570,GC_204,GC_471,GC_201
     $ ,GC_62,AMP(38))
      CALL FFFF10_11_19_2_20_6_7_8_21_110_0(W(1,1),W(1,2),W(1,15),W(1
     $ ,7),GC_43,GC_67,GC_47,GC_214,GC_69,GC_572,GC_212,GC_473,GC_209
     $ ,GC_70,AMP(39))
      CALL FFFF10_11_19_2_20_6_7_8_21_110_4(W(1,1),W(1,2),W(1,4),GC_41
     $ ,GC_59,GC_45,GC_206,GC_61,GC_570,GC_204,GC_471,GC_201,GC_62
     $ ,MDL_MT,MDL_WT,W(1,18))
      CALL FFFF10_11_19_2_20_6_7_8_21_110_4(W(1,1),W(1,2),W(1,4),GC_43
     $ ,GC_67,GC_47,GC_214,GC_69,GC_572,GC_212,GC_473,GC_209,GC_70
     $ ,MDL_MT,MDL_WT,W(1,19))
C     Amplitude(s) for diagram number 37
      CALL FFS4_0(W(1,18),W(1,7),W(1,6),GC_954,AMP(40))
      CALL FFS4_0(W(1,19),W(1,7),W(1,6),GC_954,AMP(41))
      CALL FFV1_2(W(1,4),W(1,5),GC_7,MDL_MB,ZERO,W(1,7))
C     Amplitude(s) for diagram number 38
      CALL FFVS2_5_0(W(1,7),W(1,3),W(1,17),W(1,6),GC_476,GC_48,AMP(42))
C     Amplitude(s) for diagram number 39
      CALL FFVS1_3_0(W(1,7),W(1,3),W(1,17),W(1,6),GC_733,GC_828,AMP(43)
     $ )
      CALL FFV2_3(W(1,7),W(1,3),GC_649,MDL_MW,MDL_WW,W(1,20))
C     Amplitude(s) for diagram number 40
      CALL VVS1_0(W(1,17),W(1,20),W(1,6),GC_730,AMP(44))
      CALL FFV4_3(W(1,7),W(1,3),GC_924,MDL_MW,MDL_WW,W(1,20))
C     Amplitude(s) for diagram number 41
      CALL VVS1_0(W(1,17),W(1,20),W(1,6),GC_730,AMP(45))
      CALL FFV10_3_3(W(1,7),W(1,3),GC_741,GC_768,MDL_MW,MDL_WW,W(1,20))
C     Amplitude(s) for diagram number 42
      CALL VVS1_0(W(1,17),W(1,20),W(1,6),GC_730,AMP(46))
      CALL FFV2_3(W(1,7),W(1,3),GC_740,MDL_MW,MDL_WW,W(1,20))
C     Amplitude(s) for diagram number 43
      CALL VVS1_0(W(1,17),W(1,20),W(1,6),GC_730,AMP(47))
      CALL FFS4_2(W(1,7),W(1,6),GC_953,MDL_MB,ZERO,W(1,20))
C     Amplitude(s) for diagram number 44
      CALL FFV2_0(W(1,20),W(1,3),W(1,17),GC_649,AMP(48))
C     Amplitude(s) for diagram number 45
      CALL FFV4_0(W(1,20),W(1,3),W(1,17),GC_924,AMP(49))
C     Amplitude(s) for diagram number 46
      CALL FFV10_3_0(W(1,20),W(1,3),W(1,17),GC_741,GC_768,AMP(50))
C     Amplitude(s) for diagram number 47
      CALL FFV2_0(W(1,20),W(1,3),W(1,17),GC_740,AMP(51))
C     Amplitude(s) for diagram number 48
      CALL FFV2_0(W(1,7),W(1,13),W(1,17),GC_649,AMP(52))
C     Amplitude(s) for diagram number 49
      CALL FFV2_0(W(1,7),W(1,14),W(1,17),GC_649,AMP(53))
C     Amplitude(s) for diagram number 50
      CALL FFV4_0(W(1,7),W(1,14),W(1,17),GC_924,AMP(54))
C     Amplitude(s) for diagram number 51
      CALL FFV10_3_0(W(1,7),W(1,14),W(1,17),GC_741,GC_768,AMP(55))
C     Amplitude(s) for diagram number 52
      CALL FFV2_0(W(1,7),W(1,14),W(1,17),GC_740,AMP(56))
C     Amplitude(s) for diagram number 53
      CALL FFFF10_11_19_2_20_6_7_8_21_110_0(W(1,1),W(1,2),W(1,7),W(1
     $ ,14),GC_41,GC_59,GC_45,GC_206,GC_61,GC_570,GC_204,GC_471,GC_201
     $ ,GC_62,AMP(57))
      CALL FFFF10_11_19_2_20_6_7_8_21_110_0(W(1,1),W(1,2),W(1,7),W(1
     $ ,14),GC_43,GC_67,GC_47,GC_214,GC_69,GC_572,GC_212,GC_473,GC_209
     $ ,GC_70,AMP(58))
      CALL FFFF10_11_19_2_20_6_7_8_21_110_3(W(1,1),W(1,2),W(1,3),GC_41
     $ ,GC_59,GC_45,GC_206,GC_61,GC_570,GC_204,GC_471,GC_201,GC_62
     $ ,MDL_MB,ZERO,W(1,20))
      CALL FFFF10_11_19_2_20_6_7_8_21_110_3(W(1,1),W(1,2),W(1,3),GC_43
     $ ,GC_67,GC_47,GC_214,GC_69,GC_572,GC_212,GC_473,GC_209,GC_70
     $ ,MDL_MB,ZERO,W(1,21))
C     Amplitude(s) for diagram number 54
      CALL FFS4_0(W(1,7),W(1,20),W(1,6),GC_953,AMP(59))
      CALL FFS4_0(W(1,7),W(1,21),W(1,6),GC_953,AMP(60))
      CALL FFV1_1(W(1,2),W(1,5),GC_7,ZERO,ZERO,W(1,7))
      CALL FFV2_3(W(1,1),W(1,7),GC_649,MDL_MW,MDL_WW,W(1,2))
C     Amplitude(s) for diagram number 55
      CALL VVS1_0(W(1,2),W(1,8),W(1,6),GC_730,AMP(61))
C     Amplitude(s) for diagram number 56
      CALL VVS1_0(W(1,2),W(1,10),W(1,6),GC_730,AMP(62))
C     Amplitude(s) for diagram number 57
      CALL VVS1_0(W(1,2),W(1,11),W(1,6),GC_730,AMP(63))
C     Amplitude(s) for diagram number 58
      CALL VVS1_0(W(1,2),W(1,12),W(1,6),GC_730,AMP(64))
C     Amplitude(s) for diagram number 59
      CALL FFV2_0(W(1,4),W(1,13),W(1,2),GC_649,AMP(65))
C     Amplitude(s) for diagram number 60
      CALL FFFF10_11_19_2_20_6_7_8_21_110_0(W(1,1),W(1,7),W(1,4),W(1
     $ ,14),GC_41,GC_59,GC_45,GC_206,GC_61,GC_570,GC_204,GC_471,GC_201
     $ ,GC_62,AMP(66))
      CALL FFFF10_11_19_2_20_6_7_8_21_110_0(W(1,1),W(1,7),W(1,4),W(1
     $ ,14),GC_43,GC_67,GC_47,GC_214,GC_69,GC_572,GC_212,GC_473,GC_209
     $ ,GC_70,AMP(67))
C     Amplitude(s) for diagram number 61
      CALL FFV2_0(W(1,4),W(1,14),W(1,2),GC_649,AMP(68))
C     Amplitude(s) for diagram number 62
      CALL FFV4_0(W(1,4),W(1,14),W(1,2),GC_924,AMP(69))
C     Amplitude(s) for diagram number 63
      CALL FFV10_3_0(W(1,4),W(1,14),W(1,2),GC_741,GC_768,AMP(70))
C     Amplitude(s) for diagram number 64
      CALL FFV2_0(W(1,4),W(1,14),W(1,2),GC_740,AMP(71))
C     Amplitude(s) for diagram number 65
      CALL FFFF10_11_19_2_20_6_7_8_21_110_0(W(1,1),W(1,7),W(1,15),W(1
     $ ,3),GC_41,GC_59,GC_45,GC_206,GC_61,GC_570,GC_204,GC_471,GC_201
     $ ,GC_62,AMP(72))
      CALL FFFF10_11_19_2_20_6_7_8_21_110_0(W(1,1),W(1,7),W(1,15),W(1
     $ ,3),GC_43,GC_67,GC_47,GC_214,GC_69,GC_572,GC_212,GC_473,GC_209
     $ ,GC_70,AMP(73))
C     Amplitude(s) for diagram number 66
      CALL FFV2_0(W(1,15),W(1,3),W(1,2),GC_649,AMP(74))
C     Amplitude(s) for diagram number 67
      CALL FFV4_0(W(1,15),W(1,3),W(1,2),GC_924,AMP(75))
C     Amplitude(s) for diagram number 68
      CALL FFV10_3_0(W(1,15),W(1,3),W(1,2),GC_741,GC_768,AMP(76))
C     Amplitude(s) for diagram number 69
      CALL FFV2_0(W(1,15),W(1,3),W(1,2),GC_740,AMP(77))
C     Amplitude(s) for diagram number 70
      CALL FFV2_0(W(1,1),W(1,7),W(1,9),GC_649,AMP(78))
C     Amplitude(s) for diagram number 71
      CALL FFV2_0(W(1,1),W(1,7),W(1,16),GC_649,AMP(79))
      CALL FFV6_1(W(1,13),W(1,5),GC_7,MDL_MT,MDL_WT,W(1,7))
C     Amplitude(s) for diagram number 72
      CALL FFV2_0(W(1,4),W(1,7),W(1,17),GC_649,AMP(80))
      CALL FFV6_1(W(1,14),W(1,5),GC_7,MDL_MT,MDL_WT,W(1,7))
C     Amplitude(s) for diagram number 73
      CALL FFV2_0(W(1,4),W(1,7),W(1,17),GC_649,AMP(81))
C     Amplitude(s) for diagram number 74
      CALL FFV4_0(W(1,4),W(1,7),W(1,17),GC_924,AMP(82))
C     Amplitude(s) for diagram number 75
      CALL FFV10_3_0(W(1,4),W(1,7),W(1,17),GC_741,GC_768,AMP(83))
C     Amplitude(s) for diagram number 76
      CALL FFV2_0(W(1,4),W(1,7),W(1,17),GC_740,AMP(84))
      CALL FFV11_9_1(W(1,14),W(1,5),GC_725,GC_726,MDL_MT,MDL_WT,W(1,7))
C     Amplitude(s) for diagram number 77
      CALL FFV2_0(W(1,4),W(1,7),W(1,17),GC_649,AMP(85))
      CALL FFV1_2(W(1,15),W(1,5),GC_7,MDL_MB,ZERO,W(1,7))
C     Amplitude(s) for diagram number 78
      CALL FFV2_0(W(1,7),W(1,3),W(1,17),GC_649,AMP(86))
C     Amplitude(s) for diagram number 79
      CALL FFV4_0(W(1,7),W(1,3),W(1,17),GC_924,AMP(87))
C     Amplitude(s) for diagram number 80
      CALL FFV10_3_0(W(1,7),W(1,3),W(1,17),GC_741,GC_768,AMP(88))
C     Amplitude(s) for diagram number 81
      CALL FFV2_0(W(1,7),W(1,3),W(1,17),GC_740,AMP(89))
      CALL FFVS4_6_1(W(1,3),W(1,5),W(1,6),GC_599,GC_598,MDL_MT,MDL_WT
     $ ,W(1,7))
C     Amplitude(s) for diagram number 82
      CALL FFV2_0(W(1,4),W(1,7),W(1,17),GC_649,AMP(90))
C     Amplitude(s) for diagram number 83
      CALL FFV1_0(W(1,15),W(1,20),W(1,5),GC_7,AMP(91))
      CALL FFV1_0(W(1,15),W(1,21),W(1,5),GC_7,AMP(92))
C     Amplitude(s) for diagram number 84
      CALL FFV6_0(W(1,18),W(1,14),W(1,5),GC_7,AMP(93))
      CALL FFV6_0(W(1,19),W(1,14),W(1,5),GC_7,AMP(94))
      JAMP(1)=-AMP(20)-AMP(21)-AMP(22)-AMP(23)-AMP(24)-AMP(25)-AMP(26)
     $ -AMP(27)-AMP(28)-AMP(29)-AMP(30)-AMP(31)-AMP(32)-AMP(33)-AMP(34)
     $ -AMP(35)-AMP(36)-AMP(37)-AMP(38)+1D0/6D0*AMP(39)+1D0/6D0*AMP(41)
     $ -AMP(40)-AMP(42)-AMP(43)-AMP(44)-AMP(45)-AMP(46)-AMP(47)-AMP(48)
     $ -AMP(49)-AMP(50)-AMP(51)-AMP(52)-AMP(53)-AMP(54)-AMP(55)-AMP(56)
     $ -AMP(57)+1D0/6D0*AMP(58)+1D0/6D0*AMP(60)-AMP(59)-AMP(80)-AMP(81)
     $ -AMP(82)-AMP(83)-AMP(84)-AMP(85)-AMP(86)-AMP(87)-AMP(88)-AMP(89)
     $ -AMP(90)+1D0/6D0*AMP(92)-AMP(91)+1D0/6D0*AMP(94)-AMP(93)
      JAMP(2)=+1D0/2D0*(-AMP(7)-AMP(13)-AMP(39)-AMP(41)-AMP(94))
      JAMP(3)=+1D0/2D0*(-AMP(58)-AMP(60)-AMP(67)-AMP(73)-AMP(92))
      JAMP(4)=-AMP(1)-AMP(2)-AMP(3)-AMP(4)-AMP(5)-AMP(6)+1D0/6D0*AMP(7)
     $ -AMP(8)-AMP(9)-AMP(10)-AMP(11)-AMP(12)+1D0/6D0*AMP(13)-AMP(14)
     $ -AMP(15)-AMP(16)-AMP(17)-AMP(18)-AMP(19)-AMP(61)-AMP(62)-AMP(63)
     $ -AMP(64)-AMP(65)-AMP(66)+1D0/6D0*AMP(67)-AMP(68)-AMP(69)-AMP(70)
     $ -AMP(71)-AMP(72)+1D0/6D0*AMP(73)-AMP(74)-AMP(75)-AMP(76)-AMP(77)
     $ -AMP(78)-AMP(79)

      M2_MATRIX = 0.D0
      DO I = 1, NCOLOR
        ZTEMP = (0.D0,0.D0)
        DO J = 1, NCOLOR
          ZTEMP = ZTEMP + CF(J,I)*JAMP(J)
        ENDDO
        M2_MATRIX = M2_MATRIX+ZTEMP*DCONJG(JAMP(I))/DENOM(I)
      ENDDO

      END

      SUBROUTINE M2_GET_VALUE(P, ALPHAS, NHEL ,ANS)
      IMPLICIT NONE
C     
C     CONSTANT
C     
      INTEGER    NEXTERNAL
      PARAMETER (NEXTERNAL=6)
C     
C     ARGUMENTS 
C     
      REAL*8 P(0:3,NEXTERNAL),ANS
      INTEGER NHEL
      DOUBLE PRECISION ALPHAS
      REAL*8 PI
CF2PY INTENT(OUT) :: ANS
CF2PY INTENT(IN) :: NHEL
CF2PY INTENT(IN) :: P(0:3,NEXTERNAL)
CF2PY INTENT(IN) :: ALPHAS
C     ROUTINE FOR F2PY to read the benchmark point.    
C     the include file with the values of the parameters and masses 
      INCLUDE 'coupl.inc'

      PI = 3.141592653589793D0
      G = 2* DSQRT(ALPHAS*PI)
      CALL UPDATE_AS_PARAM()
      IF (NHEL.NE.0) THEN
        CALL M2_SMATRIXHEL(P, NHEL, ANS)
      ELSE
        CALL M2_SMATRIX(P, ANS)
      ENDIF
      RETURN
      END

      SUBROUTINE M2_INITIALISEMODEL(PATH)
C     ROUTINE FOR F2PY to read the benchmark point.    
      IMPLICIT NONE
      CHARACTER*512 PATH
CF2PY INTENT(IN) :: PATH
      CALL SETPARA(PATH)  !first call to setup the paramaters    
      RETURN
      END

      LOGICAL FUNCTION M2_IS_BORN_HEL_SELECTED(HELID)
      IMPLICIT NONE
C     
C     CONSTANTS
C     
      INTEGER    NEXTERNAL
      PARAMETER (NEXTERNAL=6)
      INTEGER    NCOMB
      PARAMETER (NCOMB=32)
C     
C     ARGUMENTS
C     
      INTEGER HELID
C     
C     LOCALS
C     
      INTEGER I,J
      LOGICAL FOUNDIT
C     
C     GLOBALS
C     
      INTEGER HELC(NEXTERNAL,NCOMB)
      COMMON/M2_PROCESS_NHEL/HELC

      INTEGER POLARIZATIONS(0:NEXTERNAL,0:5)
      COMMON/M2_BORN_BEAM_POL/POLARIZATIONS
C     ----------
C     BEGIN CODE
C     ----------

      M2_IS_BORN_HEL_SELECTED = .TRUE.
      IF (POLARIZATIONS(0,0).EQ.-1) THEN
        RETURN
      ENDIF

      DO I=1,NEXTERNAL
        IF (POLARIZATIONS(I,0).EQ.-1) THEN
          CYCLE
        ENDIF
        FOUNDIT = .FALSE.
        DO J=1,POLARIZATIONS(I,0)
          IF (HELC(I,HELID).EQ.POLARIZATIONS(I,J)) THEN
            FOUNDIT = .TRUE.
            EXIT
          ENDIF
        ENDDO
        IF(.NOT.FOUNDIT) THEN
          M2_IS_BORN_HEL_SELECTED = .FALSE.
          RETURN
        ENDIF
      ENDDO

      RETURN
      END

