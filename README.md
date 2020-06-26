# comparative-genomics-project
Project for Comparative Genomics classes.

Github repo: https://github.com/santonow/comparative-genomics-project

## Requirements
- `python>=3.6`
- `BioPython`
- `MMseqs2`
- `MAFFT`
- `RAxML`
- `fasturec2`

The `fasturec2` has to reside in a folder `superdrzewa_soft` (not included in this repo).

## Usage of `generate_trees.sh` script

The script takes two positional parameters:
- A file with accession numbers. The corresponding genbank files will be downloaded by the script.
- A number of threads to use.

For example:

```bash
bash generate_trees.sh accessions.txt 16
```

## How does it work?

The script works as follows:
1. It downloads genbank files.
2. It extract coding regions from them (protein sequences).
3. Clusters the sequences using `mmseqs`.
4. Filters out clusters with less than four sequences or with more than one sequence from one organism.
5. Performs the alignment using `MAFFT`.
6. For each alignment (clusters) performs ML tree search with 100 bootstraps using `RAxML`.
7. Infers consensus trees for each cluster.
8. Infers a supertree from all clusters using `fasturec2`. 
   The program is called 100 times and the best result (in terms of the DL cost) is saved to best_supertree.tre file.
