#include "ros/ros.h"
#include "std_msgs/Int32MultiArray.h"
#include "image_transport/image_transport.h"
#include "cv_bridge/cv_bridge.h"
#include "sensor_msgs/image_encodings.h"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <math.h>

using namespace cv;
using namespace std;

static const string OPENCV_WINDOW = "Depth Image";
static const int NODE_RES = 20;
static const int SCALE_RATE = 1;
static const int PIXEL_SKIP_RATE = 5;

static const int WIDTH = 32;
static const int HEIGHT = 24;

int table[HEIGHT][WIDTH];

int get_data(Mat img, int w, int h)
{
  for(int i_h=h*NODE_RES;
      i_h<(h+1)*NODE_RES;
      i_h=i_h+PIXEL_SKIP_RATE)
  {
    for(int j_w=w*NODE_RES;
        j_w<(w+1)*NODE_RES;
        j_w=j_w+PIXEL_SKIP_RATE)
    {
      Vec3b intensity = img.at<Vec3b>(i_h, j_w);
      //cout << (int)intensity.val[0] << " " << (int)intensity.val[1] << " " << (int)intensity.val[2] << endl;
      if ((int)intensity.val[0] < 100)
      {
        return 1;
      }
    }
  }
  return 0;
}

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
    Mat image0;
    normalize(cv_ptr->image, cv_ptr->image, 0, 255, NORM_MINMAX);
    cvtColor(cv_ptr->image, image0, COLOR_GRAY2RGB);
    image0.convertTo(image0, CV_8UC3);
    // cout << re_width << "x" << re_height << endl;
    for (int h=0; h<HEIGHT; h++)
    {
      for (int w=0; w<WIDTH; w++)
      {
        table[h][w] = get_data(image0, w, h);
        //cout << table[h][w] << " ";
      }
      //cout << endl;
    }
    // imshow(OPENCV_WINDOW, image0);
    // waitKey(1);
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "env_depth_node");
  ros::NodeHandle n;
  ros::Subscriber sub = n.subscribe("/camera/depth/image", 2, cb);
  ros::Publisher pub = n.advertise<std_msgs::Int32MultiArray>("robot/grid_value", 1000);
  ros::Rate loop_rate(30);
  while (ros::ok())
  {
    std_msgs::Int32MultiArray msg;
    msg.data.clear();
    for (int i = 0; i < HEIGHT; i++)
    {
      for (int j = 0; j < WIDTH; j++)
      {
        msg.data.push_back(table[i][j]);
      }
    }
    pub.publish(msg);
    ros::spinOnce();
    loop_rate.sleep();
  }
  return 0;
}