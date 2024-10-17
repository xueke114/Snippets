cmake_minimum_required(VERSION 3.15)
project(OpenCV-Demo)

# 如果在Windows上使用的是opencv官网下载的版本
# 需要添加PATH=C:\myLibs\opencv\build\x64\vc16\bin

find_package(OpenCV)

add_executable(openCamera openCamera.cc)
target_link_libraries(openCamera PRIVATE ${OpenCV_LIBS})

add_executable(drawGraph drawGraph.cc)
target_link_libraries(drawGraph PRIVATE ${OpenCV_LIBS})
