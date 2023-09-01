import json
from fiona.crs import CRS
import geopandas as gpd
from urllib.request import urlopen
from urllib.parse import urlencode
from shapely.geometry import Point, Polygon


def get_province_extension(code, apikey):
    base_url = "https://restapi.amap.com/v3/config/district?"
    para = {"key": apikey, "keywords": code, "subdistrict": 0, "output": "json", "extensions": "all"}

    req = urlopen(base_url + urlencode(para))

    if req.status != 200:
        raise Exception(f"URL request error，error code {req.status}")

    req_content = json.loads(req.read())
    req.close()

    return req_content["districts"][0]["polyline"]

def output_extension(extension, outfile):
    
    all_geomtery = []
    for polygon_str in extension.split("|"):
        coordinates  = []
        for polygon_coor_str in polygon_str.split(";"):
            coordinates.append(tuple(map(float, polygon_coor_str.split(","))))
        all_geomtery.append(Polygon(coordinates))

    df = gpd.GeoDataFrame({"geometry":all_geomtery}, crs=CRS.from_epsg(4326))
    df.to_file(outfile)
    
if __name__ == "__main__":

    # 自定义变量
    ## adcode，见于 https://lbs.amap.com/api/webservice/download
    ## api_kay，见于 https://lbs.amap.com/dev/key
    adcode = 410600
    api_key = "de49f02249102c20ad43cb73a45df98b"
    output_shpfle = "C:\\Datasets\\Geo\HeBi\\HeBi.shp"

    # 读取并保存边界坐标点
    extension_str = get_province_extension(adcode, api_key)
    output_extension(extension_str, output_shpfle)