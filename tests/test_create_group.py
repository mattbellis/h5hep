import numpy as np
import h5py as h5

import h5hep as hp

data = hp.initialize()

hp.create_group(data,'test',counter='test')

testNum = 0

for key in ['groups','list_of_counters']:
	if len(data[key]) != 1:
		testNum += 1

if testNum > 0:
	print("create_group() does not work as expected.")
else:
	print("create_group() works as expected.")
