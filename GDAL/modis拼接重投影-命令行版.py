import os
import subprocess

# 生成数据集列表并输出到文件
with open("filelists.txt", "w") as flist:
    for file in os.listdir("/home/xueke/Desktop/modis-test/DATA/"):
        if file.endswith(".hdf"):
            flist.write(
                'HDF4_EOS:EOS_GRID:"' + file + '":MCD12Q1:LC_Type1' + "\n"
            )

# 由数据集列表生成虚拟栅格文件
subprocess.run(
    ["gdalbuildvrt", "-inputfile_list", "filelists.txt", "mosaic.vrt"]
)

# 虚拟栅格转为netCD并做重投影
subprocess.run(
    [
        "gdalwarp",
        "-multi",
        "-of",
        "netCDF",
        "-t_srs",
        "EPSG:4326",
        "-dstnodata",
        "255",
        "-co",
        "COMPRESS=DEFLATE",
        "mosaic.vrt",
        "hello-nc.nc",
    ]
)
