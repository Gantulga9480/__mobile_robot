import rospy
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_srvs.srv import Empty
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu

cmd_vel = "/cmd_vel"
laser_topic = "/scan"
odom_topic = "/odom"
imu_topic = "/imu"


class deep_mobile_control:

    def __init__(self):
        self.cmd_vel = rospy.Publisher(cmd_vel, Twist, queue_size=1)
        self.subscriber = rospy.Subscriber(laser_topic, LaserScan,
                                           callback=self.laser_callback)
        self.subscriber_odo = rospy.Subscriber(odom_topic, Odometry,
                                               callback=self.odom_callback)
        self.subscriber_imu = rospy.Subscriber(imu_topic, Imu,
                                               callback=self.imu_callback)
        self.reset = rospy.ServiceProxy("/gazebo/reset_simulation", Empty)
        self.pause = rospy.ServiceProxy("/gazebo/pause_physics", Empty)
        self.unpause = rospy.ServiceProxy("/gazebo/unpause_physics", Empty)
        self.i = 0
        self.count = 0
        self.vel = Twist()
        self.vel.linear.x = 0
        self.vel.linear.y = 0
        self.vel.linear.z = 0
        self.vel.angular.x = 0
        self.vel.angular.y = 0
        self.vel.angular.z = 0

    def odom_callback(self, msg1):
        self.odom_data = msg1.twist.twist
        self.odom_pose = msg1.pose.pose.position

    def laser_callback(self, msg):
        self.laser_data = []
        for item in msg.ranges:
            if item == float('inf'):
                self.laser_data.append(2)
            else:
                self.laser_data.append(item)

    def imu_callback(self, msg_imu):
        self.imu_x = msg_imu.orientation.x
        self.imu_y = msg_imu.orientation.y
