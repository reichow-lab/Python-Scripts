#!/home/bassam/anaconda3/bin/python
from glob import glob
from sys import argv
import statistics as st
from math import sqrt

script, globstring, outname = argv

# globstring - regular expression string

# Import all relevant files
filelist    = glob(globstring)
filelist.sort()

out = open(outname, 'w')
out.write('Frame\tElecAvg\tElec95-C.I.\tVdWAvg\tVdW95-C.I.\tTotalAvg\tTotal95-C.I.\tFile-Name\n')

for FILE in filelist:

    framecount  = 0
    ElecList    = []
    VdWList     = []
    NonbondList = []
    TotalList   = []

    with open(FILE) as FILEin:

        next(FILEin)
        for line in FILEin:

            col     = line.split()

            # Input file has columns:       Frame     Time      Elec      VdW     Nonbond     Total

            framecount  = int(col[0])
            ElecList.append(float(col[2]))
            VdWList.append(float(col[3]))
            NonbondList.append(float(col[4]))
            TotalList.append(float(col[5]))

    Frame       = framecount + 1

    ElecAvg     = st.mean(ElecList)
    ElecStDev   = st.stdev(ElecList)
    ElecStErr   = ElecStDev / sqrt(Frame)
    Elec95CI    = 1.96 * ElecStErr

    VdWAvg      = st.mean(VdWList)
    VdWStDev    = st.stdev(VdWList)
    VdWStErr    = VdWStDev / sqrt(Frame)
    VdW95CI     = 1.96 * VdWStErr

    TotalAvg    = st.mean(TotalList)
    TotalStDev  = st.stdev(TotalList)
    TotalStErr  = TotalStDev / sqrt(Frame)
    Total95CI   = 1.96 * TotalStErr

    out.write(str(Frame) + '\t' + str(ElecAvg) + '\t' + str(Elec95CI) + '\t' + str(VdWAvg) + '\t' + str(VdW95CI) + '\t' + str(TotalAvg) + '\t' + str(Total95CI) + '\t' + str(FILE) + '\n')
out.close()
