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

jointsNames = ["jointX","jointY","jointZ"]
grapper:Motor
grapper = robot.getDevice("finger motor::left")
grapper.setPosition(0)
joints = [robot.getDevice(name) for name in jointsNames if robot.getDevice(name) is not None]


def getKeys(keyboard:Keyboard):
    keys = []
    for _ in range(4):
      key = keyboard.getKey()
      if key > 0: keys.append(chr(key))
    return keys

chain = Chain(name = 'chain', active_links_mask=[False,True,True,True,True], links = [
OriginLink(),
    URDFLink(
      name="Z-axis",
      origin_translation=[0, 0, 1.375],
      origin_orientation=[1.57,0,1.57],
      translation=[0, 0, 1],
      joint_type="prismatic"
    ),
    URDFLink(
      name="Y-axis",
      origin_translation=[0, 0, 0.125],
      origin_orientation=[1.57, 0, 1.57],#[0, 1.57, 1.57],
      translation=[0, 0, 1],
      joint_type="prismatic"
    ),
    URDFLink(
      name="X-axis",
      origin_translation=[0, 0, 0.125],
      origin_orientation=[1.57, 0,3*1.57],
      translation=[0, 0, 1],
      joint_type="prismatic"
    ),
    URDFLink(
      name="Tool",
      origin_translation=[0, 0, 0.175],
      origin_orientation=[0, 0, 0],
      translation=[0, 0, 0],
      joint_type="prismatic"
    )
])

TTT_translation = robot.getFromDef("TTT_pointer").getField("translation")
base_pos = robot.getFromDef("TTT").getField("translation").getSFVec3f()
target = [0.5,0.5,0.5]

start = chain.inverse_kinematics(target_position=target)

for i,joint in enumerate(joints): 
   joint.setPosition(start[i+1])
   joint.setVelocity(1)

base_pos[0] += 0.125
base_pos[1] -= 0.125
base_pos[2] -= 1.4

grapperPos = 0

TTT_translation.setSFVec3f([base_pos[0]+target[0],base_pos[1]-target[1],base_pos[2]+target[2]])


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

      TTTpointer_position = base_pos.copy()
      TTTpointer_position[0] += target[0]
      TTTpointer_position[1] -= target[1]
      TTTpointer_position[2] += target[2]
      TTT_translation.setSFVec3f(TTTpointer_position)    

      print("TARGET: ", target)
      start_pos = [joint.getTargetPosition() for joint in joints]
      start_pos.insert(0,0)
      start_pos.append(0)
      
      newJointsPositions = chain.inverse_kinematics(target_position=target)
      print(f"NEW JOINT POSITIONS : {newJointsPositions}")
      print(f"NEW CALCULATED POSITION: {chain.forward_kinematics(newJointsPositions)[:3, 3]}\n")
      for joint,newjointPosition in zip(joints,newJointsPositions[1:4]):
         joint.setPosition(newjointPosition)
      