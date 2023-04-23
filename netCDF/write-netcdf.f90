program write_netcdf
   use netcdf
   implicit none
   integer fid, xDimID, yDimID, faceID
   integer status, I, data(5, 4)

   ! 生成数据矩阵
   data = reshape((/(I, I=1, 20)/), (/5, 4/))
   print '(5I4)', data

   ! 创建文件
   status = nf90_create("testnc.nc", NF90_NETCDF4, fid)

   ! 创建维度
   status = nf90_def_dim(fid, "x", 5, xDimID)
   status = nf90_def_dim(fid, "y", 4, yDimID)

   ! 创建变量
   status = nf90_def_var(fid, "face", NF90_INT, (/xDimID, yDimID/), faceID)

   ! 结束属性定义
   status = nf90_enddef(fid)

   ! 向变量中写入值
   status = nf90_put_var(fid, faceID, data)

   ! 写入数据
   status = nf90_close(fid)

end program write_netcdf
