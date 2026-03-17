#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.parameter import Parameter
import math
import time

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        
        # Publisher for velocity commands
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Declare parameters with default values
        self.declare_parameter('max_linear_speed', 0.5)
        self.declare_parameter('max_angular_speed', 1.0)
        self.declare_parameter('control_frequency', 10.0)
        
        # Get parameter values
        self.max_linear_speed = self.get_parameter('max_linear_speed').value
        self.max_angular_speed = self.get_parameter('max_angular_speed').value
        self.control_frequency = self.get_parameter('control_frequency').value
        
        # Timer for periodic commands
        self.timer = self.create_timer(1.0/self.control_frequency, self.timer_callback)
        self.start_time = time.time()
        
        self.get_logger().info(f'Robot Controller started with max_linear_speed: {self.max_linear_speed}')
    
    def timer_callback(self):
        """Publish velocity commands to control robot motion"""
        current_time = time.time() - self.start_time
        
        # Create a pattern of movement (square pattern)
        twist = Twist()
        
        # Move forward for 3 seconds
        if current_time < 3.0:
            twist.linear.x = self.max_linear_speed
            twist.angular.z = 0.0
        # Turn for 1.5 seconds
        elif current_time < 4.5:
            twist.linear.x = 0.0
            twist.angular.z = self.max_angular_speed
        # Move forward for 3 seconds
        elif current_time < 7.5:
            twist.linear.x = self.max_linear_speed
            twist.angular.z = 0.0
        # Turn for 1.5 seconds
        elif current_time < 9.0:
            twist.linear.x = 0.0
            twist.angular.z = self.max_angular_speed
        # Stop
        else:
            twist.linear.x = 0.0
            twist.angular.z = 0.0
        
        self.cmd_vel_pub.publish(twist)
        
        # Log current velocity values
        if twist.linear.x != 0.0 or twist.angular.z != 0.0:
            self.get_logger().info(f'Publishing: linear.x={twist.linear.x:.2f}, angular.z={twist.angular.z:.2f}')
    
    def stop_robot(self):
        """Stop the robot immediately"""
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.cmd_vel_pub.publish(twist)
        self.get_logger().info('Robot stopped')

def main(args=None):
    rclpy.init(args=args)
    
    controller = RobotController()
    
    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        controller.get_logger().info('Keyboard interrupt, stopping robot')
        controller.stop_robot()
    finally:
        controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
