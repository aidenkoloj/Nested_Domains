

#########################
#
# Script counts that frequency of a given CATH domain as an insert or parent domain
# AND counts the frequency of a given CATH appearing as an insertion that is a duplication of the parent domain
#########################

import sys
import pandas as pd

# Inputs
insertion_data = sys.argv[1]

# Outputs
insert_cath_counts_out = sys.argv[2]
parent_cath_counts_out = sys.argv[3]

# Load tab-delimited data
df = pd.read_csv(insertion_data, sep="\t", comment="#")

# Filter out rows with fewer than 7 columns
df = df[df.apply(lambda row: row.notna().sum() >= 7, axis=1)]
# Strip whitespace
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
# Filter out empty rows
df = df.dropna(how="all")

# Count non-missing insert CATH (column 6)
insert_cath_counts = (
    df['insert_cath'][(df['insert_cath'] != "-") & (df['insert_cath'].notna())]
    .value_counts()
    .reset_index(name="insert_count")
)

# Count non-missing parent CATH (column 3)
parent_cath_counts = (
    df['parent_cath'][(df['parent_cath'] != "-") & (df['parent_cath'].notna())]
    .value_counts()
    .reset_index(name="parent_count")
)

#Save to CSV
parent_cath_counts.to_csv(parent_cath_counts_out, index=False)
print(f'Saved {parent_cath_counts_out}!')

#### Count insertion duplicates
print('Calculating insertion duplicates...')
duplicates = df[df['insert_cath'] == df['parent_cath']].groupby('insert_cath').size().reset_index(name='insert_duplicate_count')
df_insert_dups = insert_cath_counts.merge(duplicates, on='insert_cath', how='left').fillna(0)
df_insert_dups['insert_duplicate_count'] = df_insert_dups['insert_duplicate_count'].astype(int)

#save to CSV
df_insert_dups.to_csv(insert_cath_counts_out, index=False)
print(f'Saved {insert_cath_counts_out}!')
