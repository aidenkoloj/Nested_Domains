rule count_caths:
    input:
        insertion_data = config["uniref50_nested_domain_pairs"]
    output:
        insert_cath_counts = config["insert_cath_counts"],
        parent_cath_counts = config["parent_cath_counts"]
    resources:
        mem_mb=8000,
        time_min=120,
        cpus_per_task=1
    log:
        "logs/count_caths.log"
    shell:
        "python -u scripts/count_caths.py {input.insertion_data} {output.insert_cath_counts} {output.parent_cath_counts} &> logs/count_caths.log"
