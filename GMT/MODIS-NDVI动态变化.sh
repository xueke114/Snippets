#!/bin/bash
# 使用MOD13A3数据，绘制2011年--2020年10年间，每年8月份的NDVI变化动图

mod13a3_dir="C:/Datasets/Terra-MODIS-NDVI"

gdal_format='HDF4_EOS:EOS_GRID:'
dataset_name=':MOD_Grid_monthly_1km_VI:"1 km monthly NDVI"'

# 数据拼接
for i in {2011..2020}
do 
day=$i"0801"
doy=$(date -d $day +"%Y%j")
echo $day >> datemark.txt
# find $mod13a3_dir -name "*$doy*.hdf" -printf $gdal_format'"'%p'"'"$dataset_name\n" > filelist.txt

# gdalbuildvrt -overwrite -input_file_list filelist.txt temp.vrt

# gdal_translate -a_scale 0.0001 temp.vrt $day.vrt

# gdalwarp -overwrite -t_srs EPSG:4326 -of NETCDF -co "FORMAT=NC4" -co "COMPRESS=DEFLATE" $day.vrt $day.nc
# rm filelist.txt temp.vrt $day.vrt
done

# 制作动图
# 底图脚本
cat << 'EOF' > main.sh
gmt begin

    # 设置经纬度网格线：0.25p，灰色，虚线
    gmt set MAP_GRID_PEN_PRIMARY 0.25p,gray,2_2
    gmt set FONT=,4,
    
    # 绘制海陆
    gmt coast -X1.5 -Y2 -G244/243/239 -S167/194/223 -R70/138/13/56  -Ba10f5g10  -JM105/35/10c 
    # 绘制比例尺、标题
    gmt basemap -Lg85/17.5+w800k+f+u -B+t"$MOVIE_COL0 NDVI" --FONT_ANNOT_PRIMARY=4p
    # 在China的范围内，绘制NDVI
    gmt clip CN-border-L1.gmt
    gmt makecpt -Cbamako -T-0.2/1/0.1 -Iz
    gmt grdimage $MOVIE_COL0.nc
    # 绘制国界
    gmt plot CN-border-L1.gmt -W0.1p
    gmt clip -C

    # 绘制南海诸岛
    gmt inset begin -DjRB+w1.8c/2.2c -F+p0.5p
    gmt coast -JM? -R105/123/3/24 -G244/243/239 -S167/194/223 -Df
    gmt plot CN-border-L1.gmt -W0.1p
    gmt clip CN-border-L1.gmt
    gmt grdimage $MOVIE_COL0.nc
    gmt clip -C
    gmt inset end

    # 绘制色条：去除色块间隔线，自动设置标注间隔
    gmt colorbar  -S -Bafg 

gmt end
EOF

echo "开始合成GIF"
gmt movie main.sh -C13cx11.5cx150 -N"NDVI-China" -Tdatemark.txt -D2 -Fgif+l -Z
rm datemark.txt main.sh