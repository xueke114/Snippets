from osgeo import gdal

gdal.UseExceptions()

geojson_file = "China.json"

# 前提是要输出的数据库加载了PostGIS插件


gdal.VectorTranslate(
    srcDS=geojson_file,
    destNameOrDestDS="PG:dbname=China user=postgres password=xxxxxxx host=127.0.0.1 port=5432",
    format="PostgreSQL",
    layerName="China", # 要创建的表名
    layerCreationOptions={"GEOMETRY_NAME": "geom"}, # 指定geometry字段的名字
)

