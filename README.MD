# BigBoy_Waiter

Real-time human pose mirroring for the Kbot. PoseBot captures human poses through a camera and replicates the movements on a physical robot.
K-BOT Hackathon code to move an arm

## Overview

PoseBot uses computer vision to detect and track human poses in real-time, then translates these movements into robot joint commands. This creates an interactive experience where the robot mirrors human movements as they happen.

## Usage

```bash
python bigboy.py
```
You will need python 3.11 to run this code (last version of kos needs that).

Make sure you change the ROBOT_IP with the IP of the raspberry pi that is running the
kos server.
You should be able to move the robot arm by pressing the arrow keys.

## Features

- Real-time human pose detection using computer vision
- Smooth translation of human movements to robot joint positions
- Built with Rust for high performance and reliability
- Generic `humanoid` interface supports different robotics platforms

## Requirements (Fix issues.)

- Rust (latest stable version)
- Compatible robot hardware (servo motors, actuators)
- USB camera or webcam
- Linux/macOS/Windows operating system


## Installation
1. Clone the repository:

```bash
git clone https://github.com/rgarreta/bigboy.git
cd bigboy
```
Create a virtual environment.

Install all the requirements:

```bash
pip install -r requirements.txt
```

## Usage

1. Connect your camera and robot hardware
2. Setup `.env` with the correct IP for the server
3. Run the bigboy service:

```bash
cargo run
```

3. Stand in front of the camera with a can or party cup.
4. Allow the robot to collect the glass/cup.

## Safety

- The robot has conservative angle movements to prevent clashing with itself or stumbling.
- Please keep a few steps away from the robot during operation.

## Architecture  *** Section needs updating ***

- `pose_mappings` crate runs pose estimation, and sends POST requests with data to the server.
- `humanoid` crate contains the generic humanoid robot interface and related types.
- `zeroth` crate includes the RPC client for the Zeroth robot.
- `bot` contains the controller server implementation.

Use format 
- 'function or variable' explanation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- We are grateful for the contributions of Ben, Dennis, and many more for their frequent advice, without which we would not have solved certain issues. Thanks to [K-Scale](https://github.com/kscalelabs) and their staff for their graciousness!
