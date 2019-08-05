#!/usr/bin/python

import random as rnd
from itertools import count

# Atom class
class Atom:

	_ids	=	count(0)

	# List of indices
	indexList	=	[]

	# Atom constructor takes no arguments as it randomly picks an atom from the list
	def __init__(self):

		self.id		=	next(self._ids)
		self.index	=	self.indexList[self.id]

	def setCoords(self, x, y, z):

		self.x	=	x
		self.y	=	y
		self.z	=	z

	def getCoords(self):

		return "X:" + str(self.x) + "\tY:" + str(self.y) + "\tZ:" + str(self.z)

	def addIndex(self, newIndex):

		self.indexList.append(str(newIndex))

# New list to append Atom objects to. The "name" of the Atom object can be thought of as the index of the list

atomList	=	[]

# Here we would append the indices from the data file to indexList i.e. with open(datafile, 'r') as df: for line in df: Atom.addIndex(line.split()[0])
# For proof of principle, we'll use this hard-coded list

Atom.indexList	=	[i for i in range(28,90,2)]

# Append new Atom objects to the list
# Here we would append the coords from the data file to the setCoords method in place of the hard-coded strings in place
for i in range(len(Atom.indexList)):

	atomList.append(Atom())
	atomList[i].setCoords("Coords", "from pdb", "or other")

# Print the index and coordinates of every atom in the list
for i in range(len(Atom.indexList)):

	print(str(atomList[i].index) + '\t' + str(atomList[i].getCoords()))
