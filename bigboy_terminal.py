import curses
import sys
import pykos
import time
import logging
import math

MIN_DELTA = 0.55

class Joint:
    def __init__(self, actuator_id, zero_position=0.0, offset=0.0, minus_delta=MIN_DELTA, plus_delta=MIN_DELTA):
        """
        Initialize a Joint with actuator ID and zero position.
        :param actuator_id: The ID of the actuator.
        :param zero_position: The zero position of the joint (default is 0.0).
        """
        self.actuator_id = actuator_id
        self.zero_position = zero_position
        self.position_setpoint = zero_position
        self.position = zero_position
        self.minus_delta = minus_delta
        self.plus_delta = plus_delta
        self.offset = offset
        # self.velocity = 0.0
        # self.torque = 0.0

    def __repr__(self):
        return f"Joint(actuator_id={self.actuator_id}, position={self.position:0.4f})"

    def set_target(self, setpoint):
        self.position_setpoint = setpoint + self.offset

    def set_zero(self):
        self.position_setpoint = self.zero_position

    def step(self):
        err = self.position_setpoint - self.position
        print(f"id: {self.actuator_id}, err: {err}")
        # if math.fabs(err) < MIN_DELTA:
        #     return []

        if (math.fabs(err) < 0.001):
            return []
        dir = err / math.fabs(err)

        if (dir > 0.0):
            if math.fabs(err) < self.plus_delta:
                return []
            cmd = self.position + self.plus_delta
        else:
            if math.fabs(err) < self.minus_delta:
                return []
            cmd = self.position - self.minus_delta

        # cmd = self.position + dir * MIN_DELTA
        print(f"pos: {self.position}, cmd: {cmd}")
        return [{
            'actuator_id'   : self.actuator_id,
            'position'      : cmd,
        }]



JOINT_ARRAY = [
    Joint(actuator_id=0, zero_position=0.0),
    Joint(actuator_id=1, zero_position=0.0),
    Joint(actuator_id=2, zero_position=0.0),
    Joint(actuator_id=3, zero_position=0.0),
    Joint(actuator_id=4, zero_position=0.0),
    Joint(actuator_id=5, zero_position=0.0),
    Joint(actuator_id=6, zero_position=0.0),
    Joint(actuator_id=7, zero_position=0.0),
    Joint(actuator_id=8, zero_position=0.0),
    Joint(actuator_id=9, zero_position=0.0),
    Joint(actuator_id=10, zero_position=0.0),
    Joint(actuator_id=11, zero_position=0.0, minus_delta=0.01, plus_delta=1),
    # Joint(actuator_id=11, zero_position=0.0),
    Joint(actuator_id=12, zero_position=0.0),
    Joint(actuator_id=13, zero_position=0.0),
    Joint(actuator_id=14, zero_position=0.563, minus_delta=0.01, plus_delta=1),
    Joint(actuator_id=15, zero_position=0.0, offset=3),
    Joint(actuator_id=16, zero_position=0.0, minus_delta=2, plus_delta=2),
    Joint(actuator_id=17, zero_position=0.0),
    Joint(actuator_id=18, zero_position=0.0),
    Joint(actuator_id=19, zero_position=0.0),
    Joint(actuator_id=20, zero_position=0.0),
    Joint(actuator_id=21, zero_position=0.0),
    Joint(actuator_id=22, zero_position=-2.6038),
    Joint(actuator_id=23, zero_position=0.0),
    Joint(actuator_id=24, zero_position=-3.6091, minus_delta=0.2, plus_delta=1),
    Joint(actuator_id=25, zero_position=0.0),
    Joint(actuator_id=26, zero_position=0.0),
    Joint(actuator_id=27, zero_position=0.0),
    Joint(actuator_id=28, zero_position=0.0),
    Joint(actuator_id=29, zero_position=0.0),
    Joint(actuator_id=30, zero_position=0.0),
    Joint(actuator_id=31, zero_position=0.0),
    Joint(actuator_id=32, zero_position=0.0),
    Joint(actuator_id=33, zero_position=0.0),
    Joint(actuator_id=34, zero_position=0.0),
    Joint(actuator_id=35, zero_position=0.0),
    Joint(actuator_id=36, zero_position=0.0),
    Joint(actuator_id=37, zero_position=0.0),
    Joint(actuator_id=38, zero_position=0.0),
    Joint(actuator_id=39, zero_position=0.0),
    Joint(actuator_id=40, zero_position=0.0),
    Joint(actuator_id=41, zero_position=0.0),
    Joint(actuator_id=42, zero_position=0.0),
    Joint(actuator_id=43, zero_position=0.0),
    Joint(actuator_id=44, zero_position=0.0),
    Joint(actuator_id=45, zero_position=0.0),
    Joint(actuator_id=46, zero_position=0.0),
    Joint(actuator_id=47, zero_position=0.0),
    Joint(actuator_id=48, zero_position=0.0),
    Joint(actuator_id=49, zero_position=0.0),
]




class KBot:
    ALL_VALID_IDS = [
        *range(11, 17), # TODO: make it work with (11, 17)
        *range(21, 26), # TODO: make it work with (21, 27)
        # *range(31, 36),
        # *range(41, 46),
    ]

    RightShoulderPitchId = 21
    RightShoulderRollId  = 22
    RightShoulderYawId   = 23
    RightElbowPitchId    = 24
    RightHandYawId       = 25
    RightHandGripId      = 26

    LeftShoulderPitchId = 11
    LeftShoulderRollId  = 12
    LeftShoulderYawId   = 13
    LeftElbowPitchId    = 14
    LeftHandYawId       = 15
    LeftHandGripId      = 16

    @staticmethod
    def stop():
        for id in KBot.ALL_VALID_IDS:
            kos.actuator.configure_actuator(
                actuator_id=id,
                kp=32,
                kd=1,
                torque_enabled=False,
                zero_position=True,
            )

    def engage():
        for id in KBot.ALL_VALID_IDS:
            kos.actuator.configure_actuator(
                actuator_id=id,
                kp=32,
                kd=1,
                torque_enabled=True,
                # zero_position=True,
            )

    @staticmethod
    def update():
        states = kos.actuator.get_actuators_state(KBot.ALL_VALID_IDS)
        for state in states.states:
            JOINT_ARRAY[state.actuator_id].position = state.position
            print(JOINT_ARRAY[state.actuator_id])

    @staticmethod
    def set_zero():
        for id in KBot.ALL_VALID_IDS:
            JOINT_ARRAY[id].set_zero()

    @staticmethod
    def set_target(id, setpoint):
        # JOINT_ARRAY[KBot.RightShoulderPitchId].set_target(setpoint)
        JOINT_ARRAY[id].set_target(setpoint)
        # ret = JOINT_ARRAY[KBot.RightShoulderPitchId].step()
        # return ret

    @staticmethod
    def step():
        ret = []
        for id in KBot.ALL_VALID_IDS:
            ret = ret + JOINT_ARRAY[id].step()
        # ret = ret + JOINT_ARRAY[KBot.RightShoulderPitchId].step()
        # ret = ret + JOINT_ARRAY[KBot.RightElbowPitchId].step()
        # ret = ret + JOINT_ARRAY[KBot.RightHandYawId].step()
        # ret = ret + JOINT_ARRAY[KBot.RightHandYawId].step()

        # ret = ret + JOINT_ARRAY[KBot.LeftShoulderPitchId].step()
        # ret = ret + JOINT_ARRAY[KBot.LeftElbowPitchId].step()
        # ret = ret + JOINT_ARRAY[KBot.LeftHandYawId].step()
        return ret

    @staticmethod
    def send_commands(commands):
        logging.info("Sending commands to actuators")
        all_ids = [c['actuator_id'] for c in commands]
        for actuator_id in all_ids:
            if actuator_id in [45, 35]:
                kos.actuator.configure_actuator(
                    actuator_id=actuator_id, kp=70, kd=3, torque_enabled=True, max_torque=60
                )
            else:
                kos.actuator.configure_actuator(
                    actuator_id=actuator_id, kp=300, kd=5, torque_enabled=True, max_torque=60
                )
        kos.actuator.command_actuators(commands)
        # commands.clear()

        


    # @staticmethod

    #     RightShoulderPitch = Joint(actuator_id=21, 3.7244)
    #     RightShoulderRoll = Joint(actuator_id=22, -2.6038)
    #     RightShoulderYaw = Joint(actuator_id=23)
    #     RightElbowPitch = Joint(actuator_id=24, -3.6091)
    #     RightHandYaw = Joint(actuator_id=25)
    #     RightHandGrip = Joint(actuator_id=26)


        







# RightShoulderPitch = Joint(actuator_id=21, 3.7244)
# RightShoulderRoll = Joint(actuator_id=22, -2.6038)
# RightShoulderYaw = Joint(actuator_id=23)
# RightElbowPitch = Joint(actuator_id=24, -3.6091)
# RightHandYaw = Joint(actuator_id=25)
# RightHandGrip = Joint(actuator_id=26)


# Configure logging
logging.basicConfig(
    filename="robot_control.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)
# ROBOT_IP = "10.33.11.199"
ROBOT_IP = "172.20.10.6"
kos = pykos.KOS(ip=ROBOT_IP)

    

ACTUATOR_STEP = 1
ACTUATOR_NAME_TO_ID = {
    "left_shoulder_updown": 21,
    "left_shoulder_lateral": 22,
    "left_elbow_yaw": 23,
    "left_elbow_updown": 24,
    "left_wrist_yaw": 25,
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

commands = []

def move_joint(actuator_name, direction, step=ACTUATOR_STEP):
    actuator_id = ACTUATOR_NAME_TO_ID[actuator_name]
    state = kos.actuator.get_actuators_state([actuator_id])
    current_position = state.states[0].position
    new_position = current_position + direction * step
    commands.append({'actuator_id': actuator_id, 'position': new_position})
    logging.info(f"Moved {actuator_name} to position {new_position}")

def send_commands():
    logging.info("Sending commands to actuators")
    all_ids = [c['actuator_id'] for c in commands]
    for actuator_id in all_ids:
        if actuator_id in [45, 35]:
            kos.actuator.configure_actuator(
                actuator_id=actuator_id, kp=70, kd=3, torque_enabled=True, max_torque=60
            )
        else:
            kos.actuator.configure_actuator(
                actuator_id=actuator_id, kp=300, kd=5, torque_enabled=True, max_torque=60
            )
    kos.actuator.command_actuators(commands)
    commands.clear()

def main(stdscr):
    # Configure curses
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)  # Non-blocking input
    stdscr.clear()
    stdscr.addstr(0, 0, "Control the robot using arrow keys:")
    stdscr.addstr(1, 0, "  ↑: Move left_shoulder_updown and left_elbow_updown up")
    stdscr.addstr(2, 0, "  ↓: Move left_shoulder_updown and left_elbow_updown down")
    stdscr.addstr(3, 0, "  ←: Move left_shoulder_lateral up")
    stdscr.addstr(4, 0, "  →: Move left_shoulder_lateral down")
    stdscr.addstr(5, 0, "Press 'q' to quit.")

    while True:
        key = stdscr.getch()  # Get key press
        if key == curses.KEY_UP:
            logging.info("Up arrow pressed")
            move_joint("left_shoulder_updown", 1, 1)
            move_joint("left_elbow_updown", 1)
            send_commands()

        elif key == curses.KEY_DOWN:
            logging.info("Down arrow pressed")
            move_joint("left_shoulder_updown", -1, 1)
            move_joint("left_elbow_updown", -1)
            send_commands()

        elif key == curses.KEY_LEFT:
            logging.info("Right arrow pressed")
            move_joint("left_shoulder_lateral", 1)
            send_commands()

        elif key == curses.KEY_RIGHT:
            logging.info("Right arrow pressed")
            move_joint("left_shoulder_lateral", -1)
            send_commands()

        elif key == ord('q'):  # Quit on 'q'
            logging.info("Exiting program")
            break

        stdscr.refresh()
        time.sleep(0.1)

# Run the curses application
# curses.wrapper(main)

GRIP_OPEN=120
GRIP_CLOSE=100
# KBot.stop()
# time.sleep(1)
# KBot.stop()
# time.sleep(1)
# KBot.engage()
# time.sleep(0.5)
# KBot.set_target(5)
KBot.update()
# # theta1_rad = JOINT_ARRAY[KBot.RightElbowPitchId].position * math.pi / 180;
# # 
# # R_mm = 30 * 10
# # d_mm = -10 * 10
# # 
# # i_rad = -theta1_rad + math.acos(math.cos(theta1_rad) - d_mm / R_mm)
# # print(i_rad)
# # 
# # t_shoulder = JOINT_ARRAY[KBot.RightShoulderPitchId].position
# # t_shoulder = t_shoulder + i_rad * 180 / math.pi
# # t_elbow = (theta1_rad - i_rad) * 180 / math.pi
# 
# # print(t_shoulder)
# # print(t_elbow)
# # KBot.set_target(KBot.RightShoulderPitchId, 0 + 20.76)
# # KBot.set_target(KBot.RightElbowPitchId, 90 + 25.76)
# KBot.set_target(KBot.RightShoulderPitchId, 0)
# KBot.set_target(KBot.RightElbowPitchId, 90)
# KBot.set_target(KBot.RightHandYawId, 0)
# KBot.set_zero()
# 
# KBot.set_target(KBot.LeftShoulderYawId, 0)
# KBot.set_target(KBot.LeftShoulderPitchId, 0 - 30)
# KBot.set_target(KBot.LeftElbowPitchId, 90 + 30)
# KBot.set_target(KBot.LeftShoulderPitchId, -30)
# KBot.set_target(KBot.LeftElbowPitchId, 90 + 30)

KBot.set_target(KBot.LeftShoulderPitchId, 0)
KBot.set_target(KBot.LeftElbowPitchId, 90 + 0)
KBot.set_target(KBot.LeftHandYawId, 90)
KBot.set_target(KBot.LeftHandGripId, 95)

for _ in range(500):
    KBot.update()
    cmds = KBot.step()
    print(cmds)
    KBot.send_commands(cmds)
    time.sleep(0.05)
