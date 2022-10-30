:: 使用CMake从源码构建netCDF-Fortran库
@echo off
chcp 65001

set HTTPS_PROXY=127.0.0.1:7070

set version=4.5.4
set nc_version=4.8.1
set build_type=Release
set source_dir=C:/Libs/build-work/build-netcdf-fortran
set install_dir=C:/Libs/netCDF-Fortran/%version%/%build_type%
set url=https://github.com/Unidata/netcdf-fortran/archive/refs/tags/v%version%.zip

echo ====== 下载netCDF-Fortran源码 ======
if not exist %source_dir% (
    echo 创建目录 %source_dir%
    mkdir %source_dir:/=\%    
)
curl -C - --output-dir %source_dir% --output %version%.zip -L %url% 

echo ====== 解压netCDF-Fortran源码 ======
7z -y x %source_dir%/%version%.zip -o%source_dir%/

echo ========== 开始生成编译目标 ==========
cmake -S %source_dir%/netcdf-fortran-%version% -B %source_dir%/build-%build_type% ^
-DCMAKE_BUILD_TYPE:STRING=%build_type% -DCMAKE_INSTALL_PREFIX=%install_dir% ^
-DnetCDF_LIBRARIES=C:/Libs/netCDF-c/%nc_version%/%build_type%/lib/netcdf.lib ^
-DnetCDF_INCLUDE_DIR=C:/Libs/netCDF-c/%nc_version%/%build_type%/include  -DUSE_NETCDF_V2=1 -DHAVE_SZIP_WRITE=1

echo ========== 手动生成链接库文件 ==========
cd %source_dir%/build-%build_type%/fortran
cmake --build %source_dir%/build-%build_type% --target netcdff netcdff_c --config %build_type%
lib netcdff.dir\%build_type%\*.obj netcdff_c.dir\%build_type%\netcdff_c.lib /out:%build_type%\netcdff.lib

echo ========== 编译并安装 ==========
cmake --build %source_dir%/build-%build_type% --target INSTALL --config %build_type%