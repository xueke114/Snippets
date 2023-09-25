//
// MSVC 编译指令
// cl opencl-test.cpp /EHsc /I C:\OSGeo4W\include\boost-1_74 /I C:\OSGeo4W\include /MD /link /libpath:C:\OSGeo4W\lib\ libboost_chrono-vc142-mt-x64-1_74.lib opencl.lib

#include<vector>
#include<algorithm>
#include<iostream>
#include<boost/compute/algorithm/transform.hpp>
#include<boost/compute/container/vector.hpp>
#include<boost/compute/functional/math.hpp>

namespace compute=boost::compute;

int main() {

    // 获取默认opencl设备并设置上下文
    compute::device device=compute::system::default_device();
    std::cout<<device.name()<<std::endl;
    std::cout<<device.platform().name()<<std::endl;

    compute::context context(device);
    compute::command_queue queue(context,device);

    // 生成随机数据
    std::vector<float> host_vector(200000000);
    std::generate(host_vector.begin(),host_vector.end(),rand);
    std::cout<<host_vector[0]<<" "<<host_vector[1]<<" "<<host_vector[2]<<std::endl;

    //在opencl设备上创建数据
    compute::vector<float> device_vector(host_vector.size(),context);

    // 将主机数据传输到opencl设备
    compute::copy(host_vector.begin(),host_vector.end(),device_vector.begin(),queue);

    // 在opencl设备上进行计算
    compute::transform(device_vector.begin(),device_vector.end(),device_vector.begin(),compute::sqrt<float>(),queue);
    // 将计算结果传输到主机
    compute::copy(device_vector.begin(),device_vector.end(),host_vector.begin(),queue);

    // 输出计算结果
    std::cout<<host_vector[0]<<" "<<host_vector[1]<<" "<<host_vector[2]<<std::endl;

    return 0;
}
