import cartopy
import matplotlib.pyplot
from matplotlib.pyplot import Figure
from cartopy.mpl.geoaxes import GeoAxes


# 新建画布
fig: Figure = matplotlib.pyplot.figure()
# 添加绘图区，并设置绘图区的投影
map_crs = cartopy.crs.PlateCarree()
shp_crs = cartopy.crs.PlateCarree()
ax: GeoAxes = fig.add_subplot(1, 1, 1, projection=map_crs)
# 设置边界
ax.set_extent(extents=[73, 136, 15, 55], crs=map_crs)
# 添加网格线，新版本可以使用draw_labels=['left','bottom']隐藏上和右的标注
gridlines = ax.gridlines(linestyle="--", draw_labels=True)
gridlines.top_labels, gridlines.right_labels = None, None
# 绘制海陆渲染地形图
# ax.stock_img()
# 绘制陆地
ax.add_feature(cartopy.feature.LAND)
# 绘制海洋
ax.add_feature(cartopy.feature.OCEAN)
#
# ax.add_feature(cartopy.feature.COASTLINE)

# 绘制国界省界shp
states_shp = r"Shapefile\China-province"
borders_shp = r"Shapefile\China-borders"
# 读shp文件
states_obj = cartopy.io.shapereader.Reader(states_shp)
borders_obj = cartopy.io.shapereader.Reader(borders_shp)
# 创建shp feature
states_shp_feature = cartopy.feature.ShapelyFeature(
    lw=0.5,
    crs=shp_crs,
    facecolor="None",
    edgecolor="black",
    geometries=states_obj.geometries(),
)
borders_shp_feature = cartopy.feature.ShapelyFeature(
    lw=1,
    crs=shp_crs,
    facecolor="None",
    edgecolor="black",
    geometries=borders_obj.geometries(),
)
# 添加国界省界 feature
ax.add_feature(states_shp_feature)
ax.add_feature(borders_shp_feature)
# 绘制南海诸岛
scs_ax: GeoAxes = fig.add_axes([0.795, 0.13, 0.1, 0.25], projection=map_crs)
scs_ax.set_extent(extents=[105, 125, 0, 25], crs=map_crs)

scs_ax.add_feature(states_shp_feature)
scs_ax.add_feature(borders_shp_feature)
scs_ax.add_feature(cartopy.feature.LAND)
scs_ax.add_feature(cartopy.feature.OCEAN)
# 存图
# fig.savefig("Cartopy.Test.png")
fig.show()
