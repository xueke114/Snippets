# geopy中有一个实现：geopy.distance.greate_circle()


# 北京到华盛顿的大圆距离

from math import radians, cos, sin, asin, sqrt, cos

beijing = (39.91, 116.39)
washington = (38.8977, -77.0365)
earth_r = 6371007.1810

lat_dif = radians(beijing[0] - washington[0]) / 2
lon_dif = radians(beijing[1] - washington[1]) / 2
lat1, lat2 = radians(beijing[0]), radians(washington[0])

a = sin(lat_dif) * sin(lat_dif) + cos(lat1) * cos(lat2) * sin(lon_dif) * sin(lon_dif)

print(a)
d = 2 * earth_r * asin(sqrt(a))
print(d)

# 11146289.728951292
