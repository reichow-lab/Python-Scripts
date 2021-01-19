import matplotlib.pyplot as plt
import numpy as np
from sys import argv
script, matfile = argv

matrix = np.load(matfile, allow_pickle=True)
plt.imshow(matrix)
plt.show()
