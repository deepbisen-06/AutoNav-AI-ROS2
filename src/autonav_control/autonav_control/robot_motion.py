
#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist, TransformStamped
from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry

from tf2_ros import TransformBroadcaster


class RobotMotion(Node):

    def __init__(self):
        super().__init__('robot_motion')

        # Robot dimensions: match Day 13 URDF
        self.wheel_radius = 0.05
        self.wheel_separation = 0.30

        # Current robot pose
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # Current commanded velocity
        self.linear_speed = 0.0
        self.angular_speed = 0.0

        # Wheel joint angles (radians)
        self.left_angle = 0.0
        self.right_angle = 0.0

        # Stop when velocity commands become stale
        self.command_timeout = 0.5
        self.last_command_time = None

        # ROS publishers and subscriber
        self.cmd_sub = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_callback, 10
        )

        self.joint_pub = self.create_publisher(
            JointState, '/joint_states', 10
        )

        self.odom_pub = self.create_publisher(
            Odometry, '/odom', 10
        )

        self.tf_broadcaster = TransformBroadcaster(self)

        self.last_update = self.get_clock().now()
        self.timer = self.create_timer(0.05, self.update)

        self.get_logger().info(
            'Day 14: Robot Motion Node Started'
        )

    def cmd_callback(self, msg):
        # Educational speed limits
        self.linear_speed = max(
            -0.5, min(0.5, msg.linear.x)
        )
        self.angular_speed = max(
            -1.5, min(1.5, msg.angular.z)
        )
        self.last_command_time = self.get_clock().now()

    def update(self):
        now = self.get_clock().now()
        dt = (now - self.last_update).nanoseconds / 1e9
        self.last_update = now

        if dt <= 0.0 or dt > 0.5:
            return

        # Timeout: stop if no fresh command arrives
        if self.last_command_time is None:
            self.linear_speed = 0.0
            self.angular_speed = 0.0
        elif (
            now - self.last_command_time
        ).nanoseconds / 1e9 > self.command_timeout:
            self.linear_speed = 0.0
            self.angular_speed = 0.0

        v = self.linear_speed
        w = self.angular_speed

        # Midpoint integration for smoother turns
        heading_mid = self.theta + 0.5 * w * dt

        self.x += v * math.cos(heading_mid) * dt
        self.y += v * math.sin(heading_mid) * dt
        self.theta += w * dt

        # Normalize heading to [-pi, pi]
        self.theta = math.atan2(
            math.sin(self.theta),
            math.cos(self.theta)
        )

        # Differential-drive wheel angular velocities
        left_speed = (
            v - w * self.wheel_separation / 2.0
        ) / self.wheel_radius

        right_speed = (
            v + w * self.wheel_separation / 2.0
        ) / self.wheel_radius

        self.left_angle += left_speed * dt
        self.right_angle += right_speed * dt

        stamp = now.to_msg()
        half_yaw = self.theta / 2.0
        qz = math.sin(half_yaw)
        qw = math.cos(half_yaw)

        # Publish odom -> base_link transform
        transform = TransformStamped()
        transform.header.stamp = stamp
        transform.header.frame_id = 'odom'
        transform.child_frame_id = 'base_link'

        transform.transform.translation.x = self.x
        transform.transform.translation.y = self.y
        transform.transform.translation.z = 0.0

        transform.transform.rotation.z = qz
        transform.transform.rotation.w = qw

        self.tf_broadcaster.sendTransform(transform)

        # Publish wheel joint states
        joints = JointState()
        joints.header.stamp = stamp
        joints.name = [
            'left_wheel_joint',
            'right_wheel_joint'
        ]
        joints.position = [
            self.left_angle,
            self.right_angle
        ]

        self.joint_pub.publish(joints)

        # Publish simulated odometry
        odom = Odometry()
        odom.header.stamp = stamp
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.orientation.z = qz
        odom.pose.pose.orientation.w = qw

        odom.twist.twist.linear.x = v
        odom.twist.twist.angular.z = w

        self.odom_pub.publish(odom)


def main(args=None):
    rclpy.init(args=args)
    node = RobotMotion()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
