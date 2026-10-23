
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import TransformStamped
from tf2_ros import StaticTransformBroadcaster


class MapFramePublisher(Node):

    def __init__(self):
        super().__init__('map_frame_publisher')

        # Static transform broadcaster
        self.broadcaster = StaticTransformBroadcaster(self)

        # Create transform message
        transform = TransformStamped()

        transform.header.stamp = (
            self.get_clock().now().to_msg()
        )

        # Parent and child frames
        transform.header.frame_id = 'map'
        transform.child_frame_id = 'odom'

        # Identity transform: no offset or rotation
        transform.transform.translation.x = 0.0
        transform.transform.translation.y = 0.0
        transform.transform.translation.z = 0.0

        transform.transform.rotation.x = 0.0
        transform.transform.rotation.y = 0.0
        transform.transform.rotation.z = 0.0
        transform.transform.rotation.w = 1.0

        # Publish once on /tf_static
        self.broadcaster.sendTransform(transform)

        self.get_logger().info(
            'Published static transform: map -> odom'
        )


def main(args=None):
    rclpy.init(args=args)

    node = MapFramePublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
