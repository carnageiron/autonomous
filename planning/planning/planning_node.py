import rclpy
from rclpy.node import Node

from av_interfaces.msg import Track, Path
from geometry_msgs.msg import Point, PoseStamped
from nav_msgs.msg import Path as RVizPath

class PlanningNode(Node):
    def __init__(self):
        super().__init__('planning_node')

        self.subscription = self.create_subscription(
            Track,
            '/mapping/track',
            self.track_callback,
            10
        )

        self.publisher_ = self.create_publisher(Path, '/planning/path', 10)
        self.rviz_publisher_ = self.create_publisher(RVizPath, '/planning/rviz_path', 10)

    def track_callback(self, msg):
        path = Path()
        points = []

        left = msg.left_cones
        right = msg.right_cones

        n = min(len(left), len(right))

        for i in range(n):
            p = Point()
            p.x = (left[i].x + right[i].x) / 2.0
            p.y = (left[i].y + right[i].y) / 2.0
            p.z = 0.0
            points.append(p)

        path.points = points
        self.publisher_.publish(path)

        self.get_logger().info(f"Path points: {len(points)}")

        # Create standard nav_msgs/Path message for RViz
        rviz_path = RVizPath()
        rviz_path.header.frame_id = 'odom'
        rviz_path.header.stamp = self.get_clock().now().to_msg()

        for p in points:
            pose_stamped = PoseStamped()
            pose_stamped.header = rviz_path.header
            pose_stamped.pose.position.x = p.x
            pose_stamped.pose.position.y = p.y
            pose_stamped.pose.position.z = p.z
            pose_stamped.pose.orientation.w = 1.0
            rviz_path.poses.append(pose_stamped)

        self.rviz_publisher_.publish(rviz_path)


def main(args=None):
    rclpy.init(args=args)
    node = PlanningNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
