from vpython import *
#GlowScript 3.1 VPython
# Pendulum 3
# Made by Masen Pitts
# A program created to simulate the motion of a pendulum in 2D under the influence 
# of gravity, a damping force, and a sinusoidal driving force. Uses Euler Richardson algorithm.

# Changes the background to a light color
scene.background = vec(0.856, 0.924, 1.000)

# Swinging Pendulum - simulates the motion of a pendulum under the influence
#                     of gravity, a damping force, and a sinusoidal driving force
#                     of variable amplitude.
#******************************************************************************
theta = pi/6 # Angle of pendulum from the vertical (radians)
omega = 0 # Angular velocity of pendulun (rads/time)
alpha = 0 # Angular acceleration of pendulum (rads/time^2)
t = 0 # time in natural units
dt = 0.01 # time step
damp = 0.5 # damping coefficient for the friction on the pendulum
driveFreq = 2/3 # frequency of driving force
running = False # Controls the loop and allows the motion of the pendulum to be paused and resumed
# Note: This code uses natural units where L = g = m = 1, where L is the length
# of the pendulum, g is the acceleration due to gravity,
# and m is the mass of the pendulum bob (the rod is massless).

# Shapes that make up the pendulum apparatus
bob = sphere(radius=0.05, pos=vec(sin(theta), -cos(theta),0),color=color.red)
rod = cylinder(radius=0.01, pos=vec(0,0,0), color=vec(0,0,0), axis=bob.pos)
pivot = cylinder(radius=0.02, pos=vec(0,0,-0.05), color=vec(0.347, 0.234, 0.002), 
                 axis=vec(0,0,0.1))

# Function tied to "Start/Stop" button
def startStop():
    global running
    running = not running
    
# Function tied to the "Clear Plot" button
def clearPlot():
    phaseSpacePlot.delete()

# Function that adjusts the displayed value of the drive amp slider
def adjustDriveAmp():
    driveAmpReadout.text = driveAmpSlider.value

# Button that pauses and starts the motion of the pendulum
startStopButton = button(text="Start/Stop", bind=startStop)

scene.append_to_caption("   ")

# Button that clears the phase space plot
clearPlotButton = button(text="Clear Plot", bind=clearPlot)

scene.append_to_caption("\n\n")

# Slider that adjusts the amplitude of the driving force
driveAmpSlider = slider(left=10, min=0, max=2.0, step=0.01, value=0.5, bind=adjustDriveAmp)

# Displays value of the drive amp slider
scene.append_to_caption("   Drive Amplitude = ")
driveAmpReadout = wtext(text=0.5)

scene.append_to_caption("\n\n")

# Phase space plot for the pendulum (a plot of omega wrt theta)
graph(width=500, height=300, title='<b>Phase Space Plot of Pendulum<b>',
      ytitle='<i>Omega (rads/time)<i>', xtitle='<i>Theta (radians)<i>',
      background=color.white, xmin=-pi, xmax=pi)

phaseSpacePlot = gdots(color=color.magenta, interval=5, size=1) # points for phase space plot

# Function that calculates the net torque in natural units due to gravity, a damping force,
# and a sinusoidal driving force (recall that L = g = 1).
def torque(theta, omega, t):
    return -sin(theta) - damp*omega + driveAmpSlider.value*sin(driveFreq*t)

# Simulates the motion of the pendulum indefinitely; allows for the pausing and resuming of
# motion with the "Start/Stop" button.
while True:
    rate(1500)
    if running: # Pauses and resumes motion of the pendulum based on the value of "running"
        alpha = torque(theta, omega, t) # Calculate the angular acceleration
        thetamid = theta + omega*0.5*dt # theta at the middle of the interval
        omegamid = omega + alpha*0.5*dt # omega at the middle of the interval
        alphamid = torque(thetamid, omegamid, t + 0.5*dt) # alpha at the middle of the interval
        theta += omegamid * dt # Incrementing theta, omega, and t. 
        omega += alphamid * dt #
        t += dt                #
        if theta > pi:      # Adjusts theta as necessary to keep its value within the bounds of the 
            theta -= 2*pi   # phase space plot (on the interval [-pi, pi])
        elif theta < -pi:   #
            theta += 2*pi   #
        bob.pos = vec(sin(theta), -cos(theta), 0) # Update position of pendulum bob and rod
        rod.axis = bob.pos                        #
        phaseSpacePlot.plot(theta, omega) # Add point to the phase space plot
    
    