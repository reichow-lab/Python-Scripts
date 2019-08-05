#!/home/bassam/anaconda3/envs/matt/bin/python

# trace.py
# by Umair Khan
# Reichow Lab

# 3D plotting experiments.


# Imports
import sys
import marshal
import operator
import numpy as np
import plotly.graph_objects as go

# Get file to load from
filename = input("Enter the name of the data file to use: ")
x = []
y = []
z = []

# Read data from file
# (each line is formatted "x y z")
with open(filename, "r") as f:
	
	# Go through each line
	for line in f:
	
		# Append to appropriate lists
		line = line.split()
		x.append(float(line[0]))
		y.append(float(line[1]))
		z.append(float(line[2]))
		
print("Loaded trajectory...")


# Plot trace
data = [go.Scatter3d(
	x = x,
	y = y,
	z = z,
	mode = "lines",
	line = dict(
		width = 1,
		color = list(range(0, 12500)),
		colorscale = "Viridis",
		colorbar = dict(thickness = 20)
		)
	)
]

figure = go.Figure(data = data)
figure.show()
