from vpython import *
#GlowScript 3.1 VPython
# Made by Masen Pitts and Carson Matthews
# A program created to simulate the non-relativistic orbital mechanics of
# several massive objects.

# Changes the background to white and disables rotation
scene.background = vec(1,1,1)
scene.userspin = False
scene.fov = 0.01

# Orbits - simulates the motion of two planets orbiting the sun. Uses Verlet Algorithm                
#******************************************************************************
tolerance = 0.0039 # A constant that controls the size of the variable time step;
                   # controls precision of program
t = 0 # time
running = False # Boolean variable that allows for the pausing and resuming of the simulation
# Note: This program uses natural units where (time) 1 yr = (distance) 1 AU = 
# 1 solar mass = 1.

# Planet 1 - Jupiter
m1 = 0.001
x1 = 5.2 # Initial x-position of planet
y1 = 0 # Initial y-position of planet
vx1 = 0                            # Intial x and y-velocities of planet calculated such
vy1 = 2*pi/sqrt(sqrt(x1**2+y1**2)) # that the orbit will remain circular in the absence
                                   # of forces from other planets

# Planet 2 - Asteroid - variables analogous to those of Planet 1
m2 = 1e-8
x2 = 0
y2 = -3.3
vx2 = 2*pi/sqrt(sqrt(x2**2+y2**2))
vy2 = 0

# Shapes the make up the sun and planets
sun = sphere(radius=0.3, pos=vec(0,0,0), color=vec(1.000, 0.853, 0.000))
planet1 = sphere(radius=0.08, pos=vec(x1,y1,0), color=color.blue, make_trail=True,
                trail_type="points", interval=1/(3*tolerance), trail_color=color.blue)
planet2 = sphere(radius=0.05, pos=vec(x2,y2,0), color=color.red, make_trail=True,
                trail_type="points", interval=1/(3*tolerance), trail_color=color.red)

# Function thet calculates the total energy (kinetic + potential) of the system
def totalE():
    energyPlanet1 = m1*(-4*(pi**2)/sqrt(x1**2+y1**2) + 0.5*(vx1**2+vy1**2))
    energyPlanet2 = m2*(-4*(pi**2)/sqrt(x2**2+y2**2) + 0.5*(vx2**2+vy2**2))
    energyBetween = -4*(pi**2)*m1*m2/sqrt((x2-x1)**2+(y2-y1)**2)
    return energyPlanet1 + energyPlanet2 + energyBetween
    
# Function that calculates and updates the accelerations of the planets
def updateAccel():
    global ax1, ay1, ax2, ay2
    # Used to calculate the gravitational force between the planets
    factorBetween = 4*(pi**2)*m1*m2/(((x2-x1)**2 + (y2-y1)**2)**(3/2))
    # Planet 1
    factorSun1 = 4*(pi**2)/((x1**2 + y1**2)**(3/2)) # Used to calculate gravitational force
                                                    # of the Sun on Planet 1
    ax1 = -x1*factorSun1 + (x2-x1)*factorBetween/m1
    ay1 = -y1*factorSun1 + (y2-y1)*factorBetween/m1
    # Planet 2
    factorSun2 = 4*(pi**2)/((x2**2 + y2**2)**(3/2)) # Used to calculate gravitational force
                                                    # of the Sun on Planet 2
    ax2 = -x2*factorSun2 - (x2-x1)*factorBetween/m2
    ay2 = -y2*factorSun2 - (y2-y1)*factorBetween/m2
 
# Function tied to "Start/Stop" button that pauses and resumes the simulation
def startStop():
    global running
    running = not running
    
# Function that updates the Time and Energy Readouts
def update():
    timeReadout.text = "Elapsed Time: {:.2f}".format(t)
    energyReadout.text = "Total System Energy: {:.5f}".format(totalE())

# Button that pauses and resumes the simulation
startStopButton = button(text="Start/Stop", bind=startStop)
    
scene.append_to_caption("\n\n")

# Text object that displays the elapsed time of the simulation
timeReadout = wtext(text="Elapsed Time: {:.2f}".format(t))

scene.append_to_caption("\n")

# Text object that displays the total energy of the system
energyReadout = wtext(text="Total System Energy: {:.3f}".format(totalE()))

updateAccel()

# Simulates the motion of the planets with a variable time step inversely proportional
# to the larger of the planets' accelerations.
while True:
    rate(5000/tolerance)
    if running: # Pauses and resumes the simulation based on the value of "running"
        # Verlet Algorithm
        dt = tolerance/max(sqrt(ax1**2 + ay1**2), sqrt(ax2**2 + ay2**2))  # Calculate variable time step
        # Planet 1
        x1 += vx1*dt + 0.5*ax1*(dt**2) # Calculate new position
        y1 += vy1*dt + 0.5*ay1*(dt**2) #
        vx1 += 0.5*ax1*dt # Calculate 1st part of new velocity using initial acceleration
        vy1 += 0.5*ay1*dt 
        # Planet 2
        x2 += vx2*dt + 0.5*ax2*(dt**2) # Calculate new position
        y2 += vy2*dt + 0.5*ay2*(dt**2) #
        vx2 += 0.5*ax2*dt # Calculate 1st part of new velocity using initial acceleration
        vy2 += 0.5*ay2*dt #
        updateAccel() # Calculate new acceleration 
        # Planet 1
        vx1 += 0.5*ax1*dt # Calculate 2nd part of new velocity using new acceleration
        vy1 += 0.5*ay1*dt #
        # Planet 2
        vx2 += 0.5*ax2*dt # Calculate 2nd part of new velocity using new acceleration
        vy2 += 0.5*ay2*dt #
        t += dt # Increment time 
        update() # Update text readouts
        planet1.pos = vec(x1,y1,0) # Update positions of planets
        planet2.pos = vec(x2,y2,0) #
#******************************************************************************

