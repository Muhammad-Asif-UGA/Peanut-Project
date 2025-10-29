import os
import cv2
import numpy as np
from pycocotools.coco import COCO

def main():
    # Adjust these paths
    annotation_file = r"A:\22May\blackbox_annotation\annotation.json"  #"A:\9march\validation_data_all_annotations\annotations.json"
    images_dir      = r"A:\22May\RGB\blackbox.png"   #"A:\9march\validation_data_all_RGB"  # If needed
    mask_output_dir = r"A:\22May\mask"  #"A:\9march\masks"

    # Create a folder for the masks if it doesn't exist
    os.makedirs(mask_output_dir, exist_ok=True)

    # Initialize COCO
    coco = COCO(annotation_file)

    # Get all the image IDs
    img_ids = coco.getImgIds()

    for img_id in img_ids:
        # Load the image metadata (file name, width, height, etc.)
        img_info = coco.loadImgs(img_id)[0]
        file_name = img_info["file_name"]
        width     = img_info["width"]
        height    = img_info["height"]

        # You could also load the actual RGB image here if needed:
        # image_path = os.path.join(images_dir, file_name)
        # rgb_img    = cv2.imread(image_path)

        # Get all annotations for this image
        ann_ids = coco.getAnnIds(imgIds=img_id)
        anns = coco.loadAnns(ann_ids)

        # Create an empty mask (same size as the image)
        # We'll store mask pixels as 0 or 255 for visualization
        mask = np.zeros((height, width), dtype=np.uint8)

        # For each annotation, convert to a binary mask
        for ann in anns:
            ann_mask = coco.annToMask(ann)  # 0/1 array
            mask[ann_mask == 1] = 255      # combine into a single mask

        # Save the mask as a PNG
        base_name = os.path.splitext(file_name)[0]
        mask_name = base_name + "_mask.png"
        mask_path = os.path.join(mask_output_dir, mask_name)
        cv2.imwrite(mask_path, mask)

        print(f"Saved mask for '{file_name}' -> {mask_path}")

if __name__ == "__main__":
    main()
