# ECE2318 Robotics Assignment - ROS 2 Simulation

## Assignment Requirements Implementation

### 1. ROS 2 Elements Explanation

**Nodes**: Independent computational units that process data. In this project:
- `robot_controller`: Publishes velocity commands to control robot motion
- `parameter_server`: Provides services to modify robot behavior
- `robot_state_publisher`: Publishes robot transform data
- `gazebo_ros`: Handles simulation interface

**Topics**: Named buses for message exchange:
- `/cmd_vel`: Robot motion control topic (Twist messages)
- `/scan`: Lidar sensor data (LaserScan messages)
- `/tf`: Transform hierarchy for robot coordinates
- `/robot_description`: URDF robot model data

**Messages**: Data structures for communication:
- `Twist`: Contains linear and velocity components for robot control
- `LaserScan`: Contains lidar distance measurements
- `TransformStamped`: Coordinate frame transformations

**Publishers**: Nodes that send data to topics:
- Robot controller publishes to `/cmd_vel`
- Gazebo publishes sensor data to `/scan`
- Robot state publisher publishes to `/tf`

**Subscribers**: Nodes that receive data from topics:
- Gazebo differential drive plugin subscribes to `/cmd_vel`
- RViz2 subscribes to `/scan` for visualization
- Navigation nodes subscribe to sensor data

**Services**: Request-response communication:
- `set_high_speed_mode`: Toggle between normal/high speed modes
- `get_robot_parameters`: Retrieve current robot parameters

**Actions**: Long-running tasks with feedback (demonstrated in parameter server)

**Parameters**: Configurable node settings:
- `max_linear_speed`: Maximum forward speed
- `max_angular_speed`: Maximum rotation speed
- `robot_speed_multiplier`: Speed behavior modifier

**Packages**: ROS 2 software containers containing nodes, launch files, and configurations

**Launch Files**: Orchestrate multiple nodes and system startup

### 2. Robot Motion Control Topic

**Topic Name**: `/cmd_vel`
**Message Type**: `geometry_msgs/Twist`

**Effect of Velocity Values**:
- `linear.x > 0`: Move forward
- `linear.x < 0`: Move backward  
- `linear.x = 0`: Stop linear motion
- `angular.z > 0`: Rotate counter-clockwise
- `angular.z < 0`: Rotate clockwise
- `angular.z = 0`: Stop rotation

**Increasing Values**: Higher speed, faster motion
**Decreasing Values**: Lower speed, slower motion

### 3. Velocity Command Control

The robot controller publishes `Twist` messages to `/cmd_vel`:
```python
twist = Twist()
twist.linear.x = 0.5  # Forward speed
twist.angular.z = 1.0 # Turn speed
cmd_vel_pub.publish(twist)
```

**Subscriber Implementation**: Gazebo differential drive plugin subscribes to `/cmd_vel` and converts Twist messages into wheel velocities for the simulated robot.

### 4. Parameter-Based Behavior Modification

Parameters modify robot behavior at runtime:
- Speed parameters control maximum velocities
- Safety parameters enable obstacle avoidance
- Sensor parameters adjust lidar configuration

**Package Role**: Organizes all related code, configurations, and launch files
**Launch File Role**: Coordinates system startup with proper parameter loading

### 5. RViz2 Visualization

RViz2 visualizes:
- Robot model from URDF
- Lidar sensor data (point cloud)
- Robot coordinate frames
- Sensor measurements

**Service Example**: `set_high_speed_mode` service allows runtime speed adjustment
**Action Example**: Parameter server uses actions for complex configuration changes

## Usage Instructions

### Build the Package
```bash
cd ~/ros2_ws
colcon build --packages-select robotics_assignment
source install/setup.bash
```

### Launch Simulation
```bash
ros2 launch robotics_assignment robot_simulation.launch.py
```

### Control Robot Speed
```bash
# Enable high speed mode
ros2 service call /set_high_speed_mode std_srvs/SetBool "{data: true}"

# Disable high speed mode  
ros2 service call /set_high_speed_mode std_srvs/SetBool "{data: false}"
```

### View Robot Parameters
```bash
ros2 param list /robot_controller
ros2 param get /robot_controller max_linear_speed
```

### Monitor Topics
```bash
ros2 topic echo /cmd_vel
ros2 topic echo /scan
```

## File Structure
```
robotics_assignment/
├── package.xml                    # Package metadata
├── setup.py                      # Package setup configuration
├── my_robot.urdf                 # Robot model definition
├── config/
│   └── robot_params.yaml         # Parameter configurations
├── launch/
│   └── robot_simulation.launch.py # Main launch file
├── robotics_assignment/
│   ├── __init__.py
│   ├── robot_controller.py       # Velocity control node
│   └── parameter_server.py       # Parameter management node
└── resource/
    └── robotics_assignment       # Package resource marker
```
