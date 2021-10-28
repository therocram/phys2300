from vpython import *
#GlowScript 3.1 VPython
# Pendulum 2
# Made by Masen Pitts
# A program created to simulate the motion of two pendulums in 2D under the influence 
# of gravity, a damping force, and a sinusoidal driving force. Uses Euler Richardson algorithm.

# Changes the background to a light color
scene.background = vec(0.856, 0.924, 1.000)

# Swinging Pendulums - simulates the motion of two pendulums under the influence
#                      of gravity, a damping force, and a sinusoidal driving force.
#******************************************************************************
t = 0 # time in natural units
dt = 0.01 # time step
damp = 0.5 # damping coefficient for the friction on the pendulums
driveAmp = 1.2 # amplitude of driving force on the pendulums
driveFreq = 2/3 # frequency of driving force on the pendulums

# Note: This code uses natural units where L = g = m = 1, where L is the length
# of the pendulum, g is the acceleration due to gravity,
# and m is the mass of the pendulum bob (the rod is massless).

# Pivot for the Pendulums
pivot = cylinder(radius=0.02, pos=vec(0,0,-0.05), color=vec(0.347, 0.234, 0.002), 
                 axis=vec(0,0,0.2))
# Pendulum 1
theta = 0 # Angle of Pendulum 1 from the vertical (radians)
omega = 0 # Angular velocity of Pendulum 1 (rads/time)
alpha = 0 # Angular acceleration of Pendulum 1 (rads/time^2)

# Shapes for Pendulum 1
bob = sphere(radius=0.05, pos=vec(sin(theta), -cos(theta),0),color=color.red)
rod = cylinder(radius=0.01, pos=vec(0,0,0), color=vec(0,0,0), axis=bob.pos)

# Pendulum 2
theta2 = 0.001 # Angle of Pendulum 2 from the vertical (radians)
omega2 = 0 # Angular velocity of Pendulum 2 (rads/time)
alpha2 = 0 # Angular acceleration of Pendulum 2 (rads/time^2)

# Shapes for Pendulum 2
bob2 = sphere(radius=0.05, pos=vec(sin(theta2), -cos(theta2), 0.1), color=color.blue)
rod2 = cylinder(radius=0.01, pos=vec(0,0,0.1), color=vec(0,0,0), axis=bob2.pos - vec(0,0,0.1))

# Graphs pendulum angles from the vertical wrt time
anglePlot = graph(width=700, height=300, title='<b>Angle of Pendulums from the Vertical w.r.t. Time<b>',
            ytitle='<i>Theta (radians)<i>', xtitle='<i>Time (natural units)<i>',
            background=color.white)

thetaPos = gdots(graph=anglePlot, color=bob.color, interval=10) # points for graph for pendulum 1
thetaPos2 = gdots(graph=anglePlot, color=bob2.color, interval=10) # points for graph for pendulum 2

# Graphs a log-difference plot for theta2 and theta wrt time
logdiffPlot = graph(width=700, height=300, title='<b>Log Difference Plot of Theta2 and Theta w.r.t. Time<b>',
              ytitle="<i>ln|Theta2 - Theta|<i>", xtitle='<i>Time (natural units)<i>',
              background=color.white)

logdiffPos = gdots(graph=logdiffPlot, color=color.magenta, interval=10) # points for log difference plot

# Function that calculates the net torque in natural units due to gravity, a damping force,
# and a sinusoidal driving force (recall that L = g = 1).
def torque(theta, omega, t):
    return -sin(theta) - damp*omega + driveAmp*sin(driveFreq*t)

# Simulates the motion of Pendulums 1 and 2 for 80 units of time
while t < 80:
    rate(400)
    # Pendulum 1
    alpha = torque(theta, omega, t) # Calculate the angular acceleration
    thetamid = theta + omega*0.5*dt # theta at the middle of the interval
    omegamid = omega + alpha*0.5*dt # omega at the middle of the interval
    # Pendulum 2
    alpha2 = torque(theta2, omega2, t) # Calculate the angular acceleration
    thetamid2 = theta2 + omega2*0.5*dt # theta2 at the middle of the interval
    omegamid2 = omega2 + alpha2*0.5*dt # omega2 at the middle of the interval
    
    tmid = t + 0.5*dt # time at the middle of the interval
    
    # Pendulum 1
    alphamid = torque(thetamid, omegamid, tmid) # alpha at the middle of the interval
    theta += omegamid * dt # Incrementing theta and omega 
    omega += alphamid * dt #
    # Pendulum 2
    alphamid2 = torque(thetamid2, omegamid2, tmid) # alpha2 at the middle of the interval
    theta2 += omegamid2 * dt # Incrementing theta2 and omega2 
    omega2 += alphamid2 * dt #
    
    t += dt                # Incrementing time
    bob.pos = vec(sin(theta), -cos(theta), 0)       # Update position of bob and rod for
    rod.axis = bob.pos                              # both Pendulums
    bob2.pos = vec(sin(theta2), -cos(theta2), 0.1)  #
    rod2.axis = bob2.pos - vec(0,0,0.1)             #
    thetaPos.plot(t,theta)                       # Add points to the anglePlot
    thetaPos2.plot(t,theta2)                     # and logdiffPlot graphs
    logdiffPos.plot(t, log(abs(theta2-theta)))   #
