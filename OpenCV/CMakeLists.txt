cmake_minimum_required(VERSION 3.15)
project(OpenCV-Demo)

# 如果在Windows上使用的是opencv官网下载的版本
# 需要添加PATH=C:\myLibs\opencv\build\x64\vc16\bin

find_package(OpenCV)

add_executable(openCamera 打开摄像头.cc)
target_link_libraries(openCamera PRIVATE ${OpenCV_LIBS})

add_executable(drawWindow 绘制图形.cc)
target_link_libraries(drawWindow PRIVATE ${OpenCV_LIBS})
