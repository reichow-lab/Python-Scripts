import numpy as np
from glob import glob
from sys import argv
import pickle as pkl
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from scipy.interpolate import interp1d
from TrackerPlot import TrackerPlot
# Parse inputs
parser = argparse.ArgumentParser()
parser.add_argument("-dat", dest = "datstring", action = "store")
parser.add_argument("-out", dest = "outname", action = "store", default = "OUTFILE")
parser.add_argument("-min", dest = "min", action = "store", type = int, default = "45")
parser.add_argument("-max", dest = "max", action = "store", type = int, default = "60")
parser.add_argument("-lt", dest = "LastTime", action = "store", type=int, default = 1800)
parser.add_argument("-ws", "--windowsize", dest = "WS", type=int, action = "store", default = 100)
parser.add_argument("-t", dest = "tchoice", type=bool, action="store", default=False)
parser.add_argument("-apbs", dest = "apbs", type=bool, action="store", default=False)
parser.add_argument("-as", dest = "apbsdat", action = "store")
parser.add_argument("-hole", dest = "hole", type=bool, action="store", default=False)
args = parser.parse_args()

def Interp(xin,yin,LT):
    f = interp1d(xin,yin,kind="previous")
    xnew = np.arange(0,LT,1)
    ynew = f(xnew)
    return xnew,ynew
if args.hole:
    # Create list of the appropriate HOLE files

    hole_file_list = glob(args.datstring)
    hole_file_list.sort()

    # Load HOLE output files
    up_lim  = 75
    low_lim = -75
    Pore_Radii = []
    Pore_Axis  = np.arange(-75,76)
    Pore_Radii_Time = [[],[],[]]
    print(len(hole_file_list))
    # Extract relevant data from HOLE output files
    h = 0
    for hole_file in hole_file_list:
        with open(hole_file) as FileIN:
            temp_radii = []
            for line in FileIN:
                val = line.split()
                if (float(val[0]) <= up_lim and float(val[0]) >= low_lim):
                    temp_radii.append(float(val[1]))
                    Pore_Radii_Time[0].append(float(val[0]))
                    Pore_Radii_Time[1].append(float(val[1]))
                    Pore_Radii_Time[2].append(h)
            if len(temp_radii) > 0:
                Pore_Radii.append(temp_radii)
            h += 1
    print(h)
    # define pore-region of interest, and record the averages through time.
    # Pore_UpVsLow: [[Time (ns)],[Upper Avg],[Lower Avg]]
    Pore_UpVsLow = [[],[],[]]
    for i in range(h):
        hold_upper, hold_lower = [], []
        for j in range(len(Pore_Radii_Time[0])):
            # separate the two halves of the channel.
            if Pore_Radii_Time[2][j] == i and Pore_Radii_Time[0][j] <= args.max and Pore_Radii_Time[0][j] >= args.min:
                hold_upper.append(Pore_Radii_Time[1][j])
            elif Pore_Radii_Time[2][j] == i and Pore_Radii_Time[0][j] >= (-1*args.max) and Pore_Radii_Time[0][j] <= (-1*args.min):
                hold_lower.append(Pore_Radii_Time[1][j])
        Pore_UpVsLow[0].append(i*10)
        Pore_UpVsLow[1].append(np.min(hold_upper))
        Pore_UpVsLow[2].append(np.min(hold_lower))
    #fss Save Extracted data for future processing
    with open(str(args.outname + '_data.pkl'), 'wb') as out:
        pkl.dump(Pore_Radii, out)
        pkl.dump(Pore_Axis, out)
    with open(str(args.outname + '_Time.pkl'), 'wb') as out:
        pkl.dump(Pore_Radii_Time, out)
    # Calculate sliding window average
    HUx, HUy = Interp(Pore_UpVsLow[0],Pore_UpVsLow[1],args.LastTime)
    HLx, HLy = Interp(Pore_UpVsLow[0],Pore_UpVsLow[2],args.LastTime)
    WinAVG = [[],[],[]]
    for i in range(len(HUx)-args.WS):
        WinAVG[0].append(HUx[i])
        holdU, holdL = [], []
        for j in range(args.WS):
            holdU.append(float(HUy[i+j]))
            holdL.append(float(HLy[i+j]))
        WinAVG[1].append(np.mean(holdU))
        WinAVG[2].append(np.mean(holdL))

    PoreRadiiDF = pd.DataFrame({"Pore Axis": Pore_Radii_Time[0], "Pore Radii": Pore_Radii_Time[1]})
    PoreTimeDF  = pd.DataFrame({"Time (ns)": WinAVG[0], "Upper Radii (Å)": WinAVG[1], "Lower Radii (Å)": WinAVG[2]})
    plt.xlabel("Pore Axis")
    #plt.xlim(-80,80)
    #plt.ylim(0,18)
    plt.ylabel('Pore Radii')
    sns.lineplot(data=PoreRadiiDF, x="Pore Axis", y="Pore Radii", hue=Pore_Radii_Time[2])
    plt.savefig(args.outname+"_HOLE_TTime.png", dpi=400)
    plt.clf()
    plt.xlabel("Time (ns)")
    plt.ylabel('Pore Radii (Å)')
    #plt.ylim(0,18)
    sns.lineplot(data=PoreTimeDF, x="Time (ns)", y="Upper Radii (Å)",label='Upper Half',legend=False, color="#00A6ED")
    sns.lineplot(data=PoreTimeDF, x="Time (ns)", y="Lower Radii (Å)",label='Lower Half',legend=False, color="#F6511D")
    plt.legend()
    plt.savefig(args.outname+"_HOLE_RTime.png", dpi=400)
    plt.clf()
    with open(args.outname+"_HOLE_RTime.txt", 'w') as out:
        out.write("Time (ns)\tUpper Radii (Å)\tLower Radii (Å)\n")
        for i in range(len(Pore_UpVsLow[0])):
            out.write(f"{Pore_UpVsLow[0][i]}\t{Pore_UpVsLow[1][i]}\t{Pore_UpVsLow[2][i]}\n")
if args.tchoice and args.hole:
    IonWindow = TrackerPlot("Cx",0,args.outname,"Blues_r",args.WS,False,args.LastTime,1,"N/A",False)
    #Final: [[Ionic Current],[UpperHole],[LowerHole]]
    Final = [[],[],[]]
    for i in range(len(WinAVG[0])):
        Final[0].append(IonWindow[1][i])
        Final[1].append(WinAVG[1][i])
        Final[2].append(WinAVG[2][i])
    FinalDF = pd.DataFrame({"Time (ns)": WinAVG[0], "Ionic Current (pA)": Final[0], "Upper Radii (Å)": Final[1], "Lower Radii (Å)": Final[2]})
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    plt.xlabel("Time (ns)")
    #plt.ylim(0,18)
    ax = sns.lineplot(data=FinalDF,x="Time (ns)",y="Upper Radii (Å)",ax=ax,color="#00A6ED",label='Upper Radii',legend=False,linewidth=1.5)
    ax = sns.lineplot(data=FinalDF,x="Time (ns)",y="Lower Radii (Å)",ax=ax,color="#7D5BA6",label='Lower Radii',legend=False,linewidth=1.5)
    ax2 = sns.lineplot(data=FinalDF,x="Time (ns)",y="Ionic Current (pA)",ax=ax2,color="#F6511D",label='Current',legend=False,linewidth=1)
    fig.set_size_inches(8, 8)
    fig.legend()
    plt.savefig(args.outname+"_HoleVsCurr_line.png", dpi=400)
    plt.clf()
if args.apbs:
    # Unpickle the APBS data.
    APBSFILE = glob(args.apbsdat)
    with open(APBSFILE[0], 'rb') as datin:
    	CenterPots = pkl.load(datin)
    	CenterPore = pkl.load(datin)
    # Load HOLE output files
    up_lim  = 75
    low_lim = -75
    Pore_Potential = []
    Pore_Axis  = np.arange(-75,76)
    Pore_Potential_Time = [[],[],[]]
    # Extract relevant data from HOLE output files
    h = 0
    for potfile in CenterPots:
        temp_Potential = []
        for i in range(len(CenterPore)):
            if (float(CenterPore[i]) <= up_lim and float(CenterPore[i]) >= low_lim):
                temp_Potential.append(float(potfile[i]))
                Pore_Potential_Time[0].append(float(CenterPore[i]))
                Pore_Potential_Time[1].append(float(potfile[i]))
                Pore_Potential_Time[2].append(h)
        if len(temp_Potential) > 0:
            Pore_Potential.append(temp_Potential)
        h += 1
    print(h)
    # define pore-region of interest, and record the averages through time.
    # Pore_UpVsLow: [[Time (ns)],[Upper Avg],[Lower Avg]]
    Pore_UpVsLow = [[],[],[]]
    for i in range(h):
        hold_upper, hold_lower = [], []
        for j in range(len(Pore_Potential_Time[0])):
            # separate the two halves of the channel.
            if Pore_Potential_Time[2][j] == i and Pore_Potential_Time[0][j] <= args.max and Pore_Potential_Time[0][j] >= args.min:
                hold_upper.append(Pore_Potential_Time[1][j])
            elif Pore_Potential_Time[2][j] == i and Pore_Potential_Time[0][j] >= (-1*args.max) and Pore_Potential_Time[0][j] <= (-1*args.min):
                hold_lower.append(Pore_Potential_Time[1][j])
        Pore_UpVsLow[0].append(i*10)
        Pore_UpVsLow[1].append(np.min(hold_upper))
        Pore_UpVsLow[2].append(np.min(hold_lower))

    # Calculate sliding window average
    HUx, HUy = Interp(Pore_UpVsLow[0],Pore_UpVsLow[1],args.LastTime)
    HLx, HLy = Interp(Pore_UpVsLow[0],Pore_UpVsLow[2],args.LastTime)
    WinAVG = [[],[],[]]
    for i in range(len(HUx)-args.WS):
        WinAVG[0].append(HUx[i])
        holdU, holdL = [], []
        for j in range(args.WS):
            holdU.append(float(HUy[i+j]))
            holdL.append(float(HLy[i+j]))
        WinAVG[1].append(np.mean(holdU))
        WinAVG[2].append(np.mean(holdL))

    PoreRadiiDF = pd.DataFrame({"Pore Axis": Pore_Potential_Time[0], "Pore Radii": Pore_Potential_Time[1]})
    PoreTimeDF  = pd.DataFrame({"Time (ns)": WinAVG[0], "Upper Radii (Å)": WinAVG[1], "Lower Radii (Å)": WinAVG[2]})
    plt.xlabel("Pore Axis")
    plt.ylabel('Pore Radii')
    sns.lineplot(data=PoreRadiiDF, x="Pore Axis", y="Pore Radii", hue=Pore_Potential_Time[2])
    plt.savefig(args.outname+"_APBS_TTime.png", dpi=400)
    plt.clf()
    plt.xlabel("Time (ns)")
    plt.ylabel('Pore Radii (Å)')
    sns.lineplot(data=PoreTimeDF, x="Time (ns)", y="Upper Radii (Å)",label='Upper Half',legend=False, color="#00A6ED")
    sns.lineplot(data=PoreTimeDF, x="Time (ns)", y="Lower Radii (Å)",label='Lower Half',legend=False, color="#F6511D")
    plt.legend()
    plt.savefig(args.outname+"_APBS_RTime.png", dpi=400)
    plt.clf()
    with open(args.outname+"_APBS_RTime.txt", 'w') as out:
        out.write("Time (ns)\tUpper Radii (Å)\tLower Radii (Å)\n")
        for i in range(len(Pore_UpVsLow[0])):
            out.write(f"{Pore_UpVsLow[0][i]}\t{Pore_UpVsLow[1][i]}\t{Pore_UpVsLow[2][i]}\n")
if args.tchoice and args.apbs:
    IonWindow = TrackerPlot("Cx",0,args.outname,"Blues_r",args.WS,False,args.LastTime,1,"N/A",False)
    #Final: [[Ionic Current],[UpperHole],[LowerHole]]
    Final = [[],[],[]]
    for i in range(len(WinAVG[0])):
        Final[0].append(IonWindow[1][i])
        Final[1].append(WinAVG[1][i])
        Final[2].append(WinAVG[2][i])
    FinalDF = pd.DataFrame({"Time (ns)": WinAVG[0], "Ionic Current (pA)": Final[0], "Upper Potential (Kcal/mol)": Final[1], "Lower Potential (Kcal/mol)": Final[2]})
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    plt.xlabel("Time (ns)")
    #plt.ylim(-150,150)
    ax = sns.lineplot(data=FinalDF,x="Time (ns)",y="Upper Potential (Kcal/mol)",ax=ax,color="#00A6ED",label='Upper Potential (Kcal/mol)',legend=False,linewidth=1.5)
    ax = sns.lineplot(data=FinalDF,x="Time (ns)",y="Lower Potential (Kcal/mol)",ax=ax,color="#7D5BA6",label='Lower Potential (Kcal/mol)',legend=False,linewidth=1.5)
    ax2 = sns.lineplot(data=FinalDF,x="Time (ns)",y="Ionic Current (pA)",ax=ax2,color="#F6511D",label='Current',legend=False,linewidth=1)
    fig.set_size_inches(8, 8)
    fig.legend()
    plt.savefig(args.outname+"_APBSVsCurr_line.png", dpi=400)
    plt.clf()
