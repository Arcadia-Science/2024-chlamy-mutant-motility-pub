from pathlib import Path

import arcadia_pycolor as apc
import matplotlib.pyplot as plt
import numpy as np
import skimage as ski
from matplotlib.patches import Rectangle


def get_well_intensity_profiles(
    image,
    num_rows,
    num_cols,
    scan_width=10,
    scan_length=40,
    normalize=True,
):
    """Get intensity profiles from a grid of ROIs."""
    # Calculate center positions of each well
    height, width = image.shape
    row_spacing = height // num_rows
    col_spacing = width // num_cols
    well_centers = [
        (int((row + 0.5) * row_spacing), int((col + 0.5) * col_spacing))
        for row in range(num_rows)
        for col in range(num_cols)
    ]

    # Store the line scan results
    intensity_profiles = []
    # Perform line scans, realign, and (optionally) normalize data
    for center_y, center_x in well_centers:
        start_x = max(center_x - scan_length // 2, 0)
        end_x = min(center_x + scan_length // 2, width - 1)

        # Perform a horizontal line scan across the center with a width of scan_width
        line_intensities = []
        for offset in range(-scan_width // 2, scan_width // 2 + 1):
            rr, cc = ski.draw.line(center_y + offset, start_x, center_y + offset, end_x)
            line_intensities.append(image[rr, cc])

        # Ensure all scans are of the same length by trimming to scan_length
        line_intensities = [scan[:scan_length] for scan in line_intensities]
        # Average each row of the line scan
        intensity_profile = np.mean(line_intensities, axis=0)

        # Realign the line scan by aligning the minimum point within a broader search region
        broader_search_indices = np.arange(10, 30)
        min_index = broader_search_indices[np.argmin(intensity_profile[broader_search_indices])]
        shift = (scan_length // 2) - min_index
        intensity_profile = np.roll(intensity_profile, shift)

        # Optionally normalize the line scan by dividing by the average intensity value
        if normalize:
            intensity_profile = intensity_profile / intensity_profile.mean()

        intensity_profiles.append(intensity_profile)
    return well_centers, intensity_profiles


def annotate_phenotypeomat_image(
    image,
    well_centers,
    labels,
    scan_width,
    scan_length,
    cmap="Greys_r",
    y_offset_label=15,
    savefig_filepath=None,
    mpl_patch_kwargs=None,
    mpl_text_kwargs=None,
):
    """Annotate each well of the Phenotype-o-mat image using the input well positions and labels."""
    # Create figure
    fig, ax = plt.subplots(figsize=(24, 8))

    # Plot plate image
    im = ax.imshow(image, cmap=cmap)
    fig.colorbar(im)

    # Handle default plotting kwargs
    if mpl_patch_kwargs is None:
        mpl_patch_kwargs = {
            "linewidth": 1,
            "edgecolor": "white",
            "facecolor": "none",
        }
    if mpl_text_kwargs is None:
        mpl_text_kwargs = {
            "color": "white",
        }

    # Loop through each well
    for well_center, label in zip(well_centers, labels, strict=True):
        # Annotate the region that the intensity was scanned
        anchor_point = (well_center[1] - scan_length / 2, well_center[0] - scan_width / 2)
        scan_region = Rectangle(
            xy=anchor_point,
            width=scan_length,
            height=scan_width,
            **mpl_patch_kwargs,
        )
        ax.add_patch(scan_region)

        # Annotate each region with the strain name
        ax.text(
            x=well_center[1],
            y=well_center[0] - y_offset_label,
            s=label,
            ha="center",
            va="center",
            fontsize=12,
            **mpl_text_kwargs,
        )

    if savefig_filepath is not None:
        savefig_filepath = Path(savefig_filepath)
        savefig_filepath.parent.mkdir(exist_ok=True)
        apc.mpl.save_figure(savefig_filepath, dpi=192)
