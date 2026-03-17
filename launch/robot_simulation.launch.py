#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Declare launch arguments
    config_file_arg = DeclareLaunchArgument(
        'config_file',
        default_value=os.path.join(
            get_package_share_directory('robotics_assignment'),
            'config',
            'robot_params.yaml'
        ),
        description='Path to robot configuration file'
    )
    
    # Load URDF file
    urdf_path = os.path.join(
        get_package_share_directory('robotics_assignment'),
        'my_robot.urdf'
    )
    with open(urdf_path, 'r') as f:
        robot_desc = f.read()

    return LaunchDescription([
        # Launch arguments
        config_file_arg,
        
        # 1. Start Gazebo Simulator
        ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        ),
        
        # 2. Robot State Publisher with parameters
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[
                {'robot_description': robot_desc},
                LaunchConfiguration('config_file')
            ]
        ),
        
        # 3. Spawn Robot into Gazebo
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'ece_bot', '-topic', 'robot_description']
        ),
        
        # 4. Start RViz2 for Sensor Visualization
        Node(
            package='rviz2',
            executable='rviz2',
            parameters=[LaunchConfiguration('config_file')]
        ),
        
        # 5. Robot Controller Node (for velocity commands)
        Node(
            package='robotics_assignment',
            executable='robot_controller',
            name='robot_controller',
            parameters=[LaunchConfiguration('config_file')],
            output='screen'
        ),
        
        # 6. Parameter Server Node (for modifying robot behavior)
        Node(
            package='robotics_assignment',
            executable='parameter_server',
            name='parameter_server',
            parameters=[LaunchConfiguration('config_file')],
            output='screen'
        ),
    ])
