# CMake 笔记

TAG: cpp; c++; cmake; 文件夹； 多层

## 1. 学习素材
1. 官方参考： [link](https://cmake.org/cmake/help/v3.22/guide/tutorial/A%20Basic%20Starting%20Point.html)
2. blibli简单视频：[link](https://www.bilibili.com/video/BV13K411M78v/?p=2&spm_id_from=333.880.my_history.page.click&vd_source=b342fa40afbba8924fa476ec9a7551fa)
3. csdn 参考：[link](https://blog.csdn.net/qq_31112205/article/details/105266306)


## 2. cmake 简单示例
创建一个简单的C++项目时，使用CMake可以帮助更方便地管理项目结构和构建过程， 说直白一些cmake通过CMakelist规则构建出编译器gcc的命令行。简单的CMake示例，包含一个源文件和一个头文件。具体文件在tuturial/cpp/cmake/get_start_2中。
### 2.1 项目结构
``` bash
project
|-- CMakeLists.txt 
|-- src # 一般存放cpp文件，具体实现的方法
|   |-- main.cpp
|   |-- hello_cmake.cpp
|-- include # 存放头文件
|   |-- hello_cmake.h
|-- build
```




## 3. cmake 第三方
### 3.1 使用opencv
以包管理的方式安装如何引入，以opencv引入。使用包管理器（如apt、brew等）来安装OpenCV，通过find进行查找。
``` bash
cmake_minimum_required(VERSION 3.12)
project(YourProjectName)

# 查找OpenCV库
find_package(OpenCV REQUIRED)

# 打印变量
message(">>> PROJECT_SOURCE_DIR=${PROJECT_SOURCE_DIR}") 
message(">>> OpenCV_INCLUDE_DIRS=${OpenCV_INCLUDE_DIRS}") 
message(">>> OpenCV_LIBS=${OpenCV_LIBS}") 

# include
include_directories(${PROJECT_SOURCE_DIR}/include)
include_directories(${OpenCV_INCLUDE_DIRS})

# 添加可执行文件, 链接OpenCV库
file(GLOB_RECURSE source_file ${PROJECT_SOURCE_DIR}/src/*.cpp)
add_executable(opencv_main ${source_file})
target_link_libraries(opencv_main -ljsoncpp ${OpenCV_LIBS})
```
### 3.2 使用eigen
手动编译的文件如何引入。这里主要讲述如何eigen通过cmake引入工程，暂不详述eigen如何编译，通过eigen官网下载素材后
``` bash
project
|-- CMakeLists.txt 
|-- src # 一般存放cpp文件，具体实现的方法
|   |-- main.cpp
|   |-- xxx.cpp
|-- include # 存放头文件
|   |-- xxx.h
|-- thirdparty
|   |-- eigen-3.4.0
```
cmake文件

```bash
cmake_minimum_required(VERSION 3.10)

project(employeeManager)

message(">>> PROJECT_SOURCE_DIR=${PROJECT_SOURCE_DIR}") 

include_directories(${PROJECT_SOURCE_DIR}/include)
include_directories(${PROJECT_SOURCE_DIR}/thirdparty/eigen-3.4.0/)
# include_directories(${PROJECT_SOURCE_DIR}/include/eigen-3.4.0/Eigen) 

file(GLOB_RECURSE source_file ${PROJECT_SOURCE_DIR}/src/*.cpp)
add_executable(eigen_learn ${source_file})
target_link_libraries(eigen_learn -ljsoncpp)
```

## 4. cmake 多个执行文件
为了执行一次编译生成多个可执行文件，使用CMake的多目标构建功能。以下是一个简单的示例，其中有两个包含main的文件read.cpp和save.cpp。 参考： [知乎link](https://zhuanlan.zhihu.com/p/57634435)
``` bash
project/
|-- CMakeLists.txt
|-- src/
|   |-- read.cpp
|   |-- save.cpp
|-- include/
|   |-- common.h
|-- src/
|   |-- common.cpp
```
read.cpp和save.cpp源码示例：
```c++
// main1.cpp 和 main2.cpp
#include <iostream>
#include "common.h"

int main() {
    printHello("main");
    return 0;
}
```
common内容
``` c++
// common.h
#pragma once

void printHello(const char* from);

// common.cpp
#include <iostream>
#include "common.h"

void printHello(const char* from) {
    std::cout << "Hello from " << from << "!" << std::endl;
}
```
CMakeLists.txt：
```bash
# 设置项目的最低版本要求
cmake_minimum_required(VERSION 3.10)

# 设置项目名称
project(MultiTargetExample)

# 指定 include 文件夹的路径
include_directories(include)

# 使用 file(GLOB ...) 命令获取 src 目录下的所有 .cpp 文件
file(GLOB SRC_FILES "src/*.cpp")

# 添加共享的 common.cpp 文件
list(REMOVE_ITEM SRC_FILES "${CMAKE_CURRENT_SOURCE_DIR}/src/read.cpp" "${CMAKE_CURRENT_SOURCE_DIR}/src/save.cpp")
set(COMMON_SOURCE "${CMAKE_CURRENT_SOURCE_DIR}/src/common.cpp")

# 添加两个可执行文件 read 和 save，分别链接 read.cpp 或 save.cpp 以及 common.cpp
add_executable(read src/read.cpp ${COMMON_SOURCE})
add_executable(save src/save.cpp ${COMMON_SOURCE})

```