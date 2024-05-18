cmake_minimum_required(VERSION 3.15)
project(MyProject)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# 设置Debug or Release
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build (Debug or Release)" FORCE)
endif()

# 包含Conan生成的CMake文件
# 相当于cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
message(STATUS "CMAKE_BINARY_DIR directory: ${CMAKE_BINARY_DIR}")
set(CMAKE_TOOLCHAIN_FILE ${CMAKE_BINARY_DIR}/conan_toolchain.cmake CACHE STRING "" FORCE)

# opencv
#set(OpenCV_DIR "/opt/homebrew/include/opencv4")
find_package(OpenCV REQUIRED)
# set(nlohmann_json_DIR "/Users/xiaomi/workspace/cvcv/tuturial/cpp/cmake/conan_opencv_json/build")
set(nlohmann_json_DIR ${CMAKE_BINARY_DIR})
find_package(nlohmann_json REQUIRED)

# 输出nlohmann_json include路径
get_target_property(NLOHMANN_JSON_INCLUDE_DIRS nlohmann_json::nlohmann_json INTERFACE_INCLUDE_DIRECTORIES)
message(STATUS "nlohmann_json include directories: ${NLOHMANN_JSON_INCLUDE_DIRS}") # 找到文件地址，可以配置到vscode


# # 添加你的源文件和库
add_executable(my_app main.cpp)

# # 链接OpenCV和json库
target_link_libraries(my_app nlohmann_json::nlohmann_json)
target_link_libraries(my_app ${OpenCV_LIBS})
