/*
 * main.cpp
 *
 *  Created on: 29 апр. 2018 г.
 *      Author: snork
 */

#include <mutex>
#include <condition_variable>

#include <boost/asio/io_service.hpp>

#include <opencv/highgui.h>
#include <opencv/cv.h>


#include "../common/log.hpp"
#include "../camera-witchcraft/Camera.hpp"

auto _slg = build_free_logger("main");

void on_frame(std::shared_ptr<Cam::Camera::Frame> frame)
{
	LOG_INFO << "got frame!";
}


int main()
{
	int width = 640;
	int height = 480;

	LOG_INFO << "hello world?";
	Cam::Camera cam;

	cam.open("/dev/video0");
	cam.set_fmt(width, height, V4L2_PIX_FMT_YUYV);

	std::mutex mtx;
	std::condition_variable frame_cv;
	std::shared_ptr<Cam::Camera::Frame> latest_frame;

	auto frame_handler = [&](std::shared_ptr<Cam::Camera::Frame> frame) {
		std::unique_lock<std::mutex> lock(mtx);
		latest_frame = frame;
		frame_cv.notify_all();
	};

	cam.on_frame.connect(frame_handler);
	cam.start();

	cv::namedWindow("cv", 1);
	cv::Mat cv_buf_frame = cv::Mat(cv::Size(width, height), CV_8UC2);
	for(;;)
	{
		cv::Mat cv_frame;
		{
			std::unique_lock<std::mutex> lock(mtx);
			while (!latest_frame)
				frame_cv.wait(lock);

			std::memcpy(cv_buf_frame.ptr<uint8_t*>(0), latest_frame->data(), latest_frame->dataSize());
		}
		cv::cvtColor(cv_buf_frame, cv_frame, cv::COLOR_YUV2BGR_YUY2);

		imshow("cv", cv_frame);
		if(cv::waitKey(30) >= 0)
			break;
	}

	return 0;
}


