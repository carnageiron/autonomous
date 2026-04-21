import rclpy
from rclpy.node import Node
from av_interfaces.msg import Cone, ConeArray
import random

class PerceptionNode(Node):
    def __init__(self):
        super().__init__('perception_node')

        self.publisher_ = self.create_publisher(ConeArray, '/perception/cones', 10)
        self.timer = self.create_timer(1.0, self.publish_cones)

    def publish_cones(self):
        cone_array = ConeArray()

        cones = []

        # Generate fake cones
        for i in range(5):
            cone = Cone()
            cone.x = float(i + random.uniform(-0.2, 0.2))
            cone.y = float(2.0 + random.uniform(-0.5, 0.5))
            cone.color = "blue"
            cones.append(cone)

        for i in range(5):
            cone = Cone()
            cone.x = float(i + random.uniform(-0.2, 0.2))
            cone.y = float(-2.0 + random.uniform(-0.5, 0.5))
            cone.color = "yellow"
            cones.append(cone)

        cone_array.cones = cones

        self.publisher_.publish(cone_array)
        self.get_logger().info(f"Published {len(cones)} cones")

def main(args=None):
    rclpy.init(args=args)
    node = PerceptionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
