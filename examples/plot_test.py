import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

data = np.random.rand(10, 10) * 20
print(data)

# create discrete colormap
#cmap = colors.ListedColormap(['red', 'blue'])
cmap = plt.get_cmap('magma')
bounds = [0,10,20]
#norm = colors.BoundaryNorm(bounds, cmap)

fig, ax = plt.subplots()
#ax.imshow(data, cmap=cmap, norm=norm)
ax.imshow(data, cmap=cmap)

# draw gridlines
ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
ax.set_xticks(np.arange(-.5, 10, 1));
ax.set_yticks(np.arange(-.5, 10, 1));

plt.show()
