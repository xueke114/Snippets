# 修改自https://rasterio.readthedocs.io/en/stable/topics/reproject.html


import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

# 目标坐标系
dst_crs = "EPSG:4326"

with rasterio.open("rgb.tif") as src:
    # 计算数据在目标crs下的transform
    transform, width, height =  calculate_default_transform(src.crs, dst_crs, src.width, src.height, *src.bounds)

    # 继承源数据的属性信息
    kwargs = src.meta.copy()
    # 对属性信息进行适应性更新
    kwargs.update({'crs': dst_crs, 'transform': transform, 'width': width, 'height': height})
    
    # 逐波段重投影
    with rasterio.open("rgb.epsg4326.tif", "w", compress='DEFLATE', **kwargs) as dst:
        for i in range(1,src.count+1):
            reproject(rasterio.band(src,i), rasterio.band(dst,i), src_transform=src.transform, src_crs=src.crs, dst_transform=transform, dst_crs=dst_crs, resampling=Resampling.nearest)