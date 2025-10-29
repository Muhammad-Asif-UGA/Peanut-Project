import open3d as o3d

# Load the new point cloud from the PLY file
new_point_cloud = o3d.io.read_point_cloud(r"A:\9march\pointclouds\1_cloud.ply") #"C:\Users\hj46265\Downloads\Peanut\validation\PLY_Output\1.ply

# Check if the new point cloud is empty
if new_point_cloud.is_empty():
    raise ValueError("The new point cloud is empty or not loaded correctly.")

# Define the same voxel size used previously
voxel_size = 0.002

# Voxelize the new point cloud
new_voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(new_point_cloud, voxel_size)

# Ensure the new voxel grid is not empty
new_voxels = new_voxel_grid.get_voxels()
if len(new_voxels) == 0:
    raise ValueError("The new voxel grid is empty. Try increasing the voxel size.")

# Calculate the total number of occupied voxels in the new point cloud
num_new_voxels = len(new_voxels)

# Volume of one voxel in ml (previously calculated)
volume_per_voxel_ml = 0.000380

# Calculate the total volume of the new point cloud in ml
total_volume_new_point_cloud_ml = num_new_voxels * volume_per_voxel_ml

# Print the results
print(f"Total number of voxels in the new point cloud: {num_new_voxels}")
print(f"Total volume of the new point cloud (ml): {total_volume_new_point_cloud_ml:.6f}")

# Visualization
#o3d.visualization.draw_geometries([new_voxel_grid])