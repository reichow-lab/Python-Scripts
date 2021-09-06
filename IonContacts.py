import MDAnalysis as mda
import numpy as np
import argparse
from glob import glob

# Parse inputs
parser = argparse.ArgumentParser()
parser.add_argument("-psf", dest="PSF", action="store")
parser.add_argument("-dat", dest="datstring", action="store")
parser.add_argument("-out", dest="outstring", action="store")
args = parser.parse_args()

# Create/sort list of trajectories
TrajList = glob(args.datstring+"*")
TrajList.sort()

# Create mda Universe
sys = mda.Universe(args.PSF, TrajList)

# Create dictionary with protein residues and their counts (0 at first)
prot = sys.select_atoms("protein")
chainA = prot.fragments[0]
ProtResDict = {}
for res in chainA.residues:
    ProtResDict[res.resname, str(res.resid)] = 0

# Create ndarray with all the interactions between protein and permeating ion
Contacts = []
for ts in sys.trajectory:
    prot = sys.select_atoms("protein and around 3 name POT")
    Contacts.append(prot.residues)

# Populate dictionary with protein-residue contact counts
for frame in Contacts:
    for res in frame:
        ProtResDict[res.resname, str(res.resid)] += 1

# Write out the results
with open(args.outstring+".txt", 'w') as out:
    for res in ProtResDict:
        out.write(f"{res[1]}\t{ProtResDict[res]}\n")
