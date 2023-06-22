ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      written by the UFO converter
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      SUBROUTINE COUP2()

      IMPLICIT NONE
      INCLUDE 'model_functions.inc'

      DOUBLE PRECISION PI, ZERO
      PARAMETER  (PI=3.141592653589793D0)
      PARAMETER  (ZERO=0D0)
      INCLUDE 'input.inc'
      INCLUDE 'coupl.inc'
      GC_68 = -(MDL_CQBQU8TI/MDL_LAMBDA__EXP__2)-(MDL_CQBQU8T
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_69 = -(MDL_CQBQU8TI/MDL_LAMBDA__EXP__2)+(MDL_CQBQU8T
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_70 = MDL_CQBQU8TI/MDL_LAMBDA__EXP__2-(MDL_CQBQU8T
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_71 = MDL_CQBQU8TI/MDL_LAMBDA__EXP__2+(MDL_CQBQU8T
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_73 = -(MDL_CQBQU8I/MDL_LAMBDA__EXP__2)+(4.000000D+00
     $ *MDL_CQBQU8TI)/MDL_LAMBDA__EXP__2-(MDL_CQBQU8*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2+(4.000000D+00*MDL_CQBQU8T*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_200 = MDL_CQTQD1I/MDL_LAMBDA__EXP__2-(4.000000D+00
     $ *MDL_CQTQD1TI)/MDL_LAMBDA__EXP__2-(MDL_CQTQD1*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2+(4.000000D+00*MDL_CQTQD1T*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_201 = -(MDL_CQTQD1TI/MDL_LAMBDA__EXP__2)-(MDL_CQTQD1T
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_202 = -(MDL_CQTQD1TI/MDL_LAMBDA__EXP__2)+(MDL_CQTQD1T
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_203 = MDL_CQTQD1TI/MDL_LAMBDA__EXP__2-(MDL_CQTQD1T
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_204 = MDL_CQTQD1TI/MDL_LAMBDA__EXP__2+(MDL_CQTQD1T
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_206 = -(MDL_CQTQD1I/MDL_LAMBDA__EXP__2)+(4.000000D+00
     $ *MDL_CQTQD1TI)/MDL_LAMBDA__EXP__2-(MDL_CQTQD1*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2+(4.000000D+00*MDL_CQTQD1T*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_208 = MDL_CQTQD8I/MDL_LAMBDA__EXP__2-(4.000000D+00
     $ *MDL_CQTQD8TI)/MDL_LAMBDA__EXP__2-(MDL_CQTQD8*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2+(4.000000D+00*MDL_CQTQD8T*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_209 = -(MDL_CQTQD8TI/MDL_LAMBDA__EXP__2)-(MDL_CQTQD8T
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_210 = -(MDL_CQTQD8TI/MDL_LAMBDA__EXP__2)+(MDL_CQTQD8T
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_211 = MDL_CQTQD8TI/MDL_LAMBDA__EXP__2-(MDL_CQTQD8T
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_212 = MDL_CQTQD8TI/MDL_LAMBDA__EXP__2+(MDL_CQTQD8T
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_214 = -(MDL_CQTQD8I/MDL_LAMBDA__EXP__2)+(4.000000D+00
     $ *MDL_CQTQD8TI)/MDL_LAMBDA__EXP__2-(MDL_CQTQD8*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2+(4.000000D+00*MDL_CQTQD8T*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_471 = -(MDL_CTQQU1I/MDL_LAMBDA__EXP__2)+(MDL_CTQQU1
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_472 = MDL_CTQQU1I/MDL_LAMBDA__EXP__2+(MDL_CTQQU1*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_473 = -(MDL_CTQQU8I/MDL_LAMBDA__EXP__2)+(MDL_CTQQU8
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_474 = MDL_CTQQU8I/MDL_LAMBDA__EXP__2+(MDL_CTQQU8*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_475 = -(MDL_CTWI/MDL_LAMBDA__EXP__2)+(MDL_CTW*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_476 = MDL_CTWI/MDL_LAMBDA__EXP__2+(MDL_CTW*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_570 = (2.000000D+00*MDL_CQQ13*MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_572 = (2.000000D+00*MDL_CQQ83*MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      END
