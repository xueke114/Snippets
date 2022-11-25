#include<vector>
#include<iostream>
#include<boost/filesystem.hpp>
#include<boost/algorithm/string.hpp>
#include<boost/xpressive/xpressive.hpp>

std::vector<boost::filesystem::path> find_files(const boost::filesystem::path& dir, const std::string filename) {
    static boost::xpressive::sregex_compiler rc;
    if (!rc[filename].regex_id()) {
        std::string str = boost::replace_all_copy(boost::replace_all_copy(filename, ".", "\\."), "*", ".*");
        rc[filename] = rc.compile(str);
    }
    std::vector<boost::filesystem::path> result_v;
    if(!boost::filesystem::exists(dir) || !boost::filesystem::is_directory(dir))
        return result_v;

    boost::filesystem::directory_iterator it_end;
    for(boost::filesystem::directory_iterator pos(dir); pos != it_end; ++pos) {
        if(!boost::filesystem::is_directory(*pos) && boost::xpressive::regex_match(pos->path().filename().string(), rc[filename]))
            result_v.push_back(pos->path());
    }
    return result_v;
}

int main() {
    auto v = find_files("C:\\Datasets\\FY3D-MERSI-SST\\day\\202206", "*.HDF");
    for(boost::filesystem::path &p : v)
        std::cout << p << std::endl;

    return 0;
}
