import math

import rclpy
from rclpy.node import Node

from av_interfaces.msg import Control, Pose2D
from geometry_msgs.msg import TransformStamped
import tf2_ros


class LocalizationNode(Node):

    def __init__(self):
        super().__init__('localization_node')

        # Declare parameters
        self.declare_parameter('wheelbase', 1.5)
        self.declare_parameter('dt', 0.01) # 100 Hz default

        self.wheelbase = self.get_parameter('wheelbase').get_parameter_value().double_value
        self.dt = self.get_parameter('dt').get_parameter_value().double_value

        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        self.velocity = 0.0

        self.throttle = 0.0
        self.steering = 0.0

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

        # Create TF Broadcaster
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)

        self.timer = self.create_timer(
            self.dt,
            self.update_pose
        )

    def control_callback(self, msg):
        self.throttle = msg.throttle
        self.steering = msg.steering

    def update_pose(self):
        # Refresh parameters in case they changed
        self.wheelbase = self.get_parameter('wheelbase').get_parameter_value().double_value
        self.dt = self.get_parameter('dt').get_parameter_value().double_value

        # Kinematic Bicycle Model
        # Limit steering input to physical limits of the vehicle (e.g., +/- 0.5 rad)
        steering_limit = 0.5
        limited_steering = max(-steering_limit, min(steering_limit, self.steering))

        # Integrate velocity (throttle is acceleration in m/s^2)
        self.velocity += self.throttle * self.dt
        # Cap velocity to be non-negative
        self.velocity = max(0.0, self.velocity)

        # Update position and heading (yaw)
        self.x += self.velocity * math.cos(self.yaw) * self.dt
        self.y += self.velocity * math.sin(self.yaw) * self.dt
        self.yaw += (self.velocity / self.wheelbase) * math.tan(limited_steering) * self.dt

        # Normalize yaw to [-pi, pi]
        self.yaw = math.atan2(math.sin(self.yaw), math.cos(self.yaw))

        # Publish Pose2D
        pose = Pose2D()
        pose.x = self.x
        pose.y = self.y
        pose.yaw = self.yaw
        pose.velocity = self.velocity
        self.pose_pub.publish(pose)

        # Broadcast odom -> base_link TF Transform
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0

        # Yaw to quaternion
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = float(math.sin(self.yaw * 0.5))
        t.transform.rotation.w = float(math.cos(self.yaw * 0.5))

        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)

    node = LocalizationNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()