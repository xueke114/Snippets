//
// Created by xueke on 2023/9/25.
//
// OSGEO4W用户：
// 安装了gdal-devel后，要设置CMAKE参数：-DCMAKE_PREFIX_PATH:PATH=C:/OSGeo4W
// 还要增加PATH变量PATH=C:\OSGeo4W\bin

#include <vector>

#include <string>
#include <iostream>
#include <gdal_priv.h>

int main() {
    GDALAllRegister();
    std::string filename = "C:/Datasets/RS/AMSR2_L3_BT-Global/6GHz/2022/GW1AM2_20211231_01D_EQMA_L3SGT06HA2220220.h5";

    // 打开文件
    auto fp = GDALOpen(filename.c_str(), GA_ReadOnly);

    // 解析数据集
    auto subsetdasets = CPLStringList(GDALGetMetadata(fp, "SUBDATASETS"));
    // 打开数据集
    auto bt_ds_name = subsetdasets["SUBDATASET_1_NAME"];
    auto bt_ds = GDALOpen(bt_ds_name, GA_ReadOnly);

    // 提取数据
    auto width = GDALGetRasterXSize(bt_ds);
    auto height = GDALGetRasterYSize(bt_ds);
    std::vector<uint16_t> data(width * height);
    auto bt_band = GDALGetRasterBand(bt_ds, 1);
    GDALRasterIO(bt_band, GF_Read, 0, 0, width, height, data.data(), width, height, GDT_UInt16, 0, 0);

    std::cout << data[width] << std::endl;

    // 关闭数据集
    GDALClose(bt_ds);
    return 0;
}