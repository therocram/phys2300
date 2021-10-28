from vpython import *
#GlowScript 3.1 VPython
# Projectile2
# Made by Masen Pitts and Harrison Ure
# Created 9/15/2021
# A simple program created to simulate 2D-projectile motion and gain experience
# simulating physical laws.

# Changes the background to a light color
scene.background = vec(0.856, 0.924, 1.000)

# Launched sphere - Simulates the 2D projectile motion of a small sphere launched 
#                   from the origin under the influence of gravity and air resistance.
#******************************************************************************
running = False # boolean that controls when the sphere's motion terminates
g = 9.8 # acceleration due to gravity (m/s^2)
dt = 0.01 # change in time: controls the amount of time that passes per movement
#          of the sphere.
r = 1 # radius of sphere (graphics only; has no bearing on calculations)

boxsize = 150 # determines the length of the ground boxes in the x-direction (m)

# These boxes make up the ground beneath the sphere
grass = box(pos=vec(boxsize/2,-0.05,0), size=vec(boxsize,0.1,10), color=vec(0.186, 0.664, 0.319))
dirt = box(pos=vec(boxsize/2,-0.3,0), size=vec(boxsize,0.4,10), color=vec(0.347, 0.234, 0.002))

scene.center = vec(boxsize/2, 40/2, 0) # Sets the position of the camera
scene.width = 600                      #
scene.height = 250                     #

# Red sphere with green trail
fsphere = sphere(pos=vec(0,0,0), radius=r, color=color.red, make_trail=True,
          trail_type="points", interval=1/(5*dt), trail_color=vec(0,1,0),
          trail_radius=0.4*r)

# A function tied to the "Launch!" button that launches the sphere 
def launch():
    if not running:     # Prevents the sphere from being launched mid-motion
        global running, x, y, ymax, vx, vy, drag, t
        running = True
        print("Launching the projectile!")
        fsphere.pos = vec(0,0,0)    # Resets sphere position
        x = 0   # x-position of sphere (m)
        y = 0   # y-position of sphere (m)
        ymax = y # maximum height acheived during motion (m)
        vx = speedSlider.value*cos(angleSlider.value*(pi/180)) # x-velocity (m/s) at time t = 0s
        vy = speedSlider.value*sin(angleSlider.value*(pi/180)) # y-velocity (m/s) at time t = 0s
        drag = dragSlider.value # drag coefficient for the sphere (m^-1)
        t = 0 # time (s)
    else:
        pass
       
# A function tied to the "Clear" button that resets the position of the sphere,
# clears its trail, and clears the text console.
def resetScene():
    global running
    fsphere.pos = vec(0,0,0)    # Resets sphere position and clears its trails
    fsphere.clear_trail()
    print_options(clear=True)   # Clears the text console
    running = False             # Ends the motion of the sphere
       
button(text="Launch!", bind=launch) # initializes "Launch!" button
scene.append_to_caption("   ")
button(text="Clear", bind=resetScene) # initializes "Clear" button
          
# Function that modifies the readout of the launch angle slider
def adjustAngle():
    angleSliderReadout.text = angleSlider.value + " degrees"
scene.append_to_caption("\n\n")

# Launch Angle Slider - modifies the launch angle of the sphere
angleSlider = slider(left=10, min=0, max=90, step=1, value=45, bind=adjustAngle)
scene.append_to_caption("   Angle = ")

# Displays angle slider value
angleSliderReadout = wtext(text="45 degrees")

# Function that modifies the readout of the speed slider
def adjustSpeed():
    speedSliderReadout.text = speedSlider.value + " m/s"
scene.append_to_caption("\n\n")
    
# Speed Slider - modifies the inital speed of the sphere when it is launched
speedSlider = slider(left=10, min=0, max=50, step=1, value=25, bind=adjustSpeed)
scene.append_to_caption("   Speed = ")

# Displays speed slider value
speedSliderReadout = wtext(text="25 m/s")

# Function that modifies the readout of the drag slider
def adjustDrag():
    dragSliderReadout.text = dragSlider.value
scene.append_to_caption("\n\n")
    
# Drag Slider - modifies the drag coefficient of the drag force
dragSlider = slider(left=10, min=0, max=1.0, step=0.005, value=0, bind=adjustDrag)
scene.append_to_caption("   Drag = ")

# Displays drag slider value
dragSliderReadout = wtext(text=dragSlider.value)
scene.append_to_caption("\n\n")

while True:
    rate(1/dt)
    if running:         # Initiates motion of sphere when launch button is 
                        #pressed and stops motion once the clear button is pressed
        ax = -drag*vx*sqrt(vx**2 + vy**2)       # ax at the beginning of the interval
        ay = -g - drag*vy*sqrt(vx**2 + vy**2)   # ay at the beginning of the interval
        xmid = x + vx*0.5*dt                # x at the middle of the interval
        ymid = y + vy*0.5*dt                # y at the middle of the interval
        vxmid = vx + ax*0.5*dt              # vy at the middle of the interval
        vymid = vy + ay*0.5*dt              # vy at the middle of the interval
        axmid = -drag*vxmid*sqrt(vxmid**2 + vymid**2)       # ax at the middle of the interval
        aymid = -g - drag*vymid*sqrt(vxmid**2 + vymid**2)   # ay at the middle of the interval
        x += vxmid * dt                     # Incrementing x, y, vx, vy, and t.
        y += vymid * dt                     #
        vx += axmid * dt                    #
        vy += aymid * dt                    #
        t += dt                             #
        if y > ymax:                        # Checking/setting max y-position
            ymax = y
        fsphere.pos.x = x                   # Updating the sphere's position
        fsphere.pos.y = y                   #
        if y <0:             # Terminates motion after the ball lands and prints info
            running = False
            texcess = (y/vy) # The excess time after the ball has reached y = 0
            t -= (texcess) # Correcting time when ball reaches y = 0 
            vy -= ay*(texcess) # Correcting final velocity
            vx -= ax*(texcess) #
            x -= vx*(texcess) # Correcting final x-position 
            print("The ball lands after {:.2f} seconds,".format(t), 
                  "travels a total horizontal distance of {:.2f} m,".format(x), 
                  "and reaches a maximum height of {:.2f} m.".format(ymax))
#******************************************************************************


