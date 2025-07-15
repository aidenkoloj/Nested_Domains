#########
# Script to get a .tsv of nested domains where the parent and the insert are the same CATH
#
#########

import sys
import pandas as pd

data = sys.argv[1]
out = sys.argv[2]

df = pd.read_csv(data, sep ='\t')

# Get rows with parent  == insert
parent_insert_duplicates = df[df['parent_cath'] == df['insert_cath']]

# Save to file
parent_insert_duplicates.to_csv(out, sep='\t', index=False)
print("Saved instances of parent = insert domains!")