import sys
import os

from Bio import SeqIO
from Bio import Entrez

print("############### GB FILE DOWNLOAD #################")

accessions = [x.strip() for x in open(sys.argv[1], "r").readlines()]
print(f"Downloading gb files for accession numbers:\n{accessions}")

Entrez.email = ""
entries = SeqIO.parse(
    Entrez.efetch(db="nucleotide", id=accessions, rettype="gb", retmode="text"), "gb"
)

folder_name = sys.argv[2]

if not os.path.exists(folder_name):
    os.mkdir(folder_name)

for entry in entries:
    print(f"Saving file {folder_name}/{entry.id}.gb")
    with open(f"{folder_name}/{entry.id}.gb", "w") as handle:
        SeqIO.write(entry, handle, "gb")
