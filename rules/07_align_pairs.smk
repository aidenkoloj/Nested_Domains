rule align_pairs:
    input:
        parent_insert_dups = config["parent_insert_duplications"]
    output:
        parent_insert_CP_scores = config["parent_insert_CP_scores"],
    conda:
        "prog_mod"
    resources:
        mem_mb=64000,
        time_min=720,
        cpus_per_task=1
    log:
        "logs/align_pairs.log"
    shell:
        "python -u scripts/align_pairs.py {input.parent_insert_dups} {output.parent_insert_CP_scores} &> logs/align_pairs.log"
