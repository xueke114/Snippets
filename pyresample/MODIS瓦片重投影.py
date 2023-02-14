#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 使用pyresample进行重投影+重采样的典型例子
# 将MODIS的瓦片重采样重投影到等经纬度网格

import numpy.ma as npm
import h5py
from pyhdf.HDF import HDF
from pyhdf.SD import SD
import pyhdf.V
from pyresample import create_area_def, kd_tree

modis_file = "/home/xueke/RSDatasets/Terra-MODIS-NDVI-1000M-30D-China/MOD13A3.A2018001.h27v05.061.2021316203504.hdf"
output_file = "/home/xueke/Desktop/MODIS-pyresample-demo.hdf5"

# 1. 读取该瓦片的角点坐标
modis_obj = HDF(modis_file)  # 打开文件
v = modis_obj.vstart()       # 初始化接口
metadata = v.attach("StructMetadata.0").read()[0][0].splitlines()  # 获取属性信息
v.end()
modis_obj.close()
# 解析属性信息（角点坐标）
upperleft_x, upperleft_y = metadata[7].split("=")[-1][1:-1].split(",")
lowerright_x, lowerright_y = metadata[8].split("=")[-1][1:-1].split(",")

# 2. 读取要处理的数据集
modis_obj = SD(modis_file)
ndvi_sd = modis_obj.select("1 km monthly NDVI")
ndvi_array = ndvi_sd.get()
mdvi_array = npm.masked_equal(ndvi_array, -3000) # 掩膜掉无效值，防止重采样时影响

# 3. 定义该瓦片的信息（用于pyresample识别）
modis_area = create_area_def(
    units="m",                              # 单位m
    area_id="modis_h27v05",                 # 为area起个名字
    projection="+proj=sinu +R=6371007.181", # 定义数据的投影，MODIS的瓦片数据都是这个投影
    width=1200,                             # 瓦片数据的宽，MODIS的瓦片数据都是1200像素宽
    height=1200,                            # 瓦片数据的高，MODIS的瓦片数据都是1200像素高
    area_extent=(upperleft_x, lowerright_y, lowerright_x, upperleft_y), # 设置瓦片的边界（有了长宽和边界就能计算分辨率）
)


# 4. 定义目标等经纬度网格（等经纬度投影、空间分辨率0.01度）
# 瓦片边界的经纬度坐标
upperleft_lon,lowerright_lat = modis_area.get_lonlat_from_projection_coordinates(upperleft_x, lowerright_y)
lowerright_lon,upperleft_lat = modis_area.get_lonlat_from_projection_coordinates(lowerright_x, upperleft_y)

target_area = create_area_def(
    units="degrees",             # 单位 度
    area_id="target_area",       # 为area起个名字
    projection="EPSG:4326",      # 投影方式：EPSG: 4326
    resolution=0.01,             # 空间分辨率：0.01度
    area_extent=(upperleft_lon, lowerright_lat, lowerright_lon, upperleft_lat) 
    # 目标区域在目标投影坐标系的边界。自定义的，也不一定是瓦片的边界。
    # 如果设置的比瓦片边界小，就相当于做了裁剪。
    # 如果设置的比瓦片边界大，那也不影响，无非是空缺像元多了。
    # 如果不设置，那就会默认是输入的瓦片的边界。但如果不设置，就无法输出目标区域的经纬度网格信息
)
# 输出目标区域每个网格的经纬度
target_lon,target_lat = target_area.get_lonlats()

# 5. 瓦片向目标区域重采样（重投影）
result = kd_tree.resample_nearest(
    fill_value=-3000,
    source_geo_def=modis_area,
    data=ndvi_array,
    target_geo_def=target_area,
    radius_of_influence=1000,   # 邻域搜索半径，单位为m，一般为目标空间空间分辨率
)

# 6. 输出重采样重投影后的数据
with h5py.File(output_file,mode="w") as h5obj:
    h5obj["NDVI"]=result
    h5obj["lon"] = target_lon
    h5obj["lat"] = target_lat
    h5obj["NDVI"].attrs["fill_value"]=-3000
    h5obj["NDVI"].attrs["scale_factor"]=1e-6