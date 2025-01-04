# Webots AI Controller

Welcome to my robotics projects repository! This is a collection of projects I've developed and continue to expand, primarily using Webots simulation. 


Feel free to explore the repository and its projects. Each project folder contains more details, including implementation and code structure. **Contributions and feedback are always welcome!**


Below is a brief overview of each project:

---

## Projects

### 1. Line Follower
A basic implementation of a line-following robot using an e-puck. It utilizes IR sensors to detect lines and adjust motor speeds to stay on track.

---

### 2. Obstacle Avoidance
This robot detects obstacles using distance sensors and a camera. It adjusts its movement dynamically to avoid collisions, demonstrating basic navigation principles.

---

### 3. Wall Following
Implements a wall-following algorithm using proximity sensors to maintain a consistent distance from walls. This project also explores reinforcement learning for improving the robot's wall-following behavior, though the RL implementation is currently under development.

---

### 4. Maze Runner
A robot designed to solve mazes using basic decision-making logic. It incorporates distance and ground sensors for path detection and navigation within maze structures.

---

### 5. Micro-Mouse
Inspired by micro-mouse competitions, this project involves generating maze structures programmatically and solving them using pathfinding algorithms. The maze generation is automated with a script inside `micro_mouse/maze_generator`, which converts a text-based design into a Webots world file.

#### Example Maze (Text-Based Design):
```text
o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o
|                                                               |
o   o---o---o---o---o---o---o---o---o---o---o---o---o---o   o   o
|   |                                                   |       |
o   o   o---o---o---o---o---o---o---o---o---o---o---o   o   o   o
|   |   |                                           |   |       |
o   o   o   o   o---o---o---o---o   o   o   o   o   o   o   o   o
|   |   |       |       |       |                   |   |       |
o   o   o---o---o   o   o   o   o---o   o   o   o   o   o   o   o
|   |               |       |       |               |   |       |
o   o---o---o---o   o   o   o   o   o   o   o   o   o   o   o   o
|               |       |       |   |               |   |       |
o   o   o   o   o---o---o---o---o   o   o   o   o   o   o   o   o
|                               |   |               |   |       |
o   o   o   o   o   o   o   o---o   o   o   o   o   o   o   o   o
|                           |       |               |   |       |
o   o   o   o   o   o   o   o   o   o   o   o   o   o   o   o   o
|                           |       |               |   |       |
o   o   o   o   o   o   o   o---o---o   o   o   o   o   o   o   o
|                                                   |   |       |
o   o   o   o   o   o   o   o   o   o   o   o   o   o   o   o   o
|                                                   |   |       |
o   o   o   o---o---o---o---o   o   o---o---o---o---o   o   o   o
|           |       |       |       |       |       |   |       |
o---o---o---o   o   o   o   o---o---o   o   o   o   o   o   o   o
|               |       |               |       |       |       |
o   o---o---o   o   o   o   o---o---o   o   o   o   o---o   o   o
|   |       |       |       |       |       |       |           |
o   o   o   o---o---o---o---o   o   o---o---o---o---o   o   o   o
|   |                                                           |
o   o   o   o   o   o   o   o   o   o   o   o   o   o   o   o   o
|   |                                                           |
o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o
```
Example of a generated maze:  
<img src="https://github.com/user-attachments/assets/49aa2a81-5dbe-440d-9d4f-669f0e41026e" width="300" alt="Example of a generated maze">

#### Different maze-solving algorithms:

1- Right-hand Wall-following
https://github.com/user-attachments/assets/2bc5ba19-d46e-4c33-9f89-5ffa444403c9




