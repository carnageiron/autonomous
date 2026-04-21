import rclpy
from rclpy.node import Node

from av_interfaces.msg import Path, Control
import math

class ControlNode(Node):
    def __init__(self):
        super().__init__('control_node')

        self.subscription = self.create_subscription(
            Path,
            '/planning/path',
            self.path_callback,
            10
        )

        self.publisher_ = self.create_publisher(Control, '/control/cmd', 10)

        self.lookahead_distance = 1.0
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0

    def path_callback(self, msg):
        if len(msg.points) == 0:
            return

        target = None

        for p in msg.points:
            dx = p.x - self.current_x
            dy = p.y - self.current_y
            dist = math.sqrt(dx**2 + dy**2)

            if dist >= self.lookahead_distance:
                target = p
                break

        if target is None:
            target = msg.points[-1]

        dx = target.x - self.current_x
        dy = target.y - self.current_y

        angle_to_target = math.atan2(dy, dx)

        steering = angle_to_target - self.current_yaw

        control = Control()
        control.steering = steering
        control.throttle = 0.5

        self.publisher_.publish(control)

        self.get_logger().info(f"Steering: {steering:.2f}")


def main(args=None):
    rclpy.init(args=args)
    node = ControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
