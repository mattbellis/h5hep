import numpy as np
from ROOT import *
import sys
from array import array

f = TFile( 'test.root', 'RECREATE' )
tree = TTree( 'T', 'My tree' )

jete = array('f', 16*[0.0])
ngen = array('i', [-1])
TreeSemiLept.Branch('ngen', ngen, 'ngen/I')
genpt = array('f', 16*[-1.])
TreeSemiLept.Branch('genpt', genpt, 'genpt[ngen]/F')




data = initialize()

create_group(data,'jet',counter='njet')
create_dataset(data,['e','px','py','pz'],group='jet',dtype=float)

event = create_single_event(data)

#'''
for i in range(0,100000):

    clear_event(event)

    njet = 5
    event['jet/njet'] = njet

    for n in range(njet):
        event['jet/e'].append(np.random.random())
        event['jet/px'].append(np.random.random())
        event['jet/py'].append(np.random.random())
        event['jet/pz'].append(np.random.random())

    fill(data,event)

print("Writing the file...")
hdfile = write_to_file('output.hdf5',data)
#'''

