import open3d as o3d

def visualize_point_cloud(ply_file_path):
    """
    Loads a .ply point cloud file and visualizes it in an interactive Open3D window.
    """
    # Read the point cloud
    pcd = o3d.io.read_point_cloud(ply_file_path)

    # Print basic info
    print(pcd)
    print(f"Number of points: {len(pcd.points)}")

    # Visualize
    o3d.visualization.draw_geometries([pcd], window_name="Point Cloud Visualization")

if __name__ == "__main__":
    # Update with the path to one of your generated .ply files
    pcd_file = r"A:\22May\pointcloud\blackbox_cloud.ply"   #"A:\9march\pointclouds\14_cloud.ply"
    visualize_point_cloud(pcd_file)

