# RandomTest
# Simple program created to perform non-exhaustive tests on just how
# random the "random()" function in Python is.
# made by Masen Pitts and Bracken Phelps
# Updated 11/5/2021

# Import necessary packages
from math import sqrt, exp, factorial
from random import random
import matplotlib.pyplot as plt

# Print a list of pseudo-random numbers ranging from 0-1
for i in range(20):
    print(random())

print("\n\n")

# Print a list of pseudo-random integers ranging from 0-9
for i in range(50):
    print(int(10*random()))

# Plot a certain number of points on an xy-plane with pseudo-random x and y
# values ranging from 0 to a specified maximum
#******************************************************************************
points = 1000 # Determines the number of points in the plot
maxValue = 10 # Determines the upper bound for the pseudo-random values
x = [0]*points # Lists that store the x and y positions of the points to be plotted
y = [0]*points #

# Assigns pseudo-random x and y values
for i in range(points):
    x[i] = maxValue*random()
    y[i] = maxValue*random()
    
# Plot the points
plt.plot(x, y, marker="+", markersize=5, color="red", linestyle="None")
plt.title("1000 Random Points")
plt.grid()
plt.axis("scaled")
plt.xlim(0,10)
plt.ylim(0,10)
plt.xticks(range(11))
plt.yticks(range(11))
plt.xlabel("X")
plt.ylabel("Y")
plt.show()
#******************************************************************************