# BigBoy_Waiter

Real-time human pose mirroring for the Kbot. PoseBot captures human poses through a camera and replicates the movements on a physical robot.
K-BOT Hackathon code to move an arm

## Overview

PoseBot uses computer vision to detect and track human poses in real-time, then translates these movements into robot joint commands. This creates an interactive experience where the robot mirrors human movements as they happen.


## Features

- Real-time human pose detection using computer vision
- Smooth translation of human movements to robot joint positions
- Built with Rust for high performance and reliability
- Generic `humanoid` interface supports different robotics platforms

## Requirements 

- Rust (latest stable version)
- Python 3.11
- Raspberry Pi 5


## Installation

Clone the repository.

```bash
git clone https://github.com/raulgarreta/bigboy.git
cd bigboy
```

Create and activate a virtual environment.

```bash
python -m venv venv
source venv/bin/activate
```

Install all the requirements:

```bash
pip install -r requirements.txt
```

Make sure you change the `ROBOT_IP` in `bigboy.py` with the IP of the raspberry pi that is running the
kos server.

## Usage

1. Follow the instructions [here](https://sponge-sled-8df.notion.site/Setting-up-K-Bot-17f9bcb033d880509bcbfaff1db4fc33) to setup the kos server on the raspberry pi.
2. Run the kos server on the raspberry pi.
```bash
cargo run
```

3. Stand in front of the camera with a can or party cup.
4. Allow the robot to collect the glass/cup.

## Safety

- The robot has conservative angle movements to prevent clashing with itself or stumbling. You may have to override them when inside pykos library when testing. 
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

- We are grateful for the contributions of Ben, Dennis, JX and many more for their frequent advice, without which we would not have solved certain issues. Thanks to [K-Scale](https://github.com/kscalelabs) and their staff for their graciousness!
