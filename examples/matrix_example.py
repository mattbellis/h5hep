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
matrix = hp.initialize()
    
#Create groups
hp.create_group(matrix, "points", "npoints")
hp.create_group(matrix, "data", "ndata")

# Create datasets within the groups
hp.create_dataset(matrix, ["x","y"], "points")
hp.create_dataset(matrix, ["data_point"], "data")

# Create an event from the matrix framework
event = hp.create_single_event(matrix)

for i in range(0,nmat):
    # Random selection of number of points in the matrix
    r = np.random.randint(0,x_size*y_size)

    # For each point, randomly select an x and y position
    # Repeats are ok in this example
    for i in range(0,r):
        event['points/x'].append(np.random.randint(1,x_size+1))
        event['points/y'].append(np.random.randint(1,y_size+1))
        event['data/data_point'].append(np.random.randint(1,70))

    # Counters are the same here because there is always one data point per point
    # They could be different if there was more data collected for each point
    event['data/ndata'] = r
    event['points/npoints'] = r
    
    # Add the event to the matrix dictionary
    hp.fill(matrix,event)

    # Clear the event matrix for the next iteration
    hp.clear_event(event)

# Write to file
hdfile = hp.write_to_file('matrix_example_output.hdf5',matrix,comp_type='gzip',comp_opts=9)

####################################################
# Plotting to check out what's inside the dictionary
####################################################
'''
count = 0
z = []
for ndata in matrix['data/ndata']:
    count += 1
    for i in range(0,ndata):
        z.append(count)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

c = ['b', 'g', 'r', 'c', 'm', 'b', 'g', 'r', 'c', 'm']

ax.scatter(matrix['points/x'], matrix['points/y'], z, c=c, marker=None)
'''

'''
# Create new figure
plt.figure(figsize=(20,10))

# Count variables to help with indexing values for each plot
count = 0
m = 1

# Loop over the points in x and y using the ndata counter to index values
for ndata in matrix['data/ndata']:
    # Weight the colors of the points by the data value
    z = np.array(matrix['data/data_point'][count:count+ndata])
    #color = [str(item*100/255.) for item in z] 
    color = plt.get_cmap('magma')
    
    plt.subplot(py_size,px_size,m)
    
    fig, ax = plt.subplots()
    ax.imshow([matrix['points/x'],matrix['points/y']], cmap=color)
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    #ax.set_xticks(np.arange(-.5, 10, 1));
    #ax.set_yticks(np.arange(-.5, 10, 1));

    #plt.scatter(matrix['points/x'][count:count+ndata],matrix['points/y'][count:count+ndata],s=100,c=color)
    #plt.xlim(0,x_size+1)
    #plt.ylim(0,y_size+1)
    plt.title('Matrix ' + str(m))    
    # Count is incremented by the number of data points in each matrix
    count += ndata
    # m is incremented by one for subplot position
    m += 1

plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9, hspace=.5)
cax = plt.axes([0.85, 0.250, 0.01, 0.5])
#plt.colorbar(cax=cax)

plt.show()
'''
count = 0
## WILL BE CHANGED WHEN READ IN FROM FILE
for i in range(0,nmat):

    npoints = matrix['points/npoints'][i]
    x = matrix['points/x'][count:count+npoints]
    y = matrix['points/y'][count:count+npoints]
    d = matrix['data/data_point'][count:count+npoints]

    data = np.zeros((x_size,y_size))

    for i in range(npoints):
        data[x[i]-1,y[i]-1] = d[i]

    # create discrete colormap
    #cmap = colors.ListedColormap(['red', 'blue'])
    cmap = plt.get_cmap('plasma')

    fig, ax = plt.subplots()
    ax.imshow(data, cmap=cmap)

    # draw gridlines
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-.5, x_size, 1));
    ax.set_yticks(np.arange(-.5, y_size, 1));

    ax.set_xticklabels(range(0,x_size))
    ax.set_yticklabels(range(0,y_size))

plt.show()















