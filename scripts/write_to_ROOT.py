import numpy as np
import ROOT
import sys
from array import array

f = ROOT.TFile("test.root", "RECREATE")
tree = ROOT.TTree("T", "My tree")

njet = array("i", [-1])
tree.Branch("njet", njet, "njet/I")
jete = array("f", 16 * [-1.0])
tree.Branch("jete", jete, "jete[njet]/F")
jetpx = array("f", 16 * [-1.0])
tree.Branch("jetpx", jetpx, "jetpx[njet]/F")
jetpy = array("f", 16 * [-1.0])
tree.Branch("jetpy", jetpy, "jetpy[njet]/F")
jetpz = array("f", 16 * [-1.0])
tree.Branch("jetpz", jetpz, "jetpz[njet]/F")

for i in range(0, 100000):

    njet[0] = 5

    for n in range(njet[0]):
        jete[n] = np.random.random()
        jetpx[n] = np.random.random()
        jetpy[n] = np.random.random()
        jetpz[n] = np.random.random()

    tree.Fill()

print("Writing the file...")
tree.Write()

f.Close()
