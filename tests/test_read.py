import numpy as np
import h5py as h5
import h5hep as hp

import matplotlib.pylab as plt

import time

def isEmpty(dictionary):
	test = True
	for key in dictionary.keys:
		if len(dictionary[key]) > 0:
			test = False

	return test
	

def test_hd5events():

	filename = "../scripts/output.hdf5"
	desired_datasets = ['jet','muon']
	subset = 1000

	test_data,test_event = hp.hd5events(filename, False, desired_datasets, subset)

	assert isinstance(test_data, dict)
	assert isinstance(test_event, dict)

	assert isEmpty(test_event) == True
	assert isEmpty(test_data) == False

def test_get_event():
	
	filename = "../scripts/output.hdf5"
	desired_datasets = ['jet','muon']
	subset = 1000
	
	event, data = hp.hd5events(filename, False, desired_datasets, subset)

	#hp.get_event()

	assert isEmpty(event) == False



