ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      written by the UFO converter
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      SUBROUTINE COUP3()

      IMPLICIT NONE
      INCLUDE 'model_functions.inc'

      DOUBLE PRECISION PI, ZERO
      PARAMETER  (PI=3.141592653589793D0)
      PARAMETER  (ZERO=0D0)
      INCLUDE 'input.inc'
      INCLUDE 'coupl.inc'
      GC_175 = (MDL_CQQ1*MDL_COMPLEXI)/MDL_LAMBDA__EXP__2-(MDL_CQQ8
     $ *MDL_COMPLEXI)/(6.000000D+00*MDL_LAMBDA__EXP__2)
      GC_176 = (MDL_CQQ1*MDL_COMPLEXI)/MDL_LAMBDA__EXP__2+(MDL_CQQ8
     $ *MDL_COMPLEXI)/(3.000000D+00*MDL_LAMBDA__EXP__2)
      GC_177 = (MDL_CQQ81*MDL_COMPLEXI)/MDL_LAMBDA__EXP__2-(MDL_CQQ83
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_178 = (MDL_CQQ81*MDL_COMPLEXI)/MDL_LAMBDA__EXP__2+(MDL_CQQ83
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_191 = -(MDL_CQTQB1I/MDL_LAMBDA__EXP__2)-(MDL_CQTQB1
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_192 = -(MDL_CQTQB1I/MDL_LAMBDA__EXP__2)+(MDL_CQTQB1
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_193 = MDL_CQTQB1I/MDL_LAMBDA__EXP__2-(MDL_CQTQB1*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_194 = MDL_CQTQB1I/MDL_LAMBDA__EXP__2+(MDL_CQTQB1*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_195 = -(MDL_CQTQB8I/MDL_LAMBDA__EXP__2)-(MDL_CQTQB8
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_196 = -(MDL_CQTQB8I/MDL_LAMBDA__EXP__2)+(MDL_CQTQB8
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_197 = MDL_CQTQB8I/MDL_LAMBDA__EXP__2-(MDL_CQTQB8*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_198 = MDL_CQTQB8I/MDL_LAMBDA__EXP__2+(MDL_CQTQB8*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_199 = MDL_CQTQD1I/MDL_LAMBDA__EXP__2-(4.000000D+00
     $ *MDL_CQTQD1TI)/MDL_LAMBDA__EXP__2+(MDL_CQTQD1*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2-(4.000000D+00*MDL_CQTQD1T*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_201 = -(MDL_CQTQD1TI/MDL_LAMBDA__EXP__2)-(MDL_CQTQD1T
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_202 = -(MDL_CQTQD1TI/MDL_LAMBDA__EXP__2)+(MDL_CQTQD1T
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_203 = MDL_CQTQD1TI/MDL_LAMBDA__EXP__2-(MDL_CQTQD1T
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_204 = MDL_CQTQD1TI/MDL_LAMBDA__EXP__2+(MDL_CQTQD1T
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_205 = -(MDL_CQTQD1I/MDL_LAMBDA__EXP__2)+(4.000000D+00
     $ *MDL_CQTQD1TI)/MDL_LAMBDA__EXP__2+(MDL_CQTQD1*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2-(4.000000D+00*MDL_CQTQD1T*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_207 = MDL_CQTQD8I/MDL_LAMBDA__EXP__2-(4.000000D+00
     $ *MDL_CQTQD8TI)/MDL_LAMBDA__EXP__2+(MDL_CQTQD8*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2-(4.000000D+00*MDL_CQTQD8T*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_209 = -(MDL_CQTQD8TI/MDL_LAMBDA__EXP__2)-(MDL_CQTQD8T
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_210 = -(MDL_CQTQD8TI/MDL_LAMBDA__EXP__2)+(MDL_CQTQD8T
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_211 = MDL_CQTQD8TI/MDL_LAMBDA__EXP__2-(MDL_CQTQD8T
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_212 = MDL_CQTQD8TI/MDL_LAMBDA__EXP__2+(MDL_CQTQD8T
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_213 = -(MDL_CQTQD8I/MDL_LAMBDA__EXP__2)+(4.000000D+00
     $ *MDL_CQTQD8TI)/MDL_LAMBDA__EXP__2+(MDL_CQTQD8*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2-(4.000000D+00*MDL_CQTQD8T*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_471 = -(MDL_CTQQU1I/MDL_LAMBDA__EXP__2)+(MDL_CTQQU1
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      END