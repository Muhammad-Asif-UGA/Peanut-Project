import numpy as np
import open3d as o3d
import cv2
import os

# -----------------------------
# 1. Paths to input files
# -----------------------------
depth_map_path = r"C:\Users\hj46265\Downloads\Peanut\validation\Depth 1\26.png"
rgb_image_path = r"C:\Users\hj46265\Downloads\Peanut\validation\RGB_Validation\26.png"

# -----------------------------
# 2. Load Data
# -----------------------------
depth_map = cv2.imread(depth_map_path, cv2.IMREAD_ANYDEPTH | cv2.IMREAD_UNCHANGED)
rgb_image = cv2.imread(rgb_image_path)

# Verify loaded data
assert depth_map is not None and rgb_image is not None, "Error: One or more files not loaded correctly."

# Convert RGB image from BGR to RGB
rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB)

# -----------------------------
# 3. Camera Intrinsics
# -----------------------------
fx, fy, cx, cy = 1906.29, 1906.29, 1099.99, 619.98  # Adjust as necessary

# -----------------------------
# 4. Generate Point Cloud
# -----------------------------
points, colors = [], []
h, w = depth_map.shape[:2]

for v in range(h):
    for u in range(w):
        Z = depth_map[v, u]  # Depth value
        if Z > 0:  # Only consider valid depth points
            X = (u - cx) * Z / fx
            Y = (v - cy) * Z / fy
            points.append([X, Y, Z])
            colors.append(rgb_image[v, u] / 255.0)  # Normalize color values

# Convert to Open3D format
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)
pcd.colors = o3d.utility.Vector3dVector(colors)

# -----------------------------
# 5. Apply Transformations
# -----------------------------
pcd.transform([[1, 0, 0, 0],
               [0, -1, 0, 0],
               [0, 0, -1, 0],
               [0, 0, 0, 1]])  # Adjust coordinate system

# -----------------------------
# 6. Outlier Removal
# -----------------------------
pcd, _ = pcd.remove_statistical_outlier(nb_neighbors=100, std_ratio=0.2)

# -----------------------------
# 7. Save & Visualize
# -----------------------------
# Save PLY File
#ply_save_path = r"C:\Users\hj46265\Downloads\Peanut\validation\PLY_Output\point_cloud26.ply"
#o3d.io.write_point_cloud(ply_save_path, pcd)
#print(f"Point cloud saved at: {ply_save_path}")

# Visualize the point cloud
o3d.visualization.draw_geometries([pcd], window_name="3D Point Cloud Visualization")
