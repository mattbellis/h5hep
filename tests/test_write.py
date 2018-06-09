import numpy as np
import h5py as h5
import h5hep as hp

import matplotlib.pylab as plt

import time

import sys
sys.path.append('./scripts')
#from write_h5hep_file_for_unit_tests import write_h5hep_file_for_unit_tests

def isEmpty(dictionary):
    test = True
    print(dictionary.keys())
    for key in dictionary.keys():
        print(key)
        print(dictionary[key])
        print(type(dictionary[key]))
        if dictionary[key] is None:
            test = True
        elif type(dictionary[key])==list or type(dictionary[key])==np.ndarray:
            if len(dictionary[key]) > 0:
                test = False

    return test

def test_initialize():

    test_data = hp.initialize()

    assert isinstance(test_data, dict)
    assert test_data['groups']['_SINGLETON_'] ==  ['INDEX']
    assert test_data['datasets_and_counters']['_SINGLETON_'] == '_SINGLETON_/INDEX'
    assert test_data['list_of_counters'] == ['_SINGLETON_/INDEX']
    assert test_data['_SINGLETON_/INDEX'] == []


def test_clear_event():
	
    # This assumes you run nosetests from the h5hep directory and not 
    # the tests directory.
    filename = "./test_data/FOR_TESTS.hdf5"
    desired_datasets = ['jet','muon']
    subset = 1000

    data, event = hp.load(filename, False, desired_datasets, subset)

    hp.clear_event(event)

    assert isEmpty(event) == True

def test_create_single_event():

    data = hp.initialize()

    hp.create_group(data,'jet',counter='njet')
    hp.create_dataset(data,['e','px','py','pz'],group='jet',dtype=float)

    hp.create_group(data,'muons',counter='nmuon')
    hp.create_dataset(data,['e','px','py','pz'],group='muons',dtype=float)

    test_event = hp.create_single_event(data)

    assert isEmpty(test_event) == False
    assert isinstance(test_event, dict)

def test_create_group():

    data = hp.initialize()
    hp.create_group(data,'jet',counter='njet')

    assert isEmpty(data['groups']) == False
    assert 'jet/njet' in data.keys()


def test_create_dataset():

    data = hp.initialize()
    hp.create_group(data,'jet',counter='njet')
    hp.create_dataset(data,['e','px','py','pz'],group='jet',dtype=float)


    assert isEmpty(data['groups']) == False
    assert 'jet/njet' in data.keys()
    assert 'jet/e' in data.keys()
    assert 'jet/px' in data.keys()
    assert 'jet/e' in data['datasets_and_counters'].keys()
    assert data['datasets_and_counters']['jet/e'] == 'jet/njet'









