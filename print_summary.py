import glob

print("Liczba taksonów:", len(glob.glob("gb/*")))
print()

print("Taksony:\n", "\n".join(x.rstrip(".gb").replace("_", " ") for x in glob.glob("gb/*")))
print()


