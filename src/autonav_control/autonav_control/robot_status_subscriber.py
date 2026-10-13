
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class RobotStatusSubscriber(Node):

    def __init__(self):
        super().__init__('robot_status_subscriber')

        self.subscription = self.create_subscription(
            String,
            '/robot_status',
            self.status_callback,
            10
        )

    def status_callback(self, msg):
        self.get_logger().info(
            f'Received: {msg.data}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = RobotStatusSubscriber()

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
