#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 使用pyresample，在同一投影系下操作数据，源投影与目标投影相同，但分辨率不同。
# 以MERSI的5km全球海温产品为例，原本为等经纬度投影，重采样到等经纬度投影，10km分辨率

import h5py
import numpy.ma as npm
from pyresample import create_area_def, kd_tree

h5_file = "/home/xueke/RSDatasets/FY3D-MERSI-SST/day/202206/FY3D_MERSI_GBAL_L2_SST_DAY_GLL_20220601_POAD_5000M_MS.HDF"
output_file = "/home/xueke/Desktop/MODIS-pyresample-demo2.hdf5"

# 1. 读取数据集数据并做无效值掩膜
h5_obj = h5py.File(h5_file)
sst_array = h5_obj["sea_surface_temperature"][:]
sst_fill_value = h5_obj["sea_surface_temperature"].attrs["FillValue"]
sst_array_masked = npm.masked_equal(sst_array, int(-888))
h5_obj.close()

# 2. 定义源区域信息
sst_area = create_area_def(
    units="degrees",
    area_id="mersi_sst",
    projection="EPSG:4326",
    width=7200,
    height=3600,
    area_extent=(-180, -90, 180, 90),
)

# 3. 定义目标区域信息
target_area = create_area_def(
    units="degrees",
    area_id="target_sst",
    projection="EPSG:4326",
    resolution=0.1,                  # 定义分辨率和边界，就相当于定义了宽高和边界。
    area_extent=(-180, -90, 180, 90),
)
# 输出目标区域每个网格的经纬度
target_lon, target_lat = target_area.get_lonlats()

# 4. 瓦片向目标区域重采样
result = kd_tree.resample_nearest(
    fill_value=-888,
    source_geo_def=sst_area,
    data=sst_array_masked,
    target_geo_def=target_area,
    radius_of_influence=10000,  # 邻域搜索半径，单位为m，一般为目标空间空间分辨率
)

# 6. 输出重采样重投影后的数据
with h5py.File(output_file, mode="w") as h5obj:
    h5obj["NDVI"] = result
    h5obj["lon"] = target_lon
    h5obj["lat"] = target_lat
    h5obj["NDVI"].attrs["fill_value"] = -888
