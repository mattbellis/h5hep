import numpy as np
import sys
sys.path.append('../h5hep')
#from write import *
from h5hep import *

data = initialize()

create_group(data,'jet',counter='njet')
create_dataset(data,['e','px','py','pz'],group='jet',dtype=float)

print("DATA =============")
for key in data.keys():
    print(key,data[key])

#create_dataset(data,['time','runnum'],dtype=float)

#print(data)
print("DATA =============")
for key in data.keys():
    print(key,data[key])


event = create_single_event(data)


print("EVENT =============")
for key in event.keys():
    print(key,event[key])


# Fill
for i in range(0,1000):

    clear_event(event)

    #event['time'] = 12.0

    njet = 5
    event['jet/njet'] = njet

    for n in range(njet):
        event['jet/e'].append(np.random.random())
        event['jet/px'].append(np.random.random())
        event['jet/py'].append(np.random.random())
        event['jet/pz'].append(np.random.random())

    fill(data,event)

#print(data)
print("Writing the file...")
#hdfile = write_to_file('output.hdf5',data)
hdfile = write_to_file('output.hdf5',data,comp_type='gzip',comp_opts=9)

