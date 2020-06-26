import sys

with open(sys.argv[1], "r") as handle:
    with open(sys.argv[2], "w") as target:
        target.write("".join(next(handle).strip().split()[1:]) + "\n")
