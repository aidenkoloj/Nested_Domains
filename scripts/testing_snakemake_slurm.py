# Test script for snakemake slurm function

import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

# Read input file line by line and write lines that start with "ATOM" to output file
with open(input_file, 'r') as f, open(output_file, 'w') as out_f:
    for line in f:
        if line.startswith("ATOM"):
            out_f.write(line)

