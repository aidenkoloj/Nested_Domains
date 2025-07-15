rule testing_snakemake_slurm:
    input:
        pdb_in=config["test_pdb"]
    output:
        pdb_out=config["test_pdb_out"]
    resources:
        mem_mb=4000,        # 4GB memory
        time_min=60,        # 1 hour time limit
        cpus_per_task=1     # 1 CPU
    shell:
        "python scripts/testing_snakemake_slurm.py {input.pdb_in} {output.pdb_out}"
