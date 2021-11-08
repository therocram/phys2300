# RandomWalk
# Simple program using Monte-Carlo methods to simulate random-walk motion
# in one dimension.
# made by Masen Pitts and Bracken Phelps
# Updated 11/8/2021

# Import necessary packages
from math import sqrt, exp, factorial
from random import random
import matplotlib.pyplot as plt

duration = 1000 # Total number of "time" steps that the simulation runs
tList = range(duration) # List used to plot the "time" axis of the postition vs. "time" graph

plt.title("Particle X-Position With Respect to Time")
plt.xlabel("\"Time\"")
plt.ylabel("X")
plt.grid()
plt.xticks(range(0, duration + 1, int(duration/10)))
plt.xlim(0, duration)

# Simulate the random walk motion a certain number of times and graph them all together
for i in range(20):
    x = 0 # Position of particle
    xPos = [0]*duration # List used to plot the positions of the particle wrt "time"
    
    # Moves the particle in random direction
    for j in range(duration):
        # Calculate a random number between 0 and 1 (including 0). If this number is less than 0.5
        # move the particle one unit in the positive x-direction. Otherwise move the particle one unit 
        # in the negative x-direction
        xPos[j] = x
        if random() < 0.5:
            x += 1
        else:
            x -= 1
    
    plt.plot(tList, xPos, color="red")

plt.show()    
