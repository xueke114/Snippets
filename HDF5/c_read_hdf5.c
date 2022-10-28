#include<hdf5.h>
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
char* get_obj_name(hid_t objid,hsize_t index) {
	ssize_t name_len = H5Lget_name_by_idx(objid, ".", H5_INDEX_NAME, H5_ITER_INC, index, NULL, 0, H5P_DEFAULT) + 1;
	char* group_name = (char*)malloc(name_len);
	H5Lget_name_by_idx(objid, ".", H5_INDEX_NAME, H5_ITER_INC, index, group_name, name_len, H5P_DEFAULT);
	return group_name;
}
void list_all_vars_name(hid_t fileid) {
	printf("List All Variables' Name\n");

	H5G_info_t ginfo;
	herr_t ret_value;
	ret_value = H5Gget_info(fileid, &ginfo);
	printf("Group Nummber is : %lld\n", ginfo.nlinks);

	for (int i = 0; i < ginfo.nlinks; i++) {
		printf("<Group> ");
		char* group_name = get_obj_name(fileid, i);
		printf("%s\n", group_name);

		//打开Group，获取该Group下的Dataset个数
		hid_t group_id = H5Gopen(fileid, group_name, H5P_DEFAULT);
		ret_value = H5Gget_info(group_id, &ginfo);
		printf("\tDatasets Number is: %lld\n", ginfo.nlinks);

		for (int j = 0; j < ginfo.nlinks; j++) {
			printf("\t<Dataset> | ");
			char* dataset_name = get_obj_name(group_id, j);
			//打开dataset，获取dataset的形状
			hid_t dataset_id = H5Dopen(group_id, dataset_name, H5P_DEFAULT);
			hid_t space_id = H5Dget_space(dataset_id);
			int space_size = H5Sget_simple_extent_ndims(space_id);
			hsize_t* shape = (hsize_t*)malloc(space_size);
			H5Sget_simple_extent_dims(space_id, shape, NULL);
			printf("<");
			hsize_t *p = shape;
			while (p<(shape+space_size))
				printf("%lld x ", *p++);
			
			printf("\b\b\b> %s\n", dataset_name);
		}
	}
}

int main() {
	printf("你好, HDF5\n");

	hsize_t file_path_len;
	hid_t file_id;
	herr_t status;

	const char* filedir = "C:/Datasets/FY3D-MWRI-10000M-Global/Ascending/20220201/";
	const char* filename = "FY3D_MWRIA_GBAL_L1_20220201_0115_010KM_MS.HDF";
	file_path_len = strlen(filedir) + strlen(filename) + 2;
	char* filepath = (char*)malloc(file_path_len);
	strcpy_s(filepath, file_path_len, filedir);
	strcat_s(filepath, file_path_len, filename);


	file_id = H5Fopen(filepath, H5F_ACC_RDONLY, H5P_DEFAULT);
	list_all_vars_name(file_id);
	status = H5Fclose(file_id);

	return 0;
}
