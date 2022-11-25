#include<iostream>
#include<opencv2/highgui.hpp>
#include<opencv2/imgproc.hpp>

int main() {
    std::cout << "OpenCV version :" << CV_VERSION << std::endl;

    cv::Mat image;
    cv::VideoCapture camera;
    camera.open(0);
    if (camera.isOpened()) {
        std::cout << "Camera is opened" << std::endl;
        while (1) {
            camera >> image;
            if (image.empty())
                break;
            cv::imshow("TestCamera", image);
            if (cv::waitKey(33) >= 0)
                break;
        }
    } else {
        std::cout << "No Camera" << std::endl;
        image = cv::Mat::zeros(400, 400, CV_8UC3);
        cv::putText(image, "No Camera", cv::Point(image.cols / 4, image.rows / 2), 2,1,cv::Scalar(0,0,255),2,16,0);
        cv::imshow("TestCamera", image);
        cv::waitKey(0);
    }
    return 0;
}
