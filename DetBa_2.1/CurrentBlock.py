import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from glob import glob
from sys import argv
import pandas as pd
script, system, N = argv
FileList = glob(system+"*Tracking.log")
    FileList.sort()
for FILE in FileList:
    with open(FILE, 'r') as file:
        all_lines = f.read().splitlines()
    
