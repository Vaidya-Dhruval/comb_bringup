import os
import time
from ament_index_python import get_package_share_directory
from launch import LaunchDescription, actions
from launch.actions import DeclareLaunchArgument
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
    TextSubstitution,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import launch_ros
from launch.actions import TimerAction
from launch.conditions import IfCondition

from moveit_configs_utils.launch_utils import (
    DeclareBooleanLaunchArg,
)
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    gp7_file = os.path.join(
        get_package_share_directory("motoman_gp7_description"), "urdf", "gp7.xacro"
    )

    robot_description = Command(
        [PathJoinSubstitution([FindExecutable(name="xacro")]), " ", gp7_file]
    )
    
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description": launch_ros.descriptions.ParameterValue(
                    value=robot_description, value_type=str
                )
            }
        ],
    )

    
    # MoveIt
    moveit_config = MoveItConfigsBuilder(
        "motoman_gp7", package_name="motoman_gp7_moveit_config"
    ).to_moveit_configs()

    move_group = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(moveit_config.package_path / "launch/move_group.launch.py")
        ),
    )

    rviz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(moveit_config.package_path / "launch/moveit_rviz.launch.py")
        ),
    )

    nodes_list = [
        robot_state_publisher,
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                str(moveit_config.package_path / "launch/move_group.launch.py")
            )
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                str(moveit_config.package_path / "launch/moveit_rviz.launch.py")
            )
        ),
    ]
    
    

    return LaunchDescription(nodes_list)