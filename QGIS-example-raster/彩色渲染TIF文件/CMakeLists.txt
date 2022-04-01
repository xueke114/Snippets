cmake_minimum_required(VERSION 3.15)

project(HelloGIS LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_MODULE_PATH /usr/share/qgis/ ${CMAKE_MODULE_PATH})

find_package(QGIS)
find_package(Qt5Xml)
find_package(Qt5Widgets)
add_executable(HelloGIS main.cpp)
target_include_directories(HelloGIS PRIVATE ${QGIS_INCLUDE_DIR})
target_link_libraries(HelloGIS Qt5::Widgets Qt5::Xml ${QGIS_CORE_LIBRARY} ${QGIS_GUI_LIBRARY})
target_compile_options(HelloGIS PRIVATE -Wno-deprecated-declarations)
