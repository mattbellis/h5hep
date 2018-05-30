import numpy as np
import h5py as h5
import h5hep as hp

import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import colors

# Number of layers
nlayers = 3

# Number of events
nevents = 3

# Assign dimensions
z_size = 10

# Max number of pixels in each layer
# Assume i pixels per degree
maxpix = []
for i in range(0,nlayers):
    maxpix.append(z_size*(i+1)*36)

# Initialize the data dictionary for a single matrix
data = hp.initialize()

#Create groups
hp.create_group(data, "pixels", counter="npixels")

# Create datasets within the groups
hp.create_dataset(data, ["z","theta","r","value"], group="pixels")

# Create an event from the data container
event = hp.create_single_event(data)

for i in range(0,nevents):
    # Random selection of number of hit pixels in the layer
    npix = np.random.randint(0,maxpix[i])

    # For each point, randomly select a z and theta
    # Repeats are ok in this example
    for i in range(0,npix):
        event['pixels/z'].append(np.random.randint(0,z_size))
        event['pixels/r'].append(np.random.randint(0,nlayers))
        event['pixels/theta'].append(np.random.random()*2*np.pi)
        event['pixels/value'].append(np.random.randint(1,70))

    # Counters are the same here because there is always one data point per point
    # They could be different if there was more data collected for each point
    event['pixels/npixels'] = npix

    # Add the event to the matrix dictionary
    hp.fill(data,event)

    # Clear the event matrix for the next iteration
    hp.clear_event(event)


###############
# Write to file
###############
filename = 'cylindrical_example_output.hdf5'
hdfile = hp.write_to_file(filename,data,comp_type='gzip',comp_opts=9)

################
# Read from file
################
data,event = hp.hd5events(filename)
nevents = data['nevents']
#print(data)
#print("nevents: ",nevents)

for i in range(0,nevents):
    
    hp.get_event(event,data,n=i)

    npixels = event['pixels/npixels']
    #npixels = data['pixels/npixels'][i]
    z = event['pixels/z']
    r = event['pixels/r']
    theta = event['pixels/theta']
    d = event['pixels/value']

    x = (r+1)*np.cos(theta)
    y = (r+1)*np.sin(theta)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x,z,y)

plt.show()


