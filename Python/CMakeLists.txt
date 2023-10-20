cmake_minimum_required(VERSION 3.15)

project(python-and-c)

find_package(Python3 COMPONENTS Development)
# Windows 如果是从官方下载安装的Python，并将Python添加到Path变量，可以正常find

add_executable(c_run_python_string runPythonString.c)
target_link_libraries(c_run_python_string PRIVATE Python3::Python)

add_executable(c_run_python_script runPythonScript.c)
target_link_libraries(c_run_python_script PRIVATE Python3::Python)