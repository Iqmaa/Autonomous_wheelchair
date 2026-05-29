## Autonomous wheelchair 

Assembling a wheelchair and making it autonomous using a LIDAR sensor for obstacle detection. This project is part of an overarcing project at Aurora Robotics to apply robotics to medical assistive tools, in this case, a wheelchair.

Current progress:

|  RViZ  |  Gazebo   |
| :---: | :---: |
| ![chair1](https://github.com/Iqmaa/Autonomous_wheelchair/blob/main/Media/week2_complete.png?raw=true)  | ![chair2](https://github.com/Iqmaa/Autonomous_wheelchair/blob/main/Media/week2_gazebo_controls.png?raw=true) |


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
```
ros2 launch urdf_tutorial display.launch.py model:=$(pwd)/src/wheelchair_description/urdf/chair.xacro
```
### Movements and Teleoperation

[basic_wheelchair_movement.webm](https://github.com/user-attachments/assets/fab8aedc-2264-45f9-b151-604158d3451f)

[gazebo_teleop.webm](https://github.com/user-attachments/assets/a195f447-2c9d-4e5e-bafd-ae7d889a2d30)


Link to progress report : https://docs.google.com/document/d/1sxpyhflVC5Y_dnnonwOcHkn5cXx0ACv0yo_RJys0I18/edit?usp=sharing
