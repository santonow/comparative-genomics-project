import sys
import os
from collections import defaultdict

print("############# CLUSTER EXTRACTION ############")

if len(sys.argv) < 4:
    print("Usage:")
    print("python extract_clusters.py tsv_file fasta_file target_fasta_folder")


def trim_number(s):
    return "_".join(s.split("_")[:-1])


with open(sys.argv[1], "r") as handle:
    clusters = defaultdict(list)
    for line in handle:
        cluster_repr, cluster_member = line.strip().split()
        clusters[cluster_repr].append(cluster_member)

print(f"Initial number of clusters: {len(clusters)}.")

clusters_filtered = {
    cluster_repr: members
    for cluster_repr, members in clusters.items()
    if len(members) > 3
    and (len(members) == len(set([trim_number(x) for x in members])))
}

print(
    f"Number of clusters after filtering out clusters with less than 4 sequences and those with repeating taxons: {len(clusters_filtered)}."
)

sequences_clustered = {}

with open(sys.argv[2], "r") as handle:
    line = next(handle).strip().lstrip(">")
    next_line = next(handle).strip().lstrip(">")
    next_next_line = None
    curr_seqs = []
    for i, l in enumerate(handle):
        if l.startswith(">"):
            if not next_next_line:
                next_next_line = l.strip().lstrip(">")
            else:
                next_line = next_next_line
                next_next_line = l.strip().lstrip(">")
            if next_line == next_next_line:
                if line in clusters_filtered:
                    sequences_clustered[line] = curr_seqs
                curr_seqs = []
                line = next_line.lstrip(">")
        else:
            if not next_next_line:
                curr_seqs.append((next_line, l.strip()))
            else:
                curr_seqs.append((next_next_line, l.strip()))

if not os.path.exists(sys.argv[3]):
    os.mkdir(sys.argv[3])

for i, (cluster_center, cluster_members) in enumerate(sequences_clustered.items()):
    with open(sys.argv[3] + f"/cluster{i}.fasta", "w") as handle:
        for gene, sequence in cluster_members:
            handle.write(f">{trim_number(gene)}\n")
            handle.write(sequence + "\n")

print(f"Writing clusters to fasta files in {sys.argv[3]} done.")
