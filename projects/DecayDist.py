# DecayDist
# A simple program using Monte-Carlo methods to model
# the probability distributions of decaying nuclei
# made by Masen Pitts and Bracken Phelps
# Updated 11/12/2021

# Import necessary packages
from math import sqrt, factorial, exp
from random import random
import matplotlib.pyplot as plt

n = 10000 # Total number of nuclei
iterations = 30000 # Determines the number of times the first
                 # decay step is simulated
probability = 0.001 # The probability of each nucleus to decay during
                    # an iteration
expectedDecayAverage = n*probability # The expected average value of the number of nuclei that decay

nDecays = 0 # Keeps track of the number of nuclei that decay in each iteration
histRange = int(3*expectedDecayAverage) # Gives an educated guess for the range of the histogram plot
hist = [0]*(histRange+1) # List used to plot a histogram of the number of occurences of each 
                 # possible value of the number of nuclei that decay

for i in range(iterations):
    nDecays = 0
    # For each atom calculate a random number between 0 and 1 (including 0). 
    # If this number is less than 0.001 add 1 to the number of nuclei that decay.
    # Otherwise nothing happens.
    for j in range(n):
        if random() < probability:
            nDecays += 1
        # This statement prints an error message with instructions and terminates the program
        # if nDecays would fall outside of histRange.
        if nDecays > histRange:
            print("Warning! More nuclei decayed than what was allowed by \"histRange\"")
            print("Please do one of the following:\n1) Run the program again\n2) Increase value of \"histRange\" if problem persists")
            quit()
    hist[nDecays] += 1
   
poissonDistribution = [0]*(histRange+1) # List used to plot the theoretical decay distribution given by
                                        # the Poisson distribution
for k in range(histRange+1):
    poissonDistribution[k] = iterations*(expectedDecayAverage**k)*exp(-expectedDecayAverage)/factorial(k)


# Plot a histogram of all possible values of the number of nuclei that decay during
# an iteration
plt.bar(range(histRange+1), hist, color="blue", label="Monte-Carlo results")
plt.plot(range(histRange+1), poissonDistribution, color="red", label="Theoretical results")
plt.xlim(0, histRange)
plt.xticks(range(0, histRange+1, int(histRange/10)))
plt.title("Number of Times Each Possible Value of Total Decayed Nuclei Occurs")
plt.xlabel("Total Number of Nuclei that Decay")
plt.ylabel("Number of Occurences")
plt.legend()
plt.show()