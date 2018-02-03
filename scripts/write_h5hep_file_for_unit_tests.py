import numpy as np
import sys
sys.path.append('../h5hep')
from h5hep import *

def write_h5hep_file_for_unit_tests():
    data = initialize()

    create_group(data,'jet',counter='njet')
    create_dataset(data,['e','px','py','pz'],group='jet',dtype=float)

    create_group(data,'muons',counter='nmuon')
    create_dataset(data,['e','px','py','pz'],group='muons',dtype=float)

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
    #hdfile = write_to_file('output.hdf5',data)
    hdfile = write_to_file('FOR_TESTS.hdf5',data,comp_type='gzip',comp_opts=9)
    #'''

if __name__ == "__main__":
    write_h5hep_file_for_unit_tests()

