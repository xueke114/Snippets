// g++ read_dataset.cpp -o read_dataset -lmfhdf

#include <iostream>
#include <vector>
#include <mfhdf.h>

int main() {
    // 打开文件
    const char* filename = "D:/RSDatasets/Terra-MODIS-NDVI-1000M/2018-China/MOD13A3.A2018001.h21v03.061.2021316203458.hdf";
    int32 sd_id = SDstart(filename, DFACC_READ);

    // 检索目标数据集的index
    int32 sds_index = SDnametoindex(sd_id, "1 km monthly NDVI");

    // 打开目标数据集
    int32 sds_id = SDselect(sd_id, sds_index);

    // 读数据,第一行的前十个数
    std::vector<int16> out_data(10);
    // 读数据，设置起始和终止的位置
    int32 start_cor[2] = {0, 0};
    int32 end_cor[2] = {1, 10};
    // 读数据
    SDreaddata(sds_id, start_cor, NULL, end_cor, out_data.data());

    // 输出数据
    for (const auto &pix : out_data)
        std::cout << pix << std::endl;

    // 关闭数据
    SDendaccess(sds_id);
    SDend(sd_id);
    return 0;
}
