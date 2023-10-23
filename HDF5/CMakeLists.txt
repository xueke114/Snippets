cmake_minimum_required(VERSION 3.15)
project(HDF5-Demo LANGUAGES C CXX Fortran)

find_package(HDF5 COMPONENTS Fortran C CXX)
set_directory_properties(PROPERTIES INCLUDE_DIRECTORIES "${HDF5_INCLUDE_DIR}")

add_executable(read_ds_c c_read_hdf5.c)
target_link_libraries(read_ds_c PRIVATE ${HDF5_C_LIBRARIES})

# Windows平台，Inter Fortran，如果使用官方的预编译版本，那么目前HDF5-1.14头文件会有问题
add_executable(fortran-write fortran_write_hdf5.f90)
target_link_libraries(fortran-write PRIVATE ${HDF5_Fortran_LIBRARIES})

# Windows平台，如果使用官方的预编译版本，那么Debug模式下会有问题
#             如果使用vcpkg，那么Fortran就没有对应的版本
#             所以还是自己编译源代码吧
add_executable(cxx_list_all_variables list_all_variables.cpp)
target_link_libraries(cxx_list_all_variables PRIVATE ${HDF5_CXX_LIBRARIES})

if (UNIX)
    set(EIGEN3_INCLUDE_DIR /usr/include/eigen3)
elseif (WINDOWS)
    set(EIGEN3_INCLUDE_DIR C:/Libs/eigen3/include/eigen3)
endif ()
include_directories(${EIGEN3_INCLUDE_DIR})
add_executable(read_into_eigen3 read_into_eigen3.cc)
target_link_libraries(read_into_eigen3 PRIVATE ${HDF5_CXX_LIBRARIES})