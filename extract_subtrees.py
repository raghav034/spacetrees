
import subprocess
anc="data/SGDP_aDNA_new_chr2.anc"
mut="data/SGDP_aDNA_new_chr2.mut"
poplabels="data/contemporary_nw_samples_only.poplabels"

populations = set()  # Use a set to ensure uniqueness

with open(poplabels, "r") as pop:
    next(pop) #Skip header
    for line in pop:
        if line.strip():  # Skip empty lines
            parts = line.strip().split()
            if len(parts) >= 2:
                populations.add(parts[1])  # Get second column

pop_string = ",".join(populations)
print(pop_string)

subprocess.run([
    "relate/bin/RelateExtract",
    "--mode", "SubTreesForSubpopulation",
    "--anc", anc,
    "--mut", mut,
    "--poplabels", poplabels,
    "--pop_of_interest", pop_string,
    "-o", "data/contemporary_nw_samples_only_extracted"
])