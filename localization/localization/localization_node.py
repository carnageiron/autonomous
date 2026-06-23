import math

import rclpy
from rclpy.node import Node

from av_interfaces.msg import Control
from av_interfaces.msg import Pose2D


class LocalizationNode(Node):

    def __init__(self):
        super().__init__('localization_node')

        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        self.velocity = 0.0

        self.throttle = 0.0
        self.steering = 0.0

        self.dt = 0.1

        self.pose_pub = self.create_publisher(
            Pose2D,
            '/localization/pose',
            10
        )

        self.control_sub = self.create_subscription(
            Control,
            '/control/cmd',
            self.control_callback,
            10
        )

        self.timer = self.create_timer(
            self.dt,
            self.update_pose
        )

    def control_callback(self, msg):
        self.throttle = msg.throttle
        self.steering = msg.steering

    def update_pose(self):
        self.velocity += self.throttle * self.dt

        self.x += self.velocity * math.cos(self.yaw) * self.dt
        self.y += self.velocity * math.sin(self.yaw) * self.dt

        self.yaw += self.steering * self.dt

        pose = Pose2D()

        pose.x = self.x
        pose.y = self.y
        pose.yaw = self.yaw
        pose.velocity = self.velocity

        self.pose_pub.publish(pose)


def main(args=None):
    rclpy.init(args=args)

    node = LocalizationNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()