########
# Script to align insert/parent domains using TM align with and without -cp
# Use to see if inserts are cps of parent domains
# USE CONDA ENVIRONMENT WITH FOLDCOMP INSTALLED: prog_mod WRITE IN THE RULE USING THIS SCRIPT!!!!!
##########

import sys
import csv
import os
import pandas as pd
import foldcomp
from pdbtools.pdb_selres_str import select_residues_from_string
sys.path.append('/home/gridsan/akolodziej/TM_tools/')
from TM_utils import TM_align

def convert_boundaries(input_str):
    ''' convert boundary str from foldcomp to one that works for pdbtools'''
    # Replace underscores with commas and hyphens with colons
    result = input_str.replace('_', ',').replace('-', ':')
    return result

data = sys.argv[1] #parent_insert_duplications.tsv
out_file = sys.argv[2] #parent_insert_CP_scores.tsv

df = pd.read_csv(data, sep ='\t')
print(f'Loaded {data} !')

af_name_bounds = {}
# loop through df
for index, row in df.iterrows():
    # Get parent_ted field
    parent_ted = row['parent_ted']
    # Remove the _TED suffix and anything after
    af_name = parent_ted.split('_TED')[0]
    # Get indices of the domains
    parent_bounds = row['parent_boundaries']
    insert_bounds = row['insert_boundaries']
    # Convert the boundaries to a format that pdbtools can use
    parent_bounds_cor = convert_boundaries(parent_bounds)
    insert_bounds_cor = convert_boundaries(insert_bounds)
   # print(f'Parsing {af_name}')
   # print(f'Corrected bounds for pdbtools parsing: {parent_bounds_cor}, {insert_bounds_cor}')

    bounds = [parent_bounds_cor,insert_bounds_cor]
    af_name_bounds[af_name] = bounds
    # Check to make sure the af_name is within the foldcomp database
    # TO DO
    # Is af_name within the foldcomp index? if not, continue to next row
    # TO DO
    # Use foldcomp to get the structure 

names = list(af_name_bounds.keys())
print('Put all af_names into a list!')

print('Loading Foldcomp database...') #Could try timing it here to see how long it takes to load?

with foldcomp.open("/home/gridsan/akolodziej/Foldcomp/afdb_uniprot_v4", ids = names) as db:
    for i in range(0,len(names)):
        pdb = db[i][1]
        #print(f'PDB: {pdb}')
        #name = db[i][0]
        #print(f'NAME: {name}')
        name = db[i][0].split('.cif')[0]
        if pdb is None:
                continue
        if pdb is not None:
            print(f'{name} pdb retrieved from foldcomp!')
        # Extract the two domains from the pdb
        # Use pdbtools to parse into domains
        parent_domain = select_residues_from_string(pdb, af_name_bounds[name][0])
        insert_domain = select_residues_from_string(pdb, af_name_bounds[name][1])
        if parent_domain is not None:
            print(f'Parent domain made with pdbtools!')
        if insert_domain is not None:
            print(f'Insert domain made with pdbtools!')
        # Write the two domains to pdb files
        parent_pdb = f'/home/gridsan/akolodziej/01_insert_domains/outputs/pdbs/{name}_parent.pdb'
        insert_pdb = f'/home/gridsan/akolodziej/01_insert_domains/outputs/pdbs/{name}_insert.pdb'
        if not os.path.exists(parent_pdb):
                with open(parent_pdb, "w") as f:
                    f.write(parent_domain)
        if not os.path.exists(insert_pdb):
                with open(insert_pdb, "w") as f:
                    f.write(insert_domain)  
        

        score = TM_align(parent_pdb, insert_pdb, cp=False)
        if score is None:
                print(f'ERROR: score: {score} is none!')
                continue
        single_score = max(list(score.values()))
        score_cp = TM_align(parent_pdb, insert_pdb, cp=True)
        single_score_cp = max(list(score_cp.values()))
        if single_score is not None:
                print(f'Score:{single_score}')
        if single_score_cp is not None:
                print(f'Score cp:{single_score_cp}')


        if single_score < single_score_cp:
                ### Write the af_name, score, and score_cp to a csv file
            with open(out_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([name, single_score, single_score_cp])
        
        if single_score >= single_score_cp:
            # Delete the parent_pdb and insert_pdb files, else, keep the files
            try:
                os.remove(parent_pdb)
                os.remove(insert_pdb)
                print(f"Deleted PDB files for {name} (score: {single_score} > score_cp: {single_score_cp})")
            except OSError as e:
                print(f"Error deleting files for {name}: {e}")
