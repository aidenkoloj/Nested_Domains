rule intersect_with_uniref50:
    input:
        uniref50_dict = config["uniref50_dict"],
        nested_domains = config["nested_domain_pairs"]
    output:
        uniref50_nested_domains = config["uniref50_nested_domain_pairs"],
        unmapped_uniprot_ids = config["unmapped_uniprot_ids"],
        uniref50_frequency = config["uniref50_frequency"]
    resources:
        mem_mb=32000,
        time_min=60, # 1 hours 
        cpus_per_task=1
    log:
        "logs/intersect_with_uniref50.log"

    shell:
        """
        python -u scripts/intersect_nested_domain_pairs.py {input.uniref50_dict} {input.nested_domains} \
{output.uniref50_nested_domains} {output.unmapped_uniprot_ids} {output.uniref50_frequency} &> logs/intersect_with_uniref50.log 
        """ 
