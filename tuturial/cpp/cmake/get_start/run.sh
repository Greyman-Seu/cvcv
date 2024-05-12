echo =============================
echo test cmake .....
echo =============================
echo 

mkdir build
cd build
cmake ..
make -j8
./my_executable
cd ..
rm -rf build

echo 
echo success