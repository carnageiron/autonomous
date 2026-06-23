import rclpy
from rclpy.node import Node

import math
from av_interfaces.msg import Cone, ConeArray, Track, Pose2D
from visualization_msgs.msg import Marker, MarkerArray

class MappingNode(Node):
    def __init__(self):
        super().__init__('mapping_node')

        self.subscription = self.create_subscription(
            ConeArray,
            '/perception/cones',
            self.cone_callback,
            10
        )

        self.pose_subscription = self.create_subscription(
            Pose2D,
            '/localization/pose',
            self.pose_callback,
            10
        )

        self.publisher_ = self.create_publisher(Track, '/mapping/track', 10)
        self.marker_publisher_ = self.create_publisher(MarkerArray, '/mapping/rviz_cones', 10)

        self.current_pose = Pose2D()

    def pose_callback(self, msg):
        self.current_pose = msg

    def cone_callback(self, msg):
        left_cones = []
        right_cones = []

        # Transform local cones to global frame
        global_cones = []
        for cone in msg.cones:
            g_cone = Cone()
            # 2D homogeneous transformation (rotation and translation)
            g_cone.x = self.current_pose.x + cone.x * math.cos(self.current_pose.yaw) - cone.y * math.sin(self.current_pose.yaw)
            g_cone.y = self.current_pose.y + cone.x * math.sin(self.current_pose.yaw) + cone.y * math.cos(self.current_pose.yaw)
            g_cone.color = cone.color
            global_cones.append(g_cone)

        # Separate cones by color
        for cone in global_cones:
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

        # Publish visualization markers to RViz
        marker_array = MarkerArray()
        id_counter = 0

        # Create a delete all marker to clear previous frame in RViz
        delete_all_marker = Marker()
        delete_all_marker.action = Marker.DELETEALL
        marker_array.markers.append(delete_all_marker)

        for cone in global_cones:
            marker = Marker()
            marker.header.frame_id = "odom"
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = "cones"
            marker.id = id_counter
            marker.type = Marker.CYLINDER
            marker.action = Marker.ADD
            marker.pose.position.x = float(cone.x)
            marker.pose.position.y = float(cone.y)
            marker.pose.position.z = 0.25 # half height
            marker.pose.orientation.w = 1.0
            marker.scale.x = 0.2
            marker.scale.y = 0.2
            marker.scale.z = 0.5
            
            if cone.color == "blue":
                marker.color.r = 0.0
                marker.color.g = 0.0
                marker.color.b = 1.0
                marker.color.a = 1.0
            elif cone.color == "yellow":
                marker.color.r = 1.0
                marker.color.g = 1.0
                marker.color.b = 0.0
                marker.color.a = 1.0
            else:
                marker.color.r = 0.5
                marker.color.g = 0.5
                marker.color.b = 0.5
                marker.color.a = 1.0
                
            marker_array.markers.append(marker)
            id_counter += 1

        self.marker_publisher_.publish(marker_array)


def main(args=None):
    rclpy.init(args=args)
    node = MappingNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
