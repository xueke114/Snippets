from osgeo import gdal

if __name__ == "__main__":
    shpfile = "/home/xueke/GeoDatasets/塔克拉玛干沙漠边界-手绘/塔克拉玛干沙漠边界-手绘.shp"
    tiffile = "/home/xueke/RSDatasets/TA-MODIS-LandCover-1000M-Yearly-GLobal/2019/MCQ12Q1-A2019001.Global.tif"
    masked_outputfile = "MCQ12Q1-A2019001.Global.Masked.tif"
    cliped_outputfile = "MCQ12Q1-A2019001.Global.Cliped.tif"

    # 掩膜：将输出栅格的范围与数据栅格的范围保持一致
    # 注意：cropToCutline=False
    # 关于cutlineLayer，一般应该是shp文件名
    masked_ds = gdal.Warp(
        srcNodata=255,
        dstNodata=255,
        format="GTiff",
        cropToCutline=False,
        cutlineDSName=shpfile,
        srcDSOrSrcDSTab=tiffile,
        destNameOrDestDS=masked_outputfile,
        cutlineLayer="塔克拉玛干沙漠边界-手绘",
        creationOptions=["COMPRESS=DEFLATE"],
    )

    # 裁剪，即将结果范围约束到shap文件的范围
    # 实现方法：cropToCutline=True
    cliped_ds = gdal.Warp(
        srcNodata=255,
        dstNodata=255,
        format="GTiff",
        cropToCutline=True,
        cutlineDSName=shpfile,
        srcDSOrSrcDSTab=tiffile,
        destNameOrDestDS=cliped_outputfile,
        cutlineLayer="塔克拉玛干沙漠边界-手绘",
        creationOptions=["COMPRESS=DEFLATE"],
    )

    masked_ds, cliped_ds = None, None
