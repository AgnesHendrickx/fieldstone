!==================================================================================================!
!==================================================================================================!
!                                                                                                  !
! ELEFANT                                                                        C. Thieulot       !
!                                                                                                  !
!==================================================================================================!
!==================================================================================================!

subroutine solve_cg_diagprec(N,NZ,mat,ia,ja,guess,rhs,diag)

implicit none

integer, intent(in) :: N,NZ
integer, intent(in) :: ia(N+1),ja(NZ)
real(8), intent(in) :: mat(NZ)  
real(8), intent(inout) :: guess(N)  
real(8), intent(in) :: rhs(N)  
real(8), intent(in) :: diag(N)  

integer, parameter :: nitermax=1000
real(8), parameter :: rtol=1.d-6

integer iter
real(8) alpha,beta,tol2,rhs_norm,gammma,ZR,ZZRR
real(8) R(N),RR(N),P(N),phi(N),Z(N),ZZ(N)

!==================================================================================================!
!==================================================================================================!
!@@ \subsubsection{solve\_cg\_diagprec}
!@@ The subroutine solves $A\cdot = b$ by means f the preconditioned Conjugate Gradient method
!@@ and the implementation follows algorithm 2.2 on page 82 of Elman, Silvester \&
!@@ Wathen \cite{elsw}:
!@@ 
!@@ Choose ${\vec u}^{(0)}$, compute ${\vec \phi}^{(0)}={\bm A}\cdot {\vec u}^{(0)}$ 
!@@ then ${\vec r}^{(0)}={\vec f}-{\vec \phi}^{(0)}$, 
!@@ ${\vec z}^{(0)}={\bm M}^{-1}\cdot {\vec r}^{(0)}$ and set ${\vec p}^{(0)}={\vec z}^{(0)}$.
!@@ 
!@@ For $k=0$ until convergence do
!@@ \begin{itemize}
!@@ \item ${\vec \phi}^{(k)}={\bm A}\cdot {\vec p}^{(k)}$
!@@ \item compute $\alpha_k = <{\vec z}^{(k)},{\vec r}^{(k)}>/<{\vec \phi}^{(k)},{\vec p}^{(k)}>$
!@@ \item ${\vec u}^{(k+1)}={\vec u}^{(k)}+\alpha_k {\vec p}^{(k)}$
!@@ \item ${\vec r}^{(k+1)}={\vec r}^{(k)}-\alpha_k{\vec \phi}^{(k)}$
!@@ \item test for convergence
!@@ \item ${\vec z}^{(k+1)}=M^{-1} {\vec r}^{(k+1)}$
!@@ \item $\beta_k= <{\vec z}^{(k+1)},{\vec r}^{(k+1)}>/<{\vec z}^{(k)},{\vec r}^{(k)}>$
!@@ \item ${\vec p}^{(k+1)}={\vec z}^{(k+1)}+\beta_k {\vec p}^{(k)}$
!@@ \end{itemize}
!@@ The convergence test is $\| \vec{r}_{k+1} \|_2/ \| \vec{r}_{k+1} \|_2 < tol$, 
!@@ the maximum number of iterations is set to 1000, and the relative tolerance to $tol=10^{-6}$.
!@@ Since the preconditioned is the diagonal of the ${\bm A}$ matrix, then the inverse of 
!@@ ${\bm M}$ is trivial to compute/apply. 
!==================================================================================================!

tol2=rtol**2 

rhs_norm=dot_product(rhs,rhs)

!------------------------------------------------

call spmv_symm (N,NZ,guess,phi,mat,ja,ia)

R=rhs-phi

Z=R/diag

P=Z
   
ZR=dot_product(Z,R)

do iter=1,nitermax

   ! compute phi_k=A.P_k

   call spmv_symm (N,NZ,P,phi,mat,ja,ia)

   ! compute alpha

   alpha=ZR/dot_product(phi,P)

   guess=guess+alpha*P

   RR=R-alpha*phi

   ! test for convergence

   gammma=dot_product(RR,RR)/rhs_norm 

   !print *,gammma

   if (gammma < tol2) then
      write(*,'(a,i4)') '        inner solver:',iter
      exit   
   end if
  
   ZZ=RR/diag

   ZZRR=dot_product(ZZ,RR)

   ! compute beta

   beta=ZZRR/ZR

   P=ZZ+beta*P

   ! update

   R=RR
   Z=ZZ
   ZR=ZZRR

end do

if (iter==nitermax+1) stop 'conv. not reached'

end subroutine

!==================================================================================================!
!==================================================================================================!
