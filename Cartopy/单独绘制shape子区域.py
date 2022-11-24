# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 12:59:33 2022

@author: xueke
"""

import cartopy
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # 新建画布
    fig = plt.figure(dpi=300)

    # 定义图的投影坐标系和shape文件的投影坐标系
    map_crs = cartopy.crs.PlateCarree()
    shp_crs = cartopy.crs.PlateCarree()

    # 在画布添加绘图区
    ax = fig.add_subplot(1, 1, 1, projection=map_crs)

    # 设置绘图区的范围
    ax.set_extent([73, 135, 18, 55])

    # 在绘图区为陆地海洋着色
    ax.add_feature(cartopy.feature.LAND)
    ax.add_feature(cartopy.feature.OCEAN)

    # 自动网格线与轴刻度
    gridlines = ax.gridlines(linestyle="--", draw_labels=True)
    gridlines.top_labels, gridlines.right_labels = None, None

    ## 加载shape文件
    shp_file = "Shapefile/China-province-simple-utf8"
    shp_obj = cartopy.io.shapereader.Reader(shp_file)
    # 遍历shape文件的每条记录，根据记录的字段值筛选需要的记录
    target_records = filter(lambda r: r.attributes["NAME"] == "河南", shp_obj.records())
    # 读取筛选到的记录的信息
    target_geometry = map(lambda r: r.geometry, target_records)
    # 绘制目标记录
    ax.add_geometries(
        target_geometry,  # 要绘制的数据（本质是一系列点）
        crs=shp_crs,      # 数据的投影坐标系
        facecolor="None", # 填充色
        edgecolor="red",  # 线条颜色
        lw=0.5            # 线宽
    )
