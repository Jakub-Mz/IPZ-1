"""ikpy controller."""
# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Supervisor,Motor,Keyboard

from ikpy.chain import Chain
from ikpy.link import OriginLink,URDFLink

joints:list[Motor]

robot = Supervisor()
keyboard = robot.getKeyboard()
timestep = int(robot.getBasicTimeStep())
keyboard.enable(timestep)

# get the time step of the current world.

jointsNames = ["base","J1","J2","J3"]
grapper:Motor
grapper = robot.getDevice("finger motor::left")
grapper.setPosition(0)

def getKeys(keyboard:Keyboard):
    keys = []
    for _ in range(4):
      key = keyboard.getKey()
      if key > 0: keys.append(chr(key))
    return keys

chain = Chain(name = 'chain', active_links_mask=[False,True,True,True,True,True], links = [
OriginLink(),
    URDFLink(
      name="base",
      origin_translation=[0, 0, 0],
      origin_orientation=[0,0,0],
      rotation=[0, 0, 1]
    ),
    URDFLink(
      name="J1",
      origin_translation=[0, 0.2, 1],
      origin_orientation=[1.57, 0, 2*1.57],#[0, 1.57, 1.57],
      rotation=[0, 0, 1],
    ),
    URDFLink(
      name="J2",
      origin_translation=[0, 0.75, -0.2],
      origin_orientation=[0, 0,3*1.57],
      rotation=[0, 0, 1],
    ),
    URDFLink(
      name="J3",
      origin_translation=[-0.75, 0, 0],
      origin_orientation=[1.57, 0,3*1.57],
      rotation=[0, 0, 1],
    ),
    URDFLink(
      name="Tool",
      origin_translation=[0, 0, 0.17],
      origin_orientation=[0, 0, 0],
      rotation=[0, 0, 0],
    )
])
target = [2,0.2,0.2]
start = chain.inverse_kinematics(target_position=target)
joints = [robot.getDevice(name) for name in jointsNames if robot.getDevice(name) is not None]
for i,joint in enumerate(joints): 
   joint.setPosition(start[i+1])
   joint.setVelocity(1)

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:

# Main loop:
# - perform simulation steps until Webots is stopping the controller
RRR_translation = robot.getFromDef("RRR_pointer").getField("translation")
base_pos = robot.getFromDef("RRR").getField("translation").getSFVec3f()

base_pos[0] += 0
base_pos[1] -= 0
base_pos[2] -= 0.5

RRR_translation.setSFVec3f([base_pos[0]+target[0],base_pos[1]-target[1],base_pos[2]+target[2]])
grapperPos = 0

while robot.step(timestep) != -1: 
    keys = getKeys(keyboard)   
    if len(keys)>0:
      for key in keys:
          if key == 'A':
            target[0] -= 0.01
          if key == 'D':
            target[0] += 0.01
          if key == 'W':
            target[1] -= 0.01
          if key == 'S':
            target[1] += 0.01
          if key == 'F':
            target[2] -= 0.01
          if key == 'G':
            target[2] += 0.01
          if key == 'E':
            grapperPos -= 0.005
            grapperPos = max(grapperPos,0)
            grapperPos = min(grapperPos,0.1)
            grapper.setPosition(grapperPos)
          if key == 'R':
            grapperPos += 0.005
            grapperPos = max(grapperPos,0)
            grapperPos = min(grapperPos,0.1)
      grapper.setPosition(grapperPos) 

      RRRpointer_position = base_pos.copy()
      RRRpointer_position[0] += target[0]
      RRRpointer_position[1] -= target[1]
      RRRpointer_position[2] += target[2]
      RRR_translation.setSFVec3f(RRRpointer_position)      
      print("TARGET: ", target)

      start_pos = [joint.getTargetPosition() for joint in joints]
      start_pos.insert(0,0)
      start_pos.append(0)
      newJointsPositions = chain.inverse_kinematics(target_position=[target[1],target[0],target[2]])
     
      #newJointsPositions = chain.inverse_kinematics(target_position=target)
      print(f"RRR NEW JOINT POSITIONS: {newJointsPositions}")
      print(f"RRR NEW CALCULATED POSITION: {chain.forward_kinematics(newJointsPositions)[:3, 3]}\n")
      #print(newJointsPositions)
      for joint,newjointPosition in zip(joints,newJointsPositions[1:5]):
         joint.setPosition(newjointPosition)
      