import sys
import os
import glob
from collections import defaultdict

from Bio import SeqIO


def create_name(record):
    return f"{record.id}_{'_'.join(record.description.split(',')[0].split())}"


print("############# GENE EXTRACTION FROM GB FILES ################")
if len(sys.argv) != 3:
    print("Usage:")
    print("python gene_extraction.py genbank_files_folder fasta_files_folder")
    print("Extracts protein sequences marked as CDS in genbank files.")
    print("Writes one fasta file corresponding per one genome.")
    print("Each sequence is named after genbank description plus a unique integer")
else:
    records = []

    for file in glob.glob(sys.argv[1] + "/*"):
        records.append(list(SeqIO.parse(file, "gb"))[0])
    print()
    print(f"Found {len(records)} records.")
    print()
    genes = defaultdict(list)
    for record in records:
        record_name = create_name(record)
        for feature in record.features:
            if feature.type == "CDS":
                try:
                    genes[record_name].append(feature.qualifiers["translation"][0])
                except KeyError:
                    pass
        print(f"Found {len(genes[record_name])} CDS in {record_name}")

    print()
    print(f"Writing to fasta files in {sys.argv[2]}")
    if not os.path.exists(sys.argv[2]):
        os.mkdir(sys.argv[2])
    for taxon, features in genes.items():
        with open(f"{sys.argv[2]}/{taxon}.fa", "w") as handle:
            for i, feature in enumerate(features):
                handle.write(f">{taxon}_{i+1}\n")
                handle.write(feature + "\n")
    print("Writing to fasta files done.")
