cmake_minimum_required(VERSION 3.15)

project(QtSnippets)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt5 COMPONENTS Core Gui Widgets Concurrent Network Multimedia MultimediaWidgets REQUIRED)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

add_executable(productRandomInt randomInt.cpp)
target_link_libraries(productRandomInt PRIVATE Qt::Core)

add_executable(fileSha256 获取文件的sha256.cpp)
target_link_libraries(fileSha256 PRIVATE Qt::Core)

add_executable(miniProgressBar miniProgressBar.cpp)
target_link_libraries(miniProgressBar PRIVATE Qt::Widgets Qt::Concurrent)

add_executable(autoManualCheckUpdate AutoManualCheckUpdate.cpp)
target_link_libraries(autoManualCheckUpdate PRIVATE Qt::Widgets Qt::Network)

add_executable(cameraMonitor CameraMonitor.cpp)
target_link_libraries(cameraMonitor PRIVATE Qt::Widgets Qt::Multimedia Qt::MultimediaWidgets)

add_executable(commandLineParser commandLineParser.cpp)
target_link_libraries(commandLineParser Qt::Core)

add_executable(httpGet httpGet.cpp)
target_link_libraries(httpGet Qt5::Core Qt5::Network)
