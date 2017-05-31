import numpy as np
import h5py as hp


################################################################################
def initialize():
    data = {}
    data['counters'] = {}
    data['groups'] = {}
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
# This adds a group in the dictionary, similar to
# a la CreateBranch in ROOT
################################################################################
def create_group(data, groupname, counter=None):

    keys = data.keys()

    # Put the counter in the dictionary first.
    '''
    if counter is not None:
        data['counters'][groupname] = counter
        keyfound = False
        for k in keys:
            if counter == k:
                keyfound = True
        if keyfound == False:
            data[counter] = []
    '''

    # Then put the group and any datasets in there next.
    keyfound = False
    for k in keys:
        if groupname == k:
            print("%s is already in the dictionary!" % (groupname))
            keyfound = True
            break
    if keyfound == False:
        #data[groupname] = []
        data['groups'][groupname] = []
        print("Adding group %s" % (groupname))
        if counter is not None:
            data['groups'][groupname].append(counter)
            name = "%s/%s" % (groupname,counter)
            data['counters'][groupname] = counter
            data[name] = []
            print("Adding a counter for %s as %s" % (groupname,counter))
        else:
            print("----------------------------------------------------")
            print("There is no counter to go with group %s" % (groupname))
            print("Are you sure that's what you want?")
            print("-----------------------------------------------------")
        
################################################################################
# This adds a group in the dictionary, similar to
# a la CreateBranch in ROOT
################################################################################
def create_dataset(data, datasets, group=None, dtype=None):

    keys = data.keys()

    if group is None:
        print("-----------------------------------------------")
        print("You need to assign this dataset(s) to a group!")
        print("Groups are not added")
        print("-----------------------------------------------")
        return -1

    # Put the counter in the dictionary first.
    keyfound = False
    for k in data['groups']:
        if group == k:
            keyfound = True
    if keyfound == False:
        print("Your group, %s is not in the dictionary yet!" % (group))
        counter = "n%s" % (group)
        print("Adding it, along with a counter of %s" % (counter))
        create_group(data,group,counter=counter)

    # Then put the datasets into the group in there next.
    if type(datasets) != list:
        datasets = [datasets]

    for dataset in datasets:
        keyfound = False
        name = "%s/%s" % (group,dataset)
        for k in keys:
            if name == k:
                print("%s is already in the dictionary!" % (name))
                keyfound = True
        if keyfound == False:
            print("Adding dataset %s to the dictionary under group %s." % (dataset,group))
            data[name] = []
            data['groups'][group].append(dataset)
    
        
################################################################################
def fill(data,event):

    keys = event.keys()
    for key in keys:
        #print(key)

        if key=='counters' or key=='groups':
            continue

        #if key[-5:] == 'counter':
            #continue
        if type(event[key]) == list:
            data[key] += event[key]
        else:
            data[key].append(event[key])


################################################################################
def write_to_file(filename,data,comp_type=None,comp_opts=None,force_single_precision=True):

    hdfile = hp.File(filename,'w')

    groups = data['groups'].keys()

    for group in groups:

        #print(group)

        hdfile.create_group(group)
        hdfile[group].attrs['counter'] = np.string_(data['counters'][group])

        datasets = data['groups'][group]

        for dataset in datasets:
            name = "%s/%s" % (group,dataset)
        
            x = data[name]
            if type(x) == list:
                x = np.array(x)

            # Do single precision only, unless specified
            if force_single_precision==True:
                if x.dtype == np.float64:
                    x = x.astype(np.float32)

            hdfile.create_dataset(name,data=x,compression=comp_type, compression_opts=comp_opts)

    hdfile.close()

    return hdfile

    

