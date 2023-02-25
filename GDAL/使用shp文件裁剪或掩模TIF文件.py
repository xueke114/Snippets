from osgeo import gdal
from pathlib import Path


def mask_tif_by_shapefile(
    shapefile: str, tiffile: str, outputtif: str, inputNodata, outputNodata
):
    """
    使用shape文件对tif文件进行掩模，并将输出栅格的范围与数据栅格的范围保持一致

    Parameters
    ----------
    shapefile : str
        shape文件的路径
    tiffile : str
        需要掩模的tif文件路径
    outputtif : str
        掩模后的tif文件路径
    inputNodata : TYPE
        输入数据的无效值
    outputNodata : TYPE
        输入数据的无效值

    Returns
    -------
    None.

    """
    gdal.Warp(
        format="GTiff",
        cropToCutline=False,
        srcNodata=inputNodata,
        dstNodata=outputNodata,
        cutlineDSName=shapefile,
        srcDSOrSrcDSTab=tiffile,
        destNameOrDestDS=outputtif,
        cutlineLayer=Path(shapefile).stem,
        creationOptions=["COMPRESS=DEFLATE"],
    )


def clip_tif_by_shapefile(
    shapefile: str, tiffile: str, outputtif: str, inputNodata, outputNodata
):
    """
    使用shape文件对tif文件进行裁剪，即将结果范围约束到shap文件的范围

    Parameters
    ----------
    shapefile : str
        shape文件的路径
    tiffile : str
        需要裁剪的tif文件路径
    outputtif : str
        裁剪后的tif文件路径
    inputNodata : TYPE
        输入数据的无效值
    outputNodata : TYPE
        输入数据的无效值

    Returns
    -------
    None.

    """
    gdal.Warp(
        format="GTiff",
        cropToCutline=True,
        srcNodata=inputNodata,
        dstNodata=outputNodata,
        cutlineDSName=shapefile,
        srcDSOrSrcDSTab=tiffile,
        destNameOrDestDS=outputtif,
        cutlineLayer=Path(shapefile).stem,
        creationOptions=["COMPRESS=DEFLATE"],
    )


if __name__ == "__main__":
    shpfile = "/home/xueke/GeoDatasets/塔克拉玛干沙漠边界-手绘/塔克拉玛干沙漠边界-手绘.shp"
    tiffile = "/home/xueke/RSDatasets/TA-MODIS-LandCover-1000M-Yearly-GLobal/2019/MCQ12Q1-A2019001.Global.tif"
    masked_outputfile = "MCQ12Q1-A2019001.Global.Masked.tif"
    cliped_outputfile = "MCQ12Q1-A2019001.Global.Cliped.tif"

    # 掩模Demo
    mask_tif_by_shapefile(
        tiffile=tiffile,
        inputNodata=255,
        outputNodata=255,
        shapefile=shpfile,
        outputtif=masked_outputfile,
    )

    # 裁剪Demo
    clip_tif_by_shapefile(
        tiffile=tiffile,
        inputNodata=255,
        outputNodata=255,
        shapefile=shpfile,
        outputtif=cliped_outputfile,
    )
