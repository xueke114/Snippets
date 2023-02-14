#! /bin/bash

nodata=-3000
offset_factor=0
scale_factor=0.0001
gdal_format='HDF4_EOS:EOS_GRID:'
dataset_name=':MOD_Grid_monthly_1km_VI:"1 km monthly NDVI"'
files_dir="/home/xueke/RSDatasets/Terra-MODIS-NDVI-1000M-30D-China"

for filename in `ls $files_dir/*.hdf`
do
echo $gdal_format$filename$dataset_name >> $files_dir/datasetsnames.txt
done

# 构建虚拟栅格
# -srcnodata $nodata：                           指定输入数据的无效值
# -vrtnodata $nodata：                           指定输出数据的无效值
# -input_file_list $files_dir/datasetsnames.txt：输入文件（数据集）列表
gdalbuildvrt -srcnodata $nodata -vrtnodata $nodata -input_file_list $files_dir/datasetsnames.txt $files_dir/temp.vrt

# 为虚拟栅格设置定标系数（可选，主要用于纠正源文件不正确的定标系数）
gdal_translate -a_scale $scale_factor -a_offset $offset_factor $files_dir/temp.vrt $files_dir/target.vrt

# 虚拟栅格处理
# -multi：              开启多线程处理
# -overwrite:           允许对输出文件覆写
# -of netCDF：          输出格式为netCDF
# -srcnodata $nodata：  指定输入数据的无效值
# -dstnodata $nodata：  指定输出数据的无效值
# -t_srs EPSG:4326：    重投影到EPSG:4326（等经纬度）
# -co COMPRESS=DEFLATE：设置输出文件选项——启用数据压缩
gdalwarp -multi -overwrite -of netCDF -srcnodata $nodata -dstnodata $nodata -t_srs EPSG:4326 -co "COMPRESS=DEFLATE" $files_dir/target.vrt $files_dir/hello.nc

# 移除中间文件
rm $files_dir/datasetsnames.txt $files_dir/*.vrt
