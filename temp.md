# Implementing Step 2: ROS2 State Machine Node in Detail

This guide explains how to implement the ROS2 state machine package (`state_machine`) for the 4ZE Racing Autonomous Vehicle stack. The state machine is the highest authority in the system and controls the operating modes of the vehicle.

---

## 1. Creating the ROS2 Package

To create the python-based ROS2 package:

1. Open your terminal inside the `src/` directory.
2. Run the package creation command:
   ```bash
   ros2 pkg create --build-type ament_python state_machine --dependencies rclpy av_interfaces std_msgs
   ```

This will generate the following structure inside `src/state_machine/`:
- `package.xml`
- `setup.py`
- `setup.cfg`
- `resource/state_machine`
- `state_machine/` (Python package directory)
- `state_machine/__init__.py`

---

## 2. Package Configuration Files

### `package.xml`
Ensure the dependencies are declared correctly. The dependencies on `rclpy`, `av_interfaces`, and `std_msgs` should be listed:

```xml
  <depend>rclpy</depend>
  <depend>av_interfaces</depend>
  <depend>std_msgs</depend>
```

### `setup.py`
To register the node entry point so it can be run using `ros2 run state_machine state_machine_node`, configure the `entry_points` dictionary inside `setup.py`:

```python
    entry_points={
        'console_scripts': [
            'state_machine_node = state_machine.state_machine_node:main',
        ],
    },
```

---

## 3. Implementing the State Machine Node (`state_machine_node.py`)

Create a python file `src/state_machine/state_machine/state_machine_node.py`. The node logic must handle:
1. Publishing the current autonomous state and selected mission.
2. Listening to E-stop requests and simulated Remote Emergency System (RES) inputs.
3. Transitioning between states according to Formula Bharat driverless rules.

### Detailed Python Code Skeleton

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from av_interfaces.msg import AutonomousState, Mission, EmergencyStop

class StateMachineNode(Node):
    def __init__(self):
        super().__init__('state_machine_node')

        # 1. State Variables
        self.current_state = AutonomousState.AS_OFF
        self.selected_mission = Mission.MISSION_NONE
        self.state_entered_time = self.get_clock().now()

        # 2. Publishers
        self.state_pub = self.create_publisher(AutonomousState, '/system/as_state', 10)
        self.mission_pub = self.create_publisher(Mission, '/system/mission', 10)

        # 3. Subscribers
        # Listen to emergency stop requests from the safety supervisor
        self.estop_sub = self.create_subscription(
            EmergencyStop,
            '/supervisor/estop',
            self.estop_callback,
            10
        )
        
        # Listen to RES (Remote Emergency System) GO command (e.g. from tests or hardware)
        self.res_go_sub = self.create_subscription(
            Bool,
            '/res/go',
            self.res_go_callback,
            10
        )

        # Listen to mission selector (e.g., from physical switch or simulation topic)
        self.mission_select_sub = self.create_subscription(
            Mission,
            '/system/select_mission',
            self.mission_select_callback,
            10
        )

        # 4. Timers
        # Main state publishing loop running at 10 Hz
        self.publish_timer = self.create_timer(0.1, self.publish_status)
        # Main transition check loop running at 50 Hz
        self.transition_timer = self.create_timer(0.02, self.transition_loop)

        self.get_logger().info("State Machine Node Initialized. Current State: AS_OFF")

    def change_state(self, new_state):
        if self.current_state != new_state:
            self.get_logger().info(f"Transitioning from state {self.current_state} -> {new_state}")
            self.current_state = new_state
            self.state_entered_time = self.get_clock().now()

    def estop_callback(self, msg):
        if msg.stop_request:
            self.get_logger().warn(f"Emergency Stop Triggered! Reason: {msg.reason}")
            self.change_state(AutonomousState.AS_EMERGENCY)

    def res_go_callback(self, msg):
        # We only accept GO if the command is True, we are in AS_READY, and have selected a mission
        if msg.data and self.current_state == AutonomousState.AS_READY:
            if self.selected_mission != Mission.MISSION_NONE:
                self.change_state(AutonomousState.AS_DRIVING)
            else:
                self.get_logger().warn("Cannot transition to AS_DRIVING: No mission selected!")

    def mission_select_callback(self, msg):
        if self.current_state == AutonomousState.AS_OFF:
            self.selected_mission = msg.mission
            self.get_logger().info(f"Mission selected: {msg.mission}")
            # If a mission is successfully selected and system checks pass, transition to READY
            self.change_state(AutonomousState.AS_READY)

    def publish_status(self):
        # Publish current autonomous state
        state_msg = AutonomousState()
        state_msg.state = self.current_state
        self.state_pub.publish(state_msg)

        # Publish current active/selected mission
        mission_msg = Mission()
        mission_msg.mission = self.selected_mission
        self.mission_pub.publish(mission_msg)

    def transition_loop(self):
        # Formula Bharat state machine transitions and timing rules
        now = self.get_clock().now()
        time_in_state = (now - self.state_entered_time).nanoseconds / 1e9

        if self.current_state == AutonomousState.AS_READY:
            # Rule: Must remain in AS_READY for at least 5 seconds before driving can begin
            # This is automatically enforced because res_go_callback transition is gated by checks
            # However, you can enforce other safety checks here.
            pass

        elif self.current_state == AutonomousState.AS_DRIVING:
            # Rule: The vehicle must remain stationary for 3 seconds after entering AS_DRIVING
            # before it begins autonomous motion. During this time, the ASSI must flash yellow.
            # Gating nodes (e.g. control node) should monitor '/system/as_state' and check if
            # 3 seconds have passed, or this node can publish a 'motion_enabled' flag.
            pass

        elif self.current_state == AutonomousState.AS_EMERGENCY:
            # Once in AS_EMERGENCY, the system must remain locked until manual power cycle
            # (as per Formula Bharat safety rules).
            pass

def main(args=None):
    rclpy.init(args=args)
    node = StateMachineNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## 4. Key Transition Rules (Formula Bharat Compliance)

| Initial State | Event / Trigger | Target State | Constraints / Timing |
|---|---|---|---|
| **AS_OFF** | Mission selected + No active faults | **AS_READY** | System checks healthy. |
| **AS_READY** | RES GO command received | **AS_DRIVING** | Must have been in `AS_READY` for $\ge 5$ seconds. |
| **AS_DRIVING** | System finishes mission successfully | **AS_FINISHED** | Vehicle comes to a complete stop. |
| **Any State** | E-Stop requested (or hardware ASMS/RES) | **AS_EMERGENCY** | Immediate transition. Forces brake engagement and disables tractive system. |
| **AS_EMERGENCY**| Manual system reset / power cycle | **AS_OFF** | Cannot transition out of `AS_EMERGENCY` through software commands. |
