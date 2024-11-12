"""ikpy controller."""
# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
import ikpy
from ikpy.chain import Chain
from ikpy.link import OriginLink,URDFLink
import numpy as np

# get the time step of the current world.
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
      origin_translation=[0, 0, 0.12],
      origin_orientation=[0, 0, 0],
      translation=[0, 0, 0],
      joint_type="prismatic"
    )
])

ik = chain.inverse_kinematics(target_position=[0, 0, 0])
print(f"XD1{ik}")
ik = chain.inverse_kinematics(target_position=[1.375, 0.125, 0.125])
print(f"XD2{ik}")
target_position = [0, 0, 0]
ik = chain.forward_kinematics(chain.inverse_kinematics(target_position=target_position))
print(f"XD3{ik}")
target_position= [1.375, 0.125, 0.125]
ik = chain.forward_kinematics(chain.inverse_kinematics(target_position=target_position))
print(f"XD4{ik}")


import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D
ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')

#chain.plot(chain.inverse_kinematics(chain.forward_kinematics([0,0,0,0,0,0])[:3, 3]), ax)
chain.plot(chain.inverse_kinematics([0.5,0.5,0.5]), ax)
matplotlib.pyplot.show()
