    ! VS + Intel Fortran 读HDF5文件

    PROGRAM HDF5Demo
    USE HDF5
    IMPLICIT NONE

    !!!!!!!!!!!
    ! 定义变量 !
    !!!!!!!!!!!
    character(LEN=*), parameter    :: in_filename = "Assets/FY3D_MWRIA_GBAL_L1_20220301_0242_010KM_MS.HDF"
    character(LEN=*), parameter    :: ds_name = "Geolocation/Latitude"
    INTEGER(HID_T)                 :: file_id, ds_id, space_id
    INTEGER(HSIZE_T), DIMENSION(3) :: real_dims, max_dims
    INTEGER(HSIZE_T), DIMENSION(2) :: geo_dims
    REAL            , ALLOCATABLE  :: lat_data(:,:)
    INTEGER                        :: error_flag

    ! 读文件
    !! 建立句柄
    call h5open_f(error_flag)
    call h5fopen_f(in_filename, H5F_ACC_RDONLY_F, file_id, error_flag)
    !! 打开ds
    call h5dopen_f(file_id, ds_name, ds_id, error_flag)
    !! 获取ds形状
    CALL h5dget_space_f(ds_id, space_id, error_flag)
    CALL h5sget_simple_extent_dims_f(space_id, real_dims, max_dims, error_flag)
    CALL h5sclose_f(space_id, error_flag)
    !! 为ds分配空间
    ALLOCATE(lat_data(real_dims(1), real_dims(2)))
    !! 读取ds
    geo_dims = [real_dims(1),real_dims(2)]
    CALL h5dread_f(ds_id, H5T_NATIVE_REAL, lat_data, geo_dims, error_flag)
    !! 输出第一列的前5行
    print*,lat_data(1,1:5)


    !! 关闭句柄
    DEALLOCATE(lat_data)
    call h5dclose_f(ds_id, error_flag)
    call h5fclose_f(file_id, error_flag)
    call h5close_f(error_flag)
    
    END PROGRAM