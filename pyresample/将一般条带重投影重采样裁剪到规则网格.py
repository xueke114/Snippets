# 将FY3D的微波成像仪 MWRI 十个通道的条带亮温（空间分辨率为10KM）
# 重投影到规则等经纬度格网
# 该等经纬网格的空间分辨率设置为为0.1度 X 0.1度
# 该等经纬网格的空间分辨率设置为河南省（北纬36.4到31.4，东经110.3到116.7）

# 实现方案采用pyresample，重采样方法选择最近邻法
# pyresample的使用方法的详细介绍可参考官方文档，地址如下：
# https://pyresample.readthedocs.io/en/latest/howtos/swath.html

import h5py
import numpy as np
from pyresample import create_area_def, SwathDefinition, kd_tree

# === 1. 读取亮温数据
mwri_file = "F:/数据集备份/RS/FY3D-MWRI/202207/D/20220729/FY3D_MWRID_GBAL_L1_20220729_0736_010KM_MS.HDF"
mwri_obj = h5py.File(mwri_file)
bt = mwri_obj["Calibration/EARTH_OBSERVE_BT_10_to_89GHz"][:]

# === 2. 对数据进行预处理

# 将亮温不在有效值范围内的像元值设为空值
# 有效值范围可以在该数据集的属性信息中找到
# 如果是重采样方法采用最近邻法，则这一步待重采样后再做
# 因为最近邻法不改变像元值，即无效值不影响重采样后的网格像元值
bt = np.where((bt >= -32766) & (bt <= 10000), bt, np.nan)

# 将亮温值缩放到正常大小，缩放系数在该数据集的属性信息中找到
bt = bt * 0.01

# 将数据形状转换成pyresample可以识别的形状
# MWRI条带数据的亮温数据形状为： 通道数 x 行数 x 列数
# pyresample要求的输入数据的形状为：行数 x 列数 x 通道数
# 数据形状不匹配，解决方案有两种
# 一种解决方案是对每个通道单独pyresample
# 另一种方案是将数据转换成pyresample要求的形状
# 这里采用第二种方案，通过使用两次numpy的swapaxes函数实现
# 效果等价于以下代码：
# bt_new=np.empty(shape=(bt.shape[1], bt.shape[2], bt.shape[0]))
# for i in range(bt.shape[0]):
#     bt_new[:, :, i] = bt[i, :, :]

bt_new = np.swapaxes(np.swapaxes(bt, 0, 1), 1, 2)
# 当然，如果源数据的形状为：行数 x 列数 x 通道数，
# 如ASCAT的后向散射数据，则不需要进行这样的转换（废话）

# === 3. 使用文件中的条带网格经纬度来定义条带
mwri_lons = mwri_obj["Geolocation/Longitude"][:]
mwri_lats = mwri_obj["Geolocation/Latitude"][:]
mwri_swath = SwathDefinition(lons=mwri_lons, lats=mwri_lats)

# === 4. 构建目标网格
target_grid = create_area_def(
    resolution=0.1,  # 目标网格的网格分辨率
    units="degrees",  # 分辨率的单位
    area_id="henan0.1d",  # 随便起个名字
    projection="EPSG:4326",  # 目标网格的投影方式
    area_extent=(110.3, 31.4, 116.7, 36.4),  # 目标网格的边界
)

# === 5. 将预处理过的亮温数据重投影到目标网格
target_bt = kd_tree.resample_nearest(
    data=bt_new,
    fill_value=np.nan,  # 如果不设置，目标网格为无效值的像元的值会被设置为0
    source_geo_def=mwri_swath,
    target_geo_def=target_grid,
    radius_of_influence=10000,  # 单位为m，一般设置为源数据的空间分辨率
)
# 之所以目标网格会存在无效值的情况，可以考虑该条带不经过或不完全经过目标网格的情况

# target_bt 即为覆盖河南省的，空间分辨率为0.1度 X 0.1度的，等经纬度网格下的亮温
# 可用于后期的分析、输出、制图等
