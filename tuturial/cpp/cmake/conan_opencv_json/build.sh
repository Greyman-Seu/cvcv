mkdir build
# install build
conan install . --output-folder=build --build=missing # TODO: 将依赖下载到子目录

# cmake
cd build
cmake ..
make -j8
./my_app