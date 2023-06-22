      SUBROUTINE M6_SMATRIXHEL(P,HEL,ANS)
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
      COMMON/M6_HELUSERCHOICE/USERHEL
C     ----------
C     BEGIN CODE
C     ----------
      USERHEL=HEL
      CALL M6_SMATRIX(P,ANS)
      USERHEL=-1

      END

      SUBROUTINE M6_SMATRIX(P,ANS)
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
C     Process: g d > t t~ h d DIM6<=1 FCNC=0 @1
C     Process: g s > t t~ h s DIM6<=1 FCNC=0 @1
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
      COMMON/M6_PROCESS_NHEL/NHEL
      REAL*8 T
      REAL*8 M6_MATRIX
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
      COMMON/M6_HELUSERCHOICE/USERHEL
      DATA USERHEL/-1/

      DATA (NHEL(I,   1),I=1,6) /-1, 1,-1, 1, 0,-1/
      DATA (NHEL(I,   2),I=1,6) /-1, 1,-1, 1, 0, 1/
      DATA (NHEL(I,   3),I=1,6) /-1, 1,-1,-1, 0,-1/
      DATA (NHEL(I,   4),I=1,6) /-1, 1,-1,-1, 0, 1/
      DATA (NHEL(I,   5),I=1,6) /-1, 1, 1, 1, 0,-1/
      DATA (NHEL(I,   6),I=1,6) /-1, 1, 1, 1, 0, 1/
      DATA (NHEL(I,   7),I=1,6) /-1, 1, 1,-1, 0,-1/
      DATA (NHEL(I,   8),I=1,6) /-1, 1, 1,-1, 0, 1/
      DATA (NHEL(I,   9),I=1,6) /-1,-1,-1, 1, 0,-1/
      DATA (NHEL(I,  10),I=1,6) /-1,-1,-1, 1, 0, 1/
      DATA (NHEL(I,  11),I=1,6) /-1,-1,-1,-1, 0,-1/
      DATA (NHEL(I,  12),I=1,6) /-1,-1,-1,-1, 0, 1/
      DATA (NHEL(I,  13),I=1,6) /-1,-1, 1, 1, 0,-1/
      DATA (NHEL(I,  14),I=1,6) /-1,-1, 1, 1, 0, 1/
      DATA (NHEL(I,  15),I=1,6) /-1,-1, 1,-1, 0,-1/
      DATA (NHEL(I,  16),I=1,6) /-1,-1, 1,-1, 0, 1/
      DATA (NHEL(I,  17),I=1,6) / 1, 1,-1, 1, 0,-1/
      DATA (NHEL(I,  18),I=1,6) / 1, 1,-1, 1, 0, 1/
      DATA (NHEL(I,  19),I=1,6) / 1, 1,-1,-1, 0,-1/
      DATA (NHEL(I,  20),I=1,6) / 1, 1,-1,-1, 0, 1/
      DATA (NHEL(I,  21),I=1,6) / 1, 1, 1, 1, 0,-1/
      DATA (NHEL(I,  22),I=1,6) / 1, 1, 1, 1, 0, 1/
      DATA (NHEL(I,  23),I=1,6) / 1, 1, 1,-1, 0,-1/
      DATA (NHEL(I,  24),I=1,6) / 1, 1, 1,-1, 0, 1/
      DATA (NHEL(I,  25),I=1,6) / 1,-1,-1, 1, 0,-1/
      DATA (NHEL(I,  26),I=1,6) / 1,-1,-1, 1, 0, 1/
      DATA (NHEL(I,  27),I=1,6) / 1,-1,-1,-1, 0,-1/
      DATA (NHEL(I,  28),I=1,6) / 1,-1,-1,-1, 0, 1/
      DATA (NHEL(I,  29),I=1,6) / 1,-1, 1, 1, 0,-1/
      DATA (NHEL(I,  30),I=1,6) / 1,-1, 1, 1, 0, 1/
      DATA (NHEL(I,  31),I=1,6) / 1,-1, 1,-1, 0,-1/
      DATA (NHEL(I,  32),I=1,6) / 1,-1, 1,-1, 0, 1/
      DATA IDEN/96/

      INTEGER POLARIZATIONS(0:NEXTERNAL,0:5)
      COMMON/M6_BORN_BEAM_POL/POLARIZATIONS
      DATA ((POLARIZATIONS(I,J),I=0,NEXTERNAL),J=0,5)/NPOLENTRIES*-1/

C     
C     FUNCTIONS
C     
      LOGICAL M6_IS_BORN_HEL_SELECTED

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
     $       -1.AND.(.NOT.M6_IS_BORN_HEL_SELECTED(IHEL))) THEN
              CYCLE
            ENDIF
            T=M6_MATRIX(P ,NHEL(1,IHEL),JC(1))
            IF(POLARIZATIONS(0,0).EQ.-1.OR.M6_IS_BORN_HEL_SELECTED(IHEL)
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


      REAL*8 FUNCTION M6_MATRIX(P,NHEL,IC)
C     
C     Generated by MadGraph5_aMC@NLO v. 2.6.5, 2018-02-03
C     By the MadGraph5_aMC@NLO Development Team
C     Visit launchpad.net/madgraph5 and amcatnlo.web.cern.ch
C     
C     Returns amplitude squared summed/avg over colors
C     for the point with external lines W(0:6,NEXTERNAL)
C     
C     Process: g d > t t~ h d DIM6<=1 FCNC=0 @1
C     Process: g s > t t~ h s DIM6<=1 FCNC=0 @1
C     
      IMPLICIT NONE
C     
C     CONSTANTS
C     
      INTEGER    NGRAPHS
      PARAMETER (NGRAPHS=198)
      INTEGER    NEXTERNAL
      PARAMETER (NEXTERNAL=6)
      INTEGER    NWAVEFUNCS, NCOLOR
      PARAMETER (NWAVEFUNCS=27, NCOLOR=4)
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
C     1 T(1,3,2) T(6,4)
      DATA DENOM(2)/1/
      DATA (CF(I,  2),I=  1,  4) /    4,   12,    0,    4/
C     1 T(1,3,4) T(6,2)
      DATA DENOM(3)/1/
      DATA (CF(I,  3),I=  1,  4) /    4,    0,   12,    4/
C     1 T(1,6,2) T(3,4)
      DATA DENOM(4)/1/
      DATA (CF(I,  4),I=  1,  4) /    0,    4,    4,   12/
C     1 T(1,6,4) T(3,2)
C     ----------
C     BEGIN CODE
C     ----------
      CALL VXXXXX(P(0,1),ZERO,NHEL(1),-1*IC(1),W(1,1))
      CALL IXXXXX(P(0,2),ZERO,NHEL(2),+1*IC(2),W(1,2))
      CALL OXXXXX(P(0,3),MDL_MT,NHEL(3),+1*IC(3),W(1,3))
      CALL IXXXXX(P(0,4),MDL_MT,NHEL(4),-1*IC(4),W(1,4))
      CALL SXXXXX(P(0,5),+1*IC(5),W(1,5))
      CALL OXXXXX(P(0,6),ZERO,NHEL(6),+1*IC(6),W(1,6))
      CALL FFV1_2(W(1,2),W(1,1),GC_7,ZERO,ZERO,W(1,7))
      CALL FFV2_8_3(W(1,4),W(1,3),GC_651,GC_660,MDL_MZ,MDL_WZ,W(1,8))
      CALL FFV2_5_3(W(1,7),W(1,6),GC_650,GC_660,MDL_MZ,MDL_WZ,W(1,9))
C     Amplitude(s) for diagram number 1
      CALL VVS1_0(W(1,8),W(1,9),W(1,5),GC_910,AMP(1))
      CALL FFV11_9_3(W(1,4),W(1,3),GC_721,GC_722,MDL_MZ,MDL_WZ,W(1,10))
C     Amplitude(s) for diagram number 2
      CALL VVS1_0(W(1,10),W(1,9),W(1,5),GC_910,AMP(2))
      CALL FFV4_3(W(1,4),W(1,3),GC_948,MDL_MZ,MDL_WZ,W(1,11))
C     Amplitude(s) for diagram number 3
      CALL VVS1_0(W(1,11),W(1,9),W(1,5),GC_910,AMP(3))
      CALL FFV2_3(W(1,4),W(1,3),GC_938,MDL_MZ,MDL_WZ,W(1,12))
C     Amplitude(s) for diagram number 4
      CALL VVS1_0(W(1,12),W(1,9),W(1,5),GC_910,AMP(4))
      CALL FFS2_4_1(W(1,3),W(1,5),GC_739,GC_738,MDL_MT,MDL_WT,W(1,13))
      CALL FFV1P0_3(W(1,7),W(1,6),GC_1,ZERO,ZERO,W(1,14))
C     Amplitude(s) for diagram number 5
      CALL FFV6_0(W(1,4),W(1,13),W(1,14),GC_2,AMP(5))
      CALL FFV1P0_3(W(1,7),W(1,6),GC_7,ZERO,ZERO,W(1,15))
C     Amplitude(s) for diagram number 6
      CALL FFV6_0(W(1,4),W(1,13),W(1,15),GC_7,AMP(6))
C     Amplitude(s) for diagram number 7
      CALL FFV2_8_0(W(1,4),W(1,13),W(1,9),GC_651,GC_660,AMP(7))
      CALL FFS4_1(W(1,3),W(1,5),GC_954,MDL_MT,MDL_WT,W(1,16))
C     Amplitude(s) for diagram number 8
      CALL FFFF11_14_18_19_2_20_6_7_21_110_0(W(1,7),W(1,6),W(1,4),W(1
     $ ,16),GC_205,GC_559,GC_589,GC_579,GC_199,GC_203,GC_149,GC_201
     $ ,GC_204,GC_202,AMP(8))
      CALL FFFF11_14_18_19_2_20_6_7_21_110_0(W(1,7),W(1,6),W(1,4),W(1
     $ ,16),GC_213,GC_560,GC_590,GC_580,GC_207,GC_211,GC_177,GC_209
     $ ,GC_212,GC_210,AMP(9))
C     Amplitude(s) for diagram number 9
      CALL FFV6_0(W(1,4),W(1,16),W(1,14),GC_2,AMP(10))
C     Amplitude(s) for diagram number 10
      CALL FFV11_9_0(W(1,4),W(1,16),W(1,14),GC_813,GC_814,AMP(11))
C     Amplitude(s) for diagram number 11
      CALL FFV6_0(W(1,4),W(1,16),W(1,15),GC_7,AMP(12))
C     Amplitude(s) for diagram number 12
      CALL FFV11_9_0(W(1,4),W(1,16),W(1,15),GC_725,GC_726,AMP(13))
C     Amplitude(s) for diagram number 13
      CALL FFV2_8_0(W(1,4),W(1,16),W(1,9),GC_651,GC_660,AMP(14))
C     Amplitude(s) for diagram number 14
      CALL FFV11_9_0(W(1,4),W(1,16),W(1,9),GC_721,GC_722,AMP(15))
C     Amplitude(s) for diagram number 15
      CALL FFV4_0(W(1,4),W(1,16),W(1,9),GC_948,AMP(16))
C     Amplitude(s) for diagram number 16
      CALL FFV2_0(W(1,4),W(1,16),W(1,9),GC_938,AMP(17))
      CALL FFS2_4_2(W(1,4),W(1,5),GC_739,GC_738,MDL_MT,MDL_WT,W(1,17))
C     Amplitude(s) for diagram number 17
      CALL FFV6_0(W(1,17),W(1,3),W(1,14),GC_2,AMP(18))
C     Amplitude(s) for diagram number 18
      CALL FFV6_0(W(1,17),W(1,3),W(1,15),GC_7,AMP(19))
C     Amplitude(s) for diagram number 19
      CALL FFV2_8_0(W(1,17),W(1,3),W(1,9),GC_651,GC_660,AMP(20))
      CALL FFS4_2(W(1,4),W(1,5),GC_954,MDL_MT,MDL_WT,W(1,18))
C     Amplitude(s) for diagram number 20
      CALL FFFF11_14_18_19_2_20_6_7_21_110_0(W(1,7),W(1,6),W(1,18),W(1
     $ ,3),GC_205,GC_559,GC_589,GC_579,GC_199,GC_203,GC_149,GC_201
     $ ,GC_204,GC_202,AMP(21))
      CALL FFFF11_14_18_19_2_20_6_7_21_110_0(W(1,7),W(1,6),W(1,18),W(1
     $ ,3),GC_213,GC_560,GC_590,GC_580,GC_207,GC_211,GC_177,GC_209
     $ ,GC_212,GC_210,AMP(22))
C     Amplitude(s) for diagram number 21
      CALL FFV6_0(W(1,18),W(1,3),W(1,14),GC_2,AMP(23))
C     Amplitude(s) for diagram number 22
      CALL FFV11_9_0(W(1,18),W(1,3),W(1,14),GC_813,GC_814,AMP(24))
C     Amplitude(s) for diagram number 23
      CALL FFV6_0(W(1,18),W(1,3),W(1,15),GC_7,AMP(25))
C     Amplitude(s) for diagram number 24
      CALL FFV11_9_0(W(1,18),W(1,3),W(1,15),GC_725,GC_726,AMP(26))
C     Amplitude(s) for diagram number 25
      CALL FFV2_8_0(W(1,18),W(1,3),W(1,9),GC_651,GC_660,AMP(27))
C     Amplitude(s) for diagram number 26
      CALL FFV11_9_0(W(1,18),W(1,3),W(1,9),GC_721,GC_722,AMP(28))
C     Amplitude(s) for diagram number 27
      CALL FFV4_0(W(1,18),W(1,3),W(1,9),GC_948,AMP(29))
C     Amplitude(s) for diagram number 28
      CALL FFV2_0(W(1,18),W(1,3),W(1,9),GC_938,AMP(30))
      CALL FFVS4_6P0_3(W(1,4),W(1,3),W(1,5),GC_604,GC_603,ZERO,ZERO
     $ ,W(1,9))
C     Amplitude(s) for diagram number 29
      CALL FFV1_0(W(1,7),W(1,6),W(1,9),GC_1,AMP(31))
      CALL FFVS1_3_3(W(1,4),W(1,3),W(1,5),GC_894,GC_904,MDL_MZ,MDL_WZ
     $ ,W(1,15))
C     Amplitude(s) for diagram number 30
      CALL FFV2_5_0(W(1,7),W(1,6),W(1,15),GC_650,GC_660,AMP(32))
      CALL FFVS4_6_3(W(1,4),W(1,3),W(1,5),GC_595,GC_594,MDL_MZ,MDL_WZ
     $ ,W(1,14))
C     Amplitude(s) for diagram number 31
      CALL FFV2_5_0(W(1,7),W(1,6),W(1,14),GC_650,GC_660,AMP(33))
      CALL FFVS4_6P0_3(W(1,4),W(1,3),W(1,5),GC_599,GC_598,ZERO,ZERO
     $ ,W(1,19))
C     Amplitude(s) for diagram number 32
      CALL FFV1_0(W(1,7),W(1,6),W(1,19),GC_7,AMP(34))
      CALL FFV6_1(W(1,3),W(1,1),GC_7,MDL_MT,MDL_WT,W(1,7))
      CALL FFV1P0_3(W(1,2),W(1,6),GC_1,ZERO,ZERO,W(1,20))
C     Amplitude(s) for diagram number 33
      CALL FFVS4_6_0(W(1,4),W(1,7),W(1,20),W(1,5),GC_604,GC_603,AMP(35)
     $ )
      CALL FFS2_4_1(W(1,7),W(1,5),GC_739,GC_738,MDL_MT,MDL_WT,W(1,21))
C     Amplitude(s) for diagram number 34
      CALL FFV6_0(W(1,4),W(1,21),W(1,20),GC_2,AMP(36))
      CALL FFS4_1(W(1,7),W(1,5),GC_954,MDL_MT,MDL_WT,W(1,22))
C     Amplitude(s) for diagram number 35
      CALL FFV6_0(W(1,4),W(1,22),W(1,20),GC_2,AMP(37))
C     Amplitude(s) for diagram number 36
      CALL FFV11_9_0(W(1,4),W(1,22),W(1,20),GC_813,GC_814,AMP(38))
      CALL FFV1P0_3(W(1,2),W(1,6),GC_7,ZERO,ZERO,W(1,23))
C     Amplitude(s) for diagram number 37
      CALL FFVS4_6_0(W(1,4),W(1,7),W(1,23),W(1,5),GC_599,GC_598,AMP(39)
     $ )
C     Amplitude(s) for diagram number 38
      CALL FFV6_0(W(1,4),W(1,21),W(1,23),GC_7,AMP(40))
C     Amplitude(s) for diagram number 39
      CALL FFV6_0(W(1,4),W(1,22),W(1,23),GC_7,AMP(41))
C     Amplitude(s) for diagram number 40
      CALL FFV11_9_0(W(1,4),W(1,22),W(1,23),GC_725,GC_726,AMP(42))
      CALL FFV2_5_3(W(1,2),W(1,6),GC_650,GC_660,MDL_MZ,MDL_WZ,W(1,24))
C     Amplitude(s) for diagram number 41
      CALL FFVS1_3_0(W(1,4),W(1,7),W(1,24),W(1,5),GC_894,GC_904,AMP(43)
     $ )
C     Amplitude(s) for diagram number 42
      CALL FFVS4_6_0(W(1,4),W(1,7),W(1,24),W(1,5),GC_595,GC_594,AMP(44)
     $ )
      CALL FFV2_8_3(W(1,4),W(1,7),GC_651,GC_660,MDL_MZ,MDL_WZ,W(1,25))
C     Amplitude(s) for diagram number 43
      CALL VVS1_0(W(1,24),W(1,25),W(1,5),GC_910,AMP(45))
      CALL FFV11_9_3(W(1,4),W(1,7),GC_721,GC_722,MDL_MZ,MDL_WZ,W(1,25))
C     Amplitude(s) for diagram number 44
      CALL VVS1_0(W(1,24),W(1,25),W(1,5),GC_910,AMP(46))
      CALL FFV4_3(W(1,4),W(1,7),GC_948,MDL_MZ,MDL_WZ,W(1,25))
C     Amplitude(s) for diagram number 45
      CALL VVS1_0(W(1,24),W(1,25),W(1,5),GC_910,AMP(47))
      CALL FFV2_3(W(1,4),W(1,7),GC_938,MDL_MZ,MDL_WZ,W(1,25))
C     Amplitude(s) for diagram number 46
      CALL VVS1_0(W(1,24),W(1,25),W(1,5),GC_910,AMP(48))
C     Amplitude(s) for diagram number 47
      CALL FFV2_8_0(W(1,4),W(1,21),W(1,24),GC_651,GC_660,AMP(49))
C     Amplitude(s) for diagram number 48
      CALL FFV2_8_0(W(1,4),W(1,22),W(1,24),GC_651,GC_660,AMP(50))
C     Amplitude(s) for diagram number 49
      CALL FFV11_9_0(W(1,4),W(1,22),W(1,24),GC_721,GC_722,AMP(51))
C     Amplitude(s) for diagram number 50
      CALL FFV4_0(W(1,4),W(1,22),W(1,24),GC_948,AMP(52))
C     Amplitude(s) for diagram number 51
      CALL FFV2_0(W(1,4),W(1,22),W(1,24),GC_938,AMP(53))
      CALL FFV11_9_1(W(1,3),W(1,1),GC_725,GC_726,MDL_MT,MDL_WT,W(1,22))
      CALL FFS4_1(W(1,22),W(1,5),GC_954,MDL_MT,MDL_WT,W(1,21))
C     Amplitude(s) for diagram number 52
      CALL FFV6_0(W(1,4),W(1,21),W(1,20),GC_2,AMP(54))
C     Amplitude(s) for diagram number 53
      CALL FFV6_0(W(1,4),W(1,21),W(1,23),GC_7,AMP(55))
      CALL FFV2_8_3(W(1,4),W(1,22),GC_651,GC_660,MDL_MZ,MDL_WZ,W(1,25))
C     Amplitude(s) for diagram number 54
      CALL VVS1_0(W(1,24),W(1,25),W(1,5),GC_910,AMP(56))
C     Amplitude(s) for diagram number 55
      CALL FFV2_8_0(W(1,4),W(1,21),W(1,24),GC_651,GC_660,AMP(57))
C     Amplitude(s) for diagram number 56
      CALL FFV6_0(W(1,17),W(1,7),W(1,20),GC_2,AMP(58))
C     Amplitude(s) for diagram number 57
      CALL FFV6_0(W(1,18),W(1,7),W(1,20),GC_2,AMP(59))
C     Amplitude(s) for diagram number 58
      CALL FFV11_9_0(W(1,18),W(1,7),W(1,20),GC_813,GC_814,AMP(60))
C     Amplitude(s) for diagram number 59
      CALL FFV6_0(W(1,17),W(1,7),W(1,23),GC_7,AMP(61))
C     Amplitude(s) for diagram number 60
      CALL FFV6_0(W(1,18),W(1,7),W(1,23),GC_7,AMP(62))
C     Amplitude(s) for diagram number 61
      CALL FFV11_9_0(W(1,18),W(1,7),W(1,23),GC_725,GC_726,AMP(63))
C     Amplitude(s) for diagram number 62
      CALL FFV2_8_0(W(1,17),W(1,7),W(1,24),GC_651,GC_660,AMP(64))
C     Amplitude(s) for diagram number 63
      CALL FFV2_8_0(W(1,18),W(1,7),W(1,24),GC_651,GC_660,AMP(65))
C     Amplitude(s) for diagram number 64
      CALL FFV11_9_0(W(1,18),W(1,7),W(1,24),GC_721,GC_722,AMP(66))
C     Amplitude(s) for diagram number 65
      CALL FFV4_0(W(1,18),W(1,7),W(1,24),GC_948,AMP(67))
C     Amplitude(s) for diagram number 66
      CALL FFV2_0(W(1,18),W(1,7),W(1,24),GC_938,AMP(68))
C     Amplitude(s) for diagram number 67
      CALL FFV6_0(W(1,18),W(1,22),W(1,20),GC_2,AMP(69))
C     Amplitude(s) for diagram number 68
      CALL FFV6_0(W(1,18),W(1,22),W(1,23),GC_7,AMP(70))
C     Amplitude(s) for diagram number 69
      CALL FFV2_8_0(W(1,18),W(1,22),W(1,24),GC_651,GC_660,AMP(71))
C     Amplitude(s) for diagram number 70
      CALL FFFF11_14_18_19_2_20_6_7_21_110_0(W(1,2),W(1,6),W(1,18),W(1
     $ ,7),GC_205,GC_559,GC_589,GC_579,GC_199,GC_203,GC_149,GC_201
     $ ,GC_204,GC_202,AMP(72))
      CALL FFFF11_14_18_19_2_20_6_7_21_110_0(W(1,2),W(1,6),W(1,18),W(1
     $ ,7),GC_213,GC_560,GC_590,GC_580,GC_207,GC_211,GC_177,GC_209
     $ ,GC_212,GC_210,AMP(73))
      CALL FFFF11_14_18_19_2_20_6_7_21_110_4(W(1,2),W(1,6),W(1,4)
     $ ,GC_205,GC_559,GC_589,GC_579,GC_199,GC_203,GC_149,GC_201,GC_204
     $ ,GC_202,MDL_MT,MDL_WT,W(1,22))
      CALL FFFF11_14_18_19_2_20_6_7_21_110_4(W(1,2),W(1,6),W(1,4)
     $ ,GC_213,GC_560,GC_590,GC_580,GC_207,GC_211,GC_177,GC_209,GC_212
     $ ,GC_210,MDL_MT,MDL_WT,W(1,21))
C     Amplitude(s) for diagram number 71
      CALL FFS4_0(W(1,22),W(1,7),W(1,5),GC_954,AMP(74))
      CALL FFS4_0(W(1,21),W(1,7),W(1,5),GC_954,AMP(75))
      CALL FFV6_2(W(1,4),W(1,1),GC_7,MDL_MT,MDL_WT,W(1,7))
C     Amplitude(s) for diagram number 72
      CALL FFVS4_6_0(W(1,7),W(1,3),W(1,20),W(1,5),GC_604,GC_603,AMP(76)
     $ )
      CALL FFS2_4_2(W(1,7),W(1,5),GC_739,GC_738,MDL_MT,MDL_WT,W(1,25))
C     Amplitude(s) for diagram number 73
      CALL FFV6_0(W(1,25),W(1,3),W(1,20),GC_2,AMP(77))
      CALL FFS4_2(W(1,7),W(1,5),GC_954,MDL_MT,MDL_WT,W(1,26))
C     Amplitude(s) for diagram number 74
      CALL FFV6_0(W(1,26),W(1,3),W(1,20),GC_2,AMP(78))
C     Amplitude(s) for diagram number 75
      CALL FFV11_9_0(W(1,26),W(1,3),W(1,20),GC_813,GC_814,AMP(79))
C     Amplitude(s) for diagram number 76
      CALL FFVS4_6_0(W(1,7),W(1,3),W(1,23),W(1,5),GC_599,GC_598,AMP(80)
     $ )
C     Amplitude(s) for diagram number 77
      CALL FFV6_0(W(1,25),W(1,3),W(1,23),GC_7,AMP(81))
C     Amplitude(s) for diagram number 78
      CALL FFV6_0(W(1,26),W(1,3),W(1,23),GC_7,AMP(82))
C     Amplitude(s) for diagram number 79
      CALL FFV11_9_0(W(1,26),W(1,3),W(1,23),GC_725,GC_726,AMP(83))
C     Amplitude(s) for diagram number 80
      CALL FFVS1_3_0(W(1,7),W(1,3),W(1,24),W(1,5),GC_894,GC_904,AMP(84)
     $ )
C     Amplitude(s) for diagram number 81
      CALL FFVS4_6_0(W(1,7),W(1,3),W(1,24),W(1,5),GC_595,GC_594,AMP(85)
     $ )
      CALL FFV2_8_3(W(1,7),W(1,3),GC_651,GC_660,MDL_MZ,MDL_WZ,W(1,27))
C     Amplitude(s) for diagram number 82
      CALL VVS1_0(W(1,24),W(1,27),W(1,5),GC_910,AMP(86))
      CALL FFV11_9_3(W(1,7),W(1,3),GC_721,GC_722,MDL_MZ,MDL_WZ,W(1,27))
C     Amplitude(s) for diagram number 83
      CALL VVS1_0(W(1,24),W(1,27),W(1,5),GC_910,AMP(87))
      CALL FFV4_3(W(1,7),W(1,3),GC_948,MDL_MZ,MDL_WZ,W(1,27))
C     Amplitude(s) for diagram number 84
      CALL VVS1_0(W(1,24),W(1,27),W(1,5),GC_910,AMP(88))
      CALL FFV2_3(W(1,7),W(1,3),GC_938,MDL_MZ,MDL_WZ,W(1,27))
C     Amplitude(s) for diagram number 85
      CALL VVS1_0(W(1,24),W(1,27),W(1,5),GC_910,AMP(89))
C     Amplitude(s) for diagram number 86
      CALL FFV2_8_0(W(1,25),W(1,3),W(1,24),GC_651,GC_660,AMP(90))
C     Amplitude(s) for diagram number 87
      CALL FFV2_8_0(W(1,26),W(1,3),W(1,24),GC_651,GC_660,AMP(91))
C     Amplitude(s) for diagram number 88
      CALL FFV11_9_0(W(1,26),W(1,3),W(1,24),GC_721,GC_722,AMP(92))
C     Amplitude(s) for diagram number 89
      CALL FFV4_0(W(1,26),W(1,3),W(1,24),GC_948,AMP(93))
C     Amplitude(s) for diagram number 90
      CALL FFV2_0(W(1,26),W(1,3),W(1,24),GC_938,AMP(94))
      CALL FFV11_9_2(W(1,4),W(1,1),GC_725,GC_726,MDL_MT,MDL_WT,W(1,26))
      CALL FFS4_2(W(1,26),W(1,5),GC_954,MDL_MT,MDL_WT,W(1,25))
C     Amplitude(s) for diagram number 91
      CALL FFV6_0(W(1,25),W(1,3),W(1,20),GC_2,AMP(95))
C     Amplitude(s) for diagram number 92
      CALL FFV6_0(W(1,25),W(1,3),W(1,23),GC_7,AMP(96))
      CALL FFV2_8_3(W(1,26),W(1,3),GC_651,GC_660,MDL_MZ,MDL_WZ,W(1,27))
C     Amplitude(s) for diagram number 93
      CALL VVS1_0(W(1,24),W(1,27),W(1,5),GC_910,AMP(97))
C     Amplitude(s) for diagram number 94
      CALL FFV2_8_0(W(1,25),W(1,3),W(1,24),GC_651,GC_660,AMP(98))
C     Amplitude(s) for diagram number 95
      CALL FFV6_0(W(1,7),W(1,13),W(1,20),GC_2,AMP(99))
C     Amplitude(s) for diagram number 96
      CALL FFV6_0(W(1,7),W(1,16),W(1,20),GC_2,AMP(100))
C     Amplitude(s) for diagram number 97
      CALL FFV11_9_0(W(1,7),W(1,16),W(1,20),GC_813,GC_814,AMP(101))
C     Amplitude(s) for diagram number 98
      CALL FFV6_0(W(1,7),W(1,13),W(1,23),GC_7,AMP(102))
C     Amplitude(s) for diagram number 99
      CALL FFV6_0(W(1,7),W(1,16),W(1,23),GC_7,AMP(103))
C     Amplitude(s) for diagram number 100
      CALL FFV11_9_0(W(1,7),W(1,16),W(1,23),GC_725,GC_726,AMP(104))
C     Amplitude(s) for diagram number 101
      CALL FFV2_8_0(W(1,7),W(1,13),W(1,24),GC_651,GC_660,AMP(105))
C     Amplitude(s) for diagram number 102
      CALL FFV2_8_0(W(1,7),W(1,16),W(1,24),GC_651,GC_660,AMP(106))
C     Amplitude(s) for diagram number 103
      CALL FFV11_9_0(W(1,7),W(1,16),W(1,24),GC_721,GC_722,AMP(107))
C     Amplitude(s) for diagram number 104
      CALL FFV4_0(W(1,7),W(1,16),W(1,24),GC_948,AMP(108))
C     Amplitude(s) for diagram number 105
      CALL FFV2_0(W(1,7),W(1,16),W(1,24),GC_938,AMP(109))
C     Amplitude(s) for diagram number 106
      CALL FFV6_0(W(1,26),W(1,16),W(1,20),GC_2,AMP(110))
C     Amplitude(s) for diagram number 107
      CALL FFV6_0(W(1,26),W(1,16),W(1,23),GC_7,AMP(111))
C     Amplitude(s) for diagram number 108
      CALL FFV2_8_0(W(1,26),W(1,16),W(1,24),GC_651,GC_660,AMP(112))
C     Amplitude(s) for diagram number 109
      CALL FFFF11_14_18_19_2_20_6_7_21_110_0(W(1,2),W(1,6),W(1,7),W(1
     $ ,16),GC_205,GC_559,GC_589,GC_579,GC_199,GC_203,GC_149,GC_201
     $ ,GC_204,GC_202,AMP(113))
      CALL FFFF11_14_18_19_2_20_6_7_21_110_0(W(1,2),W(1,6),W(1,7),W(1
     $ ,16),GC_213,GC_560,GC_590,GC_580,GC_207,GC_211,GC_177,GC_209
     $ ,GC_212,GC_210,AMP(114))
      CALL FFFF11_14_18_19_2_20_6_7_21_110_3(W(1,2),W(1,6),W(1,3)
     $ ,GC_205,GC_559,GC_589,GC_579,GC_199,GC_203,GC_149,GC_201,GC_204
     $ ,GC_202,MDL_MT,MDL_WT,W(1,26))
      CALL FFFF11_14_18_19_2_20_6_7_21_110_3(W(1,2),W(1,6),W(1,3)
     $ ,GC_213,GC_560,GC_590,GC_580,GC_207,GC_211,GC_177,GC_209,GC_212
     $ ,GC_210,MDL_MT,MDL_WT,W(1,25))
C     Amplitude(s) for diagram number 110
      CALL FFS4_0(W(1,7),W(1,26),W(1,5),GC_954,AMP(115))
      CALL FFS4_0(W(1,7),W(1,25),W(1,5),GC_954,AMP(116))
      CALL FFV1_1(W(1,6),W(1,1),GC_7,ZERO,ZERO,W(1,7))
      CALL FFV2_5_3(W(1,2),W(1,7),GC_650,GC_660,MDL_MZ,MDL_WZ,W(1,27))
C     Amplitude(s) for diagram number 111
      CALL VVS1_0(W(1,8),W(1,27),W(1,5),GC_910,AMP(117))
C     Amplitude(s) for diagram number 112
      CALL VVS1_0(W(1,10),W(1,27),W(1,5),GC_910,AMP(118))
C     Amplitude(s) for diagram number 113
      CALL VVS1_0(W(1,11),W(1,27),W(1,5),GC_910,AMP(119))
C     Amplitude(s) for diagram number 114
      CALL VVS1_0(W(1,12),W(1,27),W(1,5),GC_910,AMP(120))
      CALL FFV1P0_3(W(1,2),W(1,7),GC_1,ZERO,ZERO,W(1,12))
C     Amplitude(s) for diagram number 115
      CALL FFV6_0(W(1,4),W(1,13),W(1,12),GC_2,AMP(121))
      CALL FFV1P0_3(W(1,2),W(1,7),GC_7,ZERO,ZERO,W(1,11))
C     Amplitude(s) for diagram number 116
      CALL FFV6_0(W(1,4),W(1,13),W(1,11),GC_7,AMP(122))
C     Amplitude(s) for diagram number 117
      CALL FFV2_8_0(W(1,4),W(1,13),W(1,27),GC_651,GC_660,AMP(123))
C     Amplitude(s) for diagram number 118
      CALL FFFF11_14_18_19_2_20_6_7_21_110_0(W(1,2),W(1,7),W(1,4),W(1
     $ ,16),GC_205,GC_559,GC_589,GC_579,GC_199,GC_203,GC_149,GC_201
     $ ,GC_204,GC_202,AMP(124))
      CALL FFFF11_14_18_19_2_20_6_7_21_110_0(W(1,2),W(1,7),W(1,4),W(1
     $ ,16),GC_213,GC_560,GC_590,GC_580,GC_207,GC_211,GC_177,GC_209
     $ ,GC_212,GC_210,AMP(125))
C     Amplitude(s) for diagram number 119
      CALL FFV6_0(W(1,4),W(1,16),W(1,12),GC_2,AMP(126))
C     Amplitude(s) for diagram number 120
      CALL FFV11_9_0(W(1,4),W(1,16),W(1,12),GC_813,GC_814,AMP(127))
C     Amplitude(s) for diagram number 121
      CALL FFV6_0(W(1,4),W(1,16),W(1,11),GC_7,AMP(128))
C     Amplitude(s) for diagram number 122
      CALL FFV11_9_0(W(1,4),W(1,16),W(1,11),GC_725,GC_726,AMP(129))
C     Amplitude(s) for diagram number 123
      CALL FFV2_8_0(W(1,4),W(1,16),W(1,27),GC_651,GC_660,AMP(130))
C     Amplitude(s) for diagram number 124
      CALL FFV11_9_0(W(1,4),W(1,16),W(1,27),GC_721,GC_722,AMP(131))
C     Amplitude(s) for diagram number 125
      CALL FFV4_0(W(1,4),W(1,16),W(1,27),GC_948,AMP(132))
C     Amplitude(s) for diagram number 126
      CALL FFV2_0(W(1,4),W(1,16),W(1,27),GC_938,AMP(133))
C     Amplitude(s) for diagram number 127
      CALL FFV6_0(W(1,17),W(1,3),W(1,12),GC_2,AMP(134))
C     Amplitude(s) for diagram number 128
      CALL FFV6_0(W(1,17),W(1,3),W(1,11),GC_7,AMP(135))
C     Amplitude(s) for diagram number 129
      CALL FFV2_8_0(W(1,17),W(1,3),W(1,27),GC_651,GC_660,AMP(136))
C     Amplitude(s) for diagram number 130
      CALL FFFF11_14_18_19_2_20_6_7_21_110_0(W(1,2),W(1,7),W(1,18),W(1
     $ ,3),GC_205,GC_559,GC_589,GC_579,GC_199,GC_203,GC_149,GC_201
     $ ,GC_204,GC_202,AMP(137))
      CALL FFFF11_14_18_19_2_20_6_7_21_110_0(W(1,2),W(1,7),W(1,18),W(1
     $ ,3),GC_213,GC_560,GC_590,GC_580,GC_207,GC_211,GC_177,GC_209
     $ ,GC_212,GC_210,AMP(138))
C     Amplitude(s) for diagram number 131
      CALL FFV6_0(W(1,18),W(1,3),W(1,12),GC_2,AMP(139))
C     Amplitude(s) for diagram number 132
      CALL FFV11_9_0(W(1,18),W(1,3),W(1,12),GC_813,GC_814,AMP(140))
C     Amplitude(s) for diagram number 133
      CALL FFV6_0(W(1,18),W(1,3),W(1,11),GC_7,AMP(141))
C     Amplitude(s) for diagram number 134
      CALL FFV11_9_0(W(1,18),W(1,3),W(1,11),GC_725,GC_726,AMP(142))
C     Amplitude(s) for diagram number 135
      CALL FFV2_8_0(W(1,18),W(1,3),W(1,27),GC_651,GC_660,AMP(143))
C     Amplitude(s) for diagram number 136
      CALL FFV11_9_0(W(1,18),W(1,3),W(1,27),GC_721,GC_722,AMP(144))
C     Amplitude(s) for diagram number 137
      CALL FFV4_0(W(1,18),W(1,3),W(1,27),GC_948,AMP(145))
C     Amplitude(s) for diagram number 138
      CALL FFV2_0(W(1,18),W(1,3),W(1,27),GC_938,AMP(146))
C     Amplitude(s) for diagram number 139
      CALL FFV1_0(W(1,2),W(1,7),W(1,9),GC_1,AMP(147))
C     Amplitude(s) for diagram number 140
      CALL FFV2_5_0(W(1,2),W(1,7),W(1,15),GC_650,GC_660,AMP(148))
C     Amplitude(s) for diagram number 141
      CALL FFV2_5_0(W(1,2),W(1,7),W(1,14),GC_650,GC_660,AMP(149))
C     Amplitude(s) for diagram number 142
      CALL FFV1_0(W(1,2),W(1,7),W(1,19),GC_7,AMP(150))
      CALL FFV6_1(W(1,13),W(1,1),GC_7,MDL_MT,MDL_WT,W(1,7))
C     Amplitude(s) for diagram number 143
      CALL FFV6_0(W(1,4),W(1,7),W(1,20),GC_2,AMP(151))
      CALL FFV6_1(W(1,16),W(1,1),GC_7,MDL_MT,MDL_WT,W(1,14))
C     Amplitude(s) for diagram number 144
      CALL FFV6_0(W(1,4),W(1,14),W(1,20),GC_2,AMP(152))
C     Amplitude(s) for diagram number 145
      CALL FFV11_9_0(W(1,4),W(1,14),W(1,20),GC_813,GC_814,AMP(153))
      CALL FFV11_9_1(W(1,16),W(1,1),GC_725,GC_726,MDL_MT,MDL_WT,W(1,15)
     $ )
C     Amplitude(s) for diagram number 146
      CALL FFV6_0(W(1,4),W(1,15),W(1,20),GC_2,AMP(154))
      CALL VVV1P0_1(W(1,1),W(1,23),GC_6,ZERO,ZERO,W(1,9))
C     Amplitude(s) for diagram number 147
      CALL FFV6_0(W(1,4),W(1,13),W(1,9),GC_7,AMP(155))
C     Amplitude(s) for diagram number 148
      CALL FFV6_0(W(1,4),W(1,7),W(1,23),GC_7,AMP(156))
C     Amplitude(s) for diagram number 149
      CALL FFVV2_4_0(W(1,4),W(1,16),W(1,1),W(1,23),GC_728,GC_727
     $ ,AMP(157))
C     Amplitude(s) for diagram number 150
      CALL FFV6_0(W(1,4),W(1,16),W(1,9),GC_7,AMP(158))
C     Amplitude(s) for diagram number 151
      CALL FFV11_9_0(W(1,4),W(1,16),W(1,9),GC_725,GC_726,AMP(159))
C     Amplitude(s) for diagram number 152
      CALL FFV6_0(W(1,4),W(1,14),W(1,23),GC_7,AMP(160))
C     Amplitude(s) for diagram number 153
      CALL FFV11_9_0(W(1,4),W(1,14),W(1,23),GC_725,GC_726,AMP(161))
C     Amplitude(s) for diagram number 154
      CALL FFV6_0(W(1,4),W(1,15),W(1,23),GC_7,AMP(162))
C     Amplitude(s) for diagram number 155
      CALL FFV2_8_0(W(1,4),W(1,7),W(1,24),GC_651,GC_660,AMP(163))
C     Amplitude(s) for diagram number 156
      CALL FFV2_8_0(W(1,4),W(1,14),W(1,24),GC_651,GC_660,AMP(164))
C     Amplitude(s) for diagram number 157
      CALL FFV11_9_0(W(1,4),W(1,14),W(1,24),GC_721,GC_722,AMP(165))
C     Amplitude(s) for diagram number 158
      CALL FFV4_0(W(1,4),W(1,14),W(1,24),GC_948,AMP(166))
C     Amplitude(s) for diagram number 159
      CALL FFV2_0(W(1,4),W(1,14),W(1,24),GC_938,AMP(167))
C     Amplitude(s) for diagram number 160
      CALL FFV2_8_0(W(1,4),W(1,15),W(1,24),GC_651,GC_660,AMP(168))
      CALL FFV6_2(W(1,17),W(1,1),GC_7,MDL_MT,MDL_WT,W(1,15))
C     Amplitude(s) for diagram number 161
      CALL FFV6_0(W(1,15),W(1,3),W(1,20),GC_2,AMP(169))
      CALL FFV6_2(W(1,18),W(1,1),GC_7,MDL_MT,MDL_WT,W(1,14))
C     Amplitude(s) for diagram number 162
      CALL FFV6_0(W(1,14),W(1,3),W(1,20),GC_2,AMP(170))
C     Amplitude(s) for diagram number 163
      CALL FFV11_9_0(W(1,14),W(1,3),W(1,20),GC_813,GC_814,AMP(171))
      CALL FFV11_9_2(W(1,18),W(1,1),GC_725,GC_726,MDL_MT,MDL_WT,W(1,7))
C     Amplitude(s) for diagram number 164
      CALL FFV6_0(W(1,7),W(1,3),W(1,20),GC_2,AMP(172))
C     Amplitude(s) for diagram number 165
      CALL FFV6_0(W(1,17),W(1,3),W(1,9),GC_7,AMP(173))
C     Amplitude(s) for diagram number 166
      CALL FFV6_0(W(1,15),W(1,3),W(1,23),GC_7,AMP(174))
C     Amplitude(s) for diagram number 167
      CALL FFVV2_4_0(W(1,18),W(1,3),W(1,1),W(1,23),GC_728,GC_727
     $ ,AMP(175))
C     Amplitude(s) for diagram number 168
      CALL FFV6_0(W(1,18),W(1,3),W(1,9),GC_7,AMP(176))
C     Amplitude(s) for diagram number 169
      CALL FFV11_9_0(W(1,18),W(1,3),W(1,9),GC_725,GC_726,AMP(177))
C     Amplitude(s) for diagram number 170
      CALL FFV6_0(W(1,14),W(1,3),W(1,23),GC_7,AMP(178))
C     Amplitude(s) for diagram number 171
      CALL FFV11_9_0(W(1,14),W(1,3),W(1,23),GC_725,GC_726,AMP(179))
C     Amplitude(s) for diagram number 172
      CALL FFV6_0(W(1,7),W(1,3),W(1,23),GC_7,AMP(180))
C     Amplitude(s) for diagram number 173
      CALL FFV2_8_0(W(1,15),W(1,3),W(1,24),GC_651,GC_660,AMP(181))
C     Amplitude(s) for diagram number 174
      CALL FFV2_8_0(W(1,14),W(1,3),W(1,24),GC_651,GC_660,AMP(182))
C     Amplitude(s) for diagram number 175
      CALL FFV11_9_0(W(1,14),W(1,3),W(1,24),GC_721,GC_722,AMP(183))
C     Amplitude(s) for diagram number 176
      CALL FFV4_0(W(1,14),W(1,3),W(1,24),GC_948,AMP(184))
C     Amplitude(s) for diagram number 177
      CALL FFV2_0(W(1,14),W(1,3),W(1,24),GC_938,AMP(185))
C     Amplitude(s) for diagram number 178
      CALL FFV2_8_0(W(1,7),W(1,3),W(1,24),GC_651,GC_660,AMP(186))
C     Amplitude(s) for diagram number 179
      CALL VVV1_0(W(1,1),W(1,23),W(1,19),GC_6,AMP(187))
      CALL FFVS4_6_1(W(1,3),W(1,1),W(1,5),GC_599,GC_598,MDL_MT,MDL_WT
     $ ,W(1,19))
C     Amplitude(s) for diagram number 180
      CALL FFV6_0(W(1,4),W(1,19),W(1,20),GC_2,AMP(188))
C     Amplitude(s) for diagram number 181
      CALL FFV6_0(W(1,4),W(1,19),W(1,23),GC_7,AMP(189))
C     Amplitude(s) for diagram number 182
      CALL FFV2_8_0(W(1,4),W(1,19),W(1,24),GC_651,GC_660,AMP(190))
      CALL FFVS4_6_2(W(1,4),W(1,1),W(1,5),GC_599,GC_598,MDL_MT,MDL_WT
     $ ,W(1,19))
C     Amplitude(s) for diagram number 183
      CALL FFV6_0(W(1,19),W(1,3),W(1,20),GC_2,AMP(191))
C     Amplitude(s) for diagram number 184
      CALL FFV6_0(W(1,19),W(1,3),W(1,23),GC_7,AMP(192))
C     Amplitude(s) for diagram number 185
      CALL FFV2_8_0(W(1,19),W(1,3),W(1,24),GC_651,GC_660,AMP(193))
C     Amplitude(s) for diagram number 186
      CALL FFV6_0(W(1,18),W(1,26),W(1,1),GC_7,AMP(194))
      CALL FFV6_0(W(1,18),W(1,25),W(1,1),GC_7,AMP(195))
C     Amplitude(s) for diagram number 187
      CALL FFV6_0(W(1,22),W(1,16),W(1,1),GC_7,AMP(196))
      CALL FFV6_0(W(1,21),W(1,16),W(1,1),GC_7,AMP(197))
      CALL FFVVS2_4P0_3(W(1,4),W(1,3),W(1,1),W(1,5),GC_601,GC_600,ZERO
     $ ,ZERO,W(1,21))
C     Amplitude(s) for diagram number 188
      CALL FFV1_0(W(1,2),W(1,6),W(1,21),GC_7,AMP(198))
      JAMP(1)=+1D0/2D0*(-AMP(6)-AMP(9)-AMP(12)-AMP(13)-AMP(19)-AMP(22)
     $ -AMP(25)-AMP(26)-AMP(34)-AMP(39)-AMP(40)-AMP(41)-AMP(42)-AMP(55)
     $ -AMP(61)-AMP(62)-AMP(63)-AMP(70)-AMP(73)-AMP(75)+IMAG1*AMP(155)
     $ -AMP(156)+IMAG1*AMP(157)+IMAG1*AMP(158)+IMAG1*AMP(159)-AMP(160)
     $ -AMP(161)-AMP(162)+IMAG1*AMP(173)+IMAG1*AMP(175)+IMAG1*AMP(176)
     $ +IMAG1*AMP(177)+IMAG1*AMP(187)-AMP(189)-AMP(197)-IMAG1*AMP(198))
      JAMP(2)=-AMP(35)-AMP(36)-AMP(37)-AMP(38)+1D0/6D0*AMP(39)+1D0/6D0
     $ *AMP(40)+1D0/6D0*AMP(41)+1D0/6D0*AMP(42)-AMP(43)-AMP(44)-AMP(45)
     $ -AMP(46)-AMP(47)-AMP(48)-AMP(49)-AMP(50)-AMP(51)-AMP(52)-AMP(53)
     $ -AMP(54)+1D0/6D0*AMP(55)-AMP(56)-AMP(57)-AMP(58)-AMP(59)-AMP(60)
     $ +1D0/6D0*AMP(61)+1D0/6D0*AMP(62)+1D0/6D0*AMP(63)-AMP(64)-AMP(65)
     $ -AMP(66)-AMP(67)-AMP(68)-AMP(69)+1D0/6D0*AMP(70)-AMP(71)-AMP(72)
     $ +1D0/6D0*AMP(73)+1D0/6D0*AMP(75)-AMP(74)-AMP(76)-AMP(77)-AMP(78)
     $ -AMP(79)+1D0/6D0*AMP(80)+1D0/6D0*AMP(81)+1D0/6D0*AMP(82)+1D0
     $ /6D0*AMP(83)-AMP(84)-AMP(85)-AMP(86)-AMP(87)-AMP(88)-AMP(89)
     $ -AMP(90)-AMP(91)-AMP(92)-AMP(93)-AMP(94)-AMP(95)+1D0/6D0*AMP(96)
     $ -AMP(97)-AMP(98)-AMP(99)-AMP(100)-AMP(101)+1D0/6D0*AMP(102)+1D0
     $ /6D0*AMP(103)+1D0/6D0*AMP(104)-AMP(105)-AMP(106)-AMP(107)
     $ -AMP(108)-AMP(109)-AMP(110)+1D0/6D0*AMP(111)-AMP(112)-AMP(113)
     $ +1D0/6D0*AMP(114)+1D0/6D0*AMP(116)-AMP(115)-AMP(151)-AMP(152)
     $ -AMP(153)-AMP(154)+1D0/6D0*AMP(156)+1D0/6D0*AMP(160)+1D0/6D0
     $ *AMP(161)+1D0/6D0*AMP(162)-AMP(163)-AMP(164)-AMP(165)-AMP(166)
     $ -AMP(167)-AMP(168)-AMP(169)-AMP(170)-AMP(171)-AMP(172)+1D0/6D0
     $ *AMP(174)+1D0/6D0*AMP(178)+1D0/6D0*AMP(179)+1D0/6D0*AMP(180)
     $ -AMP(181)-AMP(182)-AMP(183)-AMP(184)-AMP(185)-AMP(186)-AMP(188)
     $ +1D0/6D0*AMP(189)-AMP(190)-AMP(191)+1D0/6D0*AMP(192)-AMP(193)
     $ +1D0/6D0*AMP(195)-AMP(194)+1D0/6D0*AMP(197)-AMP(196)
      JAMP(3)=-AMP(1)-AMP(2)-AMP(3)-AMP(4)-AMP(5)+1D0/6D0*AMP(6)-AMP(7)
     $ -AMP(8)+1D0/6D0*AMP(9)-AMP(10)-AMP(11)+1D0/6D0*AMP(12)+1D0/6D0
     $ *AMP(13)-AMP(14)-AMP(15)-AMP(16)-AMP(17)-AMP(18)+1D0/6D0*AMP(19)
     $ -AMP(20)-AMP(21)+1D0/6D0*AMP(22)-AMP(23)-AMP(24)+1D0/6D0*AMP(25)
     $ +1D0/6D0*AMP(26)-AMP(27)-AMP(28)-AMP(29)-AMP(30)-AMP(31)-AMP(32)
     $ -AMP(33)+1D0/6D0*AMP(34)-AMP(117)-AMP(118)-AMP(119)-AMP(120)
     $ -AMP(121)+1D0/6D0*AMP(122)-AMP(123)-AMP(124)+1D0/6D0*AMP(125)
     $ -AMP(126)-AMP(127)+1D0/6D0*AMP(128)+1D0/6D0*AMP(129)-AMP(130)
     $ -AMP(131)-AMP(132)-AMP(133)-AMP(134)+1D0/6D0*AMP(135)-AMP(136)
     $ -AMP(137)+1D0/6D0*AMP(138)-AMP(139)-AMP(140)+1D0/6D0*AMP(141)
     $ +1D0/6D0*AMP(142)-AMP(143)-AMP(144)-AMP(145)-AMP(146)-AMP(147)
     $ -AMP(148)-AMP(149)+1D0/6D0*AMP(150)
      JAMP(4)=+1D0/2D0*(-AMP(80)-AMP(81)-AMP(82)-AMP(83)-AMP(96)
     $ -AMP(102)-AMP(103)-AMP(104)-AMP(111)-AMP(114)-AMP(116)-AMP(122)
     $ -AMP(125)-AMP(128)-AMP(129)-AMP(135)-AMP(138)-AMP(141)-AMP(142)
     $ -AMP(150)-IMAG1*AMP(155)-IMAG1*AMP(157)-IMAG1*AMP(158)-IMAG1
     $ *AMP(159)-IMAG1*AMP(173)-AMP(174)-IMAG1*AMP(175)-IMAG1*AMP(176)
     $ -IMAG1*AMP(177)-AMP(178)-AMP(179)-AMP(180)-IMAG1*AMP(187)
     $ -AMP(192)-AMP(195)+IMAG1*AMP(198))

      M6_MATRIX = 0.D0
      DO I = 1, NCOLOR
        ZTEMP = (0.D0,0.D0)
        DO J = 1, NCOLOR
          ZTEMP = ZTEMP + CF(J,I)*JAMP(J)
        ENDDO
        M6_MATRIX = M6_MATRIX+ZTEMP*DCONJG(JAMP(I))/DENOM(I)
      ENDDO

      END

      SUBROUTINE M6_GET_VALUE(P, ALPHAS, NHEL ,ANS)
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
        CALL M6_SMATRIXHEL(P, NHEL, ANS)
      ELSE
        CALL M6_SMATRIX(P, ANS)
      ENDIF
      RETURN
      END

      SUBROUTINE M6_INITIALISEMODEL(PATH)
C     ROUTINE FOR F2PY to read the benchmark point.    
      IMPLICIT NONE
      CHARACTER*512 PATH
CF2PY INTENT(IN) :: PATH
      CALL SETPARA(PATH)  !first call to setup the paramaters    
      RETURN
      END

      LOGICAL FUNCTION M6_IS_BORN_HEL_SELECTED(HELID)
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
      COMMON/M6_PROCESS_NHEL/HELC

      INTEGER POLARIZATIONS(0:NEXTERNAL,0:5)
      COMMON/M6_BORN_BEAM_POL/POLARIZATIONS
C     ----------
C     BEGIN CODE
C     ----------

      M6_IS_BORN_HEL_SELECTED = .TRUE.
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
          M6_IS_BORN_HEL_SELECTED = .FALSE.
          RETURN
        ENDIF
      ENDDO

      RETURN
      END

