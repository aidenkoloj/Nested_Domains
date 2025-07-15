rule popular_inserts:
    input:
        insertion_data = config["uniref50_nested_domain_pairs"]
    output:
        popular_inserts = config["popular_inserts"],
    resources:
        mem_mb=64000,
        time_min=180,
        cpus_per_task=1
    log:
        "logs/pop_inserts.log"
    shell:
        "python -u scripts/popular_inserts.py {input.insertion_data} {output.popular_inserts} &> logs/pop_inserts.log"
