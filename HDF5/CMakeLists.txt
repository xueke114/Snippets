cmake_minimum_required(VERSION 3.15)
project(HDF5-Demo LANGUAGES C CXX Fortran)

find_package(HDF5 COMPONENTS Fortran C CXX)

# Windows平台，Inter Fortran，如果使用官方的预编译版本，那么目前HDF5-1.14头文件会有问题
add_executable(fortran-write fortran_write_hdf5.f90)
target_link_libraries(fortran-write PRIVATE ${HDF5_Fortran_LIBRARIES})

# Windows平台，如果使用官方的预编译版本，那么Debug模式下会有问题
#             如果使用vcpkg，那么Fortran就没有对应的版本
#             所以还是自己编译源代码吧
add_executable(cxx_list_all_variables list_all_variables.cpp)
target_link_libraries(cxx_list_all_variables PRIVATE ${HDF5_CXX_LIBRARIES})