
#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class WaypointNavigation(Node):

    def __init__(self):
        super().__init__('waypoint_navigation')

        # Publisher: turtle movement commands
        self.cmd_pub = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        # Subscriber: current turtle position
        self.pose_sub = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # Navigation targets in order
        self.waypoints = [
            (2.0, 2.0),
            (9.0, 2.0),
            (9.0, 9.0),
            (2.0, 9.0)
        ]

        self.current_index = 0
        self.pose = None
        self.finished = False

        # Controller settings
        self.kp_linear = 1.0
        self.kp_angular = 4.0

        self.max_linear = 1.5
        self.max_angular = 2.0

        self.goal_tolerance = 0.15

        # Run controller 20 times per second
        self.timer = self.create_timer(
            0.05,
            self.control_loop
        )

        self.get_logger().info(
            'Day 09: Waypoint Navigation Started'
        )

    def pose_callback(self, msg):
        self.pose = msg

    def stop_robot(self):
        self.cmd_pub.publish(Twist())

    def control_loop(self):

        if self.pose is None or self.finished:
            return

        # Stop after all waypoints are visited
        if self.current_index >= len(self.waypoints):
            self.stop_robot()
            self.finished = True

            self.get_logger().info(
                'All waypoints completed!'
            )
            return

        # Select current target
        goal_x, goal_y = self.waypoints[
            self.current_index
        ]

        # Difference between goal and position
        dx = goal_x - self.pose.x
        dy = goal_y - self.pose.y

        # Euclidean distance
        distance = math.hypot(dx, dy)

        # Desired heading
        target_angle = math.atan2(dy, dx)

        # Shortest angular difference
        angle_error = math.atan2(
            math.sin(target_angle - self.pose.theta),
            math.cos(target_angle - self.pose.theta)
        )

        # Reached current waypoint
        if distance < self.goal_tolerance:

            self.stop_robot()

            self.get_logger().info(
                f'Waypoint {self.current_index + 1} reached: '
                f'({goal_x}, {goal_y})'
            )

            self.current_index += 1
            return

        cmd = Twist()

        # Angular P controller
        cmd.angular.z = max(
            -self.max_angular,
            min(
                self.max_angular,
                self.kp_angular * angle_error
            )
        )

        # Move forward only when facing goal
        if abs(angle_error) < 0.5:
            cmd.linear.x = min(
                self.max_linear,
                self.kp_linear * distance
            )
        else:
            cmd.linear.x = 0.0

        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)

    node = WaypointNavigation()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop_robot()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
