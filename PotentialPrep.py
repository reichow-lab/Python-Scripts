import numpy as np
from gridData import Grid
import sys
import argparse
# one PMEpot unit (kT/e) of electrostatic potential is equivalent to 0.0258 Volts. (or 25.8 mV)
# Parse inputs
parser = argparse.ArgumentParser()
parser.add_argument("-f",dest="infile",action="store")
parser.add_argument("-e",dest="eField",type=float,action="store")
parser.add_argument("-o",dest="outname",action="store")
# Open the .dx from PMEPot, and calculate grid-demensions
PMEPotIN = Grid(infile)
lenx, leny, lenz = PMEPot.grid.shape
# loop through the z-axis of the reaction potential and add the applied linear-potential
for z in range(lenz):
    for x in range(lenx):
        for y in range(leny):
            PMEPotIN.grid[x][y][z] = PMEPotIN.grid[x][y][z] + (z*eField)
# writeout new potential grid
PMEPotIN.export(outname+'.dx')
