import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'autonav_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/autonav_control']
        ),
        (
            'share/autonav_control',
            ['package.xml']
        ),
        (
             os.path.join('share', 'autonav_control', 'launch'),
             glob('launch/*.launch.py')
        ),
        (
             os.path.join('share', 'autonav_control', 'config'),
             glob('config/*.yaml')
        ),
	('share/' + package_name + '/urdf', glob('urdf/*.urdf')
	),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='deep_06',
    maintainer_email='deepbisen2006@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'robot_status_publisher = autonav_control.robot_status_publisher:main',
            'robot_status_subscriber = autonav_control.robot_status_subscriber:main',
	    'add_two_ints_server = autonav_control.add_two_ints_server:main',
            'add_two_ints_client = autonav_control.add_two_ints_client:main',
	    'robot_config = autonav_control.robot_config:main',
	    'turtle_motion = autonav_control.turtle_motion:main',
	    'go_to_goal = autonav_control.go_to_goal:main',
	    'waypoint_navigation = autonav_control.waypoint_navigation:main',
	    'odometry_publisher = autonav_control.odometry_publisher:main',
	    'differential_drive = autonav_control.differential_drive:main',
	    'velocity_smoother = autonav_control.velocity_smoother:main',
	    'robot_motion = autonav_control.robot_motion:main',
	    'map_frame_publisher = autonav_control.map_frame_publisher:main',
         ],
    },
)
