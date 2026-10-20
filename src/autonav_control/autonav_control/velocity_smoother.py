
#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocitySmoother(Node):

    def __init__(self):
        super().__init__('velocity_smoother')

        # Parameters
        self.declare_parameter('max_linear_speed', 0.8)
        self.declare_parameter('max_angular_speed', 1.5)
        self.declare_parameter('linear_accel', 0.4)
        self.declare_parameter('angular_accel', 1.0)
        self.declare_parameter('command_timeout', 0.5)

        self.max_linear = float(
            self.get_parameter('max_linear_speed').value
        )
        self.max_angular = float(
            self.get_parameter('max_angular_speed').value
        )
        self.linear_accel = float(
            self.get_parameter('linear_accel').value
        )
        self.angular_accel = float(
            self.get_parameter('angular_accel').value
        )
        self.command_timeout = float(
            self.get_parameter('command_timeout').value
        )

        if min(
            self.max_linear,
            self.max_angular,
            self.linear_accel,
            self.angular_accel,
            self.command_timeout
        ) <= 0.0:
            raise ValueError('All limits must be positive')

        # Target and current velocities
        self.target_linear = 0.0
        self.target_angular = 0.0

        self.current_linear = 0.0
        self.current_angular = 0.0

        self.last_command_time = None

        # Subscribe to desired velocity
        self.cmd_sub = self.create_subscription(
            Twist,
            '/cmd_vel_raw',
            self.cmd_callback,
            10
        )

        # Publish smoothed velocity
        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.timer = self.create_timer(
            0.05,
            self.update_velocity
        )

        self.get_logger().info(
            'Day 12: Velocity Smoother Started'
        )

    def cmd_callback(self, msg):

        self.target_linear = max(
            -self.max_linear,
            min(self.max_linear, msg.linear.x)
        )

        self.target_angular = max(
            -self.max_angular,
            min(self.max_angular, msg.angular.z)
        )

        self.last_command_time = (
            self.get_clock().now()
        )

    def limit_change(self, current, target, max_step):

        difference = target - current

        if abs(difference) <= max_step:
            return target

        return current + math.copysign(
            max_step,
            difference
        )

    def update_velocity(self):

        now = self.get_clock().now()

        # Stop target if commands are stale
        if self.last_command_time is None:
            self.target_linear = 0.0
            self.target_angular = 0.0

        elif (
            now - self.last_command_time
        ).nanoseconds / 1e9 > self.command_timeout:
            self.target_linear = 0.0
            self.target_angular = 0.0

        # 20 Hz timer: nominal dt = 0.05 s
        dt = 0.05

        self.current_linear = self.limit_change(
            self.current_linear,
            self.target_linear,
            self.linear_accel * dt
        )

        self.current_angular = self.limit_change(
            self.current_angular,
            self.target_angular,
            self.angular_accel * dt
        )

        cmd = Twist()
        cmd.linear.x = self.current_linear
        cmd.angular.z = self.current_angular

        self.cmd_pub.publish(cmd)


def main(args=None):

    rclpy.init(args=args)
    node = VelocitySmoother()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.cmd_pub.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
