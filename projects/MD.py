from vpython import *
#GlowScript 3.1 VPython
# Molecular Dynamics (MD)
# Created by Masen Pitts
# Updated 10/31/2021
# Simulates the interactions of a specified number noble gas molecules confined
# to a box of width "w" in natural units. Uses Verlet Algorithm.

# Controls width of the "box" that the molecules are simulated in.
w = 70

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

N = 300  # total number of atoms
dt = 0.02 # time step in natural units
halfdt = 0.5*dt # saved value of (1/2)dt used for calculations
halfdtSquared = 0.5*dt*dt # saved value of (1/2)dt^2 used for calculations
wallStiffness = 50 # Controls the sharpness of the collisions of the atoms with container walls
running = False # Allows the simulation to be paused and resumed
x = [0]*N # List containing the x-positions of all atoms
y = [0]*N # List containing the y-positions of all atoms
vx = [0]*N # List containing the x-velocities of all atoms
vy = [0]*N # List containing the y-velocities of all atoms
ax = [0]*N # List containing the x-accelerations of all atoms
ay = [0]*N # List containing the y-accelerations of all atoms
forceCutoffSquared = 9 # The distance squared in natural units past which the forces between two atoms are ignored
energyOffset =  abs(4*(1/forceCutoffSquared**6 - 1/forceCutoffSquared**3)) # A small constant added to potential energy
                                                                           # calculations to account for the fact that
                                                                           # forces past a certain distance are ignored
potentialEnergy = 0 # Total Potential Energy of system
totalKE = 0 # Keeps track of the total kinetic energy over time; used to calculate the
            # average temperature of the system over time
averageKEover = 0 # Keeps track of the total that the kinetic energy will be averaged over
totalForce = 0 # Keeps track of the total force exerted on the walls of the container by the atoms;
               # used to calculate average pressure the atoms exert on the walls of the container
averageForceOver = 0 # Keeps track of the total that the force will be averaged over
temperature = 0 # Stores the calculated value of the average temperature
pressure = 0 # Stores the calculated value of the average pressure
totalEnergy = 0 # Stores the calculated value of the total energy

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
# by the walls of the container and the Lennard-Jones force from all other atoms;
# also calculates the total potential energy of the system and the total force
# the atoms exert on the walls of the container.
def computeAccelerations():
    global potentialEnergy # Keeps track of the system's total potential energy
    potentialEnergy = 0
    global totalForce # Keeps track of the total force exerted on the walls of the container by the atoms
    for i in range(N):
        # Causes atoms to bounce off of container walls when they draw near to them
        if x[i] < 0.5: # Bounces atoms off of left wall
            xDisplacement = 0.5 - x[i]  # Distance of atom's edge from the "equilibrium" of the wall edge
            springForce = wallStiffness * xDisplacement # Spring force exerted on the atom by the wall
            ax[i] = springForce                              # Set acceleration and increment potential energy
            potentialEnergy += 0.5*springForce*xDisplacement #
            totalForce += springForce # Use Newton's Third Law to add the force of atom on the wall to the
                                      # total force.
        elif x[i] > (w - 0.5): # Bounces atoms off of right wall
            xDisplacement = w - 0.5 - x[i]                   # Analogous variables and operations
            springForce = wallStiffness * xDisplacement      #
            ax[i] = springForce                              #
            potentialEnergy += 0.5*springForce*xDisplacement #
            totalForce += -springForce                       #
        else:
            ax[i] = 0

        if y[i] < 0.5: # Bounces atoms off of bottom wall
            yDisplacement = 0.5 - y[i]                       # Analogous variables and operations
            springForce = wallStiffness * yDisplacement      #
            ay[i] = springForce                              #
            potentialEnergy += 0.5*springForce*yDisplacement #
            totalForce += springForce                        #
        elif y[i] > (w - 0.5): # Bounces atoms off of top wall
            yDisplacement = w - 0.5 - y[i]                   # Analogous variables and operations
            springForce = wallStiffness * yDisplacement      #
            ay[i] = springForce                              #
            potentialEnergy += 0.5*springForce*yDisplacement #
            totalForce += -springForce                       #
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
            if r2 < forceCutoffSquared:
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
                potentialEnergy += 4*(oneOverR4*oneOverR8 - oneOverR4*oneOverR2) + energyOffset
            else:
                pass

# Function that uses the Verlet Algorithm to update the postion, velocity, and acceleration values
# of the atoms.
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
    resetAverages()
    for i in range(N):
        vx[i] *= 1.1
        vy[i] *= 1.1
        
# Function tied to the "Remove Energy" button that removes energy from the system by slightly
# decreasing the velocities of all atoms.
def removeEnergy():
    resetAverages()
    for i in range(N):
        vx[i] /= 1.1
        vy[i] /= 1.1

# Function tied to the "Reset Averages" button that resets the calculations of average temperature and presssure
def resetAverages():
    global totalKE, averageKEover, totalForce, averageForceOver
    totalKE = 0; averageKEover = 0
    totalForce = 0; averageForceOver = 0
    
# Function tied to the "Print Data" button 
def printData():
    calculateData()
    print("{:.5f}".format(temperature),"\t        ", "{:.5f}".format(pressure), "\t        ", "{:.2f}".format(totalEnergy))
        
# Returns the sum of the kinetic energies of all the atoms
def calculateKineticEnergy():
    kineticEnergy = 0
    for i in range(N):
        speedSquared = vx[i]*vx[i] + vy[i]*vy[i]
        kineticEnergy += 0.5*speedSquared
    return kineticEnergy
    
# Calculates values used in text objects and print statements
def calculateData():
    global temperature, pressure, totalEnergy
    temperature = totalKE/averageKEover           # Calculate average temperature, average pressure, and total energy
    pressure = totalForce/(averageForceOver*w*4)  #
    totalEnergy = potentialEnergy + kineticEnergy #
    
# Updates text readouts
def updateReadouts():
    # Updates text readouts with new energy values
    kineticEnergyReadout.text = "System Kinetic Energy: {:.2f}".format(kineticEnergy)
    potentialEnergyReadout.text = "System Potential Energy: {:.2f}".format(potentialEnergy)
    totalEnergyReadout.text = "Total System Energy: {:.2f}".format(totalEnergy)
    # Updates temperature readout with temperature averaged over time
    temperatureReadout.text = "Average Temperature: {:.5f}".format(temperature)
    # Updates the pressure readout withe the pressure on the walls of the container averaged over time
    pressureReadout.text = "Average Pressure: {:.5f}".format(pressure) 
    

# Button that pauses and resumes the simulation
startStopButton = button(text="Start/Stop", bind=startStop)

scene.append_to_caption("   ")

# Button that allows the user to add energy to the system
addEnergyButton = button(text="Add Energy", bind=addEnergy)

scene.append_to_caption(" ")

# Button that allows the user to remove energy from the system
removeEnergyButton = button(text="Remove Energy", bind=removeEnergy)

scene.append_to_caption("   ")

# Button that resets the average temeperature and pressure values
resetAveragesButton = button(text="Reset Averages", bind=resetAverages)

scene.append_to_caption("   ")

# Button that prints the values of temperature, pressure and total energy to the screen
printDataButton = button(text="Print Data", bind=printData)

scene.append_to_caption("\n\n")

# Text object that displays the average temperature of the system over time
temperatureReadout = wtext(text="Average Temperature: 0")
scene.append_to_caption("\n")

# Text object that displays the average pressure of the atoms on the walls of the container
# over time
pressureReadout = wtext(text="Average Pressure: 0")
scene.append_to_caption("\n")

# Text object that displays the kinetic energy of the system in natural units
kineticEnergyReadout = wtext(text="System Kinetic Energy: {:.2f}".format(calculateKineticEnergy()))
scene.append_to_caption("\n")

# Text object that displays the potential energy of the system in natural units
potentialEnergyReadout = wtext(text="System Potential Energy: {:.2f}".format(potentialEnergy))
scene.append_to_caption("\n")

# Text object that displays the total energy of the system in natural units
totalEnergyReadout = wtext(text="Total System Energy: {:.2f}".format(0.0))

print("Temperature  \t Pressure   \t Total Energy")

# Loop that runs the simulation indefinitely, allowing the simulation to be paused and resumed
while True:
    rate(1500)
    if running: # Pauses and resumes the simulation based on the value of "running"
        for i in range(10):                     # Update the positions of the atoms after
            singleStep()                        # a specified number of calculation steps
            averageForceOver += 1               #
        for i in range(N):                      #
            ball[i].pos = vec(x[i], y[i], 0)    #
        kineticEnergy = calculateKineticEnergy() # Stores current value of kinetic energy for calculations
        totalKE += kineticEnergy
        averageKEover += N
        calculateData()
        updateReadouts() # Updates the text readouts for temperature and pressure as well as potential,
                         # kinetic, and total energy once per animation frame.


#******************************************************************************