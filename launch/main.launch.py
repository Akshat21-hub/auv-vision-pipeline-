from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        # 1. Start the Vision Node (The Eyes)
        Node(
            package='bp_vision',
            executable='bp_node',
            name='vision_node',
            output='screen'
        ),
        
        # 2. Start the Navigator Node (The Brain)
        Node(
            package='gate_control',
            executable='gate_navigator_node',
            name='navigator_node',
            output='screen'
        ),
        
        # 3. Temporarily echo the commands (The Muscles - until hardware is ready)
        ExecuteProcess(
            cmd=['ros2', 'topic', 'echo', '/master/commands'],
            output='screen'
        )
    ])
