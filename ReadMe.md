## Autonomous wheelchair 

Assembling a wheelchair and making it autonomous using a LIDAR sensor for obstacle detection. This project is part of an overarcing project at Aurora Robotics to apply robotics to medical assistive tools, in this case, a wheelchair.

Current progress:

|  RViZ  |  Gazebo   |
| :---: | :---: |
| ![chair1](https://github.com/Iqmaa/Autonomous_wheelchair/blob/main/Media/week2_lidar.png?raw=true)  | ![chair2](https://github.com/Iqmaa/Autonomous_wheelchair/blob/main/Media/week2_lidar-rays.png?raw=true) |


### Steps to Launch

1. clone the repo
```
git clone (insert link)
```
2. build the workspace
```
colcon build --symlink-install
```
3. source the workspace
```
source install/setup.bash
```
4. launch the project
#### RViZ alone
```
ros2 launch urdf_tutorial display.launch.py model:=$(pwd)/src/wheelchair_description/urdf/chair.xacro
```
#### Gazebo Tele-op

terminal 1 (to launch the chair in gazebo)
```
ros2 launch wheelchair_bringup simulated_wheelchair.launch.py
```
terminal 2 (for keyboard control)
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard   --ros-args -p stamped:=false -r cmd_vel:=wheel_controller/cmd_vel_unstamped
```

#### Obstacle detection
terminal 1
```
ros2 launch wheelchair_bringup simulated_wheelchair.launch.py
```
terminal 2
```
ros2 run wheelchair_script obstacle_avoidance
```

### Movement, Teleoperation, and Obstacle avoidance demos

[week2_obstacle_detecting.webm](https://github.com/user-attachments/assets/06835ca2-4f37-4d6b-bc5e-a91f949c9ed5)

[basic_wheelchair_movement.webm](https://github.com/user-attachments/assets/fab8aedc-2264-45f9-b151-604158d3451f)

[gazebo_teleop.webm](https://github.com/user-attachments/assets/a195f447-2c9d-4e5e-bafd-ae7d889a2d30)


Link to progress report : https://docs.google.com/document/d/1sxpyhflVC5Y_dnnonwOcHkn5cXx0ACv0yo_RJys0I18/edit?usp=sharing
