// MSVC需要设置预处理器H5_BUILT_AS_DYNAMIC_LIB;
#include<vector>
#include <iostream>
#include<H5Cpp.h>

int main() {
    //定义变量
    std::string fileName = "Assets/FY3D_MWRIA_GBAL_L1_20220301_0242_010KM_MS.HDF";
    // 打开文件
    auto h5_obj = H5::H5File(fileName, H5F_ACC_RDONLY);
    // 打开数据集
    auto lat_ds = h5_obj.openDataSet("Geolocation/Latitude");
    // 获取数据集形状
    auto ds_space = lat_ds.getSpace();
    auto size = ds_space.getSimpleExtentNdims();
    auto shape = new hsize_t[size];
    ds_space.getSimpleExtentDims(shape);
    std::cout << "Height: " << shape[0] << " Width: " << shape[1] << std::endl;
    // 为ds分配空间
    std::vector<float> out_data(shape[0]*shape[1]);
    // 读取ds
    lat_ds.read(out_data.data(), H5::PredType::NATIVE_FLOAT);
    std::cout << out_data[1] << std::endl;

    //关闭句柄
    delete[] shape;
    ds_space.close();
    lat_ds.close();
    h5_obj.close();
}
