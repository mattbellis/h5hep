import awkward as ak


################################################################################
def unpack_awkward(data,keys):

    if type(keys) is not list:
        keys = [keys]

    ak_arrays = []

    for topkey in keys:
        topkey = key.split('/')[0]
        nkey = topkey + "/n"  + topkey
        num = data[nkey]
        vals = data[key]
        ak_array = ak.unflatten(vals,num)
        ak_arrays.append(ak_array)

    return ak_arrays

################################################################################
def pack_awkward(awkward_arrays):


    return 1
