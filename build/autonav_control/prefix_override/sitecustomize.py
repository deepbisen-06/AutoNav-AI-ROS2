import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/deep_06/AutoNav-AI-ROS2/install/autonav_control'
