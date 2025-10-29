import open3d as o3d

def visualize_voxel_grid(ply_file_path, voxel_size=10):
    """
    Loads a .ply point cloud, voxelizes it with the given voxel_size,
    and visualizes the resulting voxel grid in an interactive Open3D window.
    """
    # 1) Read the point cloud from file
    pcd = o3d.io.read_point_cloud(ply_file_path)
    print(f"Loaded point cloud: {ply_file_path}")
    print(f"Number of points: {len(pcd.points)}")

    # 2) Create a voxel grid from the point cloud
    bbox_min = pcd.get_min_bound()
    bbox_max = pcd.get_max_bound()
    voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud_within_bounds(
        pcd,
        voxel_size=voxel_size,
        min_bound=bbox_min,
        max_bound=bbox_max
    )
    print(f"Voxel grid created with voxel_size={voxel_size}.")
    print(f"Number of voxels: {len(voxel_grid.get_voxels())}")

    # 3) Visualize the voxel grid
    # This will open an interactive window where you can
    # rotate, zoom, and pan around the voxelized structure
    o3d.visualization.draw_geometries([voxel_grid], window_name="Voxel Grid Visualization")

if __name__ == "__main__":
    # Update this path to point to one of your .ply files
    sample_ply = r"A:\22May\pointcloud\blackbox_cloud.ply"   #"A:\9march\pointclouds\14_cloud.ply"
    # Adjust voxel_size as appropriate (based on your point cloud units)
    visualize_voxel_grid(sample_ply, voxel_size=10)


