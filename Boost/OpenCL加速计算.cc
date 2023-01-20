// 测试使用C++ & OpenCL，逐像元计算2022年6月白天的30个MERSI SST正弦值的耗时
// 每个MERSI SST文件的像元数3600x7200
// 在联想小新Air 13Pro上，纯C++方法耗时77秒，OpenCL方法耗时17秒
// 编译指令(For AMD on Linux)
// g++ OpenCL加速计算.cc -o helloOpenCL -I /usr/include/hdf5/serial/ -I /opt/rocm/include/ -L /usr/lib/x86_64-linux-gnu/hdf5/serial/  -L /opt/rocm/lib/ -lOpenCL -lboost_filesystem -lboost_timer -lhdf5 -lhdf5_cpp

#include<cmath>
#include<vector>
#include<iostream>
#include<algorithm>

#include<H5Cpp.h>
#include<boost/filesystem.hpp>
#include<boost/timer/timer.hpp>
#include<boost/xpressive/xpressive.hpp>
#include<boost/compute/functional/math.hpp>
#include<boost/compute/container/vector.hpp>
#include<boost/compute/algorithm/transform.hpp>


namespace compute = boost::compute;



std::vector<boost::filesystem::path> find_files(const boost::filesystem::path& dir, const std::string filename) {
    static boost::xpressive::sregex_compiler rc;
    if (!rc[filename].regex_id()) {
        std::string str = boost::replace_all_copy(boost::replace_all_copy(filename, ".", "\\."), "*", ".*");
        rc[filename] = rc.compile(str);
    }
    std::vector<boost::filesystem::path> result_v;
    if(!boost::filesystem::exists(dir) || !boost::filesystem::is_directory(dir))
        return result_v;

    boost::filesystem::directory_iterator it_end;
    for(boost::filesystem::directory_iterator pos(dir); pos != it_end; ++pos) {
        if(!boost::filesystem::is_directory(*pos) && boost::xpressive::regex_match(pos->path().filename().string(), rc[filename]))
            result_v.push_back(pos->path());
    }
    return result_v;
}


int main() {
    size_t device_idx,idx=1;
    auto v = find_files("/home/xueke/RSDatasets/FY3D-MERSI-SST/day/202206", "*.HDF");
    // 获取OpenCL设备
    auto devices = boost::compute::system::devices();
    auto device_count = boost::compute::system::device_count();

    if (device_count==0) {
        std::cout<<"OpenCL Device NOT FOUND!!!!!"<<std::endl;
        exit(EXIT_FAILURE);
    }

    std::cout<<"Available Devices:"<<std::endl;
    std::cout<<"\t"<<"ID"<<" | "<<"Device(s)"<<std::endl;
    std::cout<<"\t"<<"=="<<" | "<<"==============="<<std::endl;
    for(const auto &d:devices) {
        std::cout<<"\t"<<idx++<<"     "<<d.platform().name()<<" "<<d.name()<<std::endl;
        std::cout<<"\t"<<"--"<<" | "<<"----------------"<<std::endl;
    }
    std::cout<<"====================="<<std::endl;

    std::cout<<"Enter Device ID:";
    std::cin>>device_idx;

    while(device_idx < 1 || device_idx > device_count) {
        std::cout<<"The ID entered is invalid, please re-enter it：";
        std::cin>>device_idx;
    }

    auto device = devices[device_idx-1];
    std::cout <<"Using "<< device.platform().name() << " " << device.name() << std::endl;
    compute::context context(device);
    compute::command_queue queue(context, device);

    // 逐文件读取
    boost::timer::auto_cpu_timer t;
    for(boost::filesystem::path &filepath : v) {
        std::cout << filepath << std::endl;

        // 读取HDF5数据集
        H5::H5File h5_obj = H5::H5File(filepath.string(), H5F_ACC_RDONLY);
        H5::DataSet sst_ds = h5_obj.openDataSet("sea_surface_temperature");
        // 获取数据集大小
        H5::DataSpace sst_space = sst_ds.getSpace();
        int ds_rank = sst_space.getSimpleExtentNdims();
        std::vector<hsize_t> shape(ds_rank);
        sst_space.getSimpleExtentDims(shape.data());
        std::cout << shape[0] << " " << shape[1] << std::endl;
        // 读数据
        std::vector<int16_t> sst_data(shape[0]*shape[1]);
        sst_ds.read(sst_data.data(), H5::PredType::NATIVE_INT16);

        // 在主机上创建结果向量
        std::vector<float> result(sst_data.size());

        // 传统迭代计算
//        auto result_it = result.begin();
//        for (auto it=sst_data.cbegin(); it!=sst_data.cend(); ++it) {
//            *result_it=std::sin(*it);
//            ++result_it;
//        }


        // OpenCL迭代计算
        // 在OpenCL设备上创建数据
        compute::vector<float> device_vector(sst_data.size(), context);
        // 将主机数据传输到OpenCL设备
        compute::future<void> f=compute::copy_async(sst_data.begin(), sst_data.end(), device_vector.begin(), queue);
        // 关闭HDF5
        sst_space.close();
        sst_ds.close();
        h5_obj.close();
        // 在OpenCL设备上进行计算
        f.wait();
        compute::transform(device_vector.begin(), device_vector.end(), device_vector.begin(), compute::sin<float>(), queue);
        // 将计算结果传输到主机
        compute::copy(device_vector.begin(), device_vector.end(), result.begin(), queue);

        // 输出指定位置上的值
        std::cout<<sst_data[2880000]<<" "<<result[2880000]<<std::endl;
    }

    std::cout<<"====================="<<std::endl;
    return 0;

}
