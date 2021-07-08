#!/usr/bin/env python3
""" 
@file   base_link_to_map_transform.py
@brief  ROS Node that listens to TF from base link to map frame to get SMB_position
@author Flavio Regenass
@date   06.07.2021
"""

import roslib
import rospy
import math
import tf
import geometry_msgs.msg

if __name__ == '__main__':
    rospy.init_node('base_link_to_map_listener')

    listener = tf.TransformListener()
    publisher = rospy.Publisher('icp_node/base_pose_map', geometry_msgs.msg.PoseStamped, queue_size=100)

    rate = rospy.Rate(20.0)

    while not rospy.is_shutdown():

        try:
            
            # (t_map_odom, rot_map_odom) = listener.lookupTransform('map', 'odom_source', rospy.Time(0))
            # (t_odom_base, rot_odom_base) = listener.lookupTransform('odom_source', 'base_link', rospy.Time(0))
            (translation, rotation_quat) = listener.lookupTransform('map', 'base_link', rospy.Time(0))
            # print('yes')
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        map_pose_est = geometry_msgs.msg.PoseStamped()

        map_pose_est.header.stamp = rospy.Time(0)
        map_pose_est.header.frame_id = 'map'

        map_pose_est.pose.position.x = translation[0]
        map_pose_est.pose.position.y = translation[1]
        map_pose_est.pose.position.z = translation[2]

        map_pose_est.pose.orientation.x = rotation_quat[0]
        map_pose_est.pose.orientation.y = rotation_quat[1]
        map_pose_est.pose.orientation.z = rotation_quat[2]
        map_pose_est.pose.orientation.w = rotation_quat[3]

        publisher.publish(map_pose_est)

        rate.sleep()
