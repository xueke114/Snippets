import os
import glob
import shutil
import subprocess
from typing import Dict
from datetime import datetime


class MakeMap:
    search_dir = ""
    def __init__(self,dir:str) -> None:
        self.search_dir=dir
        os.chdir(self.search_dir)

    # 遍历文件名,按天聚类
    def mosaicDataset(self):
        files = glob.glob("*.hdf")
        files_dict: Dict[str, list] = {}
        for file in files:
            date_doy = file.split(".")[-5][1:]
            if date_doy not in files_dict:
                files_dict[date_doy] = []
            files_dict[date_doy].append(file)

        # 遍历字典,按天拼接
        datemark_file = "datemark.txt"
        if os.path.exists(datemark_file):
            os.remove(datemark_file)
        f = open(datemark_file, mode="a")

        if not os.path.exists("temp"):
            os.mkdir("temp")

        for day in files_dict:
            date = datetime.strptime(day, "%Y%j").strftime("%Y%m")
            f.write(date + "\n")

            before = 'HDF4_EOS:EOS_GRID:"'
            after = '":MOD_Grid_monthly_1km_VI:"1 km monthly NDVI"'
            datasets_name = [before + name + after for name in files_dict[day]]

            input_files = open("temp/input_list.txt", "w")
            input_files.writelines("\n".join(datasets_name))
            input_files.close()

            # 调用gdal拼接
            subprocess.run(
                [
                    "gdalbuildvrt",
                    "-input_file_list",
                    "temp/input_list.txt",
                    "temp/mosaic.vrt",
                ]
            )
            subprocess.run(
                [
                    "gdalwarp",
                    "-multi",
                    "-wo",
                    "NUM_THREADS=ALL_CPUS",
                    "-of",
                    "NETCDF",
                    "-t_srs",
                    "EPSG:4326",
                    "temp/mosaic.vrt",
                    f"temp/{date}-ChinaMarchNDVI.nc",
                ]
            )
        f.close()

    # 调用gmt绘制动图
    def makeGIF(self, gif_name: str = "gif.gif"):
        # 绘图脚本
        bat = """
    gmt begin ndvi png

    @REM 设置经纬度网格线：0.25p，灰色，虚线
    gmt set MAP_GRID_PEN_PRIMARY 0.25p,gray,2_2

    @REM 绘制
    gmt coast -X1.5 -S167/194/223 -Ba10f5g10 -B+t"%MOVIE_COL0% NDVI" -JM105/35/10c -R70/138/13/56  --FONT_TITLE=14p,4

    gmt basemap  -Lg85/17.5+c17.5+w800k+f+u --FONT_LABEL=4p,39 --FONT_ANNOT_PRIMARY=4p
    gmt clip CN-border-L1.gmt
    gmt makecpt -Cbamako -T-20000000/100000000/10000000 -Iz
    gmt grdimage temp/%MOVIE_COL0%-ChinaMarchNDVI.nc
    gmt plot CN-border-L1.gmt -W0.1p
    gmt clip -C

    @REM 绘制南海诸岛
    gmt inset begin -DjRB+w1.8c/2.2c -F+p0.5p
    gmt coast -JM? -R105/123/3/24 -G244/243/239 -S167/194/223 -Df
    gmt plot CN-border-L1.gmt -W0.1p
    gmt clip CN-border-L1.gmt
    gmt grdimage temp/%MOVIE_COL0%-ChinaMarchNDVI.nc
    gmt clip -C
    gmt inset end

    @REM 绘制色条：数值缩放1000*10000倍，去除色块间隔线，自动设置标注间隔
    gmt colorbar -W0.00000001 -S -Bafg 

    gmt end
    """
        # 输出绘图脚本

        with open("main.bat", "w") as f:
            f.writelines(bat)
            f.close()

        # 调用gmt的movie模块绘制动图
        if os.path.exists(gif_name):
            shutil.rmtree(gif_name)

        subprocess.run(
            [
                "gmt",
                "movie",
                "main.bat",
                "-C13cx12cx150",
                f"-N{gif_name}",
                "-Tdatemark.txt",
                "-D2",
                "-Fgif+l",
                "-Z",
            ],
        )

        # 删除多余文件
        shutil.rmtree("temp")
        os.remove("datemark.txt")
        os.remove("main.bat")
        # 移动结果到GIF目录
        if not os.path.exists("GIF"):
            os.mkdir("GIF")
        if os.path.exists(f"{gif_name}.gif"):
            os.rename(f"{gif_name}.gif", f"GIF/{gif_name}.gif")


# 分步执行
if __name__ == "__main__":
    files_dir="C:/Users/xueke/Downloads/MOD13A3(NDVI)-China-201703--201802"
    # mm = MakeMap(r"C:/Users/yk/Downloads/MOD13A3(NDVI)-China-Aug-2011-2020")
    mm = MakeMap(files_dir)
    mm.mosaicDataset()
    mm.makeGIF(gif_name="ChinaNDVI-201703-201802")
