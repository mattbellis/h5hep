import numpy as np
import h5py as hp


################################################################################
def initialize():
    data = {}
    return data

################################################################################
def clear_event(data):
    for key in data.keys():
        if type(data[key]) == list:
            data[key].clear()

################################################################################
# Create a single event (dictionary) that will eventually be used to fill
# the overall dataset
################################################################################
def create_single_event(data):
    event = {}

    for k in data.keys():
        if k[-5:] == 'index':
            event[k] = data[k]
        else:
            event[k] = data[k].copy()

    return event

################################################################################
# This adds an entry to the dictionary, a la CreateBranch in ROOT
################################################################################
def create_entry(data, name, dtype=float, index=None):

    keys = data.keys()

    if index is not None:
        keyfound = False
        for k in keys:
            if index == k:
                keyfound = True
        if keyfound == False:
            data[index] = []

        indexkey = "%sindex" % (name)
        data[indexkey] = index

    keyfound = False
    for k in keys:
        if name == k:
            print("%s is already in the dictionary!" % (name))
            keyfound = True
    if keyfound == False:
        data[name] = []
    
    
        
################################################################################
def fill(data,event):

    keys = event.keys()
    for key in keys:
        #print(key)
        if key[-5:] == 'index':
            continue
        elif type(event[key]) == list:
                data[key] += event[key]
        else:
            data[key].append(event[key])


################################################################################
def write_to_file(filename,data):

    hdfile = hp.File(filename,'w')

    keys = data.keys()
    for key in keys:

        x = data[key]
        if type(x) == list:
            x = np.array(x)

        hdfile.create_dataset(key,data=x)

    hdfile.close()

    return hdfile

    

