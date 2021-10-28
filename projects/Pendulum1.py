from vpython import *
#GlowScript 3.1 VPython
# Pendulum 1
# Made by Masen Pitts
# A program created to simulate the frictionless motion of a pendulum in 2D
# under the influence of gravity. Uses the Euler-Richardson algorithm.

# Changes the background to a light color
scene.background = vec(0.856, 0.924, 1.000)

# Swinging Pendulum - simulates the motion of a simple pendulum under
#                     the influence of gravity.
#******************************************************************************
dt = 0.01 # time step
iAngle = 10 # Initial amplitude of motion (degrees)
# Note: This code uses natural units where L = g = m = 1, where L is the length
# of the pendulum, g is the acceleration due to gravity,
# and m is the mass of the pendulum bob (the rod is massless).

# Shapes that make up the pendulum apparatus
bob = sphere(radius=0.05, pos=vec(0, -1,0),color=color.red)
rod = cylinder(radius=0.01, pos=vec(0,0,0), color=vec(0,0,0), axis=bob.pos)
pivot = cylinder(radius=0.02, pos=vec(0,0,-0.05), color=vec(0.347, 0.234, 0.002),
                 axis=vec(0,0,0.1))
                 
# Ajusts the position of the camera and width of the scene
scene.center = vec(0,-0.5,0)
scene.width = 550

# Function that computes the total energy of the system (potential + kinetic)
# and prints it to screen
def etotal():
    e = (1-cos(theta)) + (1/2)*(omega**2) # Total energy of system
    print("Total Energy =", e)

# Function that calculates the time of crossing
def getTime():
    texcess = (theta/omega) # Calculate excess time after pendulum crossed theta = 0
    tcross = t - texcess # Correct time of crossing
    return tcross

# Graphs pendulum angle from the vertical wrt time
graph(width=500, height=300, title='<b>Angle of Pendulum from the Vertical w.r.t. Time<b>',
      ytitle='<i>Theta (radians)<i>', xtitle='<i>Time (natural units)<i>',
      background=color.white)

thetaPos = gdots(color=color.magenta, interval=10) # points for graph

#etotal()

while iAngle <= 170:    # Calculates the period and simulates the motion of the
                        # pendulum for a series of amplitudes ranging from 10 to
                        # 170 degrees
    theta = radians(iAngle) # Angle of pendulum from the vertical (radians)
    omega = 0 # Angular velocity of pendulun (rads/s)
    alpha = 0 # Angular acceleration of pendulum (rads/s^2)
    t = 0 # time in natural units
    crossed = False # keeps track of whether the pendulum has crossed the vertical
    bob.pos = vec(sin(theta), -cos(theta), 0) # Reset position of pendulum bob and rod
    rod.axis = bob.pos                       #
    thetaPos.delete() # Clear graph
    while True:     # This embedded loop runs the motion of the pendulum just long enough
                    # to calculuate the period of motion for the given amplitude
        rate(200)
        alpha = -sin(theta) # Calculate the angular acceleration due to gravity
                            # (recall that L = g = 1)
        thetamid = theta + omega*0.5*dt # theta at the middle of the interval
        omegamid = omega + alpha*0.5*dt # omega at the middle of the interval
        alphamid = -sin(thetamid)       # alpha at the middle of the interval
        lastTheta = theta               # theta just before being incremented
        theta += omegamid * dt          # Incrementing theta
        if (theta > 0) and (lastTheta < 0): # Checks and keeps track of when the 
                                            # pendulum crosses the vertical.
            if not crossed:                 # Calculates time of first crossing
                tcross = getTime()
                crossed = True
            else:                           # Calculates period, prints results, 
                                            # and terminates loop
                period = getTime() - tcross
                print(iAngle, "\t", period)
                break
        omega += alphamid * dt # Incrementing omega and t.
        t += dt                #
        bob.pos = vec(sin(theta), -cos(theta), 0) # Update position of pendulum bob and rod
        rod.axis = bob.pos                       #
        thetaPos.plot(t,theta) # Add point to the thetaPos graph
    iAngle += 10 # Increment Amplitude
    
#etotal()
#******************************************************************************