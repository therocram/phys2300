from vpython import *
#GlowScript 3.1 VPython
# Made by Masen Pitts and Carson Matthews
# A simple program created to simulate the orbit of a single planet around the
# sun.

# Changes the background to white and disables rotation
scene.background = vec(1,1,1)
scene.userspin = False
scene.fov = 0.01

# Orbiting Planet - simulates the motion of a planet orbiting the sun. Uses
#                   Verlet Algorithm
#******************************************************************************
tolerance = 0.0039 # A constant that controls the size of the variable time step;
                   # controls precision of program
x = 0.58 # Initial x-position of planet
y = 0 # Initial y-position of planet
r = sqrt(x**2 + y**2) # Initial orbital radius of planet
vx = 0          # Intial x and y-velocities of planet
vy = 11.5729    #
v = sqrt(vx**2 + vy**2) # Initial speed of planet
rmax = r # Keeps track of maximum distance of planet away from sun
vmax = v # Keeps track of maximum speed of planet
t = 0 # time
# Note: This program uses natural units where (time) 1 yr = (distance) 1 AU = 
# 1 solar mass = 1.

# Shapes the make up the sun, planet and coordinate axes
sun = sphere(radius=0.3, pos=vec(0,0,0), color=vec(1.000, 0.853, 0.000))
planet = sphere(radius=0.1, pos=vec(x,y,0), color=color.blue, make_trail=True,
                trail_type="points", interval=1/(2*tolerance), trail_color=color.green)
axesLength = 4 
# x-axis
xaxis = cylinder(axis=vec(axesLength*2,0,0), color=vec(0.75,0.75,0.75), radius=0.01, pos=vec(-axesLength,0,0))
# y-axis
yaxis = cylinder(axis=vec(0,axesLength*2,0), color=xaxis.color, radius=xaxis.radius, pos=vec(0,-axesLength,0))

# Function thet calculates the total energy per unit mass (kinetic + potential) of the planet
def totalE():
    return (-4*(pi**2)/sqrt(x**2+y**2)) + 0.5*(vx**2+vy**2)
    
# Function that calculates the magnitude of the gravitational force in natural units
# and uses it to update the acceleration of the planet
def updateAccel():
    global ax, ay
    gMag = 4*(pi**2)/((x**2 + y**2)**(3/2)) # Magnitude of gravitational force
    ax = -x*gMag
    ay = -y*gMag

print("Initial Energy of Planet = {:.6f}".format(totalE()))

updateAccel()

# The loop runs for 76 natural units of time (years), the period for the orbit
# of Halley's Comet around the Sun.
while t < 76:
    rate(10/tolerance)
     # Euler Algorithm
#    ax = -x*gravityMagnitude(x,y) # Calculate acceleration
#    ay = -y*gravityMagnitude(x,y) #
#    x += vx*dt # Calculate new position using old velocity
#    y += vy*dt #
#    vx += ax*dt # Calculate new velocity using old acceleration
#    vy += ay*dt #
#    t += dt # Increment 

     # Euler-Richardson Algorithm
#    ax = -x*gravityMagnitude(x,y) # Calculate acceleration at beginning of interval
#    ay = -y*gravityMagnitude(x,y) #
#    xmid = x + 0.5*dt*vx # Calculate position at the middle of the interval
#    ymid = y + 0.5*dt*vy #
#    vxmid = vx + 0.5*dt*ax # Calculate the velocity at the middle of the interval
#    vymid = vy + 0.5*dt*ay #
#    axmid = -xmid*gravityMagnitude(xmid,ymid) # Calculate the acceleration at the middle of the interval
#    aymid = -ymid*gravityMagnitude(xmid,ymid) #
#    x += vxmid*dt # Calculate new position
#    y += vymid*dt #
#    vx += axmid*dt # Calculate new velocity
#    vy += aymid*dt #
#    t += dt # Increment time 
#    planet.pos = vec(x,y,0) # Update position of planet

    # Verlet Algorithm
    dt = tolerance/sqrt(ax**2 + ay**2) # Calculate variable time step
    lastY = y # Save old position
    x += vx*dt + 0.5*ax*(dt**2) # Calculate new position
    y += vy*dt + 0.5*ay*(dt**2) #
    if (lastY < 0 and y > 0) or (lastY > 0 and y < 0):  # Calculates the time and position of each crossing
        texcess = y/vy                                  # of the x-axis
        print("Time:", t-texcess, "\t X:", x-texcess*vx)
        r = sqrt(x**2 + y**2) # Calculate distance from sun
        if r > rmax:    # Check for maximum distance from sun
            rmax = r
        v = sqrt(vx**2 + vy**2) # Calculate speed of planet
        if v > vmax: # Check for maximum speed
            vmax = v
    vx += 0.5*ax*dt # Calculate 1st part of new velocity using initial acceleration
    vy += 0.5*ay*dt #
    updateAccel() # Calculate new acceleration 
    vx += 0.5*ax*dt # Calculate 2nd part of new velocity using new acceleration
    vy += 0.5*ay*dt #
    t += dt # Increment time 
    planet.pos = vec(x,y,0) # Update position of planet  
    
print("Final Energy of Planet = {:.6f}".format(totalE()))
print("Max Distance from Sun =", rmax, "\nMax Speed =", vmax)
#******************************************************************************
