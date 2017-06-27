import numpy as np
from numpy.random import beta
import sys
sys.path.append('../h5hep')
#from write import *
import h5hep as hp

################################################################################
def calc_energy(mass,px,py,pz):

    energy = np.sqrt(mass*mass + px*px + py*py + pz*pz)

    return energy

################################################################################

data = hp.initialize()

hp.create_group(data,'jet',counter='njet')
hp.create_dataset(data,['e','px','py','pz','btag'],group='jet',dtype=float)

hp.create_group(data,'muon',counter='nmuon')
hp.create_dataset(data,['e','px','py','pz','q'],group='muon',dtype=float)

hp.create_group(data,'electron',counter='nelectron')
hp.create_dataset(data,['e','px','py','pz','q'],group='electron',dtype=float)

hp.create_group(data,'photon',counter='nphoton')
hp.create_dataset(data,['e','px','py','pz'],group='photon',dtype=float)

hp.create_group(data,'MET',counter='nMET')
hp.create_dataset(data,['pt','phi'],group='MET',dtype=float)

event = hp.create_single_event(data)

nevents = 100000

#print(data)
#print(event)

#'''
for i in range(0,nevents):

    if i%1000==0:
        print(i)

    hp.clear_event(event)

    njet = np.random.randint(10)
    event['jet/njet'] = njet
    for n in range(njet):
        px = 300*beta(2,9)
        py = 300*beta(2,9)
        pz = 300*beta(2,9)
        mass = 5*beta(2,9)
        energy = calc_energy(mass,px,py,pz)
        event['jet/px'].append(px)
        event['jet/py'].append(py)
        event['jet/pz'].append(pz)
        event['jet/e'].append(energy)
        event['jet/btag'].append(np.random.random())

    nmuon = np.random.randint(10)
    event['muon/nmuon'] = nmuon
    for n in range(nmuon):
        px = 300*beta(2,9)
        py = 300*beta(2,9)
        pz = 300*beta(2,9)
        mass = 0.105
        energy = calc_energy(mass,px,py,pz)
        event['muon/px'].append(px)
        event['muon/py'].append(py)
        event['muon/pz'].append(pz)
        event['muon/e'].append(energy)
        event['muon/q'].append(2*np.random.randint(2) - 1)

    nelectron = np.random.randint(10)
    event['electron/nelectron'] = nelectron
    for n in range(nelectron):
        px = 300*beta(2,9)
        py = 300*beta(2,9)
        pz = 300*beta(2,9)
        mass = 0.000511
        energy = calc_energy(mass,px,py,pz)
        event['electron/px'].append(px)
        event['electron/py'].append(py)
        event['electron/pz'].append(pz)
        event['electron/e'].append(energy)
        event['electron/q'].append(2*np.random.randint(2) - 1)

    nphoton = np.random.randint(10)
    event['photon/nphoton'] = nphoton
    for n in range(nphoton):
        px = 300*beta(2,9)
        py = 300*beta(2,9)
        pz = 300*beta(2,9)
        mass = 0.0
        energy = calc_energy(mass,px,py,pz)
        event['photon/px'].append(px)
        event['photon/py'].append(py)
        event['photon/pz'].append(pz)
        event['photon/e'].append(energy)
        
    hp.fill(data,event)

print("Writing the file...")
#hdfile = write_to_file('output.hdf5',data)
hdfile = hp.write_to_file('HEP_random_file_LARGE.hdf5',data,comp_type='gzip',comp_opts=9)
#'''

