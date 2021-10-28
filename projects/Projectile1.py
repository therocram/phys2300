from vpython import *
#GlowScript 3.1 VPython
# Projectile1
# Made by Masen Pitts and Harrison Ure
# Created 9/3/2021
# A simple program created to simulate 1D projectile motion and gain experience
# simulating physical laws.

# Changes the background to a light color
scene.background = vec(0.856, 0.924, 1.000)

# These boxes make up the ground beneath the sphere
grass = box(pos=vec(0,-0.05,0), size=vec(10,0.1,10), color=vec(0.186, 0.664, 0.319))
dirt = box(pos=vec(0,-0.3,0), size=vec(10,0.4,10), color=vec(0.347, 0.234, 0.002))

# Falling sphere - simulates a small sphere falling under the influence of
#                  gravity and air resistance.
#******************************************************************************
y = 10 # ball starting height (m)
vy = 0 # velocity (m/s) at time t = 0s
g = 9.8 # acceleration due to gravity (m/s^2)
t = 0 # time (s)
dt = 0.02 # change in time: controls the amount of time that passes per movement
#          of the sphere.
drag = 0.1 # drag coefficient for the sphere (m^-1)
r = 0.5 # radius of sphere (graphics only; no bearing on calculations)


# red sphere
fsphere = sphere(pos=vec(0,y,0), radius=r, color=color.red, make_trail=True,
                  trail_type="points", interval=1/(10*dt), trail_color=vec(0,1,0))
                  
scene.center = vec(0,y/2,0)
scene.width = 400

graph(width=400, height=300, title='<b>Ball Y-Position w.r.t. Time<b>', 
        ytitle='<i>Ball Y-Position (m)<i>', xtitle='<i>Time (s)<i>',
        background=color.white) # Graphs ball y-position wrt time
        
yPos = gdots(color=color.green, interval=1/(20*dt)) # points for graph
      
while y > 0:
    rate(1/dt)
    ay = -g - drag*vy*abs(vy)           # ay at the beginning of the interval
    ymid = y + vy*0.5*dt                # y at the middle of the interval
    vymid = vy + ay*0.5*dt              # vy at the middle of the interval
    aymid = -g - drag*vymid*abs(vymid)  # ay at the middle of the interval
    y += vymid * dt                     # Incrementing y, vy, and t. 
    vy += aymid * dt                    #
    t += dt                             #
    fsphere.pos.y = y                   # Updating the sphere's position
    yPos.plot(t,y)                      # Adds a point to the yPos graph

texcess = (y/vy) # The excess time after the ball has reached y = 0

t -= (texcess) # Correcting time when ball reaches y = 0 
vy -= ay*(texcess) # Correcting final velocity
    
print("Ball lands at t =", t, "seconds, with velocity", vy, "m/s")
#******************************************************************************






