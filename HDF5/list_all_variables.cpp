//
// Created by xueke on 2023/9/30.
//

#include <H5Cpp.h>
#include <iostream>

using namespace H5;
using namespace std;

int main() {
    const char *filename = "C:/Datasets/RS/FY-3D_MWRI_10KM_Pass-Henan/2022/FY3D_MWRIA_GBAL_L1_20220101_0549_010KM_MS.HDF";
    H5File h5obj(filename, H5F_ACC_RDONLY);
    auto root_group = h5obj.openGroup("/");
    auto count = root_group.getNumObjs();
    cout << count << endl;
    for (int i = 0; i < count; i++) {
        cout << root_group.getObjnameByIdx(i) << endl;
    }
    h5obj.close();
}