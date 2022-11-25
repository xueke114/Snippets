#include <iostream>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <vector>

using namespace std;
using namespace cv;

void fillimg(Mat img, vector<Scalar> colors) {
    int y = 0;
    int colorsNum = colors.size();
    int step = img.rows / colorsNum;
    for (int i = 0; i < colorsNum; i++) {
        rectangle(img, Point(0, y), Point(img.cols, y + step), colors[i], FILLED);
        y += step;
    }
}

int main() {
    Mat img = Mat::zeros(400, 400, CV_8UC3);
    vector<Scalar> colorSheet = { Scalar(39, 32, 217), Scalar(52, 146, 255),
                                 Scalar(60, 205, 255), Scalar(186, 208, 53) };
    fillimg(img, colorSheet);

    imshow("TestOpencvShow", img);
    waitKey();
    return 0;
}
