import os
from os import pathsep
from pathlib import Path
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.substitutions import Command, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    wheelchair_description = get_package_share_directory("wheelchair_description")

    model_arg = DeclareLaunchArgument(
        name="model", default_value=os.path.join(
                wheelchair_description, "urdf", "chair.xacro",
            ),
        description="Absolute path to robot urdf file"
    )

    # Configure path environment search trees for mesh loading resolution
    model_path = str(Path(wheelchair_description).parent.resolve())
    # model_path += pathsep + os.path.join(get_package_share_directory("wheelchair_description"), 'models')

    # # Configure path environment search trees to include BOTH description and controller share paths
    # package_share_parent = str(Path(wheelchair_description).parent.resolve())
    
    # # Get the explicit share directory of your controller package
    # wheelchair_controller_share = get_package_share_directory("wheelchair_controller")
    # controller_share_parent = str(Path(wheelchair_controller_share).parent.resolve())

    # # Stitch them together using the standard system path separator
    # combined_model_path = package_share_parent + pathsep + controller_share_parent

    gazebo_resource_path = SetEnvironmentVariable(
        "GZ_SIM_RESOURCE_PATH",
        model_path
    )

    robot_description = ParameterValue(Command([
            "xacro ",
            LaunchConfiguration("model"),
            " is_sim:=True",
        ]),
        value_type=str
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description,
                     "use_sim_time": True}]
    )

    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory("ros_gz_sim"), "launch"), "/gz_sim.launch.py"]),
                launch_arguments={
                    "gz_args": "-r empty.sdf" 
                }.items()
             )

    gz_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-topic", "robot_description",
            "-name", "wheelchair",
            "-x", "0.0",  
            "-y", "0.0",  
            "-z", "0.5", 
            "-R", "0.0", 
            "-P", "0.0",
            "-Y", "0.0",
        ],
    )

    gz_ros2_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
            # "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
            "/scan/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked",
        ],
    )

    return LaunchDescription([
        model_arg,
        gazebo_resource_path,
        robot_state_publisher_node,
        gazebo,
        gz_spawn_entity,
        gz_ros2_bridge,
    ])