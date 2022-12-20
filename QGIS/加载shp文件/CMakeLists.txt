cmake_minimum_required(VERSION 3.15)
project(testQGIS)

#set(CMAKE_CXX_STANDARD 11)

set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

SET(CMAKE_MODULE_PATH /usr/share/qgis/ ${CMAKE_MODULE_PATH})
find_package(Qt5Widgets)
find_package(Qt5Xml)
FIND_PACKAGE(QGIS)
add_executable(testQGIS main.cpp)
target_include_directories(testQGIS PRIVATE ${QGIS_INCLUDE_DIR})
target_link_libraries(testQGIS Qt5::Widgets Qt5::Xml ${QGIS_CORE_LIBRARY} ${QGIS_GUI_LIBRARY})
