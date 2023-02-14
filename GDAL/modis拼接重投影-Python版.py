#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from osgeo import gdal

file_list = []
file_dir = "/home/xueke/RSDatasets/Terra-MODIS-NDVI-1000M-30D-China/"

for filename in os.listdir(file_dir):
    if filename.endswith(".hdf"):
        file_list.append(
            'HDF4_EOS:EOS_GRID:"'
            + os.path.join(file_dir, filename)
            + '":MOD_Grid_monthly_1km_VI:"1 km monthly NDVI"'
        )

result_file = os.path.join(file_dir, "hello-all.nc")

result = gdal.Warp(
    dstNodata=255,
    format="netCDF",
    multithread=True,
    dstSRS="EPSG:4326",
    options=["-overwrite"],
    srcDSOrSrcDSTab=file_list,
    destNameOrDestDS=result_file,
    creationOptions=["COMPRESS=DEFLATE", "format=NC4C"],
)
result = None
