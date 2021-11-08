# TwoBoxes
# Simple program using Monte-Carlo methods to simulate the random movement of gasses
# between two sides of a box seperated by a partition.
# made by Masen Pitts and Bracken Phelps
# Updated 11/8/2021

# Import necessary packages
from math import sqrt, exp, factorial
from random import random
import matplotlib.pyplot as plt

n = 100 # Total number of gas molecules
nLeft = int(n/2) # Total number of gas molecules in the left-hand box;
                 # half of the molecules start out in the left-hand box
             
duration = 100000 # Determines the number of "time" steps that the simulation runs
tList = range(duration) # List used to plot the "time" axis of the nLeft vs. "time" plot
nLeftList = [0]*duration # List used to plot the number of molecules in the left-hand box vs. "time"
hist = [0]*(n+1) # List used to plot a histogram of all all possible values of nLeft
binomialList = [0]*(n+1) # List used to plot the theoretical values of nLeft given by the binomial distribution

# Randomly selects a gas molecule and moves it to the opposite box once per "time" step
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

# Calculates the probability value predicted by the binomial distribution at a certain value of nLeft
# with a given n. 
def binomial(n, nleft):
    denominator = (2**n)*factorial(nleft)*factorial(n-nleft)
    return factorial(n)/denominator
 
# Calculate the predicted occurences of each value of nLeft and store them to be plotted 
for i in range(n + 1):
    binomialList[i] = duration*binomial(n,i)

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

# Plot a histogram of all possible values of nLeft and a line plot showing the theoretical distribution
plt.bar(range(n+1), hist, width=0.8, color="red", label="Monte-Carlo results")
plt.plot(range(n+1), binomialList, color="blue", label="Theoretical results")
plt.title("Number of Times Each Possible Value of the Number of Molecules in The Left Box Occurs")
plt.xticks(range(0, n + 1, int(n/10)))
plt.xlim(0, n)
plt.xlabel("Possible Values of NLeft")
plt.ylabel("Number of Occurences")
plt.legend()
plt.show()



