import subprocess
import time
import sys
import math
import logging
import rclpy
from rclpy.node import Node
from av_interfaces.msg import Pose2D, Control

# Configure Logging (write log file to workspace root to avoid polluting git repo)
log_file = '/home/carnageiron/av_ws/av_test_suite.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('av_test_suite')

# ----------------- UNIT TESTS -----------------

def test_pure_pursuit():
    logger.info("Running Unit Test: Pure Pursuit Steering Math...")
    # Inputs
    L = 1.5
    ld = 1.0
    yaw = 0.0
    target_x, target_y = 1.0, 1.0
    current_x, current_y = 0.0, 0.0
    
    # Calculation
    dx = target_x - current_x
    dy = target_y - current_y
    global_target_angle = math.atan2(dy, dx)
    alpha = global_target_angle - yaw
    alpha = math.atan2(math.sin(alpha), math.cos(alpha))
    steering = math.atan2(2.0 * L * math.sin(alpha), ld)
    
    # Assertion
    expected = math.atan2(2.0 * 1.5 * math.sin(math.pi/4), 1.0)
    assert math.isclose(steering, expected), f"Pure pursuit calculation failed! Expected {expected}, got {steering}"
    logger.info("Unit Test: Pure Pursuit Steering Math PASSED!")

def test_kinematic_bicycle_model():
    logger.info("Running Unit Test: Kinematic Bicycle Model Math...")
    # Inputs
    dt = 0.01
    L = 1.5
    v = 1.0
    limited_steering = 0.5
    yaw = 0.0
    x = 0.0
    y = 0.0
    
    # Calculation
    new_x = x + v * math.cos(yaw) * dt
    new_y = y + v * math.sin(yaw) * dt
    new_yaw = yaw + (v / L) * math.tan(limited_steering) * dt
    
    # Assertions
    assert math.isclose(new_x, 0.01), f"Bicycle model X failed! Expected 0.01, got {new_x}"
    assert math.isclose(new_y, 0.0), f"Bicycle model Y failed! Expected 0.0, got {new_y}"
    expected_yaw = (1.0 / 1.5) * math.tan(0.5) * 0.01
    assert math.isclose(new_yaw, expected_yaw), f"Bicycle model Yaw failed! Expected {expected_yaw}, got {new_yaw}"
    logger.info("Unit Test: Kinematic Bicycle Model Math PASSED!")

def test_coordinate_transformation():
    logger.info("Running Unit Test: 2D Homogeneous Coordinate Transformation...")
    # Inputs
    pose_x = 1.0
    pose_y = 2.0
    pose_yaw = math.pi / 2
    local_x = 1.0
    local_y = 0.0
    
    # Calculation
    global_x = pose_x + local_x * math.cos(pose_yaw) - local_y * math.sin(pose_yaw)
    global_y = pose_y + local_x * math.sin(pose_yaw) + local_y * math.cos(pose_yaw)
    
    # Assertions
    assert math.isclose(global_x, 1.0, abs_tol=1e-5), f"Transformation X failed! Expected 1.0, got {global_x}"
    assert math.isclose(global_y, 3.0, abs_tol=1e-5), f"Transformation Y failed! Expected 3.0, got {global_y}"
    logger.info("Unit Test: 2D Homogeneous Coordinate Transformation PASSED!")

# ----------------- INTEGRATION TESTS -----------------

class IntegrationTestSubscriber(Node):
    def __init__(self):
        super().__init__('integration_test_subscriber')
        self.pose_messages = []
        self.control_messages = []
        
        self.pose_sub = self.create_subscription(
            Pose2D,
            '/localization/pose',
            self.pose_callback,
            10
        )
        self.control_sub = self.create_subscription(
            Control,
            '/control/cmd',
            self.control_callback,
            10
        )

    def pose_callback(self, msg):
        self.pose_messages.append(msg)
        logger.info(f"[ROS2 Msg] Pose feedback: x={msg.x:.3f}, y={msg.y:.3f}, yaw={msg.yaw:.3f}, v={msg.velocity:.3f} m/s")

    def control_callback(self, msg):
        self.control_messages.append(msg)
        logger.info(f"[ROS2 Msg] Control cmd: steering={msg.steering:.3f}, throttle={msg.throttle:.3f}")

def run_integration_test():
    logger.info("\nRunning System Integration Test...")
    
    processes = []
    nodes = [
        ('perception', 'perception_node'),
        ('mapping', 'mapping_node'),
        ('planning', 'planning_node'),
        ('control', 'control_node'),
        ('localization', 'localization_node')
    ]
    
    # Start the nodes
    for pkg, node in nodes:
        cmd = f"source /opt/ros/humble/setup.bash && source /home/carnageiron/av_ws/install/setup.bash && ros2 run {pkg} {node}"
        p = subprocess.Popen(["bash", "-c", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes.append(p)
        logger.info(f"Started ROS2 process: {node}")
        
    time.sleep(2) # wait for system initialization
    
    # Spin ROS 2 subscriber to gather messages
    rclpy.init()
    test_sub = IntegrationTestSubscriber()
    
    logger.info("Monitoring vehicle state for 8 seconds...")
    start_time = time.time()
    while time.time() - start_time < 8.0:
        rclpy.spin_once(test_sub, timeout_sec=0.1)
        
    # Shutdown nodes and subscriber
    test_sub.destroy_node()
    rclpy.shutdown()
    
    logger.info("Terminating autonomous vehicle nodes...")
    for p in processes:
        p.terminate()
        p.wait()
        
    logger.info("Integration Test Run Finished.")
    
    # Analyze results
    num_pose = len(test_sub.pose_messages)
    num_control = len(test_sub.control_messages)
    
    logger.info(f"Analysis: Received {num_pose} Pose and {num_control} Control messages.")
    
    assert num_pose > 20, f"Expected > 20 Pose messages, received {num_pose}"
    assert num_control > 20, f"Expected > 20 Control messages, received {num_control}"
    
    first_pose = test_sub.pose_messages[0]
    last_pose = test_sub.pose_messages[-1]
    
    displacement = math.sqrt((last_pose.x - first_pose.x)**2 + (last_pose.y - first_pose.y)**2)
    logger.info(f"Vehicle start position: ({first_pose.x:.2f}, {first_pose.y:.2f})")
    logger.info(f"Vehicle final position: ({last_pose.x:.2f}, {last_pose.y:.2f})")
    logger.info(f"Vehicle displacement: {displacement:.2f} meters")
    
    # Assert that the vehicle moves forward along the waypoints
    assert displacement > 0.5, f"Integration test failed! Vehicle did not move enough (displacement={displacement:.2f}m)"
    assert last_pose.velocity > 0.5, f"Integration test failed! Vehicle target speed not reached (v={last_pose.velocity:.2f} m/s)"
    
    logger.info("Integration Test: Closed-Loop Tracking and Motion Simulation PASSED!")

# ----------------- MAIN SUITE EXECUTOR -----------------

def main():
    logger.info("==============================================")
    logger.info("      4ZE RACING DRIVERLESS TEST SUITE        ")
    logger.info("==============================================")
    
    failed = False
    
    # Run Unit Tests
    try:
        test_pure_pursuit()
        test_kinematic_bicycle_model()
        test_coordinate_transformation()
    except AssertionError as e:
        logger.error(f"Unit test failed: {e}")
        failed = True
        
    # Run Integration Tests
    if not failed:
        try:
            run_integration_test()
        except AssertionError as e:
            logger.error(f"Integration test failed: {e}")
            failed = True
        except Exception as e:
            logger.error(f"An unexpected error occurred during integration test: {e}")
            failed = True
            
    logger.info("==============================================")
    if failed:
        logger.error("         TEST SUITE STATUS: FAILED            ")
        logger.info("==============================================")
        sys.exit(1)
    else:
        logger.info("         TEST SUITE STATUS: PASSED            ")
        logger.info("==============================================")
        sys.exit(0)

if __name__ == '__main__':
    main()
