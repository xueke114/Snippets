#include <hdf5.h>



int
main(void)
{

    hid_t  file_id, dataset_id; /* identifiers */
    herr_t status;
    const float  dset_data[2041][486];
    const float
    /* Open an existing file. */
    file_id = H5Fopen("/mnt/c/Datasets/RS/AMSR2_L1B_BT-Pass-HeNan/GW1AM2_202201010435_218A_L1SGBTBR_2220220.h5", H5F_ACC_RDONLY, H5P_DEFAULT);

    /* Open an existing dataset. */
    dataset_id = H5Dopen(file_id, "Latitude of Observation Point for 89A", H5P_DEFAULT);

    status = H5Dread(dataset_id, H5T_NATIVE_FLOAT, H5S_ALL, H5S_ALL, H5P_DEFAULT, dset_data);

    /* Close the dataset. */
    status = H5Dclose(dataset_id);

    /* Open an existing dataset. */
    dataset_id = H5Dopen(file_id, "Longitude of Observation Point for 89A", H5P_DEFAULT);

    status = H5Dread(dataset_id, H5T_NATIVE_FLOAT, H5S_ALL, H5S_ALL, H5P_DEFAULT, dset_data);

    /* Close the dataset. */
    status = H5Dclose(dataset_id);
    /* Close the file. */
    status = H5Fclose(file_id);
}
