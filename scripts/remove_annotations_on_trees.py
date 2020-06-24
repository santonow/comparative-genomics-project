import sys

from Bio import Phylo
from Bio.Phylo import NewickIO

trees = list(Phylo.parse(sys.argv[1], "newick"))

print("Removing trees that are not bifurcating.")

for tree in trees:
    for nonterminal in tree.get_nonterminals():
        nonterminal.comment = None
        nonterminal.branch_length = None

writer = NewickIO.Writer([tree for tree in trees if tree.is_bifurcating()])

print()
print("Saving trees as plain newick files (no branch lengths).")
with open(sys.argv[2], "w") as handle:
    for newick_tree in writer.to_strings(plain=True):
        handle.write(newick_tree + "\n")
