# Parent/Insert Domain Dataset Pipeline

This Snakemake pipeline generates a comprehensive dataset of parent/insert domains with carefully controlled structural constraints.

## Overview

The pipeline processes TED domain data and UniRef50 sequences to identify and catalog domain insertion events, producing a dataset suitable for structural biology and evolutionary analysis.

## Dataset Constraints

The generated dataset is filtered according to the following key constraints:

1. **Length Similarity**: Parent domain length ≈ insert domain length (within 10 amino acids)
2. **Discontinuity Threshold**: >0.25% discontinuity (parent domain cannot be divided greater than 75/25 ratio)

## Required Input Data

Configure the following paths in your config file:

### Starting Inputs

```yaml
# Database of TED domains
TED_domains: '/home/gridsan/akolodziej/TED/ted_365m.domain_summary.cath.globularity.taxid.tsv'

# UniRef50 database
uniref50_xml: '/home/gridsan/akolodziej/solab_shared/uniref50/uniref50.xml.gz'
```

## Usage

1. Update the input file paths in your configuration file
2. Create a conda environment for rule 07_align_pairs.smk that includes [Foldcomp](https://github.com/steineggerlab/foldcomp), [pdbtools](https://github.com/haddocking/pdb-tools) and [TMtools](https://github.com/haddocking/pdb-tools)
3. Run the pipeline with Snakemake:
   ```bash
   snakemake --executor slurm --jobs 5 -n -p --verbose --use-conda
   ```

## Output

The pipeline generates a structured dataset containing parent/insert domain pairs that meet the specified length and discontinuity constraints, suitable for downstream structural and evolutionary analyses.
