// MSVC需要设置预处理器H5_BUILT_AS_DYNAMIC_LIB;
#include<vector>
#include<iostream>
#include<H5Cpp.h>
#include<Eigen/Dense>
#include<unsupported/Eigen/CXX11/Tensor>

int main() {
    //定义变量
    std::string fileName = "Assets/FY3D_MWRIA_GBAL_L1_20220301_0242_010KM_MS.HDF";
    // 打开文件
    auto h5_obj = H5::H5File(fileName, H5F_ACC_RDONLY);
    // 打开数据集
    auto lat_ds = h5_obj.openDataSet("Calibration/EARTH_OBSERVE_BT_10_to_89GHz");
    // 获取数据集形状
    H5::DataSpace ds_space = lat_ds.getSpace();
    auto ndims = ds_space.getSimpleExtentNdims();
    auto shape = new hsize_t[ndims];
    ds_space.getSimpleExtentDims(shape);
    std::cout << "Deep: " << shape[0] << " Height: " << shape[1] << " Width: " << shape[2] << std::endl;
    // 为ds分配空间
    Eigen::Tensor<int16_t, 3,Eigen::RowMajor> eigen_data(shape[0], shape[1], shape[2]);
    // 读取ds
    lat_ds.read(eigen_data.data(), H5::PredType::NATIVE_INT16);
    // 输出ds（每前5维的(0,0)值）
    Eigen::array<Eigen::Index, 3> offsets = {0, 0, 0};
    Eigen::array<Eigen::Index, 3> extents = {5, 1, 1};
    std::cout << eigen_data.slice(offsets, extents) << std::endl;

    //关闭句柄
    delete[] shape;
    ds_space.close();
    lat_ds.close();
    h5_obj.close();
}
