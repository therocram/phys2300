from vpython import *
#GlowScript 3.1 VPython
# MakingShapes
# made by Masen Pitts
# Created 8/28/2021
# A collection of shapes, animations, and graphs created to gain
# personal experience with the VPython environment.

# Print message and starting box
print("Hello, GlowScript-VPython!\n")
box(pos=vec(1,-1,1), size=vec(0.5,2,0.3), color=color.red)

# You can make a much more saturated purple by putting in the RGB value (1,0,1)
# This gives a combination of the brighest red and brightest blue.
# purple box
box(pos=vec(-3,0,1), size=vec(1,2,0.5), color=vec(1,0,1))

# cube (box 2)
# ommitting the "size" parameter gives a default size of vec(1,1,1)
box(pos=vec(0,3,0), color=vec(1,1,0))

# box 3
# The RBG value of this color was obtained by messing with the sliders on this
# VPython demo page: 
# https://www.glowscript.org/#/user/GlowScriptDemos/folder/Examples/program/Color-RGB-HSV-VPython
box(pos=vec(-1,-2,1), size=vec(2,1,2), color=vec(0.207, 0.816, 0.509))

#this sphere ends up being the "origin"
sphere(radius=0.25)

# This second sphere is the default radius (radius = 1)
sphere(pos=vec(-1.25,0,1.5), color=vec(0.5,0.75,0.5))

# I found out in the documentation that the lengh of the cylinder is controlled
# by the magnitude of the "axis" parameter. There is a "length" parameter but 
# the documentation recommended updating the length only through the 
# axis parameter.

# blue cylinder
cylinder(axis=vec(3,1.5,0), pos=vec(2,1,0), color=vec(0,0,1), radius=0.5)

#******************************************************************************
# The following block of code creates full 3D Cartesian coordinate axes with
# tick marks all out of cylinders. The following variables allow customization
# of the length, color,and thickness of the axes and ticks. 

dist = 5 # Determines the length of the axes and number of tick marks.
#          in this case "dist" is set so the axes span from -5 to 5 in their
#          respective directions.
cAxes = vec(0.75,0.75,0.75) # Color of the axes
cTicks = vec(1,0.7,0) # Color of the tick marks
rAxis = 0.03; rTick = 0.06 # Thickness of the axes and tick marks respectively
tLen=0.4 # Length of the tick marks

# Each of the for loops places the tick marks perpendicular to their axes and
# evenly spaces them. 

# All of the iterator variables could have been named the
# same but the idea was to associate them with the common
# Cartesian orthonormal basis vectors.

# x-axis
xaxis = cylinder(axis=vec(dist*2,0,0), color=cAxes, radius=rAxis, pos=vec(-dist,0,0))
for i in range(-dist, dist + 1):
    cylinder(pos=vec(i,(-0.5)*tLen,0), color=cTicks, radius=rTick, axis=vec(0,tLen,0))
    
# y-axis
yaxis = cylinder(axis=vec(0,dist*2,0), color=xaxis.color, radius=xaxis.radius, pos=vec(0,-dist,0))
for j in range(-dist, dist + 1):
    cylinder(pos=vec((-0.5)*tLen,j,0), color=cTicks, radius=rTick, axis=vec(tLen,0,0))

# z-axis - as convention the ticks will be parallel to the x-axis
zaxis = cylinder(axis=vec(0,0,dist*2), color=xaxis.color, radius=xaxis.radius, pos=vec(0,0,-dist))
for k in range(-dist, dist + 1):
    cylinder(pos=vec((-0.5)*tLen,0,k), color=cTicks, radius=rTick, axis=vec(tLen,0,0))
#******************************************************************************

# dumbbell  - a cylinder with two spheres attached to the ends
bar = cylinder(pos=vec(1,1,1.5), axis=vec(0.75,0.75,0.75), radius=0.1, color=vec(0,0,0))
bell1= sphere(pos=bar.pos, radius=(bar.radius)*3, color=bar.color)
bell2= sphere(pos=bar.pos + bar.axis, radius=bell1.radius, color=bar.color)

#******************************************************************************
# table - a thin box with four cylinders as legs
tablex = 3; tabley = -1; tablez = -1
tableLength = 5
tableWidth = 2.5
legRadius = 0.05*tableWidth
tableColor = vec(0.380, 0.087, 0.068)
tableHeight = 2
offset = legRadius+(0.05*abs(tableLength-tableWidth)) # This variable gives space
#                                                     between the table legs and
#                                                     the edges of the table

tabletop = box(pos=vec(tablex,tabley,tablez), size=vec(tableWidth,0.07*tableHeight,tableLength),
            color=tableColor)

# table legs
cylinder(pos=tabletop.pos+vec(0.5*tableWidth-offset,-0.5*tabletop.size.y,0.5*tableLength-offset),
            radius=legRadius, color=tableColor, axis=vec(0,-tableHeight,0))
cylinder(pos=tabletop.pos+vec(-(0.5*tableWidth-offset),-0.5*tabletop.size.y,0.5*tableLength-offset),
            radius=legRadius, color=tableColor, axis=vec(0,-tableHeight,0))
cylinder(pos=tabletop.pos+vec(-(0.5*tableWidth-offset),-0.5*tabletop.size.y,-(0.5*tableLength-offset)),
            radius=legRadius, color=tableColor, axis=vec(0,-tableHeight,0))
cylinder(pos=tabletop.pos+vec(0.5*tableWidth-offset,-0.5*tabletop.size.y,-(0.5*tableLength-offset)),
            radius=legRadius, color=tableColor, axis=vec(0,-tableHeight,0))
#******************************************************************************

# messing with the scene
scene.background = color.white # yep it works
scene.background = vec(0.856, 0.924, 1.000) # gloomy blue
scene.range = 5

# moving box - moves across the scene in a straight line
movingBox = box(pos=vec(-4.5,2,3), size=vec(0.5,0.5,0.5), color=vec(0.5,0,0))

while movingBox.pos.x < 5:
    rate(80) # Changing the rate from 50 to 125 made the box move faster
    movingBox.pos.x += 0.05
    movingBox.pos.y -= 0.01
    movingBox.pos.z -= 0.03

print("Box: \"My time has come. You must continue your journey without me.\"\n")
    
#******************************************************************************
# spinning sphere - moves a small sphere once around in a circle with radius r 
# and leaves a trail of randomly colored dots. Also graphs the (x, y) position
# of the sphere as a function of time.
r = 4
dtheta = 0.01
spinSphere = sphere(pos=vec(r,0,0), radius=0.5, make_trail=True, trail_type="points",
                        interval=20, trail_color=vec(1,0,1))
theta = 0
t = 0

graph(width=400, height=250, title='<b>Sphere X and Y Positions w.r.t. Time<b>',
        ytitle='<i>Position (x-green, y-purple)<i>', xtitle='<i>Time (t)<i>',
        background=color.white)
xPos = gdots(color=color.green)
yPos = gdots(color=color.magenta)

while theta < 2*pi:
    rate(100)
    x = r*cos(theta)
    y = r*sin(theta)
    spinSphere.trail_color = vec(random(),random(),random())
    xPos.plot(t,x)
    yPos.plot(t,y)
    spinSphere.pos = vec(x, y, 0)
    theta += dtheta
    t += 1

print("The sum of any complex number with its conjugate is equal to 2x, where x = Re(z)")
#******************************************************************************

# Glitches I Noticed While Writing this Program:
# "Reserved words" that are included in other words are lit blue when they
# probably shouldn't be.
# Examples: In lines 138 and 139 x and y are lit blue to indicate they are 
# reserved even though they are part of a different word.



