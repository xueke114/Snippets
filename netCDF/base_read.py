import netCDF4

def list_all_vars_name(obj):
    for var in nc_obj.variables:
        print(var)
    

if __name__ == "__main__":
    filename = r"C:\Datasets\OSTIA\202202\20220201120000-UKMO-L4_GHRSST-SSTfnd-OSTIA-GLOB-v02.0-fv02.0.nc"
    
    nc_obj = netCDF4.Dataset(filename,mode="r")
    list_all_vars_name(nc_obj)