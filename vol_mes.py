import os
import pandas as pd
import open3d as o3d
import numpy as np

# -----------------------------------------------------------------
# 1. Define input paths and read Excel file (to make average of volumes)
# -----------------------------------------------------------------
excel_path = r"A:\8July\validation\Validation_File.xlsx" #C:\Users\46265\Downloads\Peanut\validation\Validation_File.xlsx
ply_folder = r"A:\9march\pointclouds" #C:\Users\46265\Downloads\Peanut\validation\PLY_files

df = pd.read_excel(excel_path)  # expects columns "Image" and "Volume (ml)"

# -----------------------------------------------------------------
# 2. specify how many images to process (N)
# -----------------------------------------------------------------
num_to_choose = 105  # hard-code or read from input()

# Sort by "Image" column ascending
df_sorted = df.sort_values(by="Image")

# Grab the first N image IDs
unique_images = df_sorted["Image"].unique()
if len(unique_images) < num_to_choose:
    print(f"Excel only has {len(unique_images)} unique images, but you requested {num_to_choose}.")
    chosen_images = unique_images  # or handle error differently
else:
    chosen_images = unique_images[:num_to_choose]

print(f"Chosen images (sorted): {chosen_images}")

# -----------------------------------------------------------------
# 3. Loop over the chosen images, load PLY, voxelize, compute ratio
# -----------------------------------------------------------------
voxel_size = 0.00025  # or desired size
ratios = []  # store volume-per-voxel for each chosen image

for img_id in chosen_images:
    # Find that row in df
    row = df.loc[df["Image"] == img_id].iloc[0]
    manual_volume_ml = row["Volume (ml)"]

    # Full path to the matching PLY file, e.g. "1.ply"
    ply_path = os.path.join(ply_folder, f"{img_id}.ply")

    # -----------------------------------------------------------------
    # 4. Load PLY file
    # -----------------------------------------------------------------
    if not os.path.isfile(ply_path):
        print(f"PLY not found for image {img_id}, skipping.")
        continue

    pcd = o3d.io.read_point_cloud(ply_path)
    if pcd.is_empty():
        print(f"Empty PLY for {img_id}, skipping.")
        continue

    # -----------------------------------------------------------------
    # 5. Voxelize the point cloud
    # -----------------------------------------------------------------
    voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size)
    num_voxels = len(voxel_grid.get_voxels())
    if num_voxels == 0:
        print(f"No occupied voxels for {img_id}, skipping.")
        continue

    # -----------------------------------------------------------------
    # 6. Compute volume-per-voxel ratio
    # -----------------------------------------------------------------
    ratio = manual_volume_ml / num_voxels
    ratios.append(ratio)
    print(f"Image {img_id}: {manual_volume_ml} ml / {num_voxels} voxels => ratio={ratio:.6f} ml/voxel")

# -----------------------------------------------------------------
# 7. Compute the average ratio from all chosen images
# -----------------------------------------------------------------
if len(ratios) == 0:
    print("No valid PLYs processed; cannot compute average ratio.")
else:
    average_volume_per_voxel = np.mean(ratios)
    print(f"\nChosen images: {chosen_images}")
    print(f"Average volume per voxel: {average_volume_per_voxel:.6f} ml")
