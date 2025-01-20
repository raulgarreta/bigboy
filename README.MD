# BigBoy

Arm movement to hold a beer for K-bot, using [K-Scale OS](https://github.com/kscalelabs/kos/).

## Overview

**Goal:** 
Use the K-Bot to hold my beer

**Software Implementation:**
- Simple controller: Set actuation goal, slowly inch towards it
- Keep the forearm level at all times (Math!)
- KBot class for communication and collecting commands for all actuators
- Send commands using K-ROS and pykos

**Hardware Components:**
- K-Bot robot
- Raspberry Pi


## Features

- kOS server running on Raspberry Pi
- Python client code using kOS SDK.
- Arm movement to hold a beer, controls the left arm joints and gripper.
- Moving the robot arm and other joints using keyboard.
- Recording / Re-playing of skills.


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
