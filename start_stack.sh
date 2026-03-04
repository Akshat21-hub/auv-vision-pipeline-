#!/bin/bash

# 1. Check if you passed "off" as an argument
VISION_ARGS=""
if [ "$1" == "off" ]; then
    echo "Launching with Image Enhancement DISABLED."
    VISION_ARGS="--ros-args -p enable_enhancement:=False"
else
    echo "Launching with Image Enhancement ENABLED."
fi

echo "Launching Dreadnought Stack in separate tabs..."

# 2. Inject the arguments into the Vision Tab
gnome-terminal --tab --title="Vision" -- bash -c "source /opt/ros/jazzy/setup.bash && source ~/auv_ws/install/setup.bash && ros2 run bp_vision bp_node $VISION_ARGS; exec bash"

# Tab 2: Control Node
gnome-terminal --tab --title="Control" -- bash -c "source /opt/ros/jazzy/setup.bash && source ~/auv_ws/install/setup.bash && ros2 run gate_control gate_navigator_node; exec bash"

# Tab 3: Command Echo
gnome-terminal --tab --title="Echo" -- bash -c "source /opt/ros/jazzy/setup.bash && source ~/auv_ws/install/setup.bash && ros2 topic echo /master/commands; exec bash"
