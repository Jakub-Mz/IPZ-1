from controller import Motor
from keyboardFunctions import getKeys
VELOCITYINC = 0.1
TURNVELOCITY = 0.05
def turn_left(motors_left:list[Motor],motors_right:list[Motor]):
    # for motor in motors_left:
    #    motor.setVelocity(-TURNVELOCITY)

    # for motor in motors_right:
    #     motor.setVelocity(TURNVELOCITY)
    for motor in motors_left:
        _modify_velocity(motor, -TURNVELOCITY)
    for motor in motors_right:
        _modify_velocity(motor, TURNVELOCITY)

def turn_right(motors_left:list[Motor],motors_right:list[Motor]):
    # for motor in motors_left:
    #    motor.setVelocity(TURNVELOCITY)

    # for motor in motors_right:
    #     motor.setVelocity(-TURNVELOCITY)
    for motor in motors_left:
        _modify_velocity(motor, TURNVELOCITY)
    for motor in motors_right:
        _modify_velocity(motor, -TURNVELOCITY)

def accelerate(motors_left:list[Motor],motors_right:list[Motor]):
    for motor in motors_left:
        _modify_velocity(motor, VELOCITYINC)
    for motor in motors_right:
        _modify_velocity(motor, VELOCITYINC)

def decelerate(motors_left:list[Motor],motors_right:list[Motor]):
    for motor in motors_left:
        _modify_velocity(motor, -VELOCITYINC)
    for motor in motors_right:
        _modify_velocity(motor, -VELOCITYINC)


def stop(motors_left:list[Motor],motors_right:list[Motor]):
    for motor in motors_left:
        motor.setVelocity(0)
    for motor in motors_right:
        motor.setVelocity(0)

def _modify_velocity(motor:Motor,modify_value:float):
    max_velocity = motor.getMaxVelocity()
    current_velocity = motor.getVelocity()
    new_velocity = current_velocity + modify_value
    if new_velocity <= max_velocity and new_velocity >= -max_velocity:
        print("SETTINGVELOCITY", new_velocity)
        motor.setVelocity(new_velocity)

def steer_robot(keyboard, motors_left:list[Motor],motors_right:list[Motor]):
    keys = getKeys(keyboard)
    for key in keys:
        if key == "A":
            turn_left(motors_left,motors_right)
        if key == "D":
            turn_right(motors_left,motors_right)
        if key == "S":
            decelerate(motors_left,motors_right)
        if key == "W":
            accelerate(motors_left,motors_right)
        if key == "R":
            stop(motors_left,motors_right)
