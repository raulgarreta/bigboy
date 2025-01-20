import pygame
import sys
import pykos
import time
import json



ROBOT_IP = "10.33.11.199"
ROBOT_IP = "172.20.10.6"

ACTUATOR_STEP = 1
ACTUATOR_NAME_TO_ID = {
    "left_shoulder_updown": 21,
    "left_shoulder_lateral": 22,
    "left_elbow_yaw": 23,
    "left_elbow_updown": 24,
    "left_wrist_yaw": 25,

    "right_shoulder_updown": 11,
    "right_shoulder_lateral":12,
    "right_elbow_yaw": 13,
    "right_elbow_updown": 14,
    "right_wrist_yaw": 15,


#     "right_gripper": 24,
#     "left_hip_yaw": 31,
#     "left_hip_roll": 32,
#     "left_hip_pitch": 33,
    #  "left_knee_pitch": 34,
    #  "left_ankle_pitch": 35,
#     "right_hip_yaw": 41,
#     "right_hip_roll": 42,
#     "right_hip_pitch": 43,
    #  "right_knee_pitch": 44,
    #  "right_ankle_pitch": 45,
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
    },

    "right_shoulder_lateral": {
        "actuator_id": 13,
        "zero_position": 1.8402098417282104

    },

    "right_shoulder_updown": {
        "actuator_id": 12,
        "zero_position": 0.098901137709617615
    },

    "left_knee_pitch": {
        "actuator_id": 34,
        "zero_position": -0.098901137709617615
    }

}

kos = pykos.KOS(ip=ROBOT_IP)
commands = []

def get_joint_position(actuator_name):
    pass


def init_joints():
    pass




def turn_off_torques():
    # turn off torque for all actuators
    for actuator_name in ACTUATOR_NAME_TO_ID.keys():
        actuator_id = ACTUATOR_NAME_TO_ID[actuator_name]
        kos.actuator.configure_actuator(actuator_id=actuator_id, torque_enabled=False)
        print(f"Turning off torque for {actuator_name}")

def turn_on_torques():
    # turn on torque for all actuators
    for actuator_name in ACTUATOR_NAME_TO_ID.keys():
        actuator_id = ACTUATOR_NAME_TO_ID[actuator_name]
        kos.actuator.configure_actuator(actuator_id=actuator_id, torque_enabled=True)
        print(f"Turning on torque for {actuator_name}")

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


position_recording = False
position_playing = False
RECORDING_FREQUENCY_HZ = 40
recording_joints = ["right_shoulder_updown"]

recorded_positions = {}
playing_index = 0


def interpolate_joint_position(actuator_id, start_position, end_position):

    steps = abs(end_position-start_position) / 2

    commands_int = []
    for i in range(steps):
        commands_int.append({'actuator_id': actuator_id, 'position': start_position + (end_position - start_position) * i / steps})
    return commands_int


def play_positions():
    global playing_index
    global position_playing

    state = kos.actuator.get_actuators_state([ACTUATOR_NAME_TO_ID[name] for name in recording_joints])
    state_positions = {s.actuator_id: s.position for s in state.states}


    for joint_name in recording_joints:
        actuator_id = ACTUATOR_NAME_TO_ID[joint_name]
        if playing_index < len(recorded_positions[joint_name]):

            if abs(state_positions[actuator_id] - recorded_positions[joint_name][playing_index]) > 2.0:
                commands.extend(interpolate_joint_position(actuator_id, state_positions[actuator_id], recorded_positions[joint_name][playing_index]))
            else:
                commands.append({'actuator_id': actuator_id, 'position': recorded_positions[joint_name][playing_index]})
        else:
            print("End of recording")
            position_playing = False
            return
        print(f"Playing position {recorded_positions[joint_name][playing_index]} for {joint_name}")
    playing_index += 1

def init_recording():
    recorded_positions = {}
    for joint_name in recording_joints:
        recorded_positions[joint_name] = []
    return recorded_positions


def init_playing():
    global playing_index
    playing_index = 0
    with open("recorded_positions.json", "r") as f:
        recorded_positions = json.load(f)
    return recorded_positions


def record_positions():
    state = kos.actuator.get_actuators_state([ACTUATOR_NAME_TO_ID[name] for name in recording_joints])
    print(state.states)
    for s in state.states:
        recorded_positions[ACTUATOR_ID_TO_NAME[s.actuator_id]].append(s.position)


def store_recorded_positions():
    # store the recorded positions in a json file
    with open("recorded_positions.json", "w") as f:
        json.dump(recorded_positions, f)



# Main loop
running = True
while running:

    if position_recording:
        record_positions()
        # sleep for the configured frequency
        time.sleep(1 / RECORDING_FREQUENCY_HZ)
    elif position_playing:
        play_positions()
        kos.actuator.command_actuators(commands)
        # sleep for the configured frequency
        time.sleep(1 / RECORDING_FREQUENCY_HZ)
        
    for event in pygame.event.get():
        # Quit the application
        if event.type == pygame.QUIT:
            running = False
        
        # Check for keydown events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                print("Up arrow pressed")
                move_joint("right_shoulder_updown", 1, 1)
                #move_joint("left_elbow_updown", 1)
                # move_joint("right_shoulder_updown", 1, 1)
                # move_joint("right_elbow_updown", 1)
                # move_joint("left_knee_pitch", 1)
                # move_joint("right_knee_pitch", -1)

            elif event.key == pygame.K_DOWN:
                print("Down arrow pressed")
                move_joint("right_shoulder_updown", -1, 1)
                # move_joint("left_elbow_updown", -1)
                # move_joint("right_shoulder_updown", -1, 1)
                # move_joint("right_elbow_updown", -1)
                # move_joint("left_knee_pitch", -1)
                # move_joint("right_knee_pitch", 1)

            elif event.key == pygame.K_LEFT:
                print("Left arrow pressed")
                move_joint("left_shoulder_lateral", 1)
                move_joint("right_shoulder_lateral", 1)
            elif event.key == pygame.K_RIGHT:
                print("Right arrow pressed")
                move_joint("left_shoulder_lateral", -1)
                move_joint("right_shoulder_lateral", -1)
            elif event.key == pygame.K_ESCAPE:
                # Optionally press Escape to exit
                running = False

            elif event.key == pygame.K_l:
                turn_off_torques()

            elif event.key == pygame.K_o:
                turn_on_torques()

            elif event.key == pygame.K_r:
                position_recording = not position_recording
                if position_recording:
                    print("RECORDING POSITIONS")
                    turn_off_torques()
                    recorded_positions = init_recording()
                    print(recorded_positions)
                else:
                    print("STOPPED RECORDING POSITIONS")
                    store_recorded_positions()

            elif event.key == pygame.K_p:

                position_playing = not position_playing
                if position_playing:
                    print("PLAYING POSITIONS")
                    turn_on_torques()
                    recorded_positions = init_playing()
                    print("positions to play:", recorded_positions)
                    
                else:
                    print("STOPPED PLAYING POSITIONS")
                    


            print("SENDING COMMANDS")
            if commands:
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
