
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import Float64MultiArray


class DifferentialDrive(Node):

    def __init__(self):
        super().__init__('differential_drive')

        # Robot dimensions (meters)
        self.declare_parameter('wheel_radius', 0.05)
        self.declare_parameter('wheel_separation', 0.30)

        self.wheel_radius = self.get_parameter(
            'wheel_radius'
        ).value

        self.wheel_separation = self.get_parameter(
            'wheel_separation'
        ).value

        if self.wheel_radius <= 0 or self.wheel_separation <= 0:
            raise ValueError('Robot dimensions must be positive')

        # Subscribe to robot velocity commands
        self.cmd_sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10
        )

        # Publish left and right wheel angular speeds
        self.wheel_pub = self.create_publisher(
            Float64MultiArray,
            '/wheel_speeds',
            10
        )

        self.get_logger().info(
            'Differential Drive Kinematics Node Started'
        )

    def cmd_callback(self, msg):

        v = msg.linear.x
        omega = msg.angular.z

        r = self.wheel_radius
        L = self.wheel_separation

        # Inverse kinematics
        left_speed = (v - omega * L / 2.0) / r
        right_speed = (v + omega * L / 2.0) / r

        # Publish wheel speeds [left, right]
        wheel_msg = Float64MultiArray()
        wheel_msg.data = [left_speed, right_speed]

        self.wheel_pub.publish(wheel_msg)

        # Forward kinematics verification
        calculated_v = r * (
            right_speed + left_speed
        ) / 2.0

        calculated_omega = r * (
            right_speed - left_speed
        ) / L

        self.get_logger().info(
            f'L: {left_speed:.2f} rad/s | '
            f'R: {right_speed:.2f} rad/s | '
            f'v: {calculated_v:.2f} m/s | '
            f'w: {calculated_omega:.2f} rad/s'
        )


def main(args=None):

    rclpy.init(args=args)

    node = DifferentialDrive()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
