import os
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():

    # Path to the combined robot URDF
    combined_robot_file = os.path.join(
        get_package_share_directory("combined_description"), "urdf", "combined_robot.urdf.xacro"
    )

    # Robot description loaded via xacro
    robot_description = Command(
        [PathJoinSubstitution([FindExecutable(name="xacro")]), " ", combined_robot_file]
    )

    # Robot State Publisher
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{
            "robot_description": robot_description
        }]
    )

    # Load MoveIt configurations
    moveit_config = MoveItConfigsBuilder(
        "motoman_gp7", package_name="motoman_gp7_moveit_config"
    ).to_moveit_configs()

    # Move Group Launch
    move_group = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(moveit_config.package_path / "launch/move_group.launch.py")
        )
    )

    # RViz Launch
    rviz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(moveit_config.package_path / "launch/moveit_rviz.launch.py")
        )
    )

    return LaunchDescription([
        robot_state_publisher,
        move_group,
        rviz
    ])
