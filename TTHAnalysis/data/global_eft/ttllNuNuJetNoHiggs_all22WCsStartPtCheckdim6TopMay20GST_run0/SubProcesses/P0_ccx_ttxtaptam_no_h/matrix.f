      SUBROUTINE M91_SMATRIXHEL(P,HEL,ANS)
      IMPLICIT NONE
C     
C     CONSTANT
C     
      INTEGER    NEXTERNAL
      PARAMETER (NEXTERNAL=6)
      INTEGER                 NCOMB
      PARAMETER (             NCOMB=64)
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
      COMMON/M91_HELUSERCHOICE/USERHEL
C     ----------
C     BEGIN CODE
C     ----------
      USERHEL=HEL
      CALL M91_SMATRIX(P,ANS)
      USERHEL=-1

      END

      SUBROUTINE M91_SMATRIX(P,ANS)
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
C     Process: c c~ > t t~ ta+ ta- DIM6<=1 FCNC=0 / h
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
      PARAMETER (             NCOMB=64)
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
      COMMON/M91_PROCESS_NHEL/NHEL
      REAL*8 T
      REAL*8 M91_MATRIX
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
      COMMON/M91_HELUSERCHOICE/USERHEL
      DATA USERHEL/-1/

      DATA (NHEL(I,   1),I=1,6) / 1,-1,-1, 1, 1,-1/
      DATA (NHEL(I,   2),I=1,6) / 1,-1,-1, 1, 1, 1/
      DATA (NHEL(I,   3),I=1,6) / 1,-1,-1, 1,-1,-1/
      DATA (NHEL(I,   4),I=1,6) / 1,-1,-1, 1,-1, 1/
      DATA (NHEL(I,   5),I=1,6) / 1,-1,-1,-1, 1,-1/
      DATA (NHEL(I,   6),I=1,6) / 1,-1,-1,-1, 1, 1/
      DATA (NHEL(I,   7),I=1,6) / 1,-1,-1,-1,-1,-1/
      DATA (NHEL(I,   8),I=1,6) / 1,-1,-1,-1,-1, 1/
      DATA (NHEL(I,   9),I=1,6) / 1,-1, 1, 1, 1,-1/
      DATA (NHEL(I,  10),I=1,6) / 1,-1, 1, 1, 1, 1/
      DATA (NHEL(I,  11),I=1,6) / 1,-1, 1, 1,-1,-1/
      DATA (NHEL(I,  12),I=1,6) / 1,-1, 1, 1,-1, 1/
      DATA (NHEL(I,  13),I=1,6) / 1,-1, 1,-1, 1,-1/
      DATA (NHEL(I,  14),I=1,6) / 1,-1, 1,-1, 1, 1/
      DATA (NHEL(I,  15),I=1,6) / 1,-1, 1,-1,-1,-1/
      DATA (NHEL(I,  16),I=1,6) / 1,-1, 1,-1,-1, 1/
      DATA (NHEL(I,  17),I=1,6) / 1, 1,-1, 1, 1,-1/
      DATA (NHEL(I,  18),I=1,6) / 1, 1,-1, 1, 1, 1/
      DATA (NHEL(I,  19),I=1,6) / 1, 1,-1, 1,-1,-1/
      DATA (NHEL(I,  20),I=1,6) / 1, 1,-1, 1,-1, 1/
      DATA (NHEL(I,  21),I=1,6) / 1, 1,-1,-1, 1,-1/
      DATA (NHEL(I,  22),I=1,6) / 1, 1,-1,-1, 1, 1/
      DATA (NHEL(I,  23),I=1,6) / 1, 1,-1,-1,-1,-1/
      DATA (NHEL(I,  24),I=1,6) / 1, 1,-1,-1,-1, 1/
      DATA (NHEL(I,  25),I=1,6) / 1, 1, 1, 1, 1,-1/
      DATA (NHEL(I,  26),I=1,6) / 1, 1, 1, 1, 1, 1/
      DATA (NHEL(I,  27),I=1,6) / 1, 1, 1, 1,-1,-1/
      DATA (NHEL(I,  28),I=1,6) / 1, 1, 1, 1,-1, 1/
      DATA (NHEL(I,  29),I=1,6) / 1, 1, 1,-1, 1,-1/
      DATA (NHEL(I,  30),I=1,6) / 1, 1, 1,-1, 1, 1/
      DATA (NHEL(I,  31),I=1,6) / 1, 1, 1,-1,-1,-1/
      DATA (NHEL(I,  32),I=1,6) / 1, 1, 1,-1,-1, 1/
      DATA (NHEL(I,  33),I=1,6) /-1,-1,-1, 1, 1,-1/
      DATA (NHEL(I,  34),I=1,6) /-1,-1,-1, 1, 1, 1/
      DATA (NHEL(I,  35),I=1,6) /-1,-1,-1, 1,-1,-1/
      DATA (NHEL(I,  36),I=1,6) /-1,-1,-1, 1,-1, 1/
      DATA (NHEL(I,  37),I=1,6) /-1,-1,-1,-1, 1,-1/
      DATA (NHEL(I,  38),I=1,6) /-1,-1,-1,-1, 1, 1/
      DATA (NHEL(I,  39),I=1,6) /-1,-1,-1,-1,-1,-1/
      DATA (NHEL(I,  40),I=1,6) /-1,-1,-1,-1,-1, 1/
      DATA (NHEL(I,  41),I=1,6) /-1,-1, 1, 1, 1,-1/
      DATA (NHEL(I,  42),I=1,6) /-1,-1, 1, 1, 1, 1/
      DATA (NHEL(I,  43),I=1,6) /-1,-1, 1, 1,-1,-1/
      DATA (NHEL(I,  44),I=1,6) /-1,-1, 1, 1,-1, 1/
      DATA (NHEL(I,  45),I=1,6) /-1,-1, 1,-1, 1,-1/
      DATA (NHEL(I,  46),I=1,6) /-1,-1, 1,-1, 1, 1/
      DATA (NHEL(I,  47),I=1,6) /-1,-1, 1,-1,-1,-1/
      DATA (NHEL(I,  48),I=1,6) /-1,-1, 1,-1,-1, 1/
      DATA (NHEL(I,  49),I=1,6) /-1, 1,-1, 1, 1,-1/
      DATA (NHEL(I,  50),I=1,6) /-1, 1,-1, 1, 1, 1/
      DATA (NHEL(I,  51),I=1,6) /-1, 1,-1, 1,-1,-1/
      DATA (NHEL(I,  52),I=1,6) /-1, 1,-1, 1,-1, 1/
      DATA (NHEL(I,  53),I=1,6) /-1, 1,-1,-1, 1,-1/
      DATA (NHEL(I,  54),I=1,6) /-1, 1,-1,-1, 1, 1/
      DATA (NHEL(I,  55),I=1,6) /-1, 1,-1,-1,-1,-1/
      DATA (NHEL(I,  56),I=1,6) /-1, 1,-1,-1,-1, 1/
      DATA (NHEL(I,  57),I=1,6) /-1, 1, 1, 1, 1,-1/
      DATA (NHEL(I,  58),I=1,6) /-1, 1, 1, 1, 1, 1/
      DATA (NHEL(I,  59),I=1,6) /-1, 1, 1, 1,-1,-1/
      DATA (NHEL(I,  60),I=1,6) /-1, 1, 1, 1,-1, 1/
      DATA (NHEL(I,  61),I=1,6) /-1, 1, 1,-1, 1,-1/
      DATA (NHEL(I,  62),I=1,6) /-1, 1, 1,-1, 1, 1/
      DATA (NHEL(I,  63),I=1,6) /-1, 1, 1,-1,-1,-1/
      DATA (NHEL(I,  64),I=1,6) /-1, 1, 1,-1,-1, 1/
      DATA IDEN/36/

      INTEGER POLARIZATIONS(0:NEXTERNAL,0:5)
      COMMON/M91_BORN_BEAM_POL/POLARIZATIONS
      DATA ((POLARIZATIONS(I,J),I=0,NEXTERNAL),J=0,5)/NPOLENTRIES*-1/

C     
C     FUNCTIONS
C     
      LOGICAL M91_IS_BORN_HEL_SELECTED

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
     $       -1.AND.(.NOT.M91_IS_BORN_HEL_SELECTED(IHEL))) THEN
              CYCLE
            ENDIF
            T=M91_MATRIX(P ,NHEL(1,IHEL),JC(1))
            IF(POLARIZATIONS(0,0).EQ.-1.OR.M91_IS_BORN_HEL_SELECTED(IHE
     $L)) THEN
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


      REAL*8 FUNCTION M91_MATRIX(P,NHEL,IC)
C     
C     Generated by MadGraph5_aMC@NLO v. 2.6.5, 2018-02-03
C     By the MadGraph5_aMC@NLO Development Team
C     Visit launchpad.net/madgraph5 and amcatnlo.web.cern.ch
C     
C     Returns amplitude squared summed/avg over colors
C     for the point with external lines W(0:6,NEXTERNAL)
C     
C     Process: c c~ > t t~ ta+ ta- DIM6<=1 FCNC=0 / h
C     
      IMPLICIT NONE
C     
C     CONSTANTS
C     
      INTEGER    NGRAPHS
      PARAMETER (NGRAPHS=138)
      INTEGER    NEXTERNAL
      PARAMETER (NEXTERNAL=6)
      INTEGER    NWAVEFUNCS, NCOLOR
      PARAMETER (NWAVEFUNCS=25, NCOLOR=2)
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
      DATA (CF(I,  1),I=  1,  2) /    9,    3/
C     1 T(2,1) T(3,4)
      DATA DENOM(2)/1/
      DATA (CF(I,  2),I=  1,  2) /    3,    9/
C     1 T(2,4) T(3,1)
C     ----------
C     BEGIN CODE
C     ----------
      CALL IXXXXX(P(0,1),ZERO,NHEL(1),+1*IC(1),W(1,1))
      CALL OXXXXX(P(0,2),ZERO,NHEL(2),-1*IC(2),W(1,2))
      CALL OXXXXX(P(0,3),MDL_MT,NHEL(3),+1*IC(3),W(1,3))
      CALL IXXXXX(P(0,4),MDL_MT,NHEL(4),-1*IC(4),W(1,4))
      CALL IXXXXX(P(0,5),MDL_MTA,NHEL(5),-1*IC(5),W(1,5))
      CALL OXXXXX(P(0,6),MDL_MTA,NHEL(6),+1*IC(6),W(1,6))
      CALL FFV1P0_3(W(1,1),W(1,2),GC_2,ZERO,ZERO,W(1,7))
      CALL FFV6P0_3(W(1,4),W(1,3),GC_2,ZERO,ZERO,W(1,8))
      CALL FFV1_2(W(1,5),W(1,7),GC_3,MDL_MTA,ZERO,W(1,9))
C     Amplitude(s) for diagram number 1
      CALL FFV1_0(W(1,9),W(1,6),W(1,8),GC_3,AMP(1))
      CALL FFV1_1(W(1,6),W(1,7),GC_3,MDL_MTA,ZERO,W(1,10))
C     Amplitude(s) for diagram number 2
      CALL FFV1_0(W(1,5),W(1,10),W(1,8),GC_3,AMP(2))
      CALL FFV11_9P0_3(W(1,4),W(1,3),GC_813,GC_814,ZERO,ZERO,W(1,11))
C     Amplitude(s) for diagram number 3
      CALL FFV1_0(W(1,9),W(1,6),W(1,11),GC_3,AMP(3))
C     Amplitude(s) for diagram number 4
      CALL FFV1_0(W(1,5),W(1,10),W(1,11),GC_3,AMP(4))
      CALL FFV2_8_3(W(1,4),W(1,3),GC_651,GC_660,MDL_MZ,MDL_WZ,W(1,12))
C     Amplitude(s) for diagram number 5
      CALL FFV2_7_0(W(1,9),W(1,6),W(1,12),GC_650,GC_661,AMP(5))
C     Amplitude(s) for diagram number 6
      CALL FFV2_7_0(W(1,5),W(1,10),W(1,12),GC_650,GC_661,AMP(6))
      CALL FFV11_9_3(W(1,4),W(1,3),GC_721,GC_722,MDL_MZ,MDL_WZ,W(1,13))
C     Amplitude(s) for diagram number 7
      CALL FFV2_7_0(W(1,9),W(1,6),W(1,13),GC_650,GC_661,AMP(7))
C     Amplitude(s) for diagram number 8
      CALL FFV2_7_0(W(1,5),W(1,10),W(1,13),GC_650,GC_661,AMP(8))
      CALL FFV4_3(W(1,4),W(1,3),GC_948,MDL_MZ,MDL_WZ,W(1,14))
C     Amplitude(s) for diagram number 9
      CALL FFV2_7_0(W(1,9),W(1,6),W(1,14),GC_650,GC_661,AMP(9))
C     Amplitude(s) for diagram number 10
      CALL FFV2_7_0(W(1,5),W(1,10),W(1,14),GC_650,GC_661,AMP(10))
      CALL FFV2_3(W(1,4),W(1,3),GC_938,MDL_MZ,MDL_WZ,W(1,15))
C     Amplitude(s) for diagram number 11
      CALL FFV2_7_0(W(1,9),W(1,6),W(1,15),GC_650,GC_661,AMP(11))
C     Amplitude(s) for diagram number 12
      CALL FFV2_7_0(W(1,5),W(1,10),W(1,15),GC_650,GC_661,AMP(12))
      CALL FFV2_8_3(W(1,1),W(1,2),GC_651,GC_660,MDL_MZ,MDL_WZ,W(1,10))
      CALL FFV2_7_2(W(1,5),W(1,10),GC_650,GC_661,MDL_MTA,ZERO,W(1,9))
C     Amplitude(s) for diagram number 13
      CALL FFV1_0(W(1,9),W(1,6),W(1,8),GC_3,AMP(13))
      CALL FFV2_7_1(W(1,6),W(1,10),GC_650,GC_661,MDL_MTA,ZERO,W(1,16))
C     Amplitude(s) for diagram number 14
      CALL FFV1_0(W(1,5),W(1,16),W(1,8),GC_3,AMP(14))
C     Amplitude(s) for diagram number 15
      CALL FFV1_0(W(1,9),W(1,6),W(1,11),GC_3,AMP(15))
C     Amplitude(s) for diagram number 16
      CALL FFV1_0(W(1,5),W(1,16),W(1,11),GC_3,AMP(16))
C     Amplitude(s) for diagram number 17
      CALL FFV2_7_0(W(1,9),W(1,6),W(1,12),GC_650,GC_661,AMP(17))
C     Amplitude(s) for diagram number 18
      CALL FFV2_7_0(W(1,5),W(1,16),W(1,12),GC_650,GC_661,AMP(18))
C     Amplitude(s) for diagram number 19
      CALL FFV2_7_0(W(1,9),W(1,6),W(1,13),GC_650,GC_661,AMP(19))
C     Amplitude(s) for diagram number 20
      CALL FFV2_7_0(W(1,5),W(1,16),W(1,13),GC_650,GC_661,AMP(20))
C     Amplitude(s) for diagram number 21
      CALL FFV2_7_0(W(1,9),W(1,6),W(1,14),GC_650,GC_661,AMP(21))
C     Amplitude(s) for diagram number 22
      CALL FFV2_7_0(W(1,5),W(1,16),W(1,14),GC_650,GC_661,AMP(22))
C     Amplitude(s) for diagram number 23
      CALL FFV2_7_0(W(1,9),W(1,6),W(1,15),GC_650,GC_661,AMP(23))
C     Amplitude(s) for diagram number 24
      CALL FFV2_7_0(W(1,5),W(1,16),W(1,15),GC_650,GC_661,AMP(24))
      CALL FFV1P0_3(W(1,5),W(1,6),GC_3,ZERO,ZERO,W(1,16))
      CALL FFV6_1(W(1,3),W(1,7),GC_2,MDL_MT,MDL_WT,W(1,9))
C     Amplitude(s) for diagram number 25
      CALL FFV6_0(W(1,4),W(1,9),W(1,16),GC_2,AMP(25))
C     Amplitude(s) for diagram number 26
      CALL FFV11_9_0(W(1,4),W(1,9),W(1,16),GC_813,GC_814,AMP(26))
      CALL FFV11_9_1(W(1,3),W(1,7),GC_813,GC_814,MDL_MT,MDL_WT,W(1,17))
C     Amplitude(s) for diagram number 27
      CALL FFV6_0(W(1,4),W(1,17),W(1,16),GC_2,AMP(27))
      CALL FFV6_2(W(1,4),W(1,7),GC_2,MDL_MT,MDL_WT,W(1,18))
C     Amplitude(s) for diagram number 28
      CALL FFV6_0(W(1,18),W(1,3),W(1,16),GC_2,AMP(28))
C     Amplitude(s) for diagram number 29
      CALL FFV11_9_0(W(1,18),W(1,3),W(1,16),GC_813,GC_814,AMP(29))
      CALL FFV11_9_2(W(1,4),W(1,7),GC_813,GC_814,MDL_MT,MDL_WT,W(1,19))
C     Amplitude(s) for diagram number 30
      CALL FFV6_0(W(1,19),W(1,3),W(1,16),GC_2,AMP(30))
      CALL FFV2_7_3(W(1,5),W(1,6),GC_650,GC_661,MDL_MZ,MDL_WZ,W(1,20))
C     Amplitude(s) for diagram number 31
      CALL FFV2_8_0(W(1,4),W(1,9),W(1,20),GC_651,GC_660,AMP(31))
C     Amplitude(s) for diagram number 32
      CALL FFV11_9_0(W(1,4),W(1,9),W(1,20),GC_721,GC_722,AMP(32))
C     Amplitude(s) for diagram number 33
      CALL FFV4_0(W(1,4),W(1,9),W(1,20),GC_948,AMP(33))
C     Amplitude(s) for diagram number 34
      CALL FFV2_0(W(1,4),W(1,9),W(1,20),GC_938,AMP(34))
C     Amplitude(s) for diagram number 35
      CALL FFV2_8_0(W(1,4),W(1,17),W(1,20),GC_651,GC_660,AMP(35))
C     Amplitude(s) for diagram number 36
      CALL FFV2_8_0(W(1,18),W(1,3),W(1,20),GC_651,GC_660,AMP(36))
C     Amplitude(s) for diagram number 37
      CALL FFV11_9_0(W(1,18),W(1,3),W(1,20),GC_721,GC_722,AMP(37))
C     Amplitude(s) for diagram number 38
      CALL FFV4_0(W(1,18),W(1,3),W(1,20),GC_948,AMP(38))
C     Amplitude(s) for diagram number 39
      CALL FFV2_0(W(1,18),W(1,3),W(1,20),GC_938,AMP(39))
C     Amplitude(s) for diagram number 40
      CALL FFV2_8_0(W(1,19),W(1,3),W(1,20),GC_651,GC_660,AMP(40))
      CALL FFV1P0_3(W(1,1),W(1,2),GC_7,ZERO,ZERO,W(1,19))
      CALL FFV6_1(W(1,3),W(1,19),GC_7,MDL_MT,MDL_WT,W(1,18))
C     Amplitude(s) for diagram number 41
      CALL FFV6_0(W(1,4),W(1,18),W(1,16),GC_2,AMP(41))
C     Amplitude(s) for diagram number 42
      CALL FFV11_9_0(W(1,4),W(1,18),W(1,16),GC_813,GC_814,AMP(42))
      CALL FFV11_9_1(W(1,3),W(1,19),GC_725,GC_726,MDL_MT,MDL_WT,W(1,17)
     $ )
C     Amplitude(s) for diagram number 43
      CALL FFV6_0(W(1,4),W(1,17),W(1,16),GC_2,AMP(43))
      CALL FFV6_2(W(1,4),W(1,19),GC_7,MDL_MT,MDL_WT,W(1,9))
C     Amplitude(s) for diagram number 44
      CALL FFV6_0(W(1,9),W(1,3),W(1,16),GC_2,AMP(44))
C     Amplitude(s) for diagram number 45
      CALL FFV11_9_0(W(1,9),W(1,3),W(1,16),GC_813,GC_814,AMP(45))
      CALL FFV11_9_2(W(1,4),W(1,19),GC_725,GC_726,MDL_MT,MDL_WT,W(1,21)
     $ )
C     Amplitude(s) for diagram number 46
      CALL FFV6_0(W(1,21),W(1,3),W(1,16),GC_2,AMP(46))
C     Amplitude(s) for diagram number 47
      CALL FFV2_8_0(W(1,4),W(1,18),W(1,20),GC_651,GC_660,AMP(47))
C     Amplitude(s) for diagram number 48
      CALL FFV11_9_0(W(1,4),W(1,18),W(1,20),GC_721,GC_722,AMP(48))
C     Amplitude(s) for diagram number 49
      CALL FFV4_0(W(1,4),W(1,18),W(1,20),GC_948,AMP(49))
C     Amplitude(s) for diagram number 50
      CALL FFV2_0(W(1,4),W(1,18),W(1,20),GC_938,AMP(50))
C     Amplitude(s) for diagram number 51
      CALL FFV2_8_0(W(1,4),W(1,17),W(1,20),GC_651,GC_660,AMP(51))
C     Amplitude(s) for diagram number 52
      CALL FFV2_8_0(W(1,9),W(1,3),W(1,20),GC_651,GC_660,AMP(52))
C     Amplitude(s) for diagram number 53
      CALL FFV11_9_0(W(1,9),W(1,3),W(1,20),GC_721,GC_722,AMP(53))
C     Amplitude(s) for diagram number 54
      CALL FFV4_0(W(1,9),W(1,3),W(1,20),GC_948,AMP(54))
C     Amplitude(s) for diagram number 55
      CALL FFV2_0(W(1,9),W(1,3),W(1,20),GC_938,AMP(55))
C     Amplitude(s) for diagram number 56
      CALL FFV2_8_0(W(1,21),W(1,3),W(1,20),GC_651,GC_660,AMP(56))
      CALL FFV2_8_1(W(1,3),W(1,10),GC_651,GC_660,MDL_MT,MDL_WT,W(1,21))
C     Amplitude(s) for diagram number 57
      CALL FFV6_0(W(1,4),W(1,21),W(1,16),GC_2,AMP(57))
C     Amplitude(s) for diagram number 58
      CALL FFV11_9_0(W(1,4),W(1,21),W(1,16),GC_813,GC_814,AMP(58))
      CALL FFV11_9_1(W(1,3),W(1,10),GC_721,GC_722,MDL_MT,MDL_WT,W(1,9))
C     Amplitude(s) for diagram number 59
      CALL FFV6_0(W(1,4),W(1,9),W(1,16),GC_2,AMP(59))
      CALL FFV4_1(W(1,3),W(1,10),GC_948,MDL_MT,MDL_WT,W(1,17))
C     Amplitude(s) for diagram number 60
      CALL FFV6_0(W(1,4),W(1,17),W(1,16),GC_2,AMP(60))
      CALL FFV2_1(W(1,3),W(1,10),GC_938,MDL_MT,MDL_WT,W(1,18))
C     Amplitude(s) for diagram number 61
      CALL FFV6_0(W(1,4),W(1,18),W(1,16),GC_2,AMP(61))
      CALL FFV2_8_2(W(1,4),W(1,10),GC_651,GC_660,MDL_MT,MDL_WT,W(1,22))
C     Amplitude(s) for diagram number 62
      CALL FFV6_0(W(1,22),W(1,3),W(1,16),GC_2,AMP(62))
C     Amplitude(s) for diagram number 63
      CALL FFV11_9_0(W(1,22),W(1,3),W(1,16),GC_813,GC_814,AMP(63))
      CALL FFV11_9_2(W(1,4),W(1,10),GC_721,GC_722,MDL_MT,MDL_WT,W(1,23)
     $ )
C     Amplitude(s) for diagram number 64
      CALL FFV6_0(W(1,23),W(1,3),W(1,16),GC_2,AMP(64))
      CALL FFV4_2(W(1,4),W(1,10),GC_948,MDL_MT,MDL_WT,W(1,24))
C     Amplitude(s) for diagram number 65
      CALL FFV6_0(W(1,24),W(1,3),W(1,16),GC_2,AMP(65))
      CALL FFV2_2(W(1,4),W(1,10),GC_938,MDL_MT,MDL_WT,W(1,25))
C     Amplitude(s) for diagram number 66
      CALL FFV6_0(W(1,25),W(1,3),W(1,16),GC_2,AMP(66))
C     Amplitude(s) for diagram number 67
      CALL FFV2_8_0(W(1,4),W(1,21),W(1,20),GC_651,GC_660,AMP(67))
C     Amplitude(s) for diagram number 68
      CALL FFV11_9_0(W(1,4),W(1,21),W(1,20),GC_721,GC_722,AMP(68))
C     Amplitude(s) for diagram number 69
      CALL FFV4_0(W(1,4),W(1,21),W(1,20),GC_948,AMP(69))
C     Amplitude(s) for diagram number 70
      CALL FFV2_0(W(1,4),W(1,21),W(1,20),GC_938,AMP(70))
C     Amplitude(s) for diagram number 71
      CALL FFV2_8_0(W(1,4),W(1,9),W(1,20),GC_651,GC_660,AMP(71))
C     Amplitude(s) for diagram number 72
      CALL FFV2_8_0(W(1,4),W(1,17),W(1,20),GC_651,GC_660,AMP(72))
C     Amplitude(s) for diagram number 73
      CALL FFV2_8_0(W(1,4),W(1,18),W(1,20),GC_651,GC_660,AMP(73))
C     Amplitude(s) for diagram number 74
      CALL FFV2_8_0(W(1,22),W(1,3),W(1,20),GC_651,GC_660,AMP(74))
C     Amplitude(s) for diagram number 75
      CALL FFV11_9_0(W(1,22),W(1,3),W(1,20),GC_721,GC_722,AMP(75))
C     Amplitude(s) for diagram number 76
      CALL FFV4_0(W(1,22),W(1,3),W(1,20),GC_948,AMP(76))
C     Amplitude(s) for diagram number 77
      CALL FFV2_0(W(1,22),W(1,3),W(1,20),GC_938,AMP(77))
C     Amplitude(s) for diagram number 78
      CALL FFV2_8_0(W(1,23),W(1,3),W(1,20),GC_651,GC_660,AMP(78))
C     Amplitude(s) for diagram number 79
      CALL FFV2_8_0(W(1,24),W(1,3),W(1,20),GC_651,GC_660,AMP(79))
C     Amplitude(s) for diagram number 80
      CALL FFV2_8_0(W(1,25),W(1,3),W(1,20),GC_651,GC_660,AMP(80))
      CALL FFFF11_14_18_19_2_20_6_7_21_110_2(W(1,5),W(1,4),W(1,3)
     $ ,GC_348,GC_563,GC_586,GC_583,GC_354,GC_350,GC_569,GC_352,GC_349
     $ ,GC_351,MDL_MTA,ZERO,W(1,25))
C     Amplitude(s) for diagram number 81
      CALL FFV1_0(W(1,25),W(1,6),W(1,7),GC_3,AMP(81))
C     Amplitude(s) for diagram number 82
      CALL FFV2_7_0(W(1,25),W(1,6),W(1,10),GC_650,GC_661,AMP(82))
      CALL FFFF11_14_18_19_2_20_6_7_21_110_1(W(1,6),W(1,4),W(1,3)
     $ ,GC_348,GC_563,GC_586,GC_583,GC_354,GC_350,GC_569,GC_352,GC_349
     $ ,GC_351,MDL_MTA,ZERO,W(1,25))
C     Amplitude(s) for diagram number 83
      CALL FFV1_0(W(1,5),W(1,25),W(1,7),GC_3,AMP(83))
C     Amplitude(s) for diagram number 84
      CALL FFV2_7_0(W(1,5),W(1,25),W(1,10),GC_650,GC_661,AMP(84))
      CALL FFFF11_14_18_19_2_20_6_7_21_110_3(W(1,5),W(1,6),W(1,3)
     $ ,GC_348,GC_563,GC_586,GC_583,GC_354,GC_350,GC_569,GC_352,GC_349
     $ ,GC_351,MDL_MT,MDL_WT,W(1,25))
C     Amplitude(s) for diagram number 85
      CALL FFV6_0(W(1,4),W(1,25),W(1,7),GC_2,AMP(85))
C     Amplitude(s) for diagram number 86
      CALL FFV6_0(W(1,4),W(1,25),W(1,19),GC_7,AMP(86))
C     Amplitude(s) for diagram number 87
      CALL FFV2_8_0(W(1,4),W(1,25),W(1,10),GC_651,GC_660,AMP(87))
      CALL FFFF11_14_18_19_2_20_6_7_21_110_4(W(1,5),W(1,6),W(1,4)
     $ ,GC_348,GC_563,GC_586,GC_583,GC_354,GC_350,GC_569,GC_352,GC_349
     $ ,GC_351,MDL_MT,MDL_WT,W(1,25))
C     Amplitude(s) for diagram number 88
      CALL FFV6_0(W(1,25),W(1,3),W(1,7),GC_2,AMP(88))
C     Amplitude(s) for diagram number 89
      CALL FFV6_0(W(1,25),W(1,3),W(1,19),GC_7,AMP(89))
C     Amplitude(s) for diagram number 90
      CALL FFV2_8_0(W(1,25),W(1,3),W(1,10),GC_651,GC_660,AMP(90))
      CALL FFV1_2(W(1,1),W(1,8),GC_2,ZERO,ZERO,W(1,25))
C     Amplitude(s) for diagram number 91
      CALL FFV1_0(W(1,25),W(1,2),W(1,16),GC_2,AMP(91))
      CALL FFV1_2(W(1,1),W(1,16),GC_2,ZERO,ZERO,W(1,10))
C     Amplitude(s) for diagram number 92
      CALL FFV1_0(W(1,10),W(1,2),W(1,8),GC_2,AMP(92))
C     Amplitude(s) for diagram number 93
      CALL FFV2_8_0(W(1,25),W(1,2),W(1,20),GC_651,GC_660,AMP(93))
      CALL FFV2_8_2(W(1,1),W(1,20),GC_651,GC_660,ZERO,ZERO,W(1,25))
C     Amplitude(s) for diagram number 94
      CALL FFV1_0(W(1,25),W(1,2),W(1,8),GC_2,AMP(94))
      CALL FFV1_2(W(1,1),W(1,11),GC_2,ZERO,ZERO,W(1,8))
C     Amplitude(s) for diagram number 95
      CALL FFV1_0(W(1,8),W(1,2),W(1,16),GC_2,AMP(95))
C     Amplitude(s) for diagram number 96
      CALL FFV1_0(W(1,10),W(1,2),W(1,11),GC_2,AMP(96))
C     Amplitude(s) for diagram number 97
      CALL FFV2_8_0(W(1,8),W(1,2),W(1,20),GC_651,GC_660,AMP(97))
C     Amplitude(s) for diagram number 98
      CALL FFV1_0(W(1,25),W(1,2),W(1,11),GC_2,AMP(98))
      CALL FFV2_8_2(W(1,1),W(1,12),GC_651,GC_660,ZERO,ZERO,W(1,11))
C     Amplitude(s) for diagram number 99
      CALL FFV1_0(W(1,11),W(1,2),W(1,16),GC_2,AMP(99))
C     Amplitude(s) for diagram number 100
      CALL FFV2_8_0(W(1,10),W(1,2),W(1,12),GC_651,GC_660,AMP(100))
C     Amplitude(s) for diagram number 101
      CALL FFV2_8_0(W(1,11),W(1,2),W(1,20),GC_651,GC_660,AMP(101))
C     Amplitude(s) for diagram number 102
      CALL FFV2_8_0(W(1,25),W(1,2),W(1,12),GC_651,GC_660,AMP(102))
      CALL FFV2_8_2(W(1,1),W(1,13),GC_651,GC_660,ZERO,ZERO,W(1,12))
C     Amplitude(s) for diagram number 103
      CALL FFV1_0(W(1,12),W(1,2),W(1,16),GC_2,AMP(103))
C     Amplitude(s) for diagram number 104
      CALL FFV2_8_0(W(1,10),W(1,2),W(1,13),GC_651,GC_660,AMP(104))
C     Amplitude(s) for diagram number 105
      CALL FFV2_8_0(W(1,12),W(1,2),W(1,20),GC_651,GC_660,AMP(105))
C     Amplitude(s) for diagram number 106
      CALL FFV2_8_0(W(1,25),W(1,2),W(1,13),GC_651,GC_660,AMP(106))
      CALL FFV2_8_2(W(1,1),W(1,14),GC_651,GC_660,ZERO,ZERO,W(1,13))
C     Amplitude(s) for diagram number 107
      CALL FFV1_0(W(1,13),W(1,2),W(1,16),GC_2,AMP(107))
C     Amplitude(s) for diagram number 108
      CALL FFV2_8_0(W(1,10),W(1,2),W(1,14),GC_651,GC_660,AMP(108))
C     Amplitude(s) for diagram number 109
      CALL FFV2_8_0(W(1,13),W(1,2),W(1,20),GC_651,GC_660,AMP(109))
C     Amplitude(s) for diagram number 110
      CALL FFV2_8_0(W(1,25),W(1,2),W(1,14),GC_651,GC_660,AMP(110))
      CALL FFV2_8_2(W(1,1),W(1,15),GC_651,GC_660,ZERO,ZERO,W(1,14))
C     Amplitude(s) for diagram number 111
      CALL FFV1_0(W(1,14),W(1,2),W(1,16),GC_2,AMP(111))
C     Amplitude(s) for diagram number 112
      CALL FFV2_8_0(W(1,10),W(1,2),W(1,15),GC_651,GC_660,AMP(112))
C     Amplitude(s) for diagram number 113
      CALL FFV2_8_0(W(1,14),W(1,2),W(1,20),GC_651,GC_660,AMP(113))
C     Amplitude(s) for diagram number 114
      CALL FFV2_8_0(W(1,25),W(1,2),W(1,15),GC_651,GC_660,AMP(114))
      CALL FFV6P0_3(W(1,4),W(1,3),GC_7,ZERO,ZERO,W(1,15))
      CALL FFV1_2(W(1,1),W(1,15),GC_7,ZERO,ZERO,W(1,14))
C     Amplitude(s) for diagram number 115
      CALL FFV1_0(W(1,14),W(1,2),W(1,16),GC_2,AMP(115))
C     Amplitude(s) for diagram number 116
      CALL FFV1_0(W(1,10),W(1,2),W(1,15),GC_7,AMP(116))
C     Amplitude(s) for diagram number 117
      CALL FFV2_8_0(W(1,14),W(1,2),W(1,20),GC_651,GC_660,AMP(117))
C     Amplitude(s) for diagram number 118
      CALL FFV1_0(W(1,25),W(1,2),W(1,15),GC_7,AMP(118))
      CALL FFV11_9P0_3(W(1,4),W(1,3),GC_725,GC_726,ZERO,ZERO,W(1,15))
      CALL FFV1_2(W(1,1),W(1,15),GC_7,ZERO,ZERO,W(1,14))
C     Amplitude(s) for diagram number 119
      CALL FFV1_0(W(1,14),W(1,2),W(1,16),GC_2,AMP(119))
C     Amplitude(s) for diagram number 120
      CALL FFV1_0(W(1,10),W(1,2),W(1,15),GC_7,AMP(120))
C     Amplitude(s) for diagram number 121
      CALL FFV2_8_0(W(1,14),W(1,2),W(1,20),GC_651,GC_660,AMP(121))
C     Amplitude(s) for diagram number 122
      CALL FFV1_0(W(1,25),W(1,2),W(1,15),GC_7,AMP(122))
      CALL FFFF10_14_18_19_6_8_1(W(1,3),W(1,1),W(1,2),GC_471,GC_589
     $ ,GC_575,GC_592,GC_150,GC_472,MDL_MT,MDL_WT,W(1,15))
      CALL FFFF10_14_18_19_6_8_1(W(1,3),W(1,1),W(1,2),GC_473,GC_590
     $ ,GC_576,GC_593,GC_178,GC_474,MDL_MT,MDL_WT,W(1,25))
C     Amplitude(s) for diagram number 123
      CALL FFV6_0(W(1,4),W(1,15),W(1,16),GC_2,AMP(123))
      CALL FFV6_0(W(1,4),W(1,25),W(1,16),GC_2,AMP(124))
C     Amplitude(s) for diagram number 124
      CALL FFV2_8_0(W(1,4),W(1,15),W(1,20),GC_651,GC_660,AMP(125))
      CALL FFV2_8_0(W(1,4),W(1,25),W(1,20),GC_651,GC_660,AMP(126))
      CALL FFFF10_14_18_19_6_8_2(W(1,4),W(1,1),W(1,2),GC_471,GC_589
     $ ,GC_575,GC_592,GC_150,GC_472,MDL_MT,MDL_WT,W(1,25))
      CALL FFFF10_14_18_19_6_8_2(W(1,4),W(1,1),W(1,2),GC_473,GC_590
     $ ,GC_576,GC_593,GC_178,GC_474,MDL_MT,MDL_WT,W(1,15))
C     Amplitude(s) for diagram number 125
      CALL FFV6_0(W(1,25),W(1,3),W(1,16),GC_2,AMP(127))
      CALL FFV6_0(W(1,15),W(1,3),W(1,16),GC_2,AMP(128))
C     Amplitude(s) for diagram number 126
      CALL FFV2_8_0(W(1,25),W(1,3),W(1,20),GC_651,GC_660,AMP(129))
      CALL FFV2_8_0(W(1,15),W(1,3),W(1,20),GC_651,GC_660,AMP(130))
      CALL FFFF10_14_18_19_6_8_4(W(1,4),W(1,3),W(1,1),GC_471,GC_589
     $ ,GC_575,GC_592,GC_150,GC_472,ZERO,ZERO,W(1,15))
      CALL FFFF10_14_18_19_6_8_4(W(1,4),W(1,3),W(1,1),GC_473,GC_590
     $ ,GC_576,GC_593,GC_178,GC_474,ZERO,ZERO,W(1,25))
C     Amplitude(s) for diagram number 127
      CALL FFV1_0(W(1,15),W(1,2),W(1,16),GC_2,AMP(131))
      CALL FFV1_0(W(1,25),W(1,2),W(1,16),GC_2,AMP(132))
C     Amplitude(s) for diagram number 128
      CALL FFV2_8_0(W(1,15),W(1,2),W(1,20),GC_651,GC_660,AMP(133))
      CALL FFV2_8_0(W(1,25),W(1,2),W(1,20),GC_651,GC_660,AMP(134))
      CALL FFFF10_14_18_19_6_8_3(W(1,4),W(1,3),W(1,2),GC_471,GC_589
     $ ,GC_575,GC_592,GC_150,GC_472,ZERO,ZERO,W(1,25))
      CALL FFFF10_14_18_19_6_8_3(W(1,4),W(1,3),W(1,2),GC_473,GC_590
     $ ,GC_576,GC_593,GC_178,GC_474,ZERO,ZERO,W(1,15))
C     Amplitude(s) for diagram number 129
      CALL FFV1_0(W(1,1),W(1,25),W(1,16),GC_2,AMP(135))
      CALL FFV1_0(W(1,1),W(1,15),W(1,16),GC_2,AMP(136))
C     Amplitude(s) for diagram number 130
      CALL FFV2_8_0(W(1,1),W(1,25),W(1,20),GC_651,GC_660,AMP(137))
      CALL FFV2_8_0(W(1,1),W(1,15),W(1,20),GC_651,GC_660,AMP(138))
      JAMP(1)=-AMP(1)-AMP(2)-AMP(3)-AMP(4)-AMP(5)-AMP(6)-AMP(7)-AMP(8)
     $ -AMP(9)-AMP(10)-AMP(11)-AMP(12)-AMP(13)-AMP(14)-AMP(15)-AMP(16)
     $ -AMP(17)-AMP(18)-AMP(19)-AMP(20)-AMP(21)-AMP(22)-AMP(23)-AMP(24)
     $ -AMP(25)-AMP(26)-AMP(27)-AMP(28)-AMP(29)-AMP(30)-AMP(31)-AMP(32)
     $ -AMP(33)-AMP(34)-AMP(35)-AMP(36)-AMP(37)-AMP(38)-AMP(39)-AMP(40)
     $ +1D0/6D0*AMP(41)+1D0/6D0*AMP(42)+1D0/6D0*AMP(43)+1D0/6D0*AMP(44)
     $ +1D0/6D0*AMP(45)+1D0/6D0*AMP(46)+1D0/6D0*AMP(47)+1D0/6D0*AMP(48)
     $ +1D0/6D0*AMP(49)+1D0/6D0*AMP(50)+1D0/6D0*AMP(51)+1D0/6D0*AMP(52)
     $ +1D0/6D0*AMP(53)+1D0/6D0*AMP(54)+1D0/6D0*AMP(55)+1D0/6D0*AMP(56)
     $ -AMP(57)-AMP(58)-AMP(59)-AMP(60)-AMP(61)-AMP(62)-AMP(63)-AMP(64)
     $ -AMP(65)-AMP(66)-AMP(67)-AMP(68)-AMP(69)-AMP(70)-AMP(71)-AMP(72)
     $ -AMP(73)-AMP(74)-AMP(75)-AMP(76)-AMP(77)-AMP(78)-AMP(79)-AMP(80)
     $ -AMP(81)-AMP(82)-AMP(83)-AMP(84)-AMP(85)+1D0/6D0*AMP(86)-AMP(87)
     $ -AMP(88)+1D0/6D0*AMP(89)-AMP(90)-AMP(91)-AMP(92)-AMP(93)-AMP(94)
     $ -AMP(95)-AMP(96)-AMP(97)-AMP(98)-AMP(99)-AMP(100)-AMP(101)
     $ -AMP(102)-AMP(103)-AMP(104)-AMP(105)-AMP(106)-AMP(107)-AMP(108)
     $ -AMP(109)-AMP(110)-AMP(111)-AMP(112)-AMP(113)-AMP(114)+1D0/6D0
     $ *AMP(115)+1D0/6D0*AMP(116)+1D0/6D0*AMP(117)+1D0/6D0*AMP(118)
     $ +1D0/6D0*AMP(119)+1D0/6D0*AMP(120)+1D0/6D0*AMP(121)+1D0/6D0
     $ *AMP(122)+1D0/6D0*AMP(124)-AMP(123)+1D0/6D0*AMP(126)-AMP(125)
     $ +1D0/6D0*AMP(128)-AMP(127)+1D0/6D0*AMP(130)-AMP(129)+1D0/6D0
     $ *AMP(132)-AMP(131)+1D0/6D0*AMP(134)-AMP(133)+1D0/6D0*AMP(136)
     $ -AMP(135)+1D0/6D0*AMP(138)-AMP(137)
      JAMP(2)=+1D0/2D0*(-AMP(41)-AMP(42)-AMP(43)-AMP(44)-AMP(45)
     $ -AMP(46)-AMP(47)-AMP(48)-AMP(49)-AMP(50)-AMP(51)-AMP(52)-AMP(53)
     $ -AMP(54)-AMP(55)-AMP(56)-AMP(86)-AMP(89)-AMP(115)-AMP(116)
     $ -AMP(117)-AMP(118)-AMP(119)-AMP(120)-AMP(121)-AMP(122)-AMP(124)
     $ -AMP(126)-AMP(128)-AMP(130)-AMP(132)-AMP(134)-AMP(136)-AMP(138))

      M91_MATRIX = 0.D0
      DO I = 1, NCOLOR
        ZTEMP = (0.D0,0.D0)
        DO J = 1, NCOLOR
          ZTEMP = ZTEMP + CF(J,I)*JAMP(J)
        ENDDO
        M91_MATRIX = M91_MATRIX+ZTEMP*DCONJG(JAMP(I))/DENOM(I)
      ENDDO

      END

      SUBROUTINE M91_GET_VALUE(P, ALPHAS, NHEL ,ANS)
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
        CALL M91_SMATRIXHEL(P, NHEL, ANS)
      ELSE
        CALL M91_SMATRIX(P, ANS)
      ENDIF
      RETURN
      END

      SUBROUTINE M91_INITIALISEMODEL(PATH)
C     ROUTINE FOR F2PY to read the benchmark point.    
      IMPLICIT NONE
      CHARACTER*512 PATH
CF2PY INTENT(IN) :: PATH
      CALL SETPARA(PATH)  !first call to setup the paramaters    
      RETURN
      END

      LOGICAL FUNCTION M91_IS_BORN_HEL_SELECTED(HELID)
      IMPLICIT NONE
C     
C     CONSTANTS
C     
      INTEGER    NEXTERNAL
      PARAMETER (NEXTERNAL=6)
      INTEGER    NCOMB
      PARAMETER (NCOMB=64)
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
      COMMON/M91_PROCESS_NHEL/HELC

      INTEGER POLARIZATIONS(0:NEXTERNAL,0:5)
      COMMON/M91_BORN_BEAM_POL/POLARIZATIONS
C     ----------
C     BEGIN CODE
C     ----------

      M91_IS_BORN_HEL_SELECTED = .TRUE.
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
          M91_IS_BORN_HEL_SELECTED = .FALSE.
          RETURN
        ENDIF
      ENDDO

      RETURN
      END

