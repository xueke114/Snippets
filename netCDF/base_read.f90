! 需要同时链接netcdff.lib和netcdf.lib
PROGRAM testnc
USE netcdf
IMPLICIT NONE
INTEGER :: ncid, status
!real :: value
CHARACTER(len=*),parameter:: ncfile = "C:\Datasets\20220201120000-UKMO-L4_GHRSST-SSTfnd-OSTIA-GLOB-v02.0-fv02.0.nc"
status = nf90_open(ncfile, nf90_nowrite, ncid)

call list_all_var(ncid)

END PROGRAM

SUBROUTINE list_all_var(fid)
use netcdf
IMPLICIT NONE
integer,Intent(IN) :: fid
integer :: nVars,res,varid
character(len=20)::var_name
res=nf90_inquire(fid,nVariables=nvars)
print *,"所有变量:"
do varid=1,nVars
    res= nf90_inquire_variable(fid,varid,name=var_name)
    print *, varid,". ",var_name
end do
END SUBROUTINE