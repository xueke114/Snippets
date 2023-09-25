cmake_minimum_required(VERSION 3.15)
project(GDAL-Demo)

find_package(GDAL)

add_executable(gdal-read-to-vector gdal-read-to-vector.cpp)

target_link_libraries(gdal-read-to-vector GDAL::GDAL)