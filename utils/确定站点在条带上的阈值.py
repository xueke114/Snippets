"""
绘图查看站点是否在条带上，并确定出最小距离阈值
"""
import os.path
import numpy as np
from glob import glob
import cartopy.crs as ccrs
from netCDF4 import Dataset
from datetime import datetime
import matplotlib.pyplot as plt
from cartopy.io import shapereader


site = (114.517, 33.783)
assets_dir = "./Assets"
os.makedirs(assets_dir, exist_ok=True)
l1b_dir = "/home/xueke/RSDatasets/Metop-ASCAT-1B-25KM/NC/"
l1b_filepaths = sorted(glob(os.path.join(l1b_dir, "2018*", "*.nc")))

shp_file = "/home/xueke/GeoDatasets/HeNanShape/HeNan.shp"
shp_obj = shapereader.Reader(shp_file)

for l1b_filepath in l1b_filepaths:
    file_date_str = os.path.basename(l1b_filepath).split("_")[4]
    file_date = datetime.strptime(file_date_str, "%Y%m%d%H%M%S")
    with Dataset(l1b_filepath) as nc_obj:
        lon = nc_obj.variables["lon"][:]
        lat = nc_obj.variables["lat"][:]

        # 最近点的行列号
        distances = np.hypot(lon - site[0], lat - site[1])
        mini_dis_loc = distances.argmin()
        mini_dist = distances.min()

        row = mini_dis_loc // distances.shape[1]
        col = mini_dis_loc % distances.shape[1]
        map_point = (lon[row, col], lat[row, col])

        # 绘制出来这两个点，并保存为文件，并用距离作为文件名，方便排序
        fig = plt.figure()
        coord_crs = ccrs.PlateCarree()
        map_crs = ccrs.Mercator(central_longitude=105)
        ax = fig.add_subplot(1, 1, 1, projection=map_crs)
        # ax.set_extent([100, 150, 20, 40], crs=coord_crs)
        ax.set_extent([110, 117, 31, 37], crs=coord_crs)
        # 绘制Shapefile
        ax.add_geometries(shp_obj.geometries(), crs=coord_crs, facecolor="None")
        ax.pcolormesh(lon, lat, inc_ang[:, :, 1], transform=ccrs.PlateCarree())
        ax.plot(*map_point, "bo", transform=coord_crs, markersize=2)
        ax.plot(*site, "ro", transform=coord_crs, markersize=2)
        plt.savefig(f"Assets/png/{mini_dis_loc:5f}.png")
        plt.show()
        plt.close()
