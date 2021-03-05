import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.interpolate import interp1d
import sys
import argparse
from PMFPlotter import PMFPlotter
from TrackerPlot import TrackerPlot
# Parse inputs
parser = argparse.ArgumentParser()
parser.add_argument("-dat", dest = "datstring", action = "store")
parser.add_argument("-out", dest = "outname", action = "store", default = "OUTFILE")
parser.add_argument("-p", "--pmf", dest = "Pchoice", action = "store", type=bool, default = False)
parser.add_argument("-t", "--track", dest = "Tchoice", action = "store", type=bool, default = False)
parser.add_argument("-b", "--obs", dest = "Bchoice", action = "store", type=bool, default = False)
parser.add_argument("-bs", dest = "ObString", action = "store")
parser.add_argument("-ws", "--windowsize", dest = "WS", action = "store")
parser.add_argument("-c", dest = "palette", action = "store", default = "Blues_r")
parser.add_argument("-lt", dest = "LastTime", action = "store", type=int, default = 1800)

args = parser.parse_args()

if args.Pchoice == True:

    PMFPlotter(args.datstring,args.outname,args.palette)

if args.Tchoice == True:

    TrackerPlot(args.datstring,0,args.outname,args.palette,args.WS,args.Bchoice,args.LastTime)
