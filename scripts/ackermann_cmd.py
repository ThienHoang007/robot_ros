#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import math

wheelbase = 0.25
wheel_radius = 0.05
track = 0.25

pub_wl = None
pub_wr = None
pub_sl = None
pub_sr = None

def cb(msg):
    v = msg.linear.x
    w = msg.angular.z

    if abs(v) < 1e-5:
        steer = 0.0
    else:
        steer = math.atan(wheelbase * w / (abs(v) + 1e-5))

    # ép 2 bánh luôn giống nhau
    pub_sl.publish(steer)
    pub_sr.publish(steer)

    # wheel velocity
    wheel_angular = v / wheel_radius
    pub_wl.publish(wheel_angular)
    pub_wr.publish(wheel_angular)

rospy.init_node("ackermann_cmd")

pub_wl = rospy.Publisher("/wheel_left_controller/command", Float64, queue_size=10)
pub_wr = rospy.Publisher("/wheel_right_controller/command", Float64, queue_size=10)

pub_sl = rospy.Publisher("/front_left_steer_controller/command", Float64, queue_size=10)
pub_sr = rospy.Publisher("/front_right_steer_controller/command", Float64, queue_size=10)

rospy.Subscriber("/cmd_vel", Twist, cb)

rospy.spin()