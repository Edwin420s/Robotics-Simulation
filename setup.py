from setuptools import setup

package_name = 'robotics_assignment'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['launch_sim.py']),
        ('share/' + package_name, ['my_robot.urdf']),
        ('share/' + package_name + '/config', ['config/robot_params.yaml']),
        ('share/' + package_name + '/launch', ['launch/robot_simulation.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Student',
    maintainer_email='student@university.edu',
    description='ECE2318 Robotics Assignment - ROS 2 Simulation',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot_controller = robotics_assignment.robot_controller:main',
            'parameter_server = robotics_assignment.parameter_server:main',
        ],
    },
)
