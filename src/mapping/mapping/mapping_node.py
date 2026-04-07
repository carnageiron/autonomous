import rclpy
from rclpy.node import Node

from av_interfaces.msg import ConeArray, Track

class MappingNode(Node):
    def __init__(self):
        super().__init__('mapping_node')

        self.subscription = self.create_subscription(
            ConeArray,
            '/perception/cones',
            self.cone_callback,
            10
        )

        self.publisher_ = self.create_publisher(Track, '/mapping/track', 10)

    def cone_callback(self, msg):
        left_cones = []
        right_cones = []

        # Separate cones by color
        for cone in msg.cones:
            if cone.color == "blue":
                left_cones.append(cone)
            elif cone.color == "yellow":
                right_cones.append(cone)

        # Sort cones by x (forward direction)
        left_cones.sort(key=lambda c: c.x)
        right_cones.sort(key=lambda c: c.x)

        # Create track message
        track = Track()
        track.left_cones = left_cones
        track.right_cones = right_cones

        self.publisher_.publish(track)

        self.get_logger().info(
            f"Left: {len(left_cones)}, Right: {len(right_cones)}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = MappingNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
