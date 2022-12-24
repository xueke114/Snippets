import json
from urllib.request import urlopen
from urllib.parse import urlencode

from osgeo import gdal


def get_province_extension(code, apikey):
    base_url = "https://restapi.amap.com/v3/config/district?"
    para = {
        "key": apikey,
        "keywords": code,
        "subdistrict": 0,
        "output": "json",
        "extensions": "all",
    }

    req = urlopen(base_url + urlencode(para))

    if req.status != 200:
        raise Exception(f"URL request error，error code {req.status}")

    req_content = json.loads(req.read())
    req.close()

    return req_content["districts"][0]["polyline"]


def output_extension(extension, outfile):
    with open(outfile, mode="w") as out:
        out.write("# @VGMT1.0 @GLINESTRING\n")
        out.write('# @Jp"+proj=longlat +datum=WGS84 +no_defs"\n')
        for old, new in [("|", ";>;"), (",", " "), (";", "\n")]:
            extension = extension.replace(old, new)
        out.write(extension)


if __name__ == "__main__":

    # 自定义变量
    ## adcode，见于 https://lbs.amap.com/api/webservice/download
    ## api_kay，见于 https://lbs.amap.com/dev/key
    adcode = 410000
    api_key = "de49f02249102c20ad43cb73a45df98b"
    output_file = "C:/GeoDatasets/HeNan.txt"
    output_shpfle = "C:/GeoDatasets/HeNan.shp"

    # 读取并保存边界坐标点
    extension_str = get_province_extension(adcode, api_key)
    output_extension(extension_str, output_file)

    # 转换为shp文件
    gdal.VectorTranslate(output_shpfle, output_file, geometryType="POLYGON")
