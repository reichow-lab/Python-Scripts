#!/Users/bassam/miniconda3/bin/python
import pickle as pkl
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-dat", dest="DataIN", action="store")
parser.add_argument("-out", dest="outname", action="store")
parser.add_argument("-MM", "--MaxM", dest="MaxM", action="store", default=10)
args = parser.parse_args()

# If these analyses prove well, then I will fillout this program, otherwise it will
# work as an ad-hoc way to calculate error in HOLE profile data. Ideally this method
# Could be used for any of the data that we present that's a time (1D or 2D)

#def Block1D():

def Block2D(M, InArray, Pore):
    n = len(InArray)     # number of elements
    bl = int(n/M)       # block length
    cut = n%M
    for i in range(0,cut,1):
        InArray = np.delete(InArray, 0, 1)
    # Create list containing blocks
    bList = [[] for x in range(int(M))]
    # Populate each block with 'bl' elements
    for i in range(int(M)):
        for e in range(0,bl,1):
            e = e + i*bl
            bList[i].append(InArray[e])
    AvgList = []
    for i in range(int(M)):
        AvgList.append(np.mean(bList[i], axis=0))
    if M == 4:
        with open((args.outname+"_"+str(M)+"_final.txt"))
    Final = [[],[]]
    Final[0].append(np.mean(AvgList, axis=0))
    Final[1].append(np.std(AvgList, axis=0)/np.sqrt(M))
    with open((args.outname+'_'+str(M)+'.txt'), 'w') as out:
        for i,j,k in zip(Pore,Final[0][0],Final[1][0]):
            out.write(str(i)+'\t'+str(j)+'\t'+str(k)+'\n')
    return(Final)

# Load in pickled HOLE data (2D Array)
with open(args.DataIN, 'rb') as infile:
    Data = pkl.load(infile)
    Pore = pkl.load(infile)
# Block Size list
BSL = np.arange(1,(int(args.MaxM) + 1),1)
ErrBs = [[],[]]
for M in BSL:
    temp = Block2D(M,Data,Pore)
    ErrBs[0].append(M)
    ErrBs[1].append(np.sum(temp[1]))
with open((args.outname+'.txt'), 'w') as out:
    for i,j in zip(ErrBs[0],ErrBs[1]):
        out.write(str(i)+'\t'+str(j)+'\n')
