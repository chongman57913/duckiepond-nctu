#!/usr/bin/env python
import numpy as np
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker

def cb_odom(msg):
    position = msg.pose.pose.position
    point_list.append(position)

def draw(event):
    draw_route()
    if len(point_list) != 0:
        draw_odom()

def draw_route():
    route_marker = Marker()
    route_marker.header.frame_id = "odom"
    route_marker.header.stamp = rospy.Time.now()
    route_marker.action = route_marker.ADD
    route_marker.type = route_marker.LINE_STRIP

    # maker scale
    route_marker.scale.x = 0.1
    route_marker.scale.y = 0.1
    route_marker.scale.z = 0.1

    # marker color
    route_marker.color.a = 1.0
    route_marker.color.r = 0.0
    route_marker.color.g = 1.0
    route_marker.color.b = 0.0

    # marker orientaiton
    route_marker.pose.orientation.x = 0.0
    route_marker.pose.orientation.y = 0.0
    route_marker.pose.orientation.z = 0.0
    route_marker.pose.orientation.w = 1.0

    # marker position
    route_marker.pose.position.x = 0.0
    route_marker.pose.position.y = 0.0
    route_marker.pose.position.z = 0.0

    route_marker.lifetime = rospy.Duration()

    for point in route_list:
        x = point[0]
        y = point[1]
        pt = Point(x, y, 0)
        route_marker.points.append(pt)

    pub_route_line.publish(route_marker)

def draw_odom():
    
    line_marker = Marker()
    line_marker.header.frame_id = "odom"
    line_marker.header.stamp = rospy.Time.now()
    line_marker.action = line_marker.ADD
    line_marker.type = line_marker.LINE_STRIP

    # maker scale
    line_marker.scale.x = 0.05
    line_marker.scale.y = 0.05
    line_marker.scale.z = 0.05

    # marker color
    line_marker.color.a = 1.0
    line_marker.color.r = 1.0
    line_marker.color.g = 0.0
    line_marker.color.b = 0.0

    # marker orientaiton
    line_marker.pose.orientation.x = 0.0
    line_marker.pose.orientation.y = 0.0
    line_marker.pose.orientation.z = 0.0
    line_marker.pose.orientation.w = 1.0

    # marker position
    line_marker.pose.position.x = 0.0
    line_marker.pose.position.y = 0.0
    line_marker.pose.position.z = 0.0
        
    for point in point_list:
        x = point.x
        y = point.y
        pt = Point(x, y, 0)
        line_marker.points.append(pt)
    pub_odom_line.publish(line_marker)


if __name__ == "__main__":
    rospy.init_node("odometry_plot",anonymous=False)

    point_list = []

    # Square
    route_list = [(0, 7), (0, -21), (28, -21), (28, 7), (0, 7)]

    # Circle

    
    rospy.Subscriber("/MONICA/localization_gps_imu/odometry", Odometry, cb_odom, queue_size=1)

    pub_odom_line = rospy.Publisher("/odom_linelist", Marker, queue_size=1)
    pub_route_line = rospy.Publisher("/route_linelist", Marker, queue_size=1)

    
    rospy.Timer(rospy.Duration(1.0), draw)

    rospy.spin()