import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    # Load your custom URDF file
    urdf_path = os.path.join(os.getcwd(), 'my_robot.urdf')
    with open(urdf_path, 'r') as f:
        robot_desc = f.read()

    return LaunchDescription([
        # 1. Start Gazebo Simulator
        ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so'], output='screen'),
        
        # 2. Publish Robot State
        Node(package='robot_state_publisher', executable='robot_state_publisher', parameters=[{'robot_description': robot_desc}]),
        
        # 3. Spawn Robot into Gazebo
        Node(package='gazebo_ros', executable='spawn_entity.py', arguments=['-entity', 'my_custom_bot', '-topic', 'robot_description']),
        
        # 4. Start RViz2 for Sensor Visualization
        Node(package='rviz2', executable='rviz2')
    ])