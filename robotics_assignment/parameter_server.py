#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rcl_interfaces.srv import SetParameters, GetParameters
from rcl_interfaces.msg import ParameterValue, ParameterType
from std_srvs.srv import SetBool
import yaml

class ParameterServer(Node):
    def __init__(self):
        super().__init__('parameter_server')
        
        # Service to modify robot behavior parameters
        self.set_speed_service = self.create_service(
            SetBool, 
            'set_high_speed_mode', 
            self.set_speed_mode_callback
        )
        
        # Service to get current parameters
        self.get_params_service = self.create_service(
            GetParameters,
            'get_robot_parameters',
            self.get_parameters_callback
        )
        
        # Initialize parameters
        self.declare_parameter('robot_speed_multiplier', 1.0)
        self.declare_parameter('lidar_scan_frequency', 10.0)
        self.declare_parameter('safety_mode_enabled', False)
        
        self.get_logger().info('Parameter Server started - ready to modify robot behavior')
    
    def set_speed_mode_callback(self, request, response):
        """Service to toggle between normal and high speed mode"""
        high_speed = request.data
        
        if high_speed:
            # Set high speed parameters
            new_params = [
                rclpy.parameter.Parameter('robot_speed_multiplier', rclpy.Parameter.Type.DOUBLE, 2.0),
                rclpy.parameter.Parameter('max_linear_speed', rclpy.Parameter.Type.DOUBLE, 1.0),
                rclpy.parameter.Parameter('max_angular_speed', rclpy.Parameter.Type.DOUBLE, 2.0)
            ]
            response.message = "High speed mode enabled"
            self.get_logger().info('High speed mode activated')
        else:
            # Set normal speed parameters
            new_params = [
                rclpy.parameter.Parameter('robot_speed_multiplier', rclpy.Parameter.Type.DOUBLE, 1.0),
                rclpy.parameter.Parameter('max_linear_speed', rclpy.Parameter.Type.DOUBLE, 0.5),
                rclpy.parameter.Parameter('max_angular_speed', rclpy.Parameter.Type.DOUBLE, 1.0)
            ]
            response.message = "Normal speed mode enabled"
            self.get_logger().info('Normal speed mode activated')
        
        # Set all parameters
        self.set_parameters(new_params)
        response.success = True
        
        return response
    
    def get_parameters_callback(self, request, response):
        """Service to retrieve current robot parameters"""
        param_names = request.names
        
        for param_name in param_names:
            param = self.get_parameter(param_name)
            param_value = ParameterValue()
            
            if param.type_ == rclpy.Parameter.Type.DOUBLE:
                param_value.type = ParameterType.PARAMETER_DOUBLE
                param_value.double_value = param.value
            elif param.type_ == rclpy.Parameter.Type.BOOL:
                param_value.type = ParameterType.PARAMETER_BOOL
                param_value.bool_value = param.value
            elif param.type_ == rclpy.Parameter.Type.INTEGER:
                param_value.type = ParameterType.PARAMETER_INTEGER
                param_value.integer_value = param.value
            
            response.values.append(param_value)
        
        return response

def main(args=None):
    rclpy.init(args=args)
    
    parameter_server = ParameterServer()
    
    try:
        rclpy.spin(parameter_server)
    except KeyboardInterrupt:
        parameter_server.get_logger().info('Shutting down parameter server')
    finally:
        parameter_server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
