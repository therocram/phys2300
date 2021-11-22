# RelaxationTest
# Created to test the relaxation method and various features of NumPy
# made by Masen Pitts
# Updated 11/22/2021

import numpy as np
import matplotlib.pyplot as plt

# Addressing Possible Ambiguities in Comments:
# - "Boundary of the region" refers to the actual ends of the 3D mesh grid
# and not the points within the region that are given pre-determined values.
# - "Not Free Points" refers to points both on the boundary and within the boundary
# at which the value of the potential is not calculated.


meshResolution = 20 # Gives the number of mesh points extending in each direction;
                    # each spatial axis has points defined on [0, meshResolution]
                    # (unless it is indicated otherwise)
 
# Function that sets the potential value of the mesh points on the boundary of the region and marks them
# as not free
#**NOTE: This function expects potential and freePoints to be the same shape!**
def setBoundaries(potential, freePoints, boundaryValue):
    # Prints an error message and ends the program if the arrays passed to the function are not the same shape
    if potential.shape != freePoints.shape:
        print("Error: The array passed for the potential must be the same size as the array passed for freePoints!")
        print("Check the shapes of the arrays being passed to the function")
        quit()   
    # Variables that store the values of the non-zero ends of the region boundary
    xEnd = potential.shape[0]
    yEnd = potential.shape[1]
    zEnd = potential.shape[2]
    
    # Iterates through every mesh point on the boundary of the region, setting the potential
    # at these points equal to the given value and marking the points as not free
    for y in range(yEnd):
        for z in range(zEnd):
            potential[0, y, z] = boundaryValue
            potential[xEnd-1, y, z] = boundaryValue
            freePoints[0, y, z] = False
            freePoints[xEnd-1, y, z] = False
    for x in range(xEnd):
        for z in range(zEnd):
            potential[x, 0, z] = boundaryValue
            potential[x, yEnd-1, z] = boundaryValue
            freePoints[x, 0, z] = False
            freePoints[x, yEnd-1, z] = False
    for x in range(xEnd):
        for y in range(yEnd):
            potential[x, y, 0] = boundaryValue
            potential[x, y, zEnd-1] = boundaryValue
            freePoints[x, y, 0] = False
            freePoints[x, y, zEnd-1] = False

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

# Initializes a 3D NumPy array of float values with a shape determined by the x/y/zMesh variables;
# Used to store calculated values of the electrostatic potential at each mesh point
potential = np.full((xMesh, yMesh, zMesh), 5, dtype=np.float64)

# Initializes a 3D NumPy array of boolean values with the same shape as the "potential" array;
# Used to determine which mesh points are "free." Free mesh points are points where the potential
# is to be determined. Points that are not free are those that are given fixed values in the set-up
# of the model.
freePoints = np.full((xMesh, yMesh, zMesh), True, dtype=np.bool_)

setBoundaries(potential, freePoints, 0)

# Sets the values of the potential on the x = 0 face of the pipe
for y in range(yMesh):
    for z in range(zMesh):
        potential[0, y, z] = y*interval*z*interval
       
# print statements testing the values of array attributes and array entries
print(potential[0])
print("\n\n\n")
print(potential[xMesh-1])
print("\n\n\n")
print(potential[xMesh-2])

print(potential.ndim)
print(potential.size)
print(potential.shape)
#******************************************************************************

y = np.linspace(0, ySize, yMesh)
z = np.linspace(0, zSize, zMesh)
#Y, Z = np.meshgrid(y, z)
V = potential[xMesh-2]
plt.contourf(y, z, V, cmap='RdGy')
plt.colorbar()
plt.show()
