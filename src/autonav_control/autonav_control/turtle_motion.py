
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class TurtleMotion(Node):

    def __init__(self):
        super().__init__('turtle_motion')

        self.publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.pose = None

        self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        self.state = 'MOVE'
        self.sides_completed = 0

        self.start_x = None
        self.start_y = None
        self.start_theta = None

        self.side_length = 2.0
        self.linear_speed = 1.0
        self.angular_speed = 0.8

        self.timer = self.create_timer(
            0.05,
            self.control_loop
        )

        self.get_logger().info(
            'AutoNav AI Square Controller Started'
        )

    def pose_callback(self, msg):
        self.pose = msg

    def angle_difference(self, target, current):
        return math.atan2(
            math.sin(target - current),
            math.cos(target - current)
        )

    def control_loop(self):
        if self.pose is None:
            return

        cmd = Twist()

        if self.state == 'MOVE':

            if self.start_x is None:
                self.start_x = self.pose.x
                self.start_y = self.pose.y

            distance = math.hypot(
                self.pose.x - self.start_x,
                self.pose.y - self.start_y
            )

            remaining = self.side_length - distance

            if remaining > 0.03:
                cmd.linear.x = min(
                    self.linear_speed,
                    max(0.15, remaining * 1.5)
                )
            else:
                self.start_theta = self.pose.theta
                self.state = 'TURN'

        elif self.state == 'TURN':

            target = self.start_theta + math.pi / 2

            error = self.angle_difference(
                target,
                self.pose.theta
            )

            if abs(error) > 0.02:
                cmd.angular.z = max(
                    -self.angular_speed,
                    min(self.angular_speed, 2.0 * error)
                )
            else:
                self.sides_completed += 1

                self.get_logger().info(
                    f'Side {self.sides_completed} completed'
                )

                if self.sides_completed >= 4:
                    self.state = 'DONE'
                else:
                    self.start_x = None
                    self.start_y = None
                    self.state = 'MOVE'

        elif self.state == 'DONE':
            self.publisher.publish(cmd)
            self.timer.cancel()
            self.get_logger().info(
                'Square path completed!'
            )
            return

        self.publisher.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleMotion()

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
