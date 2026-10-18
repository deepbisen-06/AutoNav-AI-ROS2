
#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from turtlesim.msg import Pose
from nav_msgs.msg import Odometry


class OdometryPublisher(Node):

    def __init__(self):
        super().__init__('odometry_publisher')

        # Receive current turtle pose
        self.pose_sub = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # Publish ROS 2 Odometry messages
        self.odom_pub = self.create_publisher(
            Odometry,
            '/odom',
            10
        )

        self.get_logger().info(
            'Day 10: Odometry Publisher Started'
        )

    def pose_callback(self, msg):

        odom = Odometry()

        # Timestamp and reference frames
        odom.header.stamp = self.get_clock().now().to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'

        # Position from Turtlesim
        odom.pose.pose.position.x = msg.x
        odom.pose.pose.position.y = msg.y
        odom.pose.pose.position.z = 0.0

        # Convert yaw angle to quaternion
        half_yaw = msg.theta / 2.0

        odom.pose.pose.orientation.x = 0.0
        odom.pose.pose.orientation.y = 0.0
        odom.pose.pose.orientation.z = math.sin(half_yaw)
        odom.pose.pose.orientation.w = math.cos(half_yaw)

        # Velocity from Turtlesim
        odom.twist.twist.linear.x = msg.linear_velocity
        odom.twist.twist.angular.z = msg.angular_velocity

        # Covariance not estimated in this basic lesson.
        # Do not interpret the default zero values as
        # a realistic sensor uncertainty model.

        self.odom_pub.publish(odom)


def main(args=None):

    rclpy.init(args=args)

    node = OdometryPublisher()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
