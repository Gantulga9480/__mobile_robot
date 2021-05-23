#include "ros/ros.h"
#include "robot/board.h"
#include "image_transport/image_transport.h"
#include "cv_bridge/cv_bridge.h"
#include "sensor_msgs/image_encodings.h"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <math.h>

using namespace cv;
using namespace std;

static const std::string OPENCV_WINDOW = "Depth Image";
static const int NODE_RES = 20;

void cb(const sensor_msgs::ImageConstPtr& msg)
{
    cv_bridge::CvImagePtr cv_ptr;
    try
    {
      cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::TYPE_32FC1);
    }
    catch (cv_bridge::Exception& e)
    {
      ROS_ERROR("cv_bridge exception: %s", e.what());
      return;
    }
    normalize(cv_ptr->image, cv_ptr->image, 0, 255, NORM_MINMAX);
    cvtColor(cv_ptr->image, cv_ptr->image, COLOR_GRAY2RGB);
    Mat image0;
    cv_ptr->image.convertTo(image0, CV_8UC3);
    imshow(OPENCV_WINDOW, image0);
    waitKey(1);
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "env_depth_node");
    ros::NodeHandle n;
    ros::Subscriber sub = n.subscribe("/camera/depth/image", 2, cb);
    ros::spin();
    return 0;
}