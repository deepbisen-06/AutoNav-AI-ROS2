
import rclpy
from rclpy.node import Node


class RobotConfig(Node):

    def __init__(self):
        super().__init__('robot_config')

        # Declare robot configuration parameters
        self.declare_parameter('robot_name', 'AutoNav AI')
        self.declare_parameter('max_speed', 0.3)
        self.declare_parameter('safety_distance', 0.5)
        self.declare_parameter('autonomous_mode', False)

        # Print configuration every 2 seconds
        self.timer = self.create_timer(
            2.0,
            self.show_config
        )

        self.get_logger().info(
            'Robot Configuration Node Started!'
        )

    def show_config(self):

        robot_name = (
            self.get_parameter('robot_name').value
        )

        max_speed = (
            self.get_parameter('max_speed').value
        )

        safety_distance = (
            self.get_parameter('safety_distance').value
        )

        autonomous_mode = (
            self.get_parameter('autonomous_mode').value
        )

        self.get_logger().info(
            f'Robot Name: {robot_name} | '
            f'Max Speed: {max_speed} m/s | '
            f'Safety Distance: {safety_distance} m | '
            f'Autonomous Mode: {autonomous_mode}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = RobotConfig()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
