# Decay
# A simple program that uses Monte-Carlo Methods to simulate
# nuclear decay.
# made by Masen Pitts and Bracken Phelps
# Updated 11/10/2021

# Import necessary packages
from math import sqrt, exp, factorial
from random import random
import matplotlib.pyplot as plt

n = 100 # Total number of radioactive nuclei in isotope sample
nCurrent = n # Keeps track of the number of remaining nuclei
duration = 10000 # Total number of "time" steps that the simulation runs

nList = [0]*duration # List plot the number of remaining nuclei vs. "time"
