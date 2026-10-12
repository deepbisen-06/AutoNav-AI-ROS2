import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class RobotStatusPublisher(Node):

    def __init__(self):
        super().__init__('robot_status_publisher')

        self.publisher_ = self.create_publisher(
            String,
            '/robot_status',
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_status
        )

    def publish_status(self):
        msg = String()
        msg.data = 'AutoNav AI Robot is ACTIVE'

        self.publisher_.publish(msg)
        self.get_logger().info(
            f'Publishing: {msg.data}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = RobotStatusPublisher()

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

