cmake_minimum_required(VERSION 3.15)

project(QtSnippets)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 COMPONENTS Core Gui Widgets Concurrent Network REQUIRED)
qt_standard_project_setup()

add_executable(fileSha256 获取文件的sha256.cpp)
target_link_libraries(fileSha256 PRIVATE  Qt::Core)

add_executable(miniProgressBar miniProgressBar.cpp)
target_link_libraries(miniProgressBar PRIVATE  Qt::Widgets Qt::Concurrent)

add_executable(autoManualCheckUpdate AutoManualCheckUpdate.cpp)
target_link_libraries(autoManualCheckUpdate PRIVATE Qt::Widgets Qt::Network)