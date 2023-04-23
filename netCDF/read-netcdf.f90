program read_netcdf
   use netcdf
   implicit none

   integer fid, varid, status
   integer data(5, 4)

   ! 只读模式打开文件
   status = nf90_open("testnc.nc", NF90_NOWRITE, fid)

   ! 查询变量的id
   status = nf90_inq_varid(fid, "face", varid)

   ! 根据变量id读取变量值
   status = nf90_get_var(fid, varid, data)

   ! 输出变量值
   print '(5I4)', data

   ! 关闭文件
   status = nf90_close(fid)

end program read_netcdf

