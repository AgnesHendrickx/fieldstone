!==================================================================================================!
!==================================================================================================!
!                                                                                                  !
! ELEFANT                                                                        C. Thieulot       !
!                                                                                                  !
!==================================================================================================!
!==================================================================================================!

subroutine write_stats

use global_parameters
use global_measurements
use timing

implicit none


!==================================================================================================!
!==================================================================================================!
!@@ \subsubsection{write\_stats}
!@@ This subroutine writes in fort.1234 various statistics (istep, time, vrms, averages, 
!@@ errors, ...) 
!==================================================================================================!

if (iproc==0) then

call system_clock(counti,count_rate)

!==============================================================================!


write(1234,'(i4,es12.4,i7,9es12.4)') istep,time,nel,vrms,errv,errp,errq,&
              volume,avrg_u,avrg_v,avrg_w,avrg_p

call flush(1234)

!==============================================================================!

call system_clock(countf) ; elapsed=dble(countf-counti)/dble(count_rate)

write(*,'(a,f6.2,a)') 'write_stats (',elapsed,' s)'

end if ! iproc

end subroutine

!==================================================================================================!
!==================================================================================================!
