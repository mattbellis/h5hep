import h5py as h5
import numpy as np

import matplotlib.pylab as plt

import time

from hep_hdf5_tools import hd5events,get_event

import sys

filename = sys.argv[1]

#data,event = hd5events(filename,verbose=True,select_key_tags=['Jet'])
data,event = hd5events(filename,verbose=False)

nevents = len(data['Jets/num'])
print(nevents)

energies = []

#x = data['Jets/Energy']

# Print out what is stored in the files.
for key in event.keys():
    print(key)

for i in range(0,nevents):

    if i%10000==0:
        print(i)

    get_event(event,data,n=i)

    energy = event['Jets/Energy']

    for e in energy:
        energies.append(e)


print(len(energies))

plt.figure()
plt.hist(energies,bins=100,range=(0,500))

plt.show()

