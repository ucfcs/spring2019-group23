// cloud_coverage.cpp : This file contains the 'main' function. Program execution begins and ends there.
//


#include "pch.h"
#include "imgcodecs.hpp"
#include "highgui.hpp"
#include "stitching.hpp"
#include "core/core.hpp"
#include <highgui/highgui.hpp>
#include <core/mat.hpp>
#include <math.h>
#include <iostream>

using namespace std;
using namespace cv;

int main()
{
	Mat I = imread("pictures/1.jpg", CV_LOAD_IMAGE_COLOR);
	namedWindow("Display window", WINDOW_AUTOSIZE);// Create a window for display.
	imshow("Display window", image);                   // Show our image inside it.

	waitKey(0);                                          // Wait for a keystroke in the window
	return 0;

	return 0;
}