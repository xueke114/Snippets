"""
参考文档
标称上行列号和经纬度的互相转换
https://img.nsmc.org.cn/PORTAL/NSMC/DATASERVICE/AuxiliaryData/FY4B/FY-4B标称上行列号和经纬度的互相转换-133E.pdf
"""

import h5py
import numpy as np

# 常数
h = 42164
ea = 6378.137
eb = 6356.7523
rows = 2748
cols = 2748
coff = 1373.5
loff = 1373.5
cfac = 10233137
lfac = 10233137
delta_d = 105 # FY4B于2024年3月5日漂移至东经105度，之前的delta_d为133
cfac_216 = 2**-16 * cfac
lfac_216 = 2**-16 * lfac

lons = np.empty((rows, cols))
lats = np.empty((rows, cols))

for l in range(rows):
    y = np.deg2rad((l - loff) / lfac_216)
    cos2y_ea2_eb2_sin2y = np.cos(y) ** 2 + (ea / eb * np.sin(y)) ** 2

    for c in range(cols):
        x = np.deg2rad((c - coff) / cfac_216)
        h_cosx_cosy = h * np.cos(x) * np.cos(y)

        sd = np.sqrt(h_cosx_cosy**2 - cos2y_ea2_eb2_sin2y * (h**2 - ea**2))
        sn = (h_cosx_cosy - sd) / cos2y_ea2_eb2_sin2y

        s1 = h - sn * np.cos(x) * np.cos(y)
        s2 = sn * np.sin(x) * np.cos(y)
        s3 = -1 * sn * np.sin(y)
        sxy = np.hypot(s1, s2)

        lons[l, c] = np.rad2deg(np.arctan(s2 / s1)) + 105
        lats[l, c] = np.rad2deg(np.arctan((ea / eb) ** 2 * s3 / sxy))

with h5py.File(f"FY4B_{delta_d}E_GEO.h5", mode="w") as h5obj:
    h5obj.create_dataset("lon", data=lons, compression="gzip")
    h5obj.create_dataset("lat", data=lats, compression="gzip")
    