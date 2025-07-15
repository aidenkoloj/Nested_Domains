rule get_insert_domains:
    input:
        domains = config["TED_domains"]
    output:
        nested_domains = temp(config["nested_domain_pairs"])
    resources:
        mem_mb = 32000,
        time_min = 120,
        cpus_per_task = 1 
    log:
        "logs/get_insert_domains.log"
    shell:
        "python -u scripts/get_insert_domains.py {input.domains} {output.nested_domains} &> {log}"
