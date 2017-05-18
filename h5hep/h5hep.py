import h5py as h5
import numpy as np

import matplotlib.pylab as plt

import time

################################################################################
def hd5events(filename=None,verbose=False,select_key_tags=None):

    f = None
    if filename!=None:
        f = h5.File(filename,'r+')
    else:
        print("No filename passed in! Can't open file.\n")
        return None

    names = []

    ourdata = {}
    event = {}

    for name in f:
        names.append(name)

        if verbose==True:
            print(f[name])

        for data in f[name]:
            groupname = "%s/%s" % (name,data)

            ########################################################
            # Only keep select data from file
            ########################################################
            keep_name = False
            if select_key_tags is None:
                keep_name = True
            else:
                for skt in select_key_tags:
                    if skt in groupname:
                        keep_name = True
                        break

            if keep_name==False:
                continue
            ########################################################

            ourdata[groupname] = f[groupname][:]
            event[groupname] = None # This will be filled for individual events
            if verbose==True:
                print(data)

            #'''
            if data=="num":
                indexgroupname = "%s/%s" % (name,"index")
                index = np.zeros(len(ourdata[groupname]),dtype=int)
                start = 0
                nentries = len(index)
                for i in range(0,nentries):
                    index[i] = start
                    nobjs = ourdata[groupname][i]
                    start = index[i] + nobjs
                ourdata[indexgroupname] = index
            #'''

    return ourdata,event
################################################################################


################################################################################
def get_event(event,data,n=0):

    keys = event.keys()

    for key in keys:

        if "num" in key:
            event[key] = data[key][n]

        elif "num" not in key and "index" not in key:# and 'Jets' in key:
            groupname = key.split("/")[0]
            indexkey = "%s/index" % (groupname)
            numkey = "%s/num" % (groupname)

            index = data[indexkey][n]
            nobjs = data[numkey][n]

            event[key] = data[key][index:index+nobjs]

################################################################################

