import numpy as np
import sys
sys.path.append('../h5hep')
#from write import *
from h5hep import *

data = initialize()

create_group(data,'jet',counter='njet')
create_dataset(data,['e','px','py','pz','btag'],group='jet',dtype=float)

create_group(data,'muon',counter='nmuon')
create_dataset(data,['e','px','py','pz','q'],group='muon',dtype=float)

create_group(data,'electron',counter='nelectron')
create_dataset(data,['e','px','py','pz','q'],group='electron',dtype=float)

create_group(data,'photon',counter='nphoton')
create_dataset(data,['e','px','py','pz'],group='photon',dtype=float)

event = create_single_event(data)

#'''
for i in range(0,100000):

    if i%1000==0:
        print(i)

    clear_event(event)

    njet = np.random.randint(10)
    event['jet/njet'] = njet
    for n in range(njet):
        event['jet/e'].append(200*np.random.random())
        event['jet/px'].append(200*np.random.random())
        event['jet/py'].append(200*np.random.random())
        event['jet/pz'].append(200*np.random.random())
        event['jet/btag'].append(np.random.random())

    nmuon = np.random.randint(10)
    event['muon/nmuon'] = nmuon
    for n in range(nmuon):
        event['muon/e'].append(200*np.random.random())
        event['muon/px'].append(200*np.random.random())
        event['muon/py'].append(200*np.random.random())
        event['muon/pz'].append(200*np.random.random())
        event['muon/q'].append(np.random.randint(2))

    nelectron = np.random.randint(10)
    event['electron/nelectron'] = nelectron
    for n in range(nelectron):
        event['electron/e'].append(200*np.random.random())
        event['electron/px'].append(200*np.random.random())
        event['electron/py'].append(200*np.random.random())
        event['electron/pz'].append(200*np.random.random())
        event['electron/q'].append(np.random.randint(2))

    nphoton = np.random.randint(10)
    event['photon/nphoton'] = nphoton
    for n in range(nphoton):
        event['photon/e'].append(200*np.random.random())
        event['photon/px'].append(200*np.random.random())
        event['photon/py'].append(200*np.random.random())
        event['photon/pz'].append(200*np.random.random())
        
    fill(data,event)

print("Writing the file...")
#hdfile = write_to_file('output.hdf5',data)
hdfile = write_to_file('output_large.hdf5',data,comp_type='gzip',comp_opts=9)
#'''

