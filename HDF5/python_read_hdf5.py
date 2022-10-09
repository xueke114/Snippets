"""
Python 读取HDF5文件
"""

import h5py

FILENAME = "Assets/FY3D_MWRIA_GBAL_L1_20220301_0242_010KM_MS.HDF"

f_obj = h5py.File(FILENAME)

lat_obj = f_obj["Geolocation/Latitude"]

lat_data = lat_obj[:]

print(lat_data.shape)

f_obj.close()
