import h5py as h5
import numpy as np
import matplotlib.pylab as plt
import time

import h5hep as hp

import sys

filename = sys.argv[1]

#data,event = hp.hd5events(filename,subset=(0,100000))
data,event = hp.hd5events(filename,verbose=False)#,subset=10000)
#data,event = hp.hd5events(filename,desired_datasets=['jet','muon'])
#data,event = hp.hd5events(filename,desired_datasets=['jet'])
#data,event = hp.hd5events(filename,desired_datasets=['jet','muon'],subset=(0,100000))

#print(data['list_of_counters'])

nevents = data['nevents']
print("nevents: ",nevents)

#print(type(data),type(event))

energies = []

#print("A")
#print(data.keys())
#print(data)
#
#print("B")
#print(event.keys())
#print(event)
#x = data['jet/e']

# Print out what has been read in from the files.
'''
for key in event.keys():
    print(key)
'''

for i in range(0,nevents):

    if i%10000==0:
        print(i)

    hp.unpack(event,data,n=i)

    #print(event['jet/njet'])

    energy = event['jet/e']

    '''
    for e in energy:
        energies.append(e)
    '''
    energies += energy.tolist()


print(len(energies))

plt.figure()
plt.hist(energies,bins=100,range=(0,500))

#plt.show()
