
#!/usr/bin/env python3

import os

from ament_index_python.packages import (
    get_package_share_directory
)

from launch import LaunchDescription

from launch_ros.actions import Node


def generate_launch_description():

    package_name = 'autonav_control'

    package_share = get_package_share_directory(
        package_name
    )

    # Paths to existing Day 13 and Day 16 files
    urdf_file = os.path.join(
        package_share,
        'urdf',
        'autonav_robot.urdf'
    )

    rviz_config = os.path.join(
        package_share,
        'rviz',
        'autonav_dashboard.rviz'
    )

    # Read robot URDF
    with open(urdf_file, 'r', encoding='utf-8') as file:
        robot_description = file.read()

    # Publish robot link transforms from URDF
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {'robot_description': robot_description}
        ]
    )

    # Day 14: Simulated differential-drive motion
    robot_motion = Node(
        package='autonav_control',
        executable='robot_motion',
        name='robot_motion',
        output='screen'
    )

    # Day 15: map -> odom static transform
    map_frame_publisher = Node(
        package='autonav_control',
        executable='map_frame_publisher',
        name='map_frame_publisher',
        output='screen'
    )

    # Day 16: Path and goal visualization
    visualization_node = Node(
        package='autonav_control',
        executable='visualization_node',
        name='visualization_node',
        output='screen'
    )

    # Open saved RViz2 dashboard
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz',
        output='screen',
        arguments=['-d', rviz_config]
    )

    return LaunchDescription([
        robot_state_publisher,
        robot_motion,
        map_frame_publisher,
        visualization_node,
        rviz_node
    ])
