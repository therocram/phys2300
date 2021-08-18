import math

print("Hello World\nWhat's up?\n")


class Particle:

    def __init__(self, x, y, z, n, sys):
        self.X = x
        self.Y = y
        self.Z = z
        self.name = n
        self.system = sys

    def setpos(self, x, y, z):
        self.X = x
        self.Y = y
        self.Z = z

    def tostring(self):
        print(self.name + ":\n\nAt (" + str(self.X) + ", " + str(self.Y) + ", " + str(self.Z) + ") - " + self.system)


gamma = Particle(1, 1, 1, "Gamma 3XD", "Cartesian")
gamma.tostring()