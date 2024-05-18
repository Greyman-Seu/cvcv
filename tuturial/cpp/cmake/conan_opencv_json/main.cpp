#include <iostream>
#include <fstream>
#include <opencv2/opencv.hpp>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

int main() {
    // 读取 JSON 文件
    std::ifstream ifs("../data.json");
    if (!ifs.is_open()) {
        std::cerr << "Error opening JSON file" << std::endl;
        return -1;
    }

    json j;
    ifs >> j;

    // 打印is_student字段内容
    bool is_student = j["is_student"];
    std::cout << "is_student: " << std::boolalpha << is_student << std::endl;

    // 读取图像
    cv::Mat image = cv::imread("../demo.png");

    // 检查图像是否成功加载
    if (image.empty()) {
        std::cerr << "Error loading image" << std::endl;
        return -1;
    }

    // 打印图像尺寸
    std::cout << "Image Size: " << image.size() << std::endl;

    return 0;
}
