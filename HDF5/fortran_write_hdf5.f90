program write_hdf5
    use hdf5
    implicit none

    character(len=*), parameter    :: filename="testh5.h5"
    character(len=*), parameter    :: dsname="face"
    integer(HID_T)                 :: file_id
    integer(HID_T)                 :: ds_id
    integer(HID_T)                 :: space_id
    integer(HSIZE_T), dimension(2) :: dims = (/6,4/)
    real            , dimension(2) :: out_data(6,4)
    integer                        :: error_flag

    !> 创建数据
    call random_number(out_data)
    print '(6I4)', floor(out_data*100)

    !> 打开hdf5接口
    call h5open_f(error_flag)

    !> 创建文件
    call h5fcreate_f(filename, H5F_ACC_TRUNC_F, file_id, error_flag)

    !> 创建数据集的形状
    call h5screate_simple_f(2, dims, space_id, error_flag)

    !> 创建数据集
    call h5dcreate_f(file_id, dsname, H5T_NATIVE_INTEGER, space_id, ds_id, error_flag)

    !> 向数据集写数据
    call h5dwrite_f(ds_id, H5T_NATIVE_INTEGER, floor(out_data*100), dims, error_flag)

    !> 关闭打开状态
    call h5dclose_f(ds_id, error_flag)
    call h5sclose_f(space_id, error_flag)
    call h5fclose_f(file_id, error_flag)
    call h5close_f(error_flag)
end program
