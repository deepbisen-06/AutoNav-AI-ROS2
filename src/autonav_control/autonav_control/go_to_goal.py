
import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class GoToGoal(Node):

    def __init__(self):
        super().__init__('go_to_goal')

        self.publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        self.declare_parameter('goal_x', 8.0)
        self.declare_parameter('goal_y', 8.0)

        self.goal_x = self.get_parameter('goal_x').value
        self.goal_y = self.get_parameter('goal_y').value

        self.kp_linear = 1.0
        self.kp_angular = 4.0

        self.max_linear_speed = 1.5
        self.max_angular_speed = 2.0

        self.goal_tolerance = 0.15

        self.pose = None
        self.goal_reached = False

        self.timer = self.create_timer(
            0.05,
            self.control_loop
        )

        self.get_logger().info(
            f'Navigating to ({self.goal_x}, {self.goal_y})'
        )

    def pose_callback(self, msg):
        self.pose = msg

    def control_loop(self):

        if self.pose is None or self.goal_reached:
            return

        dx = self.goal_x - self.pose.x
        dy = self.goal_y - self.pose.y

        distance = math.hypot(dx, dy)

        desired_heading = math.atan2(dy, dx)

        heading_error = math.atan2(
            math.sin(desired_heading - self.pose.theta),
            math.cos(desired_heading - self.pose.theta)
        )

        cmd = Twist()

        if distance < self.goal_tolerance:

            self.goal_reached = True
            self.publisher.publish(cmd)

            self.get_logger().info(
                'GOAL REACHED! Robot stopped.'
            )

            self.timer.cancel()
            return

        angular_speed = (
            self.kp_angular * heading_error
        )

        cmd.angular.z = max(
            -self.max_angular_speed,
            min(self.max_angular_speed, angular_speed)
        )

        if abs(heading_error) < 0.5:

            linear_speed = (
                self.kp_linear * distance
            )

            cmd.linear.x = min(
                self.max_linear_speed,
                linear_speed
            )

        self.publisher.publish(cmd)


def main(args=None):
    rclpy.init(args=args)

    node = GoToGoal()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.publisher.publish(Twist())
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()

