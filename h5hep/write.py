import numpy as np
import h5py as h5


################################################################################
def initialize():

    """ Creates an empty data dictionary

    Returns:

	**data** (dict): An empty data dictionary

    """

    data = {}
    data['groups'] = {}
    data['datasets_and_counters'] = {}
    data['list_of_counters'] = []
    return data

################################################################################
def clear_event(data):

    """ Clears the data from the data dictionary - should the name of the function change?

    Args:
	**data** (dict): The dictionary to be cleared

    """

    for key in data.keys():
        if type(data[key]) == list:
            data[key].clear()
        
        #'''
        # Is this the right thing to do here?????
        elif type(data[key]) == int:
            data[key] = 0
        elif type(data[key]) == float:
            data[key] = 0.
        #'''

################################################################################
# Create a single event (dictionary) that will eventually be used to fill
# the overall dataset
################################################################################
def create_single_event(data):

    """ Creates an event dictionary that will be used to fill the overall dataset

    Args:
	**data** (dict): Data dictionary to be used to fill event dictionary

    Returns:
	**event** (dict): The new event dictionary

    """

    event = {}

    for k in data.keys():
        if k[-5:] == 'index':
            event[k] = data[k]
        elif k in data['list_of_counters']:
            event[k] = 0
        else:
            event[k] = data[k].copy()

    return event

################################################################################
# This adds a group in the dictionary, similar to
# a la CreateBranch in ROOT
################################################################################
def create_group(data, groupname, counter=None):

    """ Adds a group in the dictionary

    Args:
	**data** (dict): Dictionary to which the group will be added

	**groupname** (string): Name of the group to be added

	**counter** (string): Name of the counter key. None by default

    """

    keys = data.keys()

    # Put the counter in the dictionary first.
    '''
    if counter is not None:
        data['datasets_and_counters'][groupname] = counter
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
            print("\033[1m%s\033[0m is already in the dictionary!" % (groupname))
            keyfound = True
            break
    if keyfound == False:
        #data[groupname] = []
        data['groups'][groupname] = []
        print("Adding group \033[1m%s\033[0m" % (groupname))
        if counter is not None:
            data['groups'][groupname].append(counter)
            name = "%s/%s" % (groupname,counter)
            #data['datasets_and_counters'][groupname] = counter
            data['datasets_and_counters'][groupname] = name
            if name not in data['list_of_counters']:
                data['list_of_counters'].append(name)
            data[name] = []
            print("Adding a counter for \033[1m%s\033[0m as \033[1m%s\033[0m" % (groupname,counter))
        else:
            print("----------------------------------------------------")
            print("There is no counter to go with group \033[1m%s\033[0m" % (groupname))
            print("Are you sure that's what you want?")
            print("-----------------------------------------------------")
        
################################################################################
# This adds a group in the dictionary, similar to
# a la CreateBranch in ROOT
################################################################################
def create_dataset(data, datasets, group=None, dtype=None):

    """ Adds a dataset to a group in a dictionary. If the group does not exist, it will be created.

    Args:
	**data** (dict): Dictionary that contains the group
	
	**datasets** (list): Dataset to be added to the group (This doesn't have to be a list)

	**group** (string): Name of group the dataset will be added to.  None by default

	**dtype** (type): The data type. None by default - I don't think this is every used 

    Returns:
	**-1**: If the group is None


    """

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
        print("Your group, \033[1m%s\033[0m is not in the dictionary yet!" % (group))
        counter = "n%s" % (group)
        print("Adding it, along with a counter of \033[1m%s\033[0m" % (counter))
        create_group(data,group,counter=counter)

    # Then put the datasets into the group in there next.
    if type(datasets) != list:
        datasets = [datasets]

    for dataset in datasets:
        keyfound = False
        name = "%s/%s" % (group,dataset)
        for k in keys:
            if name == k:
                print("\033[1m%s\033[0m is already in the dictionary!" % (name))
                keyfound = True
        if keyfound == False:
            print("Adding dataset \033[1m%s\033[0m to the dictionary under group \033[1m%s\033[0m." % (dataset,group))
            data[name] = []
            data['groups'][group].append(dataset)

            # Add a counter for this dataset for the group with which it is associated.
            counter = data['datasets_and_counters'][group]
            #counter_name = "%s/%s" % (group,counter)
            data['datasets_and_counters'][name] = counter
    
        
################################################################################
def fill(data,event):

    """ Fills an event with given data

    Args:
	**data** (dict): Data to be added to event

	**event** (dict): Event to be filled

    """

    keys = list(event.keys())

    for key in keys:
        #print(key)

        if key=='datasets_and_counters' or key=='groups' or key=='list_of_counters':
            continue

        #if key[-5:] == 'counter':
            #continue
        if type(event[key]) == list:
            value = event[key]
            if len(value)>0:
                data[key] += value
            '''
            else:
                # No entries for this event
                #print(key)
                counter = data['datasets_and_counters'][key]
                data[counter].append(0)
                if counter in keys:
                    keys.remove(counter)
            '''
        else:
            data[key].append(event[key])


################################################################################
def convert_dict_to_string_data(dictionary):

    """ Converts data dictionary to a string

    Args:
	**dictionary** (dict): Dictionary to be converted to a string

    Returns:
	**mydataset** (string): String representation of the dataset

    """

    keys = dictionary.keys()

    nkeys = len(keys)

    mydataset = []
    for i,key in enumerate(keys):
        #print(i,key,dictionary[key])
        a = np.string_(key)
        b = np.string_(dictionary[key])
        mydataset.append([a,b])

    return mydataset

################################################################################

################################################################################
def write_to_file(filename,data,comp_type=None,comp_opts=None,force_single_precision=True):

    """ Writes the selected data to an h5hep file

    Args:
	**filename** (string): Name of output file

	**data** (dictionary): Data to be written into output file

	**comp_type** (string): Type of compression

	**force_single_precision** (boolean): True if data should be written in single precision

    Returns:
	**hdoutfile** (h5hep): File to which the data has been written 

    """

    hdoutfile = h5.File(filename,'w')

    groups = data['groups'].keys()

    # Convert this to a 2xN array for writing to the hdf5 file. 
    # This gives us one small list of informtion if we need to pull out
    # small chunks of data
    mydataset = convert_dict_to_string_data(data['datasets_and_counters'])
    dset = hdoutfile.create_dataset('datasets_and_counters', \
                                 data = mydataset, \
                                 dtype='S256', \
                                 compression=comp_type, \
                                 compression_opts=comp_opts)

    for group in groups:

        #print(group)

        hdoutfile.create_group(group)
        hdoutfile[group].attrs['counter'] = np.string_(data['datasets_and_counters'][group])

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

            hdoutfile.create_dataset(name,data=x,compression=comp_type, compression_opts=comp_opts)

    # Get the number of events
    counters = data['list_of_counters']
    nevents = -1
    prevcounter = None
    for i,countername in enumerate(counters):
        ncounter = len(data[countername])
        print("%-32s has %-12d entries" % (countername,ncounter))
        if i>0 and ncounter != nevents: 
            print("-------- WARNING -----------")
            print("%s and %s have differing numbers of entries!" % (countername,prevcounter))
            print("-------- WARNING -----------")
            # SHOULD WE EXIT ON THIS?

        if nevents < ncounter:
            nevents = ncounter

        prevcounter = countername

    hdoutfile.attrs['nevents'] = nevents
    hdoutfile.close()

    return hdoutfile

    

