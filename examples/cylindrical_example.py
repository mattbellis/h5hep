import numpy as np
import h5py as h5
import h5hep as hp

import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import colors

# Number of layers
nlayers = 3

# Number of events
nevents = 4

# Assign dimensions
z_size = [20, 24, 28]

# Max number of pixels in each layer
# Assume i pixels per ten degrees
maxpix = []
for i in range(0,nlayers):
    #maxpix.append(z_size[i]*(i+1)*36)
    maxpix.append(z_size[i]*(i+1)*18)

# Initialize the data dictionary for a single matrix
data = hp.initialize()

#Create groups
hp.create_group(data, "pixels", counter="npixels")

# Create datasets within the groups
hp.create_dataset(data, ["z","theta","r","value"], group="pixels")

# Create an event from the data container
event = hp.create_single_event(data)

for i in range(0,nevents):

    npixtot = 0
    ## Random selection of number of hit pixels in the layer
    for j in range(nlayers): 
        npix = np.random.randint(0,maxpix[j])

        # For each point, randomly select a z and theta
        # Repeats are ok in this example
        for i in range(0,npix):
            event['pixels/z'].append(np.random.randint(0,z_size[j]) - z_size[j]/2)
            event['pixels/r'].append(j)
            event['pixels/theta'].append(np.random.random()*2*np.pi)
            event['pixels/value'].append(np.random.randint(1,70))

        # Keep a count of the total number of pixels
        npixtot += npix

    # Counters are the same here because there is always one data point per point
    # They could be different if there was more data collected for each point
    event['pixels/npixels'] = npixtot

    # Add the event to the matrix dictionary
    hp.pack(data,event)

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

fig = plt.figure()

for i in range(0,nevents):
    
    hp.unpack(event,data,n=i)

    npixels = event['pixels/npixels']
    #npixels = data['pixels/npixels'][i]
    z = event['pixels/z']
    r = event['pixels/r']
    theta = event['pixels/theta']
    d = event['pixels/value']

    x = (r+1)*np.cos(theta)
    y = (r+1)*np.sin(theta)
    
    x1 = np.linspace(-1,1,100)
    y1 = np.linspace(-1,1,100)
    z1 = np.linspace(0,10,100)

    zipped = zip(x,y,z,d)
    sorted(zipped, key=lambda g: g[2])

    ax = fig.add_subplot(2, 2, i+1, projection='3d')
    ax.scatter(x,y,z,c=d, alpha=0.2)
    #ax.scatter(x,y,z,c=r, alpha=0.2)
    #ax.plot_surface(x1,y1,z1)
    #ax.plot_surface(x1,y1,z1)
    ax.set_zlim(0, 10)

plt.show()


