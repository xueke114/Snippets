#include <H5Cpp.h>
#include <iostream>
using namespace std;
int main()
{
    string filename = "Assets/FY3D_MWRIA_GBAL_L1_20220301_0242_010KM_MS.HDF";
    cout << "Open " << filename << endl;
    H5::H5File h5file(filename, H5F_ACC_RDONLY);
    h5file.close();
}
