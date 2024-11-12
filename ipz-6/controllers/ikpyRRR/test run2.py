"""ikpy controller."""
# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from ikpy.chain import Chain
from ikpy.link import OriginLink,URDFLink
import numpy as np

# get the time step of the current world. active_links_mask=[False,True,True,True,True,True]
chain = Chain(name = 'chain', links = [
  OriginLink(),
      URDFLink(
        name="base",
        origin_translation=[0, 0, 0],
        origin_orientation=[0,0,0],
        rotation=[0, 0, 1],
      ),
      URDFLink(
      name="J1",
      origin_translation=[0, 0.1, 1],
      origin_orientation=[1.57, 0, 2*1.57],#[0, 1.57, 1.57],
      rotation=[0, 0, 1],
    ),
      URDFLink(
        name="J2",
        origin_translation=[0, 1, -0.1],
        origin_orientation=[0, 0,3*1.57],
        rotation=[0, 0, 1],
      ),
      URDFLink(
        name="J3",
        origin_translation=[-0.5, 0, 0],
        origin_orientation=[1.57, 0,3*1.57],
        rotation=[0, 0, 1],
      ),
      URDFLink(
        name="Tool",
        origin_translation=[0, 0, 0.25],
        origin_orientation=[0, 0, 0],
        rotation=[0, 0, 0],
      )
      ])

ik = chain.inverse_kinematics(target_position=[0, 0, 0])
print(f"1{ik}")
ik = chain.inverse_kinematics(target_position=[1.375, 0.125, 0.125])
print(f"2{ik}")
target_position = [0, 0, 0]
ik = chain.forward_kinematics(chain.inverse_kinematics(target_position=target_position))
print(f"3{ik}")
target_position= [1.375, 0.125, 0.125]
ik = chain.forward_kinematics(chain.inverse_kinematics(target_position=target_position))
print(f"4{ik}")


import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D
ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')
targerVec = [0 for _ in chain.links]
#chain.plot(chain.inverse_kinematics(chain.forward_kinematics(targerVec)[:3, 3]), ax)
chain.plot(chain.inverse_kinematics([0.7,0.7,0.7]), ax)
matplotlib.pyplot.show()
