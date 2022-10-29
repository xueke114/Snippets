:: 使用CMake从源码构建netCDF-C(netCDF4)库
@echo off
chcp 65001
set HTTPS_PROXY=127.0.0.1:7070

echo ====== 下载netCDF-C源码 ======
set version=4.8.1
set build_type=Release
set hdf5_dir=C:/Libs/HDF5/1.10.9
set source_dir=C:/Libs/build-work/build-netcdf4
set install_dir=C:/Libs/netCDF-C/%version%/%build_type%
set url=https://github.com/Unidata/netcdf-c/archive/refs/tags/v%version%.zip

if not exist %source_dir% (
    echo 创建目录 %source_dir%
    mkdir %source_dir:/=\%    
)

curl -C - --output-dir %source_dir% --output %version%.zip -L %url% 

echo ====== 解压netCDF-C源码 ======
7z -y x %source_dir%/%version%.zip -o%source_dir%/

echo ========== 开始生成编译目标 ==========
cmake -S %source_dir%/netcdf-c-%version% -B %source_dir%/build-%build_type% ^
-DCMAKE_BUILD_TYPE:STRING=%build_type% -DCMAKE_INSTALL_PREFIX=%install_dir% ^
-DSZIP_LIBRARY=%hdf5_dir%/lib/libszaec.lib -DENABLE_DAP=OFF -DENABLE_TESTS=OFF ^
-DCMAKE_C_FLAGS="/utf-8"

echo ========== 开始编译 ==========
cmake --build %source_dir%/build-%build_type% --target INSTALL --config %build_type%