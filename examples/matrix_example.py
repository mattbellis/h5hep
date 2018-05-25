import numpy as np
import h5py as h5
import h5hep as hp

import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import colors

###################################################
# Fill a matrix with a random amount of points.
# Store many of these matrices using h5hep.
###################################################

# Number of matrices
nmat = 10

# Assign matrix dimensions
x_size = 25
y_size = 25
x_size = int(x_size)
y_size = int(y_size)

# Subplot size for later
px_size = 2
py_size = 5

# Initialize the data dictionary for a single matrix
data = hp.initialize()
    
#Create groups
hp.create_group(data, "pixels", counter="npixels")

# Create datasets within the groups
hp.create_dataset(data, ["x","y","value"], group="pixels")

# Create an event from the data container
event = hp.create_single_event(data)

for i in range(0,nmat):
    # Random selection of number of pixels in the matrix
    r = np.random.randint(0,x_size*y_size)

    # For each point, randomly select an x and y position
    # Repeats are ok in this example
    for i in range(0,r):
        event['pixels/x'].append(np.random.randint(1,x_size+1))
        event['pixels/y'].append(np.random.randint(1,y_size+1))
        event['pixels/value'].append(np.random.randint(1,70))

    # Counters are the same here because there is always one data point per point
    # They could be different if there was more data collected for each point
    event['pixels/npixels'] = r
    
    # Add the event to the matrix dictionary
    hp.fill(data,event)

    # Clear the event matrix for the next iteration
    hp.clear_event(event)

###############
# Write to file
###############
filename = 'matrix_example_output.hdf5'
hdfile = hp.write_to_file(filename,data,comp_type='gzip',comp_opts=9)

################
# Read from file
################
data,event = hp.hd5events(filename)
nevents = data['nevents']
print(data)
print("nevents: ",nevents)
#nevents = data['nevents']

for i in range(0,nevents):

    hp.get_event(event,data,n=i)

    print(event.keys())

    npixels = event['pixels/npixels']
    x = event['pixels/x']
    y = event['pixels/y']
    d = event['pixels/value']

    grid = np.zeros((x_size,y_size))

    for i in range(npixels):
        grid[x[i]-1,y[i]-1] = d[i]

    # create discrete colormap
    #cmap = colors.ListedColormap(['red', 'blue'])
    cmap = plt.get_cmap('plasma')

    fig, ax = plt.subplots()
    ax.imshow(grid, cmap=cmap)

    # draw gridlines
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-.5, x_size, 1));
    ax.set_yticks(np.arange(-.5, y_size, 1));

    ax.set_xticklabels(range(0,x_size))
    ax.set_yticklabels(range(0,y_size))



plt.show()















