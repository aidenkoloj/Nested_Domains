import pickle
import csv
from collections import defaultdict
import sys

### Script to intersect nested_domain_pairs with the uniref50 database 
### In other words, deduplicated the nested_domain pairs dataset

# Input variables

uniref50_dictionary = sys.argv[1]
nested_domains = sys.argv[2]

# Output variables

uniref50_nested_domains = sys.argv[3]
unmapped_uniprot_ids_out = sys.argv[4]
uniref50_frequency = sys.argv[5]

# Load UniProt -> UniRef50 mapping
with open(uniref50_dictionary, "rb") as f:
    uniprot_to_uniref = pickle.load(f)
print(f"Loaded dictionary with {len(uniprot_to_uniref):,} entries")

# Track seen clusters, unmapped IDs, row counts, and frequencies
seen_clusters = set()
unmapped_uniprot_ids = []
uniref50_freq = defaultdict(int)

total_rows = 0
written_rows = 0
print_interval = 100_000  # lines

# Open input TSV and output TSV
with open(nested_domains, "r") as in_f, open(uniref50_nested_domains, "w", newline='') as out_f:
    reader = csv.reader(in_f, delimiter='\t')
    writer = csv.writer(out_f, delimiter='\t')

    header = next(reader)
    writer.writerow(header)

    if 'uniprot_id' in header:
        uniprot_idx = header.index('uniprot_id')
    else:
        raise ValueError("No 'uniprot_id' column found in header.")

    for row in reader:
        total_rows += 1
        if total_rows % print_interval == 0:
            print(f"Processed {total_rows:,} rows...")

        if not row or len(row) <= uniprot_idx:
            continue

        uniprot_id = row[uniprot_idx]
        uniref50_id = uniprot_to_uniref.get(uniprot_id)

        if not uniref50_id:
            ## Keep track of unmapped uniprot ids, but still add these to the output tsv
            unmapped_uniprot_ids.append(uniprot_id)
            writer.writerow(row)
            written_rows += 1
            continue
            
        # Count frequency
        uniref50_freq[uniref50_id] += 1

        # Write the first row per cluster
        if uniref50_id not in seen_clusters:
            seen_clusters.add(uniref50_id)
            writer.writerow(row)
            written_rows += 1

# Save unmapped UniProt IDs
with open(unmapped_uniprot_ids_out, "w") as f:
    for uid in unmapped_uniprot_ids:
        f.write(uid + "\n")

# Save UniRef50 frequency counts
with open(uniref50_frequency, "w", newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(["UniRef50_ID", "Count"])
    for uid, count in sorted(uniref50_freq.items(), key=lambda x: -x[1]):
        writer.writerow([uid, count])

# Summary
print("Processing complete")
print(f"Total rows in original TSV (excluding header): {total_rows:,}")
print(f"Rows written to filtered output: {written_rows:,}")
print(f"Unique UniRef50 clusters written: {len(seen_clusters):,}")
print(f"Frequency counts saved to 'uniref50_frequency.tsv'")
print(f"UniProt IDs with no UniRef50 mapping: {len(unmapped_uniprot_ids):,} (saved to 'unmapped_uniprot_ids.txt')")
