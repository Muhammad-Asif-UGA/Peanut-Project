import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_volume_scatter(xlsx_path, output_dir):
    """
    Reads an Excel file containing columns:
       - 'Image Number'
       - 'Manual Volume (ml)'
       - 'Calculated Volume (ml)'
    Creates a scatter plot of "Manual Volume (ml)" vs. "Calculated Volume (ml)"
    and labels each point with the image number.

    ONLY the image numbers [86, 99] are colored RED; all others are GREEN.
    Saves the scatter plot to the specified output directory.
    """
    # 1) Read the Excel file into a DataFrame
    df = pd.read_excel(xlsx_path)

    # 2) Extract the relevant columns
    image_numbers = df["Image Number"]
    manual_vol    = df["Manual Volume (ml)"]
    calc_vol      = df["Calculated Volume (ml)"]

    # 3) Build a list of colors
    point_colors = []
    for i in range(len(df)):
        # If the image number is 86 or 99, color it red; else green
        if image_numbers.iloc[i] in [86, 99]:
            point_colors.append("red")
        else:
            point_colors.append("green")

    # 4) Create the scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(manual_vol, calc_vol, c=point_colors, alpha=0.7, label='Data Points')

    # 5) Add a reference line y = x
    min_val = min(manual_vol.min(), calc_vol.min())
    max_val = max(manual_vol.max(), calc_vol.max())
    plt.plot([min_val, max_val], [min_val, max_val],
             color='black', linestyle='--', label='y = x')

    # 6) Annotate each point with the image number
    for i in range(len(df)):
        x = manual_vol.iloc[i]
        y = calc_vol.iloc[i]
        label_text = str(image_numbers.iloc[i])
        plt.text(x + 1, y + 1, label_text, fontsize=8, color='black')

    # 7) Labels and legend
    plt.xlabel("Manually calculated Volume (ml)")
    plt.ylabel("Voxelized Volume (ml)")
    plt.title("Manual vs. Voxelized Volume")
    plt.legend()
    plt.grid(True)

    # 8) Save the plot
    output_file = os.path.join(output_dir, "volume_scatter_plot.png")
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Scatter plot saved to: {output_file}")

    # 9) Show the plot (optional)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Update these paths
    xlsx_file = r"A:\9march\voxel_results_excel_file_updated.xlsx"
    output_dir = r"A:\9march"

    plot_volume_scatter(xlsx_file, output_dir)
