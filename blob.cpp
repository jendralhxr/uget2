#include <iostream>
#include <iomanip>
#include <fstream>
#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <math.h>

using namespace std;
using namespace cv;
	
int main(int argc, char **argv){
	Ptr<Feature2D> sbd = SimpleBlobDetector::create();
	
	FileStorage fs_read("SimpleBlobDetector_params.xml", FileStorage::READ);
    if (fs_read.isOpened()) // if we have file with parameters, read them
    {
        sbd->read(fs_read.root());
        fs_read.release();
    }
    else // else modify the parameters and store them; user can later edit the file to use different parameters
    {
        fs_read.release();
        FileStorage fs_write("SimpleBlobDetector_params.xml", FileStorage::WRITE);
        sbd->write(fs_write);
        fs_write.release();
    }
	Mat result, image = imread(argv[1], IMREAD_COLOR); 
	vector<KeyPoint> keypoints;
	sbd->detect(image, keypoints, Mat());
	
	int n;
	drawKeypoints(image, keypoints, result);
	for (vector<KeyPoint>::iterator k = keypoints.begin(); k != keypoints.end(); ++k)
		{circle(result, k->pt, (int)k->size, Scalar(0, 0, 255), 2);
		n++;}
	cout << n << " points" << endl;
	imshow("result", result);
	imwrite("output.png", result);
	waitKey(0);
}
