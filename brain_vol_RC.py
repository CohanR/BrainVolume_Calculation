# This code uses the segmented Gannet data to calculate brain volume
# Remeber that c1 = GM, c2 = WM and c3 = CSF
# June 10, 2023
# Remy Cohan
#-------------------------------------------------------
import nibabel as nib
import numpy as np
import os
from nilearn import plotting

# Define the paths to the image files
base_dir = "/Volumes/REMY_Neuro/MRS/sub-013/twix/anat"
T1_image = os.path.join(base_dir, "sub-013_T1w.nii.gz")
c1_grey = os.path.join(base_dir, "c1sub-013_T1w.nii")
c2_white = os.path.join(base_dir, "c2sub-013_T1w.nii")
c3_csf = os.path.join(base_dir, "c3sub-013_T1w.nii")

# Function to compute volume from a mask
def compute_volume_from_mask(file_path):
    img = nib.load(file_path)
    data = img.get_fdata()
    
    # Get voxel dimensions from the header
    voxel_dims = img.header.get_zooms()
    voxel_volume = np.prod(voxel_dims)
    
    # Count non-zero voxels and compute volume
    volume = np.count_nonzero(data) * voxel_volume
    return volume

# Calculate volumes
c1_volume = compute_volume_from_mask(c1_grey)
c2_volume = compute_volume_from_mask(c2_white)
c3_volume = compute_volume_from_mask(c3_csf)

# Compute the volume of the brain minus the CSF
brain_minus_csf = c1_volume + c2_volume

# I understand this better if the values are convert to mL 
c1_volume_ml = c1_volume * 0.001
c2_volume_ml = c2_volume * 0.001
c3_volume_ml = c3_volume * 0.001
brain_minus_csf_ml = brain_minus_csf * 0.001
total_volume_ml = (brain_minus_csf + c3_volume) * 0.001

# Print results in a structured manner
print("Volumes (in both mm^3 and mL):\n")
print(f"Grey matter (c1): {c1_volume:.2f} mm^3 or {c1_volume_ml:.2f} mL")
print(f"White matter (c2): {c2_volume:.2f} mm^3 or {c2_volume_ml:.2f} mL")
print(f"CSF (c3): {c3_volume:.2f} mm^3 or {c3_volume_ml:.2f} mL")
print(f"Total brain (excluding CSF): {brain_minus_csf:.2f} mm^3 or {brain_minus_csf_ml:.2f} mL")
print(f"Overall brain volume: {brain_minus_csf + c3_volume:.2f} mm^3 or {total_volume_ml:.2f} mL")
print("\n")

# Interactive Visualisation in grayscale (opens in Jupyter lab)
img = nib.load(T1_image)
view = plotting.view_img(img, title='sub-013 Anatomical T1w')
view

# Visualising the grey and white matter segmentation overlayed on the anatomical image (opnes as html in your browser)
plotting.view_img(stat_map_img=c1_grey, bg_img=T1_image, threshold="90%", 
                  output_file="sub-013_GreyMatter.html").open_in_browser()
plotting.view_img(stat_map_img=c2_white, bg_img=T1_image, threshold="90%", 
                  output_file="sub-013_WhiteMatter.html").open_in_browser()
