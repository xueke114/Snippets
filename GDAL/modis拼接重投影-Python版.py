#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from osgeo import gdal

file_list = []
file_dir = "/home/xueke/RSDatasets/Terra-MODIS-NDVI-1000M-30D-China/"

before = 'HDF4_EOS:EOS_GRID:"'
after = '":MOD_Grid_monthly_1km_VI:"1 km monthly NDVI"'

# 收集数据集列表
for filename in os.listdir(file_dir):
    if filename.endswith(".hdf"):
        file_list.append(before + os.path.join(file_dir, filename) + after)

# 构建虚拟栅格
print("开始构建虚拟栅格")
vrt_file = os.path.join(file_dir, "vrt.vrt")
gdal.BuildVRT(vrt_file, file_list, srcNodata=255, VRTNodata=255)

# 虚拟栅格合成TIF
print("开始合成tif")
result_file = os.path.join(file_dir, "hello-mosic.tif")

result = gdal.Warp(
    srcNodata=255,
    dstNodata=255,
    format="GTiff",
    multithread=True,
    dstSRS="EPSG:4326",
    options=["-overwrite"],
    srcDSOrSrcDSTab=vrt_file,
    destNameOrDestDS=result_file,
    creationOptions=["COMPRESS=DEFLATE"],
)
result = None
