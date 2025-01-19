import pygame
import sys
import pykos
import time

ROBOT_IP = "10.33.11.199"
ACTUATOR_STEP = 1
ACTUATOR_NAME_TO_ID = {
    "left_shoulder_updown": 21,
    "left_shoulder_lateral": 22,
    "left_elbow_yaw": 23,
    "left_elbow_updown": 24,
    "left_wrist_yaw": 25,
#     "right_shoulder_yaw": 21,
#     "right_shoulder_pitch": 22,
#     "right_elbow_yaw": 23,
#     "right_gripper": 24,
#     "left_hip_yaw": 31,
#     "left_hip_roll": 32,
#     "left_hip_pitch": 33,
#     "left_knee_pitch": 34,
#     "left_ankle_pitch": 35,
#     "right_hip_yaw": 41,
#     "right_hip_roll": 42,
#     "right_hip_pitch": 43,
#     "right_knee_pitch": 44,
#     "right_ankle_pitch": 45,
}
ACTUATOR_ID_TO_NAME = {v: k for k, v in ACTUATOR_NAME_TO_ID.items()}

joints = {

    "left_shoulder_updown": {
        "actuator_id": 21,
        "zero_position": 3.7244203090667725
    },

    "left_elbow_updown": {
        "actuator_id": 24,
        "zero_position": -3.6091001033782959
    },

    "left_shoulder_lateral": {
        "actuator_id": 22,
        "zero_position": -2.6038320064544678
    }

}

kos = pykos.KOS(ip=ROBOT_IP)
commands = []

def get_joint_position(actuator_name):
    pass


def init_joints():
    pass


def move_joint(actuator_name, direction, step=ACTUATOR_STEP):
    actuator_id = ACTUATOR_NAME_TO_ID[actuator_name]
    state = kos.actuator.get_actuators_state([actuator_id])
    print(state.states)
    current_position = state.states[0].position
    commands.append({'actuator_id' : actuator_id, 'position' : current_position + direction*step})

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Arrow Key Listener")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        # Quit the application
        if event.type == pygame.QUIT:
            running = False
        
        # Check for keydown events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                print("Up arrow pressed")
                move_joint("left_shoulder_updown", 1, 1)
                move_joint("left_elbow_updown", 1)


            elif event.key == pygame.K_DOWN:
                print("Down arrow pressed")
                move_joint("left_shoulder_updown", -1, 1)
                move_joint("left_elbow_updown", -1)

            elif event.key == pygame.K_LEFT:
                print("Left arrow pressed")
                move_joint("left_shoulder_lateral", 1)

            elif event.key == pygame.K_RIGHT:
                print("Right arrow pressed")
                move_joint("left_shoulder_lateral", -1)

            elif event.key == pygame.K_ESCAPE:
                # Optionally press Escape to exit
                running = False

            print("SENDING COMMANDS")
            all_ids = [c['actuator_id'] for c in commands]
            for id in all_ids:
                if id in [45, 35]:
                    kos.actuator.configure_actuator(actuator_id=id, kp=70, kd=3, torque_enabled=True, max_torque=60)
                else:
                    kos.actuator.configure_actuator(actuator_id=id, kp=300, kd=5, torque_enabled=True, max_torque=60)
            kos.actuator.command_actuators(commands)
            commands = []

    # Optionally fill the screen with a color
    screen.fill((30, 30, 30))

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()
sys.exit()
