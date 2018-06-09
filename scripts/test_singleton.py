import numpy as np
import time
import sys
sys.path.append('../h5hep')
#from write import *
import h5hep as hp

data = hp.initialize()

hp.create_group(data,'jet',counter='njet')
hp.create_dataset(data,['e','px','py','pz'],group='jet',dtype=float)

hp.create_dataset(data,['time','runnum'],dtype=float)

event = hp.create_single_event(data)


# Fill
for i in range(0,10):

    hp.clear_event(event)

    #event['time'] = 12.0

    event['time'] = time.time()
    event['runnum'] = 122300
    print(event['time'],event['runnum'])

    njet = 5
    event['jet/njet'] = njet

    for n in range(njet):
        event['jet/e'].append(np.random.random())
        event['jet/px'].append(np.random.random())
        event['jet/py'].append(np.random.random())
        event['jet/pz'].append(np.random.random())

    hp.pack(data,event)

#print(data)

print("Writing the file...")
#hdfile = write_to_file('output.hdf5',data)
outputfilename = 'test_singleton_OUTPUT.hdf5'
hdfile = hp.write_to_file(outputfilename,data,comp_type='gzip',comp_opts=9)

################################################################################
# Reading in file
################################################################################
inputfilename = outputfilename

data,event = hp.load(inputfilename)

#print("----------------")
#print(data)
#print("----------------")

nevents = data['nevents']
#print("nevents: ",nevents)

for i in range(0,nevents):
    
    hp.unpack(event,data,n=i)

    t = event['time']
    rn = event['runnum']
    print('{0:f}'.format(t), rn)

    print(event['jet/e'])
