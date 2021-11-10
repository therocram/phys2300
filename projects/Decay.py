# Decay
# A simple program that uses Monte-Carlo Methods to simulate
# nuclear decay.
# made by Masen Pitts and Bracken Phelps
# Updated 11/10/2021

# Import necessary packages
from math import sqrt, exp, factorial
from random import random
import matplotlib.pyplot as plt

n = 10000 # Total number of radioactive nuclei in isotope sample
nCurrent = n # Keeps track of the number of remaining nuclei
duration = 8000 # Total number of "time" steps that the simulation runs

nList = [0]*(duration+1) # List used to plot the number of remaining nuclei vs. "time"

# Simulate random radioactive decay of the nuclei. Probability of decay is
# 0.001 for each nucleus
for i in range(duration+1):
    nList[i] = nCurrent
    # For each remaining atom calculate a random number between 0 and 1 (including 0). 
    # If this number is less than 0.001 decrease the number of remaining nuclei by 1.
    # Otherwise nothing happens.
    for j in range(nCurrent):
        if random() < 0.001:
            nCurrent -= 1
    
# Plot number of remaining nuclei in sample vs. "time"
plt.plot(range(duration+1), nList, color="green")
plt.xticks(range(0, duration + 1, int(duration/10)))
plt.xlim(0, duration)
plt.ylim(0, n)
plt.grid()
plt.title("Number of Remaining Nuclei in the Sample With Respect to \"Time\"")
plt.xlabel("\"Time\"")
plt.ylabel("Number of Remaining Nuclei")
plt.show()