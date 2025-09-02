import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    # Configure the use_sim_time launch argument
    use_sim_time = LaunchConfiguration('use_sim_time')
    declare_use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )

    # Get the path to the URDF xacro file
    pkg_path = get_package_share_directory('box_bot')
    xacro_file = os.path.join(pkg_path, 'description', 'robot.urdf.xacro')

    # Use the Command substitution to process the xacro file
    robot_description_command = Command(['xacro ', xacro_file])

    # Create the robot_state_publisher node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_command,
            'use_sim_time': use_sim_time
        }]
    )

    # Launch!
    return LaunchDescription([
        declare_use_sim_time_arg,
        node_robot_state_publisher
    ])