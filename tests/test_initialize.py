import numpy as np
import h5py as h5

import h5hep as hp

data = hp.initialize()

testNum = 0

if type(data) == dict:
	print("initialize() returned a dictionary.")
	testNum += 1
else:
	print("initialize() did not return a dictionary.")

test = True

for key in data.keys():
	if len(data[key]) > 0:
		test = False 

if test:
	print("The directory is empty.")
	testNum += 1
else:
	print("The directory is not empty.")

if testNum == 2:
	print("initialize() works as expected.")
else:
	print("initialize() does not work as expected.")
