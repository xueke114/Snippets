import os.path

import netCDF4

west, east, north, south = 73, 135, 55, 18

# 读进来条带经纬度
file_dir = "C:/RSDatasets/Metop-ASCAT-1B-25KM"
filename = "W_XX-EUMETSAT-Darmstadt,SURFACE+SATELLITE,METOPB+ASCAT_C_EUMP_20220529114800_50304_eps_o_250_l1.nc"
with netCDF4.Dataset(os.path.join(file_dir, filename)) as ncobj:
    lon = ncobj.variables["lon"][:]
    lat = ncobj.variables["lat"][:]

    # 判断是否有像元落在区域内。
    x = (lat > south) & (lat < north) & (lon > west) & (lon < east)
    if x.any():
        print("经过")
