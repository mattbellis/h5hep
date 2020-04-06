import h5py as h5
import numpy as np
import matplotlib.pylab as plt
import time

import h5hep as hp

import sys

filename = sys.argv[1]

energies = []

for nfiles in range(0, 30):

    data, event = hp.load(filename)

    # Print out what has been read in from the files.
    """
    for key in event.keys():
        print(key)
    """

    nentries = data["nentries"]
    print("nentries: ", nentries)
    print(type(data), type(event))

    energies += data["jet/e"].tolist()

    """
    for i in range(0,nentries):

        if i%10000==0:
            print(i)

        hp.unpack(event,data,n=i)

        energy = event['jet/e']

        energies += energy.tolist()
    """

    del data
    del event


print(len(energies))

plt.figure()
plt.hist(energies, bins=100, range=(0, 500))

# plt.show()
