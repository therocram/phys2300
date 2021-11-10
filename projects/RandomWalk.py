# RandomWalk
# Simple program using Monte-Carlo methods to simulate random-walk motion
# in one dimension.
# made by Masen Pitts and Bracken Phelps
# Updated 11/8/2021

# Import necessary packages
from math import sqrt, exp, factorial
from random import random
import matplotlib.pyplot as plt

duration = 1000 # Total number of "time" steps that the simulation runs for each "walker"
tList = range(duration) # List used to plot the "time" axis of the postition vs. "time" graph
nWalkers = 20 # Determines the number of "walkers" that the program will simulate
totalDistanceSquared = 0 # Variable used to keep track of the sum of the squares of the net distances
                         # of each of the "walkers"

plt.title("Particle X-Position With Respect to Time")
plt.xlabel("\"Time\"")
plt.ylabel("X")
plt.grid()
plt.xticks(range(0, duration + 1, int(duration/10)))
plt.xlim(0, duration)

# Simulate the random walk motion for a certain number of "walkers" and graph their positions as a function
# of "time"
for i in range(nWalkers):
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
    totalDistanceSquared += (xPos[duration-1])**2 # Add the square of the final position of the current 
                                                  # "walker" to the total
    plt.plot(tList, xPos, color="red")

rms = sqrt(totalDistanceSquared/nWalkers) # Calculate the root-mean-square net distance traveled by the "walkers"
print(rms)

plt.show()    
