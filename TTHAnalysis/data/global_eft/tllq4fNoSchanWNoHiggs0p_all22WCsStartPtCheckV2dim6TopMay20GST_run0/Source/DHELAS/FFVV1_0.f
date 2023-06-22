C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     Gamma(3,2,-2)*Gamma(4,-2,-1)*ProjM(-1,1) - Gamma(3,-2,-1)*Gamma(4
C     ,2,-2)*ProjM(-1,1)
C     
      SUBROUTINE FFVV1_0(F1, F2, V3, V4, COUP,VERTEX)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 V3(*)
      COMPLEX*16 TMP10
      COMPLEX*16 F1(*)
      COMPLEX*16 V4(*)
      COMPLEX*16 F2(*)
      COMPLEX*16 VERTEX
      COMPLEX*16 COUP
      COMPLEX*16 TMP9
      TMP9 = (F1(3)*(F2(3)*(V3(3)*(V4(3)+V4(6))+(V3(4)*(-1D0)*(V4(4)
     $ +CI*(V4(5)))+(V3(5)*(+CI*(V4(4))-V4(5))-V3(6)*(V4(3)+V4(6)))))
     $ +F2(4)*(V3(3)*(V4(4)+CI*(V4(5)))+(V3(4)*(-1D0)*(V4(3)+V4(6))
     $ +(V3(5)*(-1D0)*(+CI*(V4(3)+V4(6)))+V3(6)*(V4(4)+CI*(V4(5)))))))
     $ +F1(4)*(F2(3)*(V3(3)*(V4(4)-CI*(V4(5)))+(V3(4)*(V4(6)-V4(3))
     $ +(V3(5)*(-CI*(V4(6))+CI*(V4(3)))+V3(6)*(+CI*(V4(5))-V4(4)))))
     $ +F2(4)*(V3(3)*(V4(3)-V4(6))+(V3(4)*(+CI*(V4(5))-V4(4))+(V3(5)*(
     $ -1D0)*(V4(5)+CI*(V4(4)))+V3(6)*(V4(3)-V4(6)))))))
      TMP10 = (F1(3)*(F2(3)*(V3(3)*(V4(3)-V4(6))+(V3(4)*(+CI*(V4(5))
     $ -V4(4))+(V3(5)*(-1D0)*(V4(5)+CI*(V4(4)))+V3(6)*(V4(3)-V4(6)))))
     $ +F2(4)*(V3(3)*(-1D0)*(V4(4)+CI*(V4(5)))+(V3(4)*(V4(3)+V4(6))
     $ +(V3(5)*(+CI*(V4(3)+V4(6)))-V3(6)*(V4(4)+CI*(V4(5)))))))+F1(4)
     $ *(F2(3)*(V3(3)*(+CI*(V4(5))-V4(4))+(V3(4)*(V4(3)-V4(6))+(V3(5)
     $ *(-CI*(V4(3))+CI*(V4(6)))+V3(6)*(V4(4)-CI*(V4(5))))))+F2(4)
     $ *(V3(3)*(V4(3)+V4(6))+(V3(4)*(-1D0)*(V4(4)+CI*(V4(5)))+(V3(5)*(
     $ +CI*(V4(4))-V4(5))-V3(6)*(V4(3)+V4(6)))))))
      VERTEX = COUP*(-CI*(TMP9)+CI*(TMP10))
      END


C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     Gamma(3,2,-2)*Gamma(4,-2,-1)*ProjM(-1,1) - Gamma(3,-2,-1)*Gamma(4
C     ,2,-2)*ProjM(-1,1)
C     
      SUBROUTINE FFVV1_3_0(F1, F2, V3, V4, COUP1, COUP2,VERTEX)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 COUP2
      COMPLEX*16 V3(*)
      COMPLEX*16 F1(*)
      COMPLEX*16 V4(*)
      COMPLEX*16 COUP1
      COMPLEX*16 F2(*)
      COMPLEX*16 VERTEX
      COMPLEX*16 TMP
      CALL FFVV1_0(F1,F2,V3,V4,COUP1,VERTEX)
      CALL FFVV3_0(F1,F2,V3,V4,COUP2,TMP)
      VERTEX = VERTEX + TMP
      END


