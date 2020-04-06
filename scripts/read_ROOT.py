import ROOT
import numpy as np
import matplotlib.pylab as plt

import sys

filename = sys.argv[1]

# Open the file
f = ROOT.TFile(filename)
f.ls()  # Print out what's in it.

# Pull out the tree
tree = f.Get("T")
tree.Print()  # Print what branches it has

# Event loop
nev = tree.GetEntries()

energies = []

for n in range(nev):
    tree.GetEntry(n)

    for i in range(tree.njet):
        energies.append(tree.jete[i])

print(len(energies))

plt.figure()
plt.hist(energies, bins=100, range=(0, 1))

# plt.show()
