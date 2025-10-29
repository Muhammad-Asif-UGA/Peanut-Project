import open3d as o3d

# Load the point cloud
point_cloud = o3d.io.read_point_cloud(r"A:\9march\pointclouds\1_cloud.ply")   #C:\Users\hj46265\Downloads\Peanut\validation\masks\point_cloud1.ply

# Check if the point cloud is empty
if point_cloud.is_empty():
    raise ValueError("The point cloud is empty or not loaded correctly.")

# voxel size
voxel_size = 0.002

# Voxelize the point cloud
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(point_cloud, voxel_size)

# Visualize the voxel grid
#o3d.visualization.draw_geometries([voxel_grid], window_name="Voxelized Point Cloud")


# Calculate the total number of occupied voxels
num_voxels = len(voxel_grid.get_voxels())

# Manually measured volume in milliliters
manual_volume_ml = 115  # in milliliters

# Calculate the volume of one voxel in ml
volume_per_voxel_ml = manual_volume_ml / num_voxels

print(f"Total number of voxels: {num_voxels}")
print(f"Volume of one voxel (ml): {volume_per_voxel_ml:.6f}")