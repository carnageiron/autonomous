import rclpy
from rclpy.node import Node

from av_interfaces.msg import Path, Control, Pose2D
import math

class ControlNode(Node):
    def __init__(self):
        super().__init__('control_node')

        # Declare parameters with default values
        self.declare_parameter('lookahead_distance', 1.0)
        self.declare_parameter('wheelbase', 1.5)
        self.declare_parameter('target_velocity', 2.0)
        self.declare_parameter('kp', 1.0)
        self.declare_parameter('ki', 0.1)
        self.declare_parameter('kd', 0.05)

        # Get parameter values
        self.lookahead_distance = self.get_parameter('lookahead_distance').get_parameter_value().double_value
        self.wheelbase = self.get_parameter('wheelbase').get_parameter_value().double_value
        self.target_velocity = self.get_parameter('target_velocity').get_parameter_value().double_value
        self.kp = self.get_parameter('kp').get_parameter_value().double_value
        self.ki = self.get_parameter('ki').get_parameter_value().double_value
        self.kd = self.get_parameter('kd').get_parameter_value().double_value

        self.subscription = self.create_subscription(
            Path,
            '/planning/path',
            self.path_callback,
            10
        )

        self.pose_subscription = self.create_subscription(
            Pose2D,
            '/localization/pose',
            self.pose_callback,
            10
        )

        self.publisher_ = self.create_publisher(Control, '/control/cmd', 10)

        # Vehicle state variables
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0
        self.current_velocity = 0.0

        self.latest_path = None

        # PID controller variables
        self.prev_error = 0.0
        self.integral_error = 0.0

        # 50 Hz control loop timer
        self.dt = 0.02
        self.timer = self.create_timer(self.dt, self.control_loop)

    def path_callback(self, msg):
        self.latest_path = msg

    def pose_callback(self, msg):
        self.current_x = msg.x
        self.current_y = msg.y
        self.current_yaw = msg.yaw
        self.current_velocity = msg.velocity

    def control_loop(self):
        # Refresh parameters in case they changed
        self.lookahead_distance = self.get_parameter('lookahead_distance').get_parameter_value().double_value
        self.wheelbase = self.get_parameter('wheelbase').get_parameter_value().double_value
        self.target_velocity = self.get_parameter('target_velocity').get_parameter_value().double_value
        self.kp = self.get_parameter('kp').get_parameter_value().double_value
        self.ki = self.get_parameter('ki').get_parameter_value().double_value
        self.kd = self.get_parameter('kd').get_parameter_value().double_value

        if self.latest_path is None or len(self.latest_path.points) == 0:
            # Stop if no path is available
            control = Control()
            control.steering = 0.0
            control.throttle = 0.0
            self.publisher_.publish(control)
            return

        target = None

        for p in self.latest_path.points:
            dx = p.x - self.current_x
            dy = p.y - self.current_y
            dist = math.sqrt(dx**2 + dy**2)

            if dist >= self.lookahead_distance:
                target = p
                break

        if target is None:
            target = self.latest_path.points[-1]

        dx = target.x - self.current_x
        dy = target.y - self.current_y

        # Angle to target in global frame
        global_target_angle = math.atan2(dy, dx)

        # Alpha: angle between vehicle heading and target lookahead vector
        alpha = global_target_angle - self.current_yaw
        alpha = math.atan2(math.sin(alpha), math.cos(alpha))

        # Pure Pursuit steering formula
        steering = math.atan2(2.0 * self.wheelbase * math.sin(alpha), self.lookahead_distance)

        # Speed PID control
        error = self.target_velocity - self.current_velocity
        self.integral_error += error * self.dt
        # Prevent integral windup
        self.integral_error = max(-10.0, min(10.0, self.integral_error))
        
        derivative_error = (error - self.prev_error) / self.dt
        self.prev_error = error

        throttle = (self.kp * error) + (self.ki * self.integral_error) + (self.kd * derivative_error)
        # Limit throttle to a reasonable range
        throttle = max(-2.0, min(2.0, throttle))

        control = Control()
        control.steering = float(steering)
        control.throttle = float(throttle)

        self.publisher_.publish(control)

        self.get_logger().info(f"Speed: {self.current_velocity:.2f} m/s, Throttle: {throttle:.2f}, Steering: {steering:.2f}")


def main(args=None):
    rclpy.init(args=args)
    node = ControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
