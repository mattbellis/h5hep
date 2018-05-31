import h5py as h5
import numpy as np

import matplotlib.pylab as plt

import time

################################################################################
def hd5events(filename=None,verbose=False,desired_datasets=None,subset=None):

    """ Reads all, or a subset of the data, from the HDF5 file to fill a data dictionary.
    Returns an empty dictionary to be filled later with select events.

    Args:
	**filename** (string): Name of the input file
	
	**verbose** (boolean): True if debug output is required

	**desired_datasets** (list): Datasets to be read from input file

	**subset** (int): Number of events to be read from input file

    Returns:
	**ourdata (dict): Selected data from HDF5 file
	
	**event** (dict): An empty event dictionary to be filled by individual events

    """

    f = None
    if filename!=None:
        f = h5.File(filename,'r+')
    else:
        print("No filename passed in! Can't open file.\n")
        return None

    ourdata = {}
    ourdata['datasets_and_counters'] = {}
    ourdata['datasets_and_indices'] = {}
    ourdata['list_of_counters'] = []
    ourdata['all_datasets'] = []

    ourdata['nevents'] = f.attrs['nevents']
    if subset is not None:
        if type(subset) == int:
            subset = (0,subset)
        ourdata['nevents'] = subset[1] - subset[0]

    event = {}

    # Get the datasets and counters
    dc = f['datasets_and_counters']
    for vals in dc:
        # The decode is there because vals were stored as numpy.bytes
        counter = vals[1].decode()
        index = "%s_INDEX" % (counter)
        ourdata['datasets_and_counters'][vals[0].decode()] = counter
        ourdata['datasets_and_indices'][vals[0].decode()] = index
        ourdata['list_of_counters'].append(vals[1].decode())
        ourdata['all_datasets'].append(vals[0].decode())
        ourdata['all_datasets'].append(vals[1].decode()) # Get the counters as well

    # We may have added some strings (like counters) multiple times.
    ourdata['list_of_counters'] = np.unique(ourdata['list_of_counters']).tolist()
    ourdata['all_datasets'] = np.unique(ourdata['all_datasets']).tolist()

    # Pull out the SINGLETON datasets
    sg = f['_SINGLETONGROUP_'][0] # This is a numpy array of strings
    decoded_string = sg[1].decode()

    vals = decoded_string.split("__:__")
    vals.remove('INDEX')

    ourdata['_SINGLETON_'] = vals


    # Get the list of datasets and groups, but remove the 
    # 'datasets_and_counters', as that is a protected key.
    entries = ourdata['all_datasets']

    ########################################################
    # Only keep select data from file
    ########################################################
    if desired_datasets is not None:
        if type(desired_datasets) != list:
            desired_datasets = list(desired_datasets)

        # Count backwards because we'll be removing stuff as we go.
        i = len(entries)-1
        while i>=0:
            entry = entries[i]

            is_dropped = True
            for desdat in desired_datasets:
                if desdat in entry:
                    is_dropped = False
                    break

            if is_dropped==True:
                print("Not reading out %s from the file...." % (entry))
                entries.remove(entry)

            i -= 1
    #######################################################

    if verbose==True:
        print("Datasets and counters:")
        print(ourdata['datasets_and_counters'])
        print("\nDatasets and indices:")
        print(ourdata['list_of_counters'])

    # Pull out the counters first and build the indices
    print("Building the indices...")
    for name in ourdata['list_of_counters']:
        if subset is not None:
            ourdata[name] = f[name][subset[0]:subset[1]]
        else:
            ourdata[name] = f[name][:]

        #counter = f[name].value
        indexname = "%s_INDEX" % (name)
        index = np.zeros(len(ourdata[name]),dtype=int)
        start = 0
        nentries = len(index)
        for i in range(0,nentries):
            index[i] = start
            nobjs = ourdata[name][i]
            start = index[i] + nobjs
        ourdata[indexname] = index
    print("Built the indices!")

    
    # Loop over the entries we want and pull out the data.
    for name in entries:

        # The decode is there because counter is a numpy.bytes object
        counter = None
        if name not in ourdata['list_of_counters']:
            counter = ourdata['datasets_and_counters'][name]

        if verbose==True:
            print(f[name])

        data = f[name]
        #for data in f[name]:
        if type(data)==h5.Dataset:
            datasetname = name

            if subset is not None:
                ourdata[datasetname] = data[subset[0]:subset[1]]
            else:
                ourdata[datasetname] = data[:]

            event[datasetname] = None # This will be filled for individual events
            if verbose==True:
                print(data)

    f.close()
    print("Data is read in and input file is closed.")

    return ourdata,event
################################################################################


################################################################################
def unpack(event,data,n=0):

    """ Fills the event dictionary with selected events.

    Args:

	**event** (dict): Event dictionary to be filled

	**data** (dict): Data dictionary used to fill the event dictionary

    """

    keys = event.keys()

    for key in keys:

        #if "num" in key:
        # IS THERE A WAY THAT THIS COULD BE FASTER?
        #print(data['list_of_counters'],key)
        if key in data['list_of_counters'] or key in data['_SINGLETON_']:
            #print("here! ",key)
            event[key] = data[key][n]

        elif "INDEX" not in key:# and 'Jets' in key:
            indexkey = data['datasets_and_indices'][key]
            numkey = data['datasets_and_counters'][key]

            if len(data[indexkey])>0:
                index = data[indexkey][n]

            if len(data[numkey])>0:
                nobjs = data[numkey][n]
                event[key] = data[key][index:index+nobjs]

################################################################################

