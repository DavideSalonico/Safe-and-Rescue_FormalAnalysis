import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# Define a 3x3 dataset
data1 = np.array([
    [0.450, 0.400, 0.274],
    [0.406, 0.311, 0.189],
    [0.291, 0.175, 0.164]
])

data2 = np.array([
    [0.478, 0.327, 0.249],
    [0.400, 0.282, 0.218],
    [0.299, 0.177, 0.146]
])

# Define specific x and y values
x_values = np.array([0.05, 0.25, 0.45])
y_values = np.array([0.05, 0.25, 0.45])

# Create meshgrid for the specific x and y values
x, y = np.meshgrid(x_values, y_values)

# Flatten the x, y, and z data for bar3d function
x = x.flatten()
y = y.flatten()
z = np.zeros_like(x)
dx = dy = 0.1
data = data1
z_label = "Probability P1 holding"
#data = data2
#z_label = "Probability P2 holding"
dz = data.flatten()

norm = plt.Normalize(data.min(), data.max())
colors = cm.viridis(norm(dz))  # Use the viridis colormap

# Create a figure and a 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the 3D histogram
ax.bar3d(x, y, z, dx, dy, dz, color=colors, shade=True)

ax.set_xticks(np.array([0.1, 0.3, 0.5]))
ax.set_yticks(np.array([0.1, 0.3, 0.5]))

# Set labels
ax.set_xlabel('P_fail')
ax.set_ylabel('P_ignore')
ax.set_zlabel(z_label)

# Show the plot
plt.show()
