# RelaxationTest
# Created to test the relaxation method and various features of NumPy
# made by Masen Pitts
# Updated 11/21/2021

import numpy as np
import matplotlib.pyplot as plt

meshResolution = 20 # Gives the number of mesh points extending in each direction;
              # each spatial axis has points defined on [0, meshResolution]
              # (unless it is indicated otherwise)

#**Unless otherwise specified the value of the potential at the boudaries of the region
# will be 0 for each case** 

# Rectangular Metal Pipe
# Compare to: Infinitely Long Rectangular Metal Pipe (Griffiths Chapter 3, Example 5)
#******************************************************************************
xFactor = 5 # Determines the length of the pipe in the x direction as a multiple
            # of the width of the pipe
            
# Variables that determine the rectangular bounds of the region
# in Cartesian Coordinates
ySize = 10
zSize = ySize
xSize = xFactor*ySize

# Variables stored for convience for initializing the arrays and performing
# iterative calculations on the mesh points
yMesh = meshResolution + 1
zMesh = yMesh
xMesh = xFactor*meshResolution + 1

# Variable that stores the actual space between each of the mesh points
interval = ySize/meshResolution


#work on: look at endpoints a bit more
#         add variables: xMesh, yMesh, zMesh, xSize, ySize, zSize
#         implement relaxation method: make it work for arbitrary charge distribution

# Initializes a 3D NumPy array with a shape determined by the x/y/zMesh variables;
# Used to store calculated values of the electrostatic potential at each mesh point
potential = np.full((xMesh, yMesh, zMesh), 0, dtype=np.float64)

# Sets the values of the potential on the x = 0 face of the pipe
for y in range(yMesh):
    for z in range(zMesh):
        potential[0, y, z] = y*interval*z*interval
       
# print statements testing the values of array attributes and array entries
print(potential[0])

print(potential.ndim)
print(potential.size)
print(potential.shape)