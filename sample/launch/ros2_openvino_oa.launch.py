# Copyright 2018 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Launch face detection and rviz."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
import launch_ros.actions
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    default_yaml = os.path.join(get_package_share_directory('dynamic_vino_sample'), 'param',
                                'lite_pipeline_object_topic.yaml')
    default_rviz = os.path.join(get_package_share_directory('dynamic_vino_sample'), 'launch',
                                'rviz/default.rviz')
    open_rviz = LaunchConfiguration('open_rviz', default='false')

    return LaunchDescription([
        # RealSense
        launch_ros.actions.Node(
            package='realsense_node', 
            node_executable='realsense_node',
            node_namespace='',
            output='screen'),

        # Openvino detection
        launch_ros.actions.Node(
            package='dynamic_vino_sample', node_executable='pipeline_with_params',
            arguments=['-config', default_yaml],
            remappings=[
                ('/openvino_toolkit/image_raw', '/camera/color/image_raw'),
                ('/openvino_toolkit/object/detected_objects',
                 '/ros2_openvino_toolkit/detected_objects'),
                ('/openvino_toolkit/object/images', '/ros2_openvino_toolkit/image_rviz')],
            output='screen'),

        # Rviz
        DeclareLaunchArgument(
            'open_rviz',
            default_value='false',
            description='Launch Rviz?'),        
        launch_ros.actions.Node(
            package='rviz2', node_executable='rviz2', output='screen',
            condition=IfCondition(LaunchConfiguration("open_rviz")),
            arguments=['--display-config', default_rviz]),
    ])
