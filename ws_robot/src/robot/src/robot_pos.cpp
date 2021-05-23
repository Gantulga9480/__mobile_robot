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

static const std::string OPENCV_WINDOW = "Image window";
static const int NODE_RES = 20;

bool is_placed = false;

int center_tmp[2] = {0, 0};
int ball_tmp[2] = {0, 0};
int robot_radius, ball_radius = 0;
int dir_vect[2];
int dir;

void cb(const sensor_msgs::ImageConstPtr& msg)
{
    cv_bridge::CvImagePtr cv_ptr;
    try
    {
      cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
    }
    catch (cv_bridge::Exception& e)
    {
      ROS_ERROR("cv_bridge exception: %s", e.what());
      return;
    }
    Mat image0;
    cv_ptr->image.convertTo(image0, CV_8UC3);
    cvtColor(image0, image0, COLOR_RGB2GRAY);
    medianBlur(image0, image0, 5);
    // GaussianBlur( image0, image0, Size(9, 9), 2, 2 );
    vector<Vec3f> robot, ball;
    HoughCircles(image0, robot, HOUGH_GRADIENT, 1, 1, 150, 5, 34, 36);
    HoughCircles(image0, ball, HOUGH_GRADIENT, 1, 1, 150, 5, 10, 12);
    for(size_t i = 0; i < robot.size(); i++)
    {
        if (is_placed)
        {
            if ((abs(robot[i][0] - center_tmp[0]) < 10) && (abs(robot[i][1] - center_tmp[1]) < 10))
            {
                robot_radius = cvRound(robot[i][2]);
                center_tmp[0] = robot[i][0];
                center_tmp[1] = robot[i][1];
                break;
            }
        }
        else
        {
            is_placed = true;
            robot_radius = cvRound(robot[i][2]);
            center_tmp[0] = robot[i][0];
            center_tmp[1] = robot[i][1];
            break;
        }
    }
    for(size_t i = 0; i < robot.size(); i++)
    {
        if ((abs(ball[i][0] - center_tmp[0]) < 10) && (abs(ball[i][1] - center_tmp[1]) < 30))
        {
            ball_radius = cvRound(ball[i][2]);
            ball_tmp[0] = ball[i][0];
            ball_tmp[1] = ball[i][1];
            break;
        }
    }
    try
    {
        dir_vect[0] = center_tmp[0] - ball_tmp[0];
        dir_vect[1] = center_tmp[1] - ball_tmp[1];
        if (dir_vect[0] > 0 && dir_vect[1] <= 0)
            dir = atan(-dir_vect[1]/dir_vect[0]) / M_PI * 180;
        else if (dir_vect[0] > 0 && dir_vect[1] > 0)
            dir = 360 + atan(-dir_vect[1]/dir_vect[0]) / M_PI * 180;
        else if (dir_vect[0] < 0 && dir_vect[1] >= 0)
            dir = atan(-dir_vect[1]/dir_vect[0]) / M_PI * 180 + 180;
        else if (dir_vect[0] < 0 && dir_vect[1] < 0)
            dir = atan(-dir_vect[1]/dir_vect[0]) / M_PI * 180 + 180;
        else if (dir_vect[0] == 0 && dir_vect[1] < 0)
            dir = 90;
        else if (dir_vect[0] == 0 && dir_vect[1] > 0)
            dir = 270;
    }
    catch (exception& e)
    {

    }
    circle(cv_ptr->image, Point(center_tmp[0], center_tmp[1]), 3, Scalar(0,255,0), -1, 8, 0);
    circle(cv_ptr->image, Point(center_tmp[0], center_tmp[1]), robot_radius, Scalar(0,0,255), 3, 8, 0);
    circle(cv_ptr->image, Point(ball_tmp[0], ball_tmp[1]), 3, Scalar(0,255,0), -1, 8, 0);
    circle(cv_ptr->image, Point(ball_tmp[0], ball_tmp[1]), ball_radius, Scalar(255,0,255), 3, 8, 0);
    imshow(OPENCV_WINDOW, cv_ptr->image);
    waitKey(1);
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "robot_position_node");
    ros::NodeHandle n;
    ros::Subscriber sub = n.subscribe("/camera/rgb/image_color", 2, cb);
    ros::Publisher pub = n.advertise<robot::board>("robot/cordinate", 1000);
    ros::Rate loop_rate(30);
    while (ros::ok())
    {
        robot::board msg;
        msg.robot_x = center_tmp[0];
        msg.robot_y = center_tmp[1];
        msg.robot_dir = dir;
        pub.publish(msg);
        ros::spinOnce();
        loop_rate.sleep();
    }
    return 0;
}