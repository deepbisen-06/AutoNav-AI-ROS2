
import sys

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class AddTwoIntsClient(Node):

    def __init__(self):
        super().__init__('add_two_ints_client')

        self.client = self.create_client(
            AddTwoInts,
            '/add_two_ints'
        )

        while not self.client.wait_for_service(
            timeout_sec=1.0
        ):
            self.get_logger().info(
                'Waiting for service server...'
            )

    def send_request(self, a, b):
        request = AddTwoInts.Request()

        request.a = a
        request.b = b

        return self.client.call_async(request)


def main(args=None):
    rclpy.init(args=args)

    node = None

    try:
        node = AddTwoIntsClient()

        a = int(sys.argv[1])
        b = int(sys.argv[2])

        future = node.send_request(a, b)

        rclpy.spin_until_future_complete(node, future)

        result = future.result()

        if result is not None:
            node.get_logger().info(
                f'Result: {a} + {b} = {result.sum}'
            )
        else:
            node.get_logger().error(
                'Service call failed'
            )

    except (IndexError, ValueError):
        print('Usage: add_two_ints_client <a> <b>')

    except KeyboardInterrupt:
        pass

    finally:
        if node is not None:
            node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
