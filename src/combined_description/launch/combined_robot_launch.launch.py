from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.substitutions import Command, PathJoinSubstitution, FindExecutable
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # Paths to package directories
    combined_description_path = get_package_share_directory('combined_description')
    robotiq_description_path = get_package_share_directory('ros2_robotiq_gripper')
    motoman_moveit_config_path = get_package_share_directory('motoman_gp7_moveit_config')
    
    # Load combined robot description (GP7 + Robotiq)
    combined_robot_file = combined_description_path + "/urdf/combined_robot.urdf.xacro"
    robot_description = {"robot_description": Command([PathJoinSubstitution([FindExecutable(name="xacro")]), " ", combined_robot_file])}

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )
    
    # Load MoveIt for GP7
    moveit_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([motoman_moveit_config_path + '/launch/move_group.launch.py'])
    )

    # Launch the Robotiq Gripper driver
    gripper_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([robotiq_description_path + '/launch/gripper_driver.launch.py'])
    )
    
    # Launch RViz with MoveIt visualization for GP7
    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([motoman_moveit_config_path + '/launch/moveit_rviz.launch.py'])
    )

    return LaunchDescription([
        robot_state_publisher,
        moveit_launch,
        gripper_driver_launch,
        rviz_launch
    ])
