# 设置项目的最低版本要求
cmake_minimum_required(VERSION 3.10)

# 设置项目名称
project(MyProject)

#打印一下目录情况
message(">>> PROJECT_SOURCE_DIR=${PROJECT_SOURCE_DIR}") 

# 指定 include 文件夹的路径
include_directories(${PROJECT_SOURCE_DIR}/include)

# 使用 file(GLOB ...) 命令获取 src 目录下的所有 .cpp 文件
# file(GLOB SRC_FILES ${PROJECT_SOURCE_DIR}/src/*.cpp)
file(GLOB_RECURSE SRC_FILES ${PROJECT_SOURCE_DIR}/src/*.cpp)

# 输出 SRC_FILES 的内容
message(STATUS "Source files: ${SRC_FILES}")

# 添加可执行文件，并将所有源文件链接到该可执行文件
add_executable(my_executable ${SRC_FILES})
