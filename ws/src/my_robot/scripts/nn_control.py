import numpy as np
import rospy
import os
from mobile_control import deep_mobile_control
from tensorflow.keras.models import load_model


def take_action(a):
    Robot.vel.linear.x = a[0]
    Robot.vel.angular.z = a[1]
    Robot.cmd_vel.publish(Robot.vel)


def choose_action(s):
    Q = model.predict(np.array([s]))
    a = vels[np.argmax(Q)]
    return a


def get_state():
    s_temp = Robot.data_laser
    ang_sp = Robot.odom_data.angular.z
    lin_sp = Robot.odom_data.linear.x
    s_temp = np.append(s_temp, [ang_sp, lin_sp])
    return s_temp


def test_model():
    while True:
        s = get_state()
        a = choose_action(s)
        take_action(a)
        rospy.sleep(0.1)
    rospy.signal_shutdown("END")


os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

vels = [[1, 0], [0.5, 1], [0.5, -1], [0, 1], [0, -1], [-0.8, 0]]
legal_actions = len(vels)

rospy.init_node('Mobile_Control', anonymous=True)
Robot = deep_mobile_control()
Robot.reset()

model = load_model('model_2.h5')


def main():
    test_model()


if __name__ == "__main__":
    main()
