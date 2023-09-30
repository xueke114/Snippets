// 来自文心一言，有改动
// 原方法是递归，让它改栈实现了

#include <H5Cpp.h>
#include <iostream>
#include <string>
#include <stack>

void print_group_names(const H5::Group &group) {
    // 获取组的成员数量
    hsize_t num_members = group.getNumObjs();

    // 遍历组的所有成员
    for (hsize_t i = 0; i < num_members; i++) {
        // 获取成员的名称和类型
        H5std_string member_name = group.getObjnameByIdx(i);
        H5G_obj_t member_type = group.getObjTypeByIdx(i);

        // 如果成员是组，则将其添加到待处理组的栈中
        if (member_type == H5G_GROUP) {
            std::cout << "/" << member_name << std::endl;
            std::stack<H5::Group> groups;
            groups.push(group.openGroup(member_name));

            // 处理待处理的组，直到栈为空
            while (!groups.empty()) {
                H5::Group current_group = groups.top();
                groups.pop();

                num_members = current_group.getNumObjs();
                for (hsize_t j = 0; j < num_members; j++) {
                    H5std_string sub_member_name = current_group.getObjnameByIdx(j);
                    H5G_obj_t sub_member_type = current_group.getObjTypeByIdx(j);

                    if (sub_member_type == H5G_GROUP) {
                        std::cout << "  " << sub_member_name << std::endl;
                        groups.push(current_group.openGroup(sub_member_name));
                    } else if (sub_member_type == H5G_DATASET) {
                        std::cout << "  " << sub_member_name << std::endl;
                    }
                }
            }
        }
            // 如果成员是数据集，则打印其名称
        else if (member_type == H5G_DATASET) {
            std::cout << "/" << member_name << std::endl;
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