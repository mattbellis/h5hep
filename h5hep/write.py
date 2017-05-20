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
def create_group(data, groupname, index=None):

    keys = data.keys()

    # Put the index in the dictionary first.
    '''
    if index is not None:
        data['counters'][groupname] = index
        keyfound = False
        for k in keys:
            if index == k:
                keyfound = True
        if keyfound == False:
            data[index] = []
    '''

        #indexkey = "%sindex" % (groupname)
        #data[indexkey] = index

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
        if index is not None:
            data['groups'][groupname].append(index)
            name = "%s/%s" % (groupname,index)
            data['counters'][groupname] = index
            data[name] = []
        else:
            print("-----------------------------------------------------")
            print("There is no index to go with group %s" % (groupname))
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

    # Put the index in the dictionary first.
    keyfound = False
    for k in keys:
        if group == k:
            keyfound = True
    if keyfound == False:
        print("Your group, %s is not in the dictionary yet!")
        index = "n%s" % (group)
        print("Adding it, along with an index counter of %s" % (index))
        create_group(data,group,index=index)

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
            data[name] = []
            data['groups'][group].append(dataset)
    
        
################################################################################
def fill(data,event):

    keys = event.keys()
    for key in keys:
        #print(key)

        if key=='counters' or key=='groups':
            continue

        #if key[-5:] == 'index':
            #continue
        if type(event[key]) == list:
            data[key] += event[key]
        else:
            data[key].append(event[key])


################################################################################
def write_to_file(filename,data,comp_type=None,comp_opts=None):

    hdfile = hp.File(filename,'w')

    groups = data['groups'].keys()

    for group in groups:

        print(group)

        hdfile.create_group(group)
        hdfile[group].attrs['index'] = np.string_(data['counters'][group])

        datasets = data['groups'][group]

        for dataset in datasets:
            name = "%s/%s" % (group,dataset)
        
            x = data[name]
            if type(x) == list:
                x = np.array(x)

            hdfile.create_dataset(name,data=x,compression=comp_type, compression_opts=comp_opts)

    hdfile.close()

    return hdfile

    

