from osgeo import gdal
from pathlib import Path


def parse_arg(arg):
    """
    判断要裁剪还是要掩模，函数内部使用
    """
    iscropToCutline = False

    if arg == "mask":
        iscropToCutline = False
    elif arg == "clip":
        iscropToCutline = True
    else:
        raise Exception("mask_or_clip参数不规范")

    return iscropToCutline


def mask_clip_tif_by_shapefile(
    tiffile: str,
    shapefile: str,
    outputtif: str,
    inputNodata,
    outputNodata,
    mask_or_clip: str,
):
    """
    使用shape文件对tif文件进行掩模，并将输出栅格的范围与数据栅格的范围保持一致

    Parameters
    ----------
    tiffile : str
        待处理的tif文件路径
    shapefile : str
        shape文件的路径
    outputtif : str
        处理后的tif文件路径
    inputNodata : TYPE
        输入数据的无效值
    outputNodata : TYPE
        输入数据的无效值
    mask_or_clip : str
        掩模还是裁剪：输入mask则掩模，输入clip则裁剪

    Returns
    -------
    None.

    """

    gdal.Warp(
        format="GTiff",                          # 输出文件的格式
        multithread=True,                        # 是否开启多线程处理（可加速处理，maybe）
        srcNodata=inputNodata,                   # 输入文件的无效值
        dstNodata=outputNodata,                  # 输出文件的无效值
        cutlineDSName=shapefile,                 # shape文件
        srcDSOrSrcDSTab=tiffile,                 # 待处理的tif文件
        destNameOrDestDS=outputtif,              # 待输出的tif文件
        cutlineLayer=Path(shapefile).stem,       # shape文件图层名（一般是文件名）
        creationOptions=["COMPRESS=DEFLATE"],    # 对输出的tif进行无损压缩（减小文件文件体积）
        cropToCutline=parse_arg(mask_or_clip),   # 裁剪还是掩模，根据传入的参数而定
    )
    # gdal.Warp的更多参数请参看
    # https://gdal.org/api/python/osgeo.gdal.html#osgeo.gdal.WarpOptions


if __name__ == "__main__":

    # === 用户定义部分 ==========
    shpfile = "/home/xueke/GeoDatasets/塔克拉玛干沙漠边界-手绘/塔克拉玛干沙漠边界-手绘.shp"
    tiffile = "/home/xueke/RSDatasets/TA-MODIS-LandCover-1000M-Yearly-GLobal/2019/MCQ12Q1-A2019001.Global.tif"
    masked_outputfile = "MCQ12Q1-A2019001.Global.Masked.tif"
    cliped_outputfile = "MCQ12Q1-A2019001.Global.Cliped.tif"
    in_nodata = 255
    out_nodata = 255

    # === 执行部分 ==========
    # 掩模Demo
    mask_clip_tif_by_shapefile(
        tiffile=tiffile,
        shapefile=shpfile,
        mask_or_clip="mask",
        inputNodata=in_nodata,
        outputNodata=out_nodata,
        outputtif=masked_outputfile,
    )

    # 裁剪Demo
    mask_clip_tif_by_shapefile(
        tiffile=tiffile,
        shapefile=shpfile,
        mask_or_clip="clip",
        inputNodata=in_nodata,
        outputNodata=out_nodata,
        outputtif=cliped_outputfile,
    )
