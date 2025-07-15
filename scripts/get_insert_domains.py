#!/usr/bin/env python3
"""
Domain analysis script for finding nested domain pairs in TED data.
"""

import csv
import re
import sys
import os
import logging
from pathlib import Path

# Define cutoff for parent domain division
# Used in validate_parent_range
parent_fraction_cutoff = 0.25
# Define cutoff for length similarity
len_cutoff = 10
def parse_boundaries(bstr):
    return [tuple(map(int, part.split('-'))) for part in bstr.split('_')]

def is_inserted(insert_ranges, parent_ranges):
    '''Checks if one domain is inserted in another and that the parent domain
    is a discontinuous domain composed only of two ranges'''
    if len(parent_ranges) != 2:
        return False  # parent must be discontinuous AND exactly split into two 
    # Sort parent ranges by start
    parent_ranges = sorted(parent_ranges)
    # Compute gaps between parent segments
    gaps = []
    for (a_start, a_end), (b_start, b_end) in zip(parent_ranges, parent_ranges[1:]):
        gaps.append((a_end, b_start))  # gap is from end of one to start of next
    # Check if insert fits entirely inside one of the gaps
    if len(insert_ranges) != 1:
        return False  # insert must be continuous
    i_start, i_end = insert_ranges[0]
    for g_start, g_end in gaps:
        if g_start <= i_start and i_end <= g_end:
            return True
    return False

def validate_parent_range(range):
    '''Function to validate that the parent range is split by the insert
     domain not more that 90/10 or 10/90. 
      This avoids parent domains that are not really parent domains. 
       e.g. cases where it is split 98/2 and the insert is really just a duplication 
       Input: parsed_boundaries ex: [(338, 354), (586, 756)]'''
    len1 = (range[0][1]-range[0][0])+1
    len2 = (range[1][1]-range[1][0])+1
    total_len = len1+len2
    len1_fraction = len1/total_len
    len2_fraction = len2/total_len
    return len1_fraction >= parent_fraction_cutoff and len2_fraction >= parent_fraction_cutoff

def same_len_as_insert(prange, irange):
    '''Function that checks that parent domain is roughly the same as the insert domain'''
    plen1 = (prange[0][1]-prange[0][0])+1
    plen2 = (prange[1][1]-prange[1][0])+1
    total_plen = plen1+plen2
    ilen = (irange[0][1]-irange[0][0])+1
    return abs(total_plen - ilen) <= len_cutoff
        
    
def check_cath(cath):
    '''Check that the CATH is the full CATH down to homologous supergroup.
    Input: cath label as string.
    Returns: True if the CATH label has exactly 3 periods (i.e., 4 levels), else False.'''
    return cath.count('.') == 3

def main():
    # Input and output files
    #TED_data = '/home/gridsan/akolodziej/TED/ted_365m.domain_summary.cath.globularity.taxid.tsv'
    TED_data = sys.argv[1]
    #outfile = "nested_domain_pairs_hq.tsv"
    outfile = sys.argv[2]
    # Check if input file exists
    if not os.path.exists(TED_data):
        print(f"Input file {TED_data} not found")
        sys.exit(1)
    
    print(f"Processing {TED_data}")
    print(f"Output will be written to {outfile}")
    
    processed_lines = 0
    pairs_found = 0
    skipped_low_quality = 0
    
    with open(TED_data, 'r') as f_in, open(outfile, 'w', newline='') as f_out:
        
        writer = csv.writer(f_out, delimiter='\t')
        writer.writerow([
            'uniprot_id', 'parent_ted', 'parent_boundaries', 'parent_cath',
            'insert_ted', 'insert_boundaries', 'insert_cath'
        ])
        
        current_protein = None
        buffer = []
            
        for line in f_in:
            processed_lines += 1
            
            # Progress reporting
            if processed_lines % 10000 == 0:
                print(f"Processed {processed_lines} lines, found {pairs_found} nested pairs, skipped {skipped_low_quality} low quality")
            
            columns = line.strip().split('\t')
                
            # Check if columns is empty
            if not columns:
                continue
                
            # Check if there are enough columns
            if len(columns) < 14:
                continue
            
            #Extract CATH and if it's not full CATH, continue
            cath_id = columns[13]
            if not check_cath(cath_id):
                continue


            # Extract TED quality metric and check first
            quality = columns[2]
            if quality != 'high':
                skipped_low_quality += 1
                continue
                
            # Extract ted_id
            ted_id = columns[0]
            
            # Use regex to get the uniprot ID from the TED ID
            match = re.match(r'^AF-([^-]+)', ted_id)
            if not match:
                continue
            uniprot_id = match.group(1)
                
            # Get domain boundaries    
            domain_bounds = columns[3]
            
            
            if current_protein is not None and uniprot_id != current_protein:
                # Compare insert/parent within buffer
                for parent in buffer:
                    for insert in buffer:
                        # Comparing every entry in buffer, but don't need to compare self vs self, hence this if statement to continue if 
                        # they are the same.
                        if parent == insert:
                            continue
                        if is_inserted(insert['ranges'], parent['ranges']) and validate_parent_range(parent['ranges']) and same_len_as_insert(parent['ranges'], insert['ranges']):
                            writer.writerow([
                                current_protein,
                                parent['ted_id'], parent['boundaries'], parent['cath_id'],
                                insert['ted_id'], insert['boundaries'], insert['cath_id'],
                            ])
                            pairs_found += 1
                buffer = []  # reset buffer
            
            # Add current domain to buffer
            buffer.append({
                'ted_id': ted_id,
                'boundaries': domain_bounds,
                'ranges': parse_boundaries(domain_bounds),
                'cath_id': cath_id,
            })
            
            current_protein = uniprot_id
        
        # Don't forget to process the last group
        for parent in buffer:
            for insert in buffer:
                if parent == insert:
                    continue
                if is_inserted(insert['ranges'], parent['ranges']):  # Fixed function name
                    writer.writerow([
                        current_protein,
                        parent['ted_id'], parent['boundaries'], parent['cath_id'],
                        insert['ted_id'], insert['boundaries'], insert['cath_id'],
                    ])
                    pairs_found += 1
    
    print("Analysis complete!")
    print(f"Total lines processed: {processed_lines}")
    print(f"Total nested domain pairs found: {pairs_found}")
    print(f"Total low quality entries skipped: {skipped_low_quality}")
    print(f"Results written to: {outfile}")

if __name__ == "__main__":
    main()
