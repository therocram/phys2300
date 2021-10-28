from vpython import *
#GlowScript 3.1 VPython
# Molecular Dynamics (MD)
# Created by Masen Pitts
# Simulates the interactions of a specified number noble gas molecules confined
# to a box of width "w" in natural units. Uses Verlet Algorithm

# Controls width of the "box" that the molecules are simulated in.
w = 27

# Set background to white
scene.background = vec(1,1,1)

# Set the scene width, height, center, range, and FOV. Disable autoscaling, zooming, and rotation.
scene.width = 600
scene.height = scene.width
scene.center = vec(w/2,w/2,0)
scene.range = w/2
scene.fov = 0.01
scene.autoscale = False
scene.userspin = False
scene.userzoom = False

# Molecules
#******************************************************************************
# Note: This program uses natural units where r0 (molecular diameter) = epsilon
# (strength of interaction) = m (molecular mass) = 1

N = 500 # total number of atoms
dt = 0.02 # time step in natural units
halfdt = 0.5*dt # save value of (1/2)dt used for calculations
halfdtSquared = 0.5*dt*dt # saved value of (1/2)dt^2 used for calculations
wallStiffness = 50 # Controls the sharpness of the collisions of the atoms with container walls
running = False # Allows the simulation to be paused and resumed
x = [0]*N # List containing the x-positions of all atoms
y = [0]*N # List containing the y-positions of all atoms
vx = [0]*N # List containing the x-velocities of all atoms
vy = [0]*N # List containing the y-velocities of all atoms
ax = [0]*N # List containing the x-accelerations of all atoms
ay = [0]*N # List containing the y-accelerations of all atoms
potentialEnergy = 0.0 # Total Potential Energy of system
columnPosition = w-1; rowPosition = 1 # Keeps track of the row and column positions of the atoms
                                      # when spacing the atoms during initialization

ball = []*N # List containing the graphical sphere objects for all atoms

# Initializes the atoms into evenly spaced rows that span the container horizontally starting from 
# the top left-hand corner of the container
for i in range(N):
    # Starts next row if next atom is near the wall of the container
    if rowPosition + 1 > w:
        rowPosition = 1         # Reset row position
        columnPosition -= 1.1   # Increment column position
    x[i] = rowPosition      # Initialize position, velocity and acceleration values for all atoms    
    y[i] = columnPosition   #
    vx[i] = 0               #
    vy[i] = 0               #
    ax[i] = 0               #
    ay[i] = 0               #
    rowPosition += 1.1  # Increment row position
    # Graphically initialize atoms to their respective positions
    ball[i] = sphere(radius=0.5, pos=vec(x[i], y[i], 0), color=color.green)
    
# Function that updates the accelerations of the atoms due to the forces exerted
# by the walls of the container and the Lennard-Jones force from all other atoms
def computeAccelerations():
    global potentialEnergy = 0
    for i in range(N):
        # Causes atoms to bounce off of container walls when they draw near to them
        if x[i] < 0.5: # Bounces atoms off of left wall
            ax[i] = wallStiffness * (0.5 - x[i])
        elif x[i] > (w - 0.5): # Bounces atoms off of right wall
            ax[i] = wallStiffness * (w - 0.5 - x[i])
        else:
            ax[i] = 0
        if y[i] < 0.5: # Bounces atoms off of bottom wall
            ay[i] = wallStiffness * (0.5 - y[i])
        elif y[i] > (w - 0.5): # Bounces atoms off of top wall
            ay[i] = wallStiffness * (w - 0.5 - y[i])
        else:
            ay[i] = 0
        # Computes the acceleration of each atom due to the forces from every other atom
        for j in range(i):
            # Pre-calculated x and y coordinate differences of the ith and jth atoms
            # stored to optimize performance
            xDifference = x[i]-x[j]
            yDifference = y[i]-y[j]
            # Distance between the atoms squared
            r2 = xDifference*xDifference + yDifference*yDifference
            # Only considers the influence of the Lennard-Jones force from atoms that are
            # within about 3 natural units of distance. The exact distance is not calculated
            # using the sqrt function in an attempt to optimize performance.
            if r2 < 9:
                # Pre-calculated quantities used to optimize performance
                oneOverR2 = 1/(r2)
                oneOverR4 = oneOverR2*oneOverR2
                oneOverR8 = oneOverR4*oneOverR4
                oneOverR14 = oneOverR8*oneOverR4*oneOverR2
                forceFactor = 24*(2*oneOverR14 - oneOverR8)
                # Pre-calculated magnitudes of x and y forces used to optimize performance
                xForceFactor = forceFactor * xDifference
                yForceFactor = forceFactor * yDifference
                # Update acceleration for first atom
                ax[i] += xForceFactor
                ay[i] += yForceFactor
                # Update acceleration for second atom
                ax[j] += -xForceFactor
                ay[j] += -yForceFactor
                # Add potential energy between the molecules to the total potential energy of the system
                potentialEnergy += 4*(oneOverR4*oneOverR8 - oneOverR4*oneOverR2)
            else:
                pass

def singleStep():
    for i in range(N):
        # Verlet Algorithm
        x[i] += vx[i]*dt + ax[i]*halfdtSquared # Calculate new positions
        y[i] += vy[i]*dt + ay[i]*halfdtSquared #
        vx[i] += ax[i]*halfdt # Calculate 1st part of new velocities using initial accelerations
        vy[i] += ay[i]*halfdt #
        
    computeAccelerations() # Calculate new accelerations
    
    for i in range(N):
        vx[i] += ax[i]*halfdt # Calculate 2nd part of new velocities using new accelerations
        vy[i] += ay[i]*halfdt #

# Function tied to the "Start/Stop" button that pauses and resumes the program
def startStop():
    global running
    running = not running
    
# Function tied to the "Add Energy" button that adds energy to the system by slightly
# increasing the velocities of all atoms.
def addEnergy():
    for i in range(N):
        vx[i] *= 1.1
        vy[i] *= 1.1
        
# Function tied to the "Remove Energy" button that removes energy from the system by slightly
# decreasing the velocities of all atoms.
def removeEnergy():
    for i in range(N):
        vx[i] /= 1.1
        vy[i] /= 1.1
        
# Returns the sum of the kinetic energies of all the atoms
def calculateKineticEnergy():
    kineticEnergy = 0
    for i in range(N):
        speedSquared = vx[i]*vx[i] + vy[i]*vy[i]
        kineticEnergy += 0.5*speedSquared
    return kineticEnergy
    
# Updates energy text readouts
def updateEnergy():
    kineticEnergy = calculateKineticEnergy() # Stores value of kinetic energy for calculations
    # Updates text readouts with new energy values
    kineticEnergyReadout.text = "System Kinetic Energy: {:.2f}".format(kineticEnergy)
    potentialEnergyReadout.text = "System Potential Energy: {:.2f}".format(potentialEnergy)
    totalEnergyReadout.text = "Total System Energy: {:.2f}".format(potentialEnergy + kineticEnergy)
    

# Button that pauses and resumes the simulation
startStopButton = button(text="Start/Stop", bind=startStop)

scene.append_to_caption("   ")

# Button that allows the user to add energy to the system
addEnergyButton = button(text="Add Energy", bind=addEnergy)

scene.append_to_caption(" ")

# Button that allows the user to remove energy from the system
removeEnergyButton = button(text="Remove Energy", bind=removeEnergy)

scene.append_to_caption("\n\n")

# Text object that displays the kinetic energy of the system in natural units
kineticEnergyReadout = wtext(text="System Kinetic Energy: {:.2f}".format(calculateKineticEnergy()))
scene.append_to_caption("\n")

# Text object that displays the potential of the system in natural units
potentialEnergyReadout = wtext(text="System Potential Energy: {:.2f}".format(potentialEnergy))
scene.append_to_caption("\n")

# Text object that displays the total of the system in natural units
totalEnergyReadout = wtext(text="Total System Energy: {:.2f}".format(0.0))

# Loop that runs the simulation indefinitely, allowing the simulation to be paused and resumed
while True:
    rate(1500)
    if running: # Pauses and resumes the simulation based on the value of "running"
        for i in range(10):                     # Update the positions of the atoms after
            singleStep()                        # a specified number of calculation steps
        for i in range(N):                      #
            ball[i].pos = vec(x[i], y[i], 0)    #
        updateEnergy() # Updates the text readouts for the potential, kinetic, and total energy
                       # once per animation frame.


#******************************************************************************