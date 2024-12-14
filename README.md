# 2024-chlamy-mutant-motility-pub

[![run with conda](https://img.shields.io/badge/run%20with-conda-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/projects/miniconda/en/latest/)
[![Arcadia Pub](https://img.shields.io/badge/Arcadia-Pub-596F74.svg?logo=data:image/svg%2bxml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPCEtLSBHZW5lcmF0b3I6IEFkb2JlIElsbHVzdHJhdG9yIDI3LjcuMCwgU1ZHIEV4cG9ydCBQbHVnLUluIC4gU1ZHIFZlcnNpb246IDYuMDAgQnVpbGQgMCkgIC0tPgo8c3ZnIHZlcnNpb249IjEuMSIgaWQ9IkxheWVyXzEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHg9IjBweCIgeT0iMHB4IgoJIHZpZXdCb3g9IjAgMCA0My4yIDQwLjQiIHN0eWxlPSJlbmFibGUtYmFja2dyb3VuZDpuZXcgMCAwIDQzLjIgNDAuNDsiIHhtbDpzcGFjZT0icHJlc2VydmUiPgo8c3R5bGUgdHlwZT0idGV4dC9jc3MiPgoJLnN0MHtmaWxsOm5vbmU7c3Ryb2tlOiNGRkZGRkY7c3Ryb2tlLXdpZHRoOjI7c3Ryb2tlLWxpbmVqb2luOmJldmVsO3N0cm9rZS1taXRlcmxpbWl0OjEwO30KPC9zdHlsZT4KPGc+Cgk8cG9seWdvbiBjbGFzcz0ic3QwIiBwb2ludHM9IjIxLjYsMyAxLjcsMzcuNCA0MS41LDM3LjQgCSIvPgoJPGxpbmUgY2xhc3M9InN0MCIgeDE9IjIxLjYiIHkxPSIzIiB4Mj0iMjEuNiIgeTI9IjI3LjMiLz4KCTxwb2x5bGluZSBjbGFzcz0ic3QwIiBwb2ludHM9IjEyLjIsMTkuNCAyNC42LDMwLjEgMjQuNiwzNy40IAkiLz4KCTxsaW5lIGNsYXNzPSJzdDAiIHgxPSIxNy42IiB5MT0iMTYuNyIgeDI9IjE3LjYiIHkyPSIyNC4xIi8+Cgk8bGluZSBjbGFzcz0ic3QwIiB4MT0iMjguNiIgeTE9IjE1LjIiIHgyPSIyMS43IiB5Mj0iMjIuMSIvPgoJPHBvbHlsaW5lIGNsYXNzPSJzdDAiIHBvaW50cz0iNi44LDI4LjcgMTkuNSwzNC40IDE5LjUsMzcuNCAJIi8+Cgk8bGluZSBjbGFzcz0ic3QwIiB4MT0iMzQuOCIgeTE9IjI1LjgiIHgyPSIyNC42IiB5Mj0iMzYuMSIvPgoJPGxpbmUgY2xhc3M9InN0MCIgeDE9IjI5LjciIHkxPSIyMi4yIiB4Mj0iMjkuNyIgeTI9IjMwLjkiLz4KPC9nPgo8L3N2Zz4K)](https://doi.org/10.57844/arcadia-fe2a-711e)

<img src=resources/figure-2_GA_70.png alt=tracked cells width=720>
<!-- <img src=resources/figure-4_cropped.gif alt=tracked cells width=720> -->

## Purpose

This repository accompanies the pub "[Rescuing _Chlamydomonas_ motility in mutants modeling spermatogenic failure](https://doi.org/10.57844/arcadia-fe2a-711e)." It contains the code, scripts, and notebooks developed for the acquisition, processing, and analysis involved in the pub as well as the motility data on which the analysis was based.


## Installation and Setup

This repository uses conda to manage software environments and installations. If you do not already have conda installed, you can find operating system-specific instructions for installing miniconda [here](https://docs.anaconda.com/miniconda/). After installing conda, navigate to a directory where you would like to clone the repository, and run the following commands to create the pipeline run environment.

Start by cloning the repository and installing the required dependencies into a fresh conda environment:
```{bash}
git clone https://github.com/Arcadia-Science/2024-chlamy-mutant-motility-pub.git
cd 2024-chlamy-mutant-motility-pub
conda env create -n chlamy-mutant-motility --file envs/dev.yml
conda activate chlamy-mutant-motility
```

In order to enable cell tracking capabilities to process the raw image data or run the script `compute_motility_metrics.py`, you must also install the Python package within the repo [`2024-unicellular-tracking`](https://github.com/Arcadia-Science/2024-unicellular-tracking). This can be done by running the following commands:
```{bash}
cd ..
git clone https://github.com/Arcadia-Science/2024-unicellular-tracking.git
cd 2024-unicellular-tracking
conda env update --file envs/dev.yml
pip install -e .
```


## Data

The data accompanying this pub is divided into two main folders, each corresponding to one of the assays described in the pub.

- **Assay 1**: [`vbottom_motility_assay`](data/vbottom_motility_assay/):  
Raw images from the v-bottom motility assay are stored as ZIP files within this directory. The ZIP files contain single frame AVI files of either 96- or 384-well v-bottom plates containing *C. reinhardtii* cultures. Additionally, the final frame from each of these data acquisitions was cropped in FIJI and are available in [`cropped_final_frames`](data/vbottom_motility_assay/cropped_final_frames/).

- **Assay 2**: [`single-cell-motility-assay`](data/single-cell-motility-assay/):  
As described in the [pub](https://doi.org/10.57844/arcadia-fe2a-711e), the motility data was derived from processing brightfield time-lapse microscopy data of _C. reinhardtii_ cells swimming in a 384-well plate. The image dataset underlying the pub is 108 GB and has been uploaded to the BioImage Archive: [S-BIAD1470](https://doi.org/10.6019/S-BIAD1470).  
While the image data is too large to be included in this repository, CSV files of the detected cell trajectories can be found in [`cell_trajectories`](data/single-cell-motility-assay/cell_trajectories/). The CSV files contain time series of x, y coordinates of tracked cells, from which summary motility statistics are calculated and output to a [single CSV file](data/single-cell-motility-assay/single-cell-motility-assay_summary-statistics.csv) as described in [Methods](#computing-summary-motility-statistics).


## Overview

### Description of the folder structure

This repository is organized into the following top-level directories.
- **data**: See [Data](#data).
- **envs**: Contains a conda environment YML file that lists the packages and dependencies used for creating the conda environment.
- **notebooks**: A collection of Jupyter notebooks for analyzing motility data.
- **resources**: Static files rendered within the repository.
- **src**: Python modules that support the analyses composed in the notebooks such as for extracting intensity profiles for the v-bottom motility assay and calculating statistics.
- **src/scripts**: 
  - `bioimage_archive_file_list.py`: A Python script for generating the list of files needed for the BioImage Archive upload. (No longer intended to be run.)
  - `compute_motility_metrics.py`: A Python script for computing summary motility statistics from cell trajectories.
  - `create_vbottom_gifs.py`: A Python script for creating GIFs from the zipped AVI files from the v-bottom motility assay data.

### Methods

#### Cell tracking
Cell tracking was performed using the [`track_cells.py`](https://github.com/Arcadia-Science/2024-unicellular-tracking/blob/eed79846209ec2ed7b805f843b0a4d89c272a339/src/chlamytracker/scripts/track_cells.py) script included in [`2024-unicellular-tracking`](https://github.com/Arcadia-Science/2024-unicellular-tracking). To extract cell trajectories from image data, the image data must first be downloaded from [TODO: insert link to dataset on BioImage Archive]. The following command was used to perform cell tracking:
```{bash}
python src/chlamytracker/scripts/track_cells.py 20240425_174057_487 --use-dask
```

The same command was repeated for the dataset of cells after 18 hours by substituting in `20240426_095610_676` for the first argument.
See the [README](https://github.com/Arcadia-Science/2024-unicellular-tracking?tab=readme-ov-file#scripts) for more extensive documentation on how the `track_cells.py` script can be configured.

#### Computing summary motility statistics
To generate the summary motility statistics for each dataset of cell trajectories, the script `compute_motility_metrics.py` was run using the commands:
```{bash}
python src/scripts/compute_motility_metrics.py data/cell_trajectories/20240425_174057_487/
python src/scripts/compute_motility_metrics.py data/cell_trajectories/20240426_095610_676/
```

#### Generating figures
The statistical analysis was done through a series of Jupyter notebooks in which several figures in the pub were also created. The list below maps each figure to the corresponding analysis notebook.
- **Figure 3**: [1_vbottom-motility-linescan.ipynb](notebooks/1_vbottom-motility-linescan.ipynb)
- **Figure 4**: [2_mutant-motility-pca.ipynb](notebooks/2_mutant-motility-pca.ipynb)
- **Figure 5**: [1_vbottom-motility-linescan.ipynb](notebooks/1_vbottom-motility-linescan.ipynb)
- **Figure 6**: [2_mutant-motility-pca.ipynb](notebooks/2_mutant-motility-pca.ipynb)
- **Figure S1**: [3_supplemental-analysis.ipynb](notebooks/3_supplemental-analysis.ipynb)
- **Figure S2**: [3_supplemental-analysis.ipynb](notebooks/3_supplemental-analysis.ipynb)


### Compute Specifications

Cell tracking was done on a Supermicro X12SPA-TF 64L running Ubuntu 22.04.1 with 512 GB RAM, 64 cores, and a 2 TB SSD.

The notebooks for statistical analysis were run on an Apple MacBook Pro with an Apple M3 Max chip running macOS Sonoma version 14.5 with 36 GB RAM, 14 cores, and 1 TB SSD.


## Contributing

See how we recognize [feedback and contributions to our code](https://github.com/Arcadia-Science/arcadia-software-handbook/blob/main/guides-and-standards/guide-credit-for-contributions.md).
