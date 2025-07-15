rule parent_insert_duplications:
    input:
        insertion_data = config["uniref50_nested_domain_pairs"]
    output:
        parent_insert_duplications = config["parent_insert_duplications"],
    resources:
        mem_mb=4000,
        time_min=10,
        cpus_per_task=1
    log:
        "logs/parent_insert_dup.log"
    shell:
        "python -u scripts/parent_insert_duplications.py {input.insertion_data} {output.parent_insert_duplications} &> logs/parent_insert_dup.log"
