import sys
import glob

best_trees = []
for f in glob.glob(sys.argv[1] + "/*"):
    with open(f, "r") as handle:
        best_trees.append(next(handle).strip().split())

with open(sys.argv[2], "w") as handle:

    score, tree = min(best_trees, key=lambda x: int(x[0]))
    print("Best score:", score)
    handle.write(tree)



