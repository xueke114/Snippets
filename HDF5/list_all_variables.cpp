// 来自文心一言，有改动
// 但递归似乎不是个好的方法，Clang-Tidy给标记出来了（但感觉很合适这个场景）

#include <H5Cpp.h>
#include <iostream>
#include <string>

void print_group_names(const H5::Group &group, const std::string &indent = "") {
    // 获取组的成员数量
    hsize_t num_members = group.getNumObjs();
    // 遍历组的所有成员
    for (hsize_t i = 0; i < num_members; i++) {
        // 获取成员的名称和类型
        auto member_name = group.getObjnameByIdx(i);
        auto member_type = group.getObjTypeByIdx(i);
        // 如果成员是组，则递归打印其名称和子组的名称
        if (member_type == H5G_GROUP) {
            std::cout << indent << "Group -> " << member_name << std::endl;
            H5::Group subgroup(group.openGroup(member_name));
            print_group_names(subgroup, indent + "  ");
        }
            // 如果成员是数据集，则打印其名称
        else if (member_type == H5G_DATASET) {
            std::cout << indent << "Datasets -> " << member_name << std::endl;
        }
    }
}

int main(int argc, char **argv) {
    // 检查命令行参数
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <hdf5_file>" << std::endl;
        return 1;
    }
    std::cout << argv[1] << std::endl;
    // 打开HDF5文件
    H5::H5File file(argv[1], H5F_ACC_RDONLY);

    // 获取文件的根组
    H5::Group root_group = file.openGroup("/");

    // 打印根组的名称和子组的名称以及数据集的名称
    print_group_names(root_group);

    return 0;
}