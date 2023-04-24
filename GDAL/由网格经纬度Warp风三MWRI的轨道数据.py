from pprint import pprint
from osgeo import gdal, osr

filename = "FY3D_MWRIA_GBAL_L1_20220311_0621_010KM_MS.HDF"

file_obj = gdal.Open(filename, gdal.GA_ReadOnly)

subdatasets = file_obj.GetSubDatasets()
pprint(subdatasets)

bt_dsname = subdatasets[1][0]
lon_dsname = subdatasets[6][0]
lat_dsname = subdatasets[5][0]


sp = osr.SpatialReference()
sp.SetWellKnownGeogCS("WGS84")
sp_wkt = sp.ExportToWkt()

vrt = gdal.Translate("fy3.vrt", bt_dsname)
geo_info = [
    "LINE_OFFSET=1",
    "LINE_STEP=1",
    "PIXEL_OFFSET=1",
    "PIXEL_STEP=1",
    f"SRS={sp_wkt}",
    "X_BAND=1",
    f"X_DATASET={lon_dsname}",
    "Y_BAND=1",
    f"Y_DATASET={lat_dsname}"
]

vrt.SetMetadata(geo_info, "GEOLOCATION")
vrt = None

warped = gdal.Warp("warped.tif", "fy3.vrt", geoloc=True, resampleAlg="average")

warped = None
