# 1 安装Conan

首先，确保你已经安装了Conan。如果还没有安装，可以通过Python的pip工具来安装：
~~~
pip install conan
~~~
# 2 依赖编写
## 2.1 创建一个Conan文件

在你的项目根目录下，创建一个名为conanfile.txt的文件，这个文件将用来声明你的项目依赖。
这里，我们指定了OpenCV的版本为4.x，nlohmann_json（一个流行的C++ JSON库）的版本为3.x，并且指定了CMake作为生成器。
官方说明：https://docs.conan.io/2/tutorial/consuming_packages/build_simple_cmake_project.html

## 2.2 conan源

1. 首先，查看当前Conan配置中已知的远程仓库列表：
~~~
conan remote list
~~~
这会显示出所有已经配置的远程仓库及其别名和URL。

2. 添加新的远程仓库

如果列表中没有包含你想要的包（例如，OpenCV 4.5.4），你可以尝试添加一个新的远程仓库。Conan Center Index (CCI) 是Conan官方推荐的包仓库，包含了大量的开源库，包括OpenCV的多个版本。

~~~
conan remote add conan-center https://center.conan.io
~~~
这条命令会添加Conan Center Index作为远程源，命名为conan-center。如果你已经添加过但仍然找不到包，可以尝试更新远程索引：

~~~
conan remote update conan-center
~~~

3. 搜索包

在更新或添加远程之后，你可以尝试搜索你需要的包版本，确认它是否可用：

~~~
conan search opencv/4.5.4@
~~~

4. 重新安装依赖

现在你应该能够重新运行conan install命令来安装OpenCV了：


