import os
from pyresample import create_area_def

china_0125 = create_area_def(
    area_id="china0.125",
    projection="EPSG:4326",
    resolution=0.125,
    units="degrees",
    area_extent=(73.5, 3.375, 135.125, 53.625),
)

henan_0125 = create_area_def(
    area_id="henan0.125",
    projection="EPSG:4326",
    resolution=0.125,
    units="degrees",
    area_extent=(110.25, 31.375, 116.75, 36.375),
)
henan_01 = create_area_def(
    area_id="henan0.1",
    projection="EPSG:4326",
    resolution=0.1,
    units="degrees",
    area_extent=(110.3, 31.3, 116.7, 36.4),
)

hebi_0125 = create_area_def(
    units="degrees",
    resolution=0.125,
    area_id="hebi0.125",
    projection="EPSG:4326",
    area_extent=(114,35.375,114.75,36.125)
)
if os.path.exists("pyresample-area-extent.yaml"):
    os.remove("pyresample-area-extent.yaml")
china_0125.dump("pyresample-area-extent.yaml")
henan_0125.dump("pyresample-area-extent.yaml")
henan_01.dump("pyresample-area-extent.yaml")
hebi_0125.dump("pyresample-area-extent.yaml")


print(henan_01.get_lonlats())
