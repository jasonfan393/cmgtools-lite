ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      written by the UFO converter
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      SUBROUTINE COUP4()

      IMPLICIT NONE
      INCLUDE 'model_functions.inc'

      DOUBLE PRECISION PI, ZERO
      PARAMETER  (PI=3.141592653589793D0)
      PARAMETER  (ZERO=0D0)
      INCLUDE 'input.inc'
      INCLUDE 'coupl.inc'
      GC_336 = MDL_CTLTI1/MDL_LAMBDA__EXP__2+(MDL_CTLT1*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_337 = -(MDL_CTLSI1/MDL_LAMBDA__EXP__2)+(4.000000D+00
     $ *MDL_CTLTI1)/MDL_LAMBDA__EXP__2+(MDL_CTLS1*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2-(4.000000D+00*MDL_CTLT1*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_338 = -(MDL_CTLSI1/MDL_LAMBDA__EXP__2)+(4.000000D+00
     $ *MDL_CTLTI1)/MDL_LAMBDA__EXP__2-(MDL_CTLS1*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2+(4.000000D+00*MDL_CTLT1*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_339 = MDL_CTLSI2/MDL_LAMBDA__EXP__2-(4.000000D+00*MDL_CTLTI2)
     $ /MDL_LAMBDA__EXP__2+(MDL_CTLS2*MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
     $ -(4.000000D+00*MDL_CTLT2*MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_340 = MDL_CTLSI2/MDL_LAMBDA__EXP__2-(4.000000D+00*MDL_CTLTI2)
     $ /MDL_LAMBDA__EXP__2-(MDL_CTLS2*MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
     $ +(4.000000D+00*MDL_CTLT2*MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_341 = -(MDL_CTLTI2/MDL_LAMBDA__EXP__2)-(MDL_CTLT2
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_342 = -(MDL_CTLTI2/MDL_LAMBDA__EXP__2)+(MDL_CTLT2
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_343 = MDL_CTLTI2/MDL_LAMBDA__EXP__2-(MDL_CTLT2*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_344 = MDL_CTLTI2/MDL_LAMBDA__EXP__2+(MDL_CTLT2*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_345 = -(MDL_CTLSI2/MDL_LAMBDA__EXP__2)+(4.000000D+00
     $ *MDL_CTLTI2)/MDL_LAMBDA__EXP__2+(MDL_CTLS2*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2-(4.000000D+00*MDL_CTLT2*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_346 = -(MDL_CTLSI2/MDL_LAMBDA__EXP__2)+(4.000000D+00
     $ *MDL_CTLTI2)/MDL_LAMBDA__EXP__2-(MDL_CTLS2*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2+(4.000000D+00*MDL_CTLT2*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_347 = MDL_CTLSI3/MDL_LAMBDA__EXP__2-(4.000000D+00*MDL_CTLTI3)
     $ /MDL_LAMBDA__EXP__2+(MDL_CTLS3*MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
     $ -(4.000000D+00*MDL_CTLT3*MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_348 = MDL_CTLSI3/MDL_LAMBDA__EXP__2-(4.000000D+00*MDL_CTLTI3)
     $ /MDL_LAMBDA__EXP__2-(MDL_CTLS3*MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
     $ +(4.000000D+00*MDL_CTLT3*MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_349 = -(MDL_CTLTI3/MDL_LAMBDA__EXP__2)-(MDL_CTLT3
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_350 = -(MDL_CTLTI3/MDL_LAMBDA__EXP__2)+(MDL_CTLT3
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_351 = MDL_CTLTI3/MDL_LAMBDA__EXP__2-(MDL_CTLT3*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_352 = MDL_CTLTI3/MDL_LAMBDA__EXP__2+(MDL_CTLT3*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_353 = -(MDL_CTLSI3/MDL_LAMBDA__EXP__2)+(4.000000D+00
     $ *MDL_CTLTI3)/MDL_LAMBDA__EXP__2+(MDL_CTLS3*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2-(4.000000D+00*MDL_CTLT3*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_354 = -(MDL_CTLSI3/MDL_LAMBDA__EXP__2)+(4.000000D+00
     $ *MDL_CTLTI3)/MDL_LAMBDA__EXP__2-(MDL_CTLS3*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2+(4.000000D+00*MDL_CTLT3*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_471 = -(MDL_CTQQU1I/MDL_LAMBDA__EXP__2)+(MDL_CTQQU1
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_472 = MDL_CTQQU1I/MDL_LAMBDA__EXP__2+(MDL_CTQQU1*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_473 = -(MDL_CTQQU8I/MDL_LAMBDA__EXP__2)+(MDL_CTQQU8
     $ *MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_474 = MDL_CTQQU8I/MDL_LAMBDA__EXP__2+(MDL_CTQQU8*MDL_COMPLEXI)
     $ /MDL_LAMBDA__EXP__2
      GC_559 = (MDL_CQD1*MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      GC_560 = (MDL_CQD8*MDL_COMPLEXI)/MDL_LAMBDA__EXP__2
      END
