## Autonomous wheelchair 

Assembling a wheelchair and making it autonomous using a LIDAR sensor for obstacle detection

Current progress:

|     |     |
| :---: | :---: |
| ![chair1]()  | ![chair2]() |


Link to progress report : https://docs.google.com/document/d/1sxpyhflVC5Y_dnnonwOcHkn5cXx0ACv0yo_RJys0I18/edit?usp=sharing

### Learnings

1. - used to think collision tags were all obj and visuals DAE/STL, this showed me that wasn't the case and people use them interchangeably becuase of their needs. (This project uses obj + mtl for visuals and stl for collision)

- dae was heavily recommended for visuals because it natively stored complex color gradients, textures, and material shine perfectly inside a single file but apparently .obj is preferred over .dae for visuals because it is simpler, lightweight, and universally supported by almost every 3D application (Blender, Gazebo, Unity) then it pairs with the .mtl file to handle textures. (.stl equivalents are sometimes left as fallback since some people's simulator versions can't run .mtl + .obj formats)

- stl files do not support colors or textures at all—they only store raw 3D triangles. Because they are "blind" to color, they are perfect for the collision engine, which only cares about shapes. (using obj for collisions is heavy and might even crash gazebo?)

2. - don't use all 0s in the inertial inertia tag, it can cause because division-by-zero errors occur in the rigid-body physics calculations (a = F/m). use something like this instead `<inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>`

3. when trying to assemble different links, the only xyz coordinates i have to chnage are the ones in the joint tag.

4. Learnt how to directly measure required xyz coordinates using meshlab(and the prismatic joint type) instead of guessing and doing trial and error.

5. since i used '--symlink-install' when building, the only time i actually have to build again is when i do things like file structure changes, editing cmakelists.txt, package.xml, setup.py, anything that ends with .cpp or .hpp(because cpp is a compile language) or adding a new package