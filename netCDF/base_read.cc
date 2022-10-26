#include<netcdf>

void list_all_vars_name(netCDF::NcFile& ncObj) {
	for (auto x : ncObj.getVars())
		std::cout << x.first << std::endl;
}

int main() {
	std::string filename = "C:/Datasets/20220201120000-UKMO-L4_GHRSST-SSTfnd-OSTIA-GLOB-v02.0-fv02.0.nc";

	try {
		netCDF::NcFile ncfile(filename, netCDF::NcFile::read);
		list_all_vars_name(ncfile);
		ncfile.close();
	}
	catch (netCDF::exceptions::NcException& e) {
		std::cout << e.what() << std::endl;
	}

	return 0;
}