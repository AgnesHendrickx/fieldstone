!==================================================================================================!
!==================================================================================================!
!                                                                                                  !
! ELEFANT                                                                        C. Thieulot       !
!                                                                                                  !
!==================================================================================================!
!==================================================================================================!

subroutine name

!use module_parameters
!use module_mesh 
!use module_constants
!use module_swarm
!use module_materials
use module_timing

implicit none


!==================================================================================================!
!==================================================================================================!
!@@ \subsubsection{template}
!@@
!==================================================================================================!

if (iproc==0) then

call system_clock(counti,count_rate)

!==============================================================================!











!==============================================================================!

call system_clock(countf) ; elapsed=dble(countf-counti)/dble(count_rate)

write(*,'(a,f6.2,a)') 'name (',elapsed,' s)'

end if ! iproc

end subroutine

!==================================================================================================!
!==================================================================================================!
