import h5py
import pygmt
import numpy as np
import xarray as xr
from functools import partial
from pyresample import kd_tree, SwathDefinition, create_area_def


def swath_resample(swath_file, area_definition):
    with h5py.File(swath_file) as h5obj:
        lons = h5obj["Geolocation/Longitude"][:]
        lats = h5obj["Geolocation/Latitude"][:]
        bt_89h = h5obj["Calibration/EARTH_OBSERVE_BT_10_to_89GHz"][-1]
        swath = SwathDefinition(lons, lats)
        result = kd_tree.resample_nearest(
            swath, bt_89h, area_definition, 10000, fill_value=-32767
        )
        return result


if __name__ == "__main__":
    # 待的合并的条带文件
    swath_files = [
        "FY3D_MWRID_GBAL_L1_20231001_1800_010KM_MS.HDF",
        "FY3D_MWRID_GBAL_L1_20231001_1941_010KM_MS.HDF",
        "FY3D_MWRID_GBAL_L1_20231001_2123_010KM_MS.HDF",
    ]
    
    # 创建一个目标网格
    target_area = create_area_def(
        resolution=0.1,
        units="degrees",
        area_id="china0.1",
        projection="EPSG:4326",
        area_extent=(73.4, 3.0, 135.1, 53.6),
    )
    area_lon, area_lat = target_area.get_lonlats()
    
    # 所有条带都重采样到这一个网格上，得到三个网格
    resample_func = partial(swath_resample, area_definition=target_area)
    resampled_swathes = map(resample_func, swath_files)
    
    # 三个网格合并 
    resampled_swathes = np.stack(list(resampled_swathes))
    masked_resampled_swathes = np.ma.masked_equal(resampled_swathes, -32767)
    merged_swath = np.ma.mean(masked_resampled_swathes, axis=0)
    
    # 画图看看效果
    swath_xd = xr.DataArray(
        dims=["lat", "lon"],
        data=merged_swath.filled(np.nan),
        coords=dict(
            lon=(["lon"], area_lon[0, :]), lat=(["lat"], area_lat[:, 0])
        ),
    )
    fig = pygmt.Figure()
    fig.grdimage(
        frame="afg",
        grid=swath_xd,
        projection="Q12c",
        nan_transparent=True,
        region=[73, 135, 3, 54],
    )
    fig.plot("CN-border-L1.gmt",pen="0.5p,blue")
    fig.show()