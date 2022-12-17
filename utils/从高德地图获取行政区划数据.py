import json
from urllib.request import urlopen
from urllib.parse import urlencode



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


def output_extensions(extensions,outfile):
    with open(outfile,mode="w") as out:
        out.write(extensions.replace("|",";>;").replace(";","\n"))

if __name__ == "__main__":

    # 自定义变量
    ## adcode，见于 https://lbs.amap.com/api/webservice/download
    ## api_kay，见于 https://lbs.amap.com/dev/key
    adcode = 410000
    api_key = "de49f02249102c20ad43cb73a45dfxxx"
    output_file = "D:/GeoDatasets/HeNan.txt"

    extensions_str = get_province_extension(adcode, api_key)
    output_extensions(extensions_str, output_file)
