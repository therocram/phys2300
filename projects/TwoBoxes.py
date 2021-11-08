# TwoBoxes
# Simple program using Monte-Carlo methods to simulates two boxes
# of gas molecules seperated by a partition.
# made by Masen Pitts and Bracken Phelps
# Updated 11/5/2021

# Import necessary packages
from math import sqrt, exp, factorial
from random import random
import matplotlib.pyplot as plt

n = 1000 # Total number of gas molecules
nLeft = int(n/2) # Total number of gas molecules in the left-hand box;
                 # all molecules start out in the left-hand box
             
duration = 10000 # Determines the number of "time" steps that the simulation runs
tList = range(duration) # List used to plot the "time" axis of the plot
nLeftList = [0]*duration # List used to plot the number of molecules in the left-hand box vs. "time"
hist = [0]*(n+1) # List used to plot a histogram of all all possible values of nLeft

# Randomly selects a gas molecule and moves it to the opposite box
for i in range(duration):
    # Calculate a random number between 0 and n. If this number is less than nLeft
    # then one of the molecules in the left-hand box is moved to the right-hand box. Otherwise
    # a molecule moves from the right-hand box to the left-hand box.
    nLeftList[i] = nLeft
    hist[nLeft] += 1
    if n*random() < nLeft:
        nLeft -= 1
    else:
        nLeft += 1

'''
# Plot the number of molecules in the left-hand box vs. "time"
plt.plot(tList, nLeftList, marker="+", markersize=5, color="red", linestyle="None")
plt.title("Number of Molecules in Left Side of the Box wrt \"Time\"")
plt.grid()
plt.xlim(0, duration)
plt.ylim(0, n)
plt.xticks(range(0, duration + 1, int(duration/10)))
plt.yticks(range(0, n + 1, int(n/10)))
plt.xlabel("\"Time\"")
plt.ylabel("Number of Molecules in Left Side")
plt.show()
'''

plt.bar(range(n+1), hist, width=0.8, color="red")
plt.title("Number of Times Each Possible Value of the Number of Molecules in The Left Box Occurs")
plt.xticks(range(0, n + 1, int(n/10)))
plt.xlabel("Possible Values of NLeft")
plt.ylabel("Number of Occurences")
plt.show()

