# K-BOT Hackathon code to detect objects 
The code uses the camera that is attached on the gripper to detect objects. Since we need to pick up objects with the gripper, we need to first make sure that we are aligned perpendicularly with the object. This code current detects the angle of the object which when subtracted with 90 degree will give the angle the robot needs to rotate with.

## Requirements
You will need python 3.11 to run this code (last version of kos needs that).

## Installation

Create a virtual environment.

Install all the requirements:

```bash
pip install -r requirements.txt
```

Make sure to update which camera you are using when running the code. 

## Usage

```bash
python main.py
```
