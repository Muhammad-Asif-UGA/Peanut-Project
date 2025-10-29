import os
import glob
import cv2
import numpy as np
import open3d as o3d

def main():
    # -------------------------------------------------------------------------
    # Change these to match your actual directories
    # -------------------------------------------------------------------------
    rgb_dir   = r"A:\22May\RGB"          # folder with your RGB images "A:\9march\validation_data_all_RGB"
    depth_dir = r"A:\22May\depth"        # folder with your depth images  "A:\9march\depth_images"
    mask_dir  = r"A:\22May\mask"    # folder with masks generated in Step 1  "A:\9march\masks"
    out_dir   = r"A:\22May\pointcloud"              # where to save the output PLY files  "A:\9march\pointclouds"

    # Make sure output directory exists
    os.makedirs(out_dir, exist_ok=True)

    # -------------------------------------------------------------------------
    # Camera intrinsics for the Left Camera (ignore distortion and depth scale)
    #     fx = 1912.58
    #     fy = 1912.58
    #     cx = 1106.29
    #     cy =  605.90
    # -------------------------------------------------------------------------
    fx = 1906.29        # fx: 1906.29, fy: 1906.29, cx: 1099.99, cy: 619.98
    fy = 1906.29
    cx = 1099.99
    cy =  619.98

    # -------------------------------------------------------------------------
    # Gather depth files. We assume .png extension for depth images.
    # Adjust extension if necessary.
    # -------------------------------------------------------------------------
    depth_files = sorted(glob.glob(os.path.join(depth_dir, "*.png")))

    for depth_path in depth_files:
        base_name = os.path.splitext(os.path.basename(depth_path))[0]

        # Attempt to find corresponding RGB and mask
        rgb_path  = os.path.join(rgb_dir,  base_name + ".png")   # or .jpg, etc.
        mask_path = os.path.join(mask_dir, base_name + "_mask.png")

        # Validate that the files exist
        if not os.path.exists(rgb_path):
            print(f"[WARNING] No matching RGB found for {depth_path}")
            continue
        if not os.path.exists(mask_path):
            print(f"[WARNING] No matching mask found for {depth_path}")
            continue

        # ---------------------------------------------------------------------
        # Load images
        # ---------------------------------------------------------------------
        depth_img = cv2.imread(depth_path, cv2.IMREAD_ANYDEPTH)
        rgb_img   = cv2.imread(rgb_path,  cv2.IMREAD_COLOR)      # shape: (H, W, 3)
        mask_img  = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)  # shape: (H, W)

        if depth_img is None or rgb_img is None or mask_img is None:
            print(f"[WARNING] Failed to read one or more files for {base_name}")
            continue

        # ---------------------------------------------------------------------
        # Build the 3D point cloud (masked)
        # ---------------------------------------------------------------------
        mask_bool = (mask_img > 0)
        height, width = depth_img.shape
        u_coords, v_coords = np.meshgrid(np.arange(width), np.arange(height))

        # Keep only masked pixels
        u_coords = u_coords[mask_bool]
        v_coords = v_coords[mask_bool]

        z_values = depth_img[mask_bool].astype(np.float32)

        # Convert color BGR -> RGB if desired
        colors_bgr = rgb_img[mask_bool]        # shape: (N, 3)
        colors_rgb = colors_bgr[:, ::-1]       # reverse B <-> R

        # Pinhole projection -> 3D
        x_values = (u_coords - cx) * z_values / fx
        y_values = (v_coords - cy) * z_values / fy

        xyz_points = np.column_stack((x_values, y_values, z_values))

        # Create Open3D point cloud
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(xyz_points)
        pcd.colors = o3d.utility.Vector3dVector(colors_rgb.astype(np.float32) / 255.0)

        # ---------------------------------------------------------------------
        # (Optional) Noise/Outlier Removal
        # ---------------------------------------------------------------------
        # Using Statistical Outlier Removal with default parameters:
        #  - nb_neighbors: how many neighbors are considered in analyzing each point
        #  - std_ratio: the threshold based on standard deviation of average distances
        # The function returns two outputs:
        #   pcd_clean, inlier_indices = pcd.remove_statistical_outlier(nb_neighbors, std_ratio)
        # By default, pcd_clean is the subset of points that are inliers
        # (i.e., not outliers).
        # ---------------------------------------------------------------------
        nb_neighbors = 350
        std_ratio    = 0.5
        pcd_clean, inlier_indices = pcd.remove_statistical_outlier(
            nb_neighbors=nb_neighbors,
            std_ratio=std_ratio
        )

        # If you prefer radius-based outlier removal, you could do:
        # pcd_clean, inlier_indices = pcd.remove_radius_outlier(
        #     nb_points=16,   # minimum number of neighbors in radius
        #     radius=0.05     # distance threshold
        # )

        # We’ll use the clean point cloud going forward
        pcd = pcd_clean

        # ---------------------------------------------------------------------
        # Write to disk
        # ---------------------------------------------------------------------
        ply_output_path = os.path.join(out_dir, base_name + "_cloud.ply")
        o3d.io.write_point_cloud(ply_output_path, pcd)
        print(f"[INFO] Saved cleaned point cloud: {ply_output_path}")


if __name__ == "__main__":
    main()

