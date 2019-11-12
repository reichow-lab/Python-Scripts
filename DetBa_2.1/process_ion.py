# process_ion.py
# by Umair Khan
# Reichow Lab

# Slide together ion trajectories with ease.
# Usage: python process_ion.py [number of files] [output prefix] [list of input prefixes]

# Imports
import sys
import os
from tqdm import tqdm

# Get input arguments
num_files = int(sys.argv[1])
output_prefix = sys.argv[2]
input_prefixes = sys.argv[3:]
num_inputs = len(input_prefixes)

# For each input file, create a list keyed with the filename
# that contains each line of the input file as a list, with
# the first entry being the frame (as an int) and the second
# entry being the coordinate (as a str).
#
print("\nReading input files...")
input_dict = {}
for prefix in input_prefixes:
    for suffix in tqdm(range(num_files), ncols = 100, desc = prefix + "[n]"):
        input_dict[prefix + str(suffix)] = []
        lines = [line.rstrip().split() for line in open(prefix + str(suffix), "r")]
        for line in lines:
            input_dict[prefix + str(suffix)].append([int(line[0]), line[1]])

# For each prefix and suffix, get the final frame value of the
# previous prefix with the same suffix and add that value
# to each frame of the current file.
#
print("\nSliding...")
for i in range(1, num_inputs):
    for suffix in tqdm(range(num_files), ncols = 100, desc = input_prefixes[i] + "[n]"):
        offset = input_dict[input_prefixes[i - 1] + str(suffix)][-1][0] + 1
        for line in input_dict[input_prefixes[i] + str(suffix)]:
            line[0] += offset

# For each suffix, combine all the lines from the input prefixes
# as strings and then combine all of those strings, then write
# the result to the output prefix with the suffix.
#
print("\nWriting output files...")
for suffix in tqdm(range(num_files), ncols = 100, desc = output_prefix + "[n]"):
    split_files = []
    for prefix in input_prefixes:
        split_files.append("\n".join(["\t".join([str(line[0]), line[1]]) for line in input_dict[prefix + str(suffix)]]))
    with open(output_prefix + str(suffix), "w") as f:
        f.write("\n".join(split_files))

# For each input prefix and suffix combination, delete the file.
#
rm_input = input("\nWould you like to delete the input files? (y/n) ")
if rm_input == "y":
    print("\nDeleting input files...")
    for prefix in input_prefixes:
        for suffix in tqdm(range(num_files), ncols = 100, desc = prefix + "[n]"):
            os.remove(prefix + str(suffix))

# Line break for consistency
print("")
