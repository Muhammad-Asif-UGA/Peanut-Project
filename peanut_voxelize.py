import os
import open3d as o3d
import pandas as pd

def voxelize_and_compute_volumes(
    pointcloud_dir,
    excel_file,
    output_csv=None,
    voxel_size=10.0
):
    """
    1. Reads volume info from 'excel_file' (two columns: 'Image Number' and 'Volume (ml)').
    2. For each row, attempts to load the corresponding .ply point cloud from 'pointcloud_dir'.
    3. Voxelizes the point cloud at 'voxel_size' (in the same units as the point cloud).
    4. Computes:
        - num_voxels = number of occupied voxels
        - avg_vol_per_voxel = manual_volume / num_voxels
    5. Optionally, saves results to 'output_csv'.

    :param pointcloud_dir: Directory containing *.ply point cloud files.
    :param excel_file: Path to your Excel file (with columns: "Image Number", "Volume (ml)").
    :param output_csv: If provided, we will save the results as a CSV here.
    :param voxel_size: The voxel size you want to experiment with (e.g. 10.0, etc.).
    """
    # 1) Read the Excel
    df = pd.read_excel(excel_file)

    results = []

    # 2) Loop over each row in the Excel
    for idx, row in df.iterrows():
        image_num = row["Image Number"]
        manual_volume_ml = row["Volume (ml)"]

        # Build the .ply file name
        # For example, if your PLY is named "1_cloud.ply" for Image Number 1
        # Adjust if your naming differs
        ply_filename = f"{image_num}_cloud.ply"
        ply_path = os.path.join(pointcloud_dir, ply_filename)

        if not os.path.exists(ply_path):
            print(f"[WARNING] PLY file not found for image {image_num} -> {ply_path}")
            continue

        # Load the point cloud
        pcd = o3d.io.read_point_cloud(ply_path)

        if len(pcd.points) == 0:
            print(f"[WARNING] Empty point cloud for {image_num}")
            results.append({
                "Image Number": image_num,
                "Manual Volume (ml)": manual_volume_ml,
                "Num Voxels": 0,
                "Avg Volume per Voxel (ml/voxel)": 0.0
            })
            continue

        # 3) Voxelize the point cloud
        # We'll create a voxel grid from min_bound to max_bound of the cloud
        bbox_min = pcd.get_min_bound()
        bbox_max = pcd.get_max_bound()
        voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud_within_bounds(
            pcd,
            voxel_size=voxel_size,
            min_bound=bbox_min,
            max_bound=bbox_max
        )

        # 4) Count how many voxels are occupied
        num_voxels = len(voxel_grid.get_voxels())

        if num_voxels == 0:
            avg_vol_per_voxel = 0.0
        else:
            avg_vol_per_voxel = manual_volume_ml / num_voxels

        # Accumulate the results
        results.append({
            "Image Number": image_num,
            "Manual Volume (ml)": manual_volume_ml,
            "Num Voxels": num_voxels,
            "Avg Volume per Voxel (ml/voxel)": avg_vol_per_voxel
        })

        print(f"[INFO] Image {image_num} -> #Voxels: {num_voxels}, "
              f"Avg Vol/Voxel: {avg_vol_per_voxel:.3f} ml")

    # 5) Optionally save to CSV
    if output_csv:
        out_df = pd.DataFrame(results)
        out_df.to_csv(output_csv, index=False)
        print(f"[INFO] Results saved to {output_csv}")
    else:
        # Or just print them
        print("\n=== Results ===")
        for r in results:
            print(r)

def main():
    # Change these paths as needed
    pointcloud_dir = r"A:\9march\pointclouds"
    excel_file     = r"A:\9march\Validation_File_updated.xlsx"
    output_csv     = r"A:\9march\voxel_results.csv"

    # You can experiment with different voxel sizes here
    # For example, if your point cloud is in millimeters and you want 10 mm cubes => voxel_size=10
    # If it's in meters and you want 0.01 m cubes => voxel_size=0.01, etc.
    voxel_size = 10.0

    voxelize_and_compute_volumes(
        pointcloud_dir=pointcloud_dir,
        excel_file=excel_file,
        output_csv=output_csv,
        voxel_size=voxel_size
    )

if __name__ == "__main__":
    main()
