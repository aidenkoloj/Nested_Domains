rule make_uniref50_dictionary:
    input:
        data=config["uniref50_xml"]
    output:
        dictionary=config["uniref50_dict"]
    resources:
        mem_mb=64000,        # 64GB memory
        time_min=1200,        # 12 hour time limit
        cpus_per_task=1     # 1 CPU
    log:
        "logs/uniref50_dictionary.log"
    shell:
        "python -u scripts/uniref50_to_dict.py {input.data} {output.dictionary} &> {log}"
