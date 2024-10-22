from controller import Motor
from keyboardFunctions import getKeys
VELOCITYINC = 0.1
TURNINC = 0.05
def turn_left(hinge_motors:list[Motor]):
    for motor in hinge_motors:
        position = motor.getPositionSensor().getValue()
        motor.setPosition(position+TURNINC)

def turn_right(hinge_motors:list[Motor]):
    for motor in hinge_motors:
        position = motor.getPositionSensor().getValue()
        motor.setPosition(position-TURNINC)

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

def go_straight(hingeMotors:list[Motor]):
    for motor in hingeMotors:
        motor.setPosition(0)

def steer_robot(keyboard, motors_left:list[Motor],motors_right:list[Motor],
                hinge_motors:list[Motor]):
    keys = getKeys(keyboard)
    for key in keys:
        if key == "A":
            turn_left(hinge_motors)
        if key == "D":
            turn_right(hinge_motors)
        if key == "S":
            decelerate(motors_left,motors_right)
        if key == "W":
            accelerate(motors_left,motors_right)
        if key =="Q":
            go_straight(hinge_motors)
        if key == "R":
            stop(motors_left,motors_right)
