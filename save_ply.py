import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.cm import ScalarMappable
import cv2
import os

# Paths to files
binary_mask_path = r"C:\Users\hj46265\Downloads\Peanut\validation\output_masks\26_mask.png"
depth_map_path = r"C:\Users\hj46265\Downloads\Peanut\validation\Depth 1\26.png"
rgb_image_path = r"C:\Users\hj46265\Downloads\Peanut\validation\RGB_Validation\26.png"

# Load data
binary_mask = cv2.imread(binary_mask_path, cv2.IMREAD_GRAYSCALE)
depth_map = cv2.imread(depth_map_path, cv2.IMREAD_ANYDEPTH | cv2.IMREAD_UNCHANGED)
rgb_image = cv2.imread(rgb_image_path)

# Verify loaded data
assert depth_map is not None and rgb_image is not None, "Files not loaded correctly."

# Camera intrinsic parameters
fx, fy, cx, cy = 1906.29, 1906.29, 1099.99, 619.98

# Generate point cloud data
points, colors = [], []
for v in range(depth_map.shape[0]):
    for u in range(depth_map.shape[1]):
        if binary_mask[v, u]:
            Z = depth_map[v, u]
            if Z > 0:  # Filter out invalid depth
                X = (u - cx) * Z / fx
                Y = (v - cy) * Z / fy
                points.append([X, Y, Z])
                colors.append(rgb_image[v, u] / 255.0)  # Normalize colors

# Create Open3D Point Cloud
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)
pcd.colors = o3d.utility.Vector3dVector(colors)
pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])

# Outlier removal
pcd, _ = pcd.remove_statistical_outlier(nb_neighbors=100, std_ratio=0.2)

# Apply scaling
scaling_factor = 1 / np.max(pcd.get_max_bound() - pcd.get_min_bound())
pcd.scale(scaling_factor, center=pcd.get_center())

# Define save path for the PLY file
ply_save_path = r"C:\Users\hj46265\Downloads\Peanut\validation\masks\point_cloud26.ply"

# Save point cloud to PLY file
o3d.io.write_point_cloud(ply_save_path, pcd)
print(f"Point cloud saved as PLY at: {ply_save_path}")

# Custom colormap
n_bins = 110
colors = [(0, 0, 0.5), (0, 1, 0), (1, 1, 0), (1, 0, 0)]
cmap_name = 'my_density_map'
custom_cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

# Voxel downsampling
voxel_size = 0.02
down_pcd = pcd.voxel_down_sample(voxel_size)

# KDTree
kdtree = o3d.geometry.KDTreeFlann(down_pcd)

# Compute densities
densities = []
radius = 0.35
volume_of_sphere = (4.0 / 3.0) * np.pi * (radius ** 3)
for i in range(len(pcd.points)):
    [k, idx, _] = kdtree.search_radius_vector_3d(pcd.points[i], radius)
    densities.append(k / volume_of_sphere)

# Update point cloud colors for density visualization
densities_array = np.array(densities)
colors = custom_cmap(densities_array / np.max(densities_array))
pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])

# Visualization
vis = o3d.visualization.Visualizer()
vis.create_window('Point Cloud Visualization - DS2_02', width=1200, height=800)
vis.get_render_option().background_color = np.array([0.5, 0.5, 0.5])  # Set gray background
vis.add_geometry(pcd)
vis.run()
vis.destroy_window()

# Reverse the scaling
pcd.scale(1 / scaling_factor, center=pcd.get_center())

# Convert Open3D.o3d.geometry.PointCloud to numpy array
points = np.asarray(pcd.points)
colors = np.asarray(pcd.colors)

# Calculate the centers of x and y
center_x = (points[:, 0].max() + points[:, 0].min()) * 0.5
center_y = (points[:, 1].max() + points[:, 1].min()) * 0.5

# Find the max range in x and y
max_range_x = (points[:, 0].max() - points[:, 0].min()) * 0.5
max_range_y = (points[:, 1].max() - points[:, 1].min()) * 0.5

# Create a 3D plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot with zero-centered coordinates
sc = ax.scatter(points[:, 0] - center_x, points[:, 1] - center_y, points[:, 2], s=1, c=colors, cmap=custom_cmap, edgecolor='none')

# Centering x and y axes at zero by setting equal limits around the center
ax.set_xlim(-max_range_x, max_range_x)
ax.set_ylim(-max_range_y, max_range_y)

# Set plot labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Set title
ax.set_title('3D Point Cloud Visualization')

# Add a color bar
sm = ScalarMappable(cmap=custom_cmap)
sm.set_array(densities_array)
cbar = plt.colorbar(sm, ax=ax, shrink=0.5, aspect=5)
cbar.set_label('Density Distribution')

# Set the view angle
ax.view_init(elev=45, azim=45)

# Save the figure to a valid Windows path
output_dir = r"C:\Users\hj46265\Downloads\Peanut\validation\3D_Visualization"
os.makedirs(output_dir, exist_ok=True)
fig_save_path = os.path.join(output_dir, "3d_points.png")
fig.savefig(fig_save_path, dpi=300)
print(f"3D plot saved at: {fig_save_path}")

# Show the plot
plt.show()

# Histogram
plt.figure(figsize=(7, 5))
plt.hist(densities_array, bins=n_bins, color='gray', edgecolor='black')
plt.xlabel('Density')
plt.ylabel('Count')
plt.title('Volume Density Histogram')

# Show histogram
plt.show()
