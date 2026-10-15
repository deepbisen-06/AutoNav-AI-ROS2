import os

from ament_index_python.packages import (
    get_package_share_directory
)

from launch import LaunchDescription

from launch_ros.actions import Node


def generate_launch_description():

    package_dir = get_package_share_directory(
        'autonav_control'
    )

    config_file = os.path.join(
        package_dir,
        'config',
        'robot_config.yaml'
    )

    publisher_node = Node(
        package='autonav_control',
        executable='robot_status_publisher',
        name='robot_status_publisher',
        output='screen'
    )

    subscriber_node = Node(
        package='autonav_control',
        executable='robot_status_subscriber',
        name='robot_status_subscriber',
        output='screen'
    )

    config_node = Node(
        package='autonav_control',
        executable='robot_config',
        name='robot_config',
        parameters=[config_file],
        output='screen'
    )

    return LaunchDescription([
        publisher_node,
        subscriber_node,
        config_node
    ])
