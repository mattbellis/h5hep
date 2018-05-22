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
    assert isEmpty(test_data) == True

def test_clear_event():
	
    # This assumes you run nosetests from the h5hep directory and not 
    # the tests directory.
    filename = "./test_data/FOR_TESTS.hdf5"
    desired_datasets = ['jet','muon']
    subset = 1000

    data, event = hp.hd5events(filename, False, desired_datasets, subset)

    hp.clear_event(event)

    assert isEmpty(event) == True

def test_create_single_event():

    filename = "./test_data/FOR_TESTS.hdf5"
    desired_datasets = ['jet','muon']
    subset = 1000

    data, event = hp.hd5events(filename, False, desired_datasets, subset)

    test_event = hp.create_single_event(data)

    assert isEmpty(test_event) == False
    assert isinstance(test_event, dict)

def test_create_group():

    filename = "./test_data/FOR_TESTS.hdf5"
    desired_datasets = ['jet','muon']
    subset = 1000

    data, test_event = hp.hd5events(filename, False, desired_datasets, subset)

    test_key = "test_key"

    hp.create_group(test_event, test_key)

    assert isEmpty(test_event) == False

def test_create_dataset():

    filename = "./test_data/FOR_TESTS.hdf5"
    desired_datasets = ['jet','muon']
    subset = 1000

    data, test_event = hp.hd5events(filename, False, desired_datasets, subset)

    test = hp.create_dataset(test_event, desired_datasets)

    assert isEmpty(test_event) == False









