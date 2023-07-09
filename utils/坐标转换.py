from pyproj import Transformer

transformer = Transformer.from_crs("EPSG:4326", "EPSG:6933")

# 输入经纬度是先纬度后经度，输出的是x和y
print(transformer.transform(18, 114))
# (10999435.948602203, 2259695.383341077)