! 测试使用Fortan & openMP多线程，逐像元计算MERSI SST正弦值的耗时
! 每个MERSI SST文件的像元数3600x7200
! 在联想小新Air 13Pro上，纯Fortran方法耗时57秒，OpenMP方法耗时24秒
! 编译指令
! gfortran OpenMP加速内部函数.f90 -I /mingw64/include -lhdf5 -lhdf5_fortran
! gfortran OpenMP加速内部函数.f90 -I /mingw64/include -lhdf5 -lhdf5_fortran -fopenmp
PROGRAM testHDF5Performance
    USE hdf5
    IMPLICIT NONE

    ! 定义变量
    INTEGER                           :: error_flag, I, io
    INTEGER            , ALLOCATABLE  :: sst_data(:,:)
    REAL               , ALLOCATABLE  :: result_data(:,:)
    INTEGER(HID_T)                    :: file_id, ds_id, space_id
    INTEGER(HSIZE_T)   , DIMENSION(2) :: real_dims, max_dims
    CHARACTER(LEN=100)                :: filename
    CHARACTER(LEN=*)   , PARAMETER    :: infile_dbfile="C:\Datasets\FY3D-MERSI-SST\day\202206\filenames.txt"

    ! 准备工作
    CALL h5open_f(error_flag)
    OPEN(UNIT=90, FILE=infile_dbfile)
    ! 遍历HDF5文件
    DO
        READ(unit=90, fmt=*, iostat=io)filename
        IF (io/=0) EXIT
        print*,filename
        ! 打开数据集
        CALL h5fopen_f(filename,H5F_ACC_RDONLY_F,file_id,error_flag)
        CALL h5dopen_f(file_id,"sea_surface_temperature",ds_id,error_flag)
        ! 获取数据形状
        CALL h5dget_space_f(ds_id, space_id, error_flag)
        CALL h5sget_simple_extent_dims_f(space_id, real_dims, max_dims, error_flag)
        CALL h5sclose_f(space_id, error_flag)
        print*,real_dims
        ! 为数据集分配空间
        ALLOCATE(sst_data(real_dims(1),real_dims(2)))
        ALLOCATE(result_data(real_dims(1),real_dims(2)))
        ! 读取sst数据
        CALL h5dread_f(ds_id, H5T_NATIVE_INTEGER, sst_data, real_dims, error_flag)
        result_data=REAL(sst_data)
        ! 进行计算
        !$OMP PARALLEL WORKSHARE
        result_data=SIN(result_data)
        !$OMP END PARALLEL WORKSHARE
        ! 输出指定位置上的值
        print*,sst_data(1,401),result_data(1,401)


        DEALLOCATE(sst_data)
        DEALLOCATE(result_data)
        CALL h5dclose_f(ds_id, error_flag)
        CALL h5fclose_f(file_id, error_flag)
    END DO

    CLOSE(UNIT=90)
    CALL h5close_f(error_flag)
END PROGRAM
