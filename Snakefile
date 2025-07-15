configfile: "config/config.yml"

rule all:
    input:
        config["uniref50_dict"],
        config["nested_domain_pairs"],
        config["uniref50_nested_domain_pairs"],
        config["insert_cath_counts"],
        config["popular_inserts"],
        config["parent_insert_duplications"],
        config["parent_insert_CP_scores"]
        
include: "rules/01_make_uniref50_dictionary.smk"
include: "rules/02_get_insert_domains.smk"
include: "rules/03_intersect_with_uniref50.smk"
include: "rules/04_count_caths.smk"
include: "rules/05_popular_inserts.smk"
include: "rules/06_parent_insert_duplicates.smk"
include: "rules/07_align_pairs.smk"