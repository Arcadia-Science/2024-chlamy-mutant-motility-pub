# 2024-chlamy-mutant-motility-pub

[![run with conda](https://img.shields.io/badge/run%20with-conda-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/projects/miniconda/en/latest/)
[![Arcadia Pub](https://img.shields.io/badge/Arcadia-Pub-596F74.svg?logo=data:image/svg%2bxml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPCEtLSBHZW5lcmF0b3I6IEFkb2JlIElsbHVzdHJhdG9yIDI3LjcuMCwgU1ZHIEV4cG9ydCBQbHVnLUluIC4gU1ZHIFZlcnNpb246IDYuMDAgQnVpbGQgMCkgIC0tPgo8c3ZnIHZlcnNpb249IjEuMSIgaWQ9IkxheWVyXzEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHg9IjBweCIgeT0iMHB4IgoJIHZpZXdCb3g9IjAgMCA0My4yIDQwLjQiIHN0eWxlPSJlbmFibGUtYmFja2dyb3VuZDpuZXcgMCAwIDQzLjIgNDAuNDsiIHhtbDpzcGFjZT0icHJlc2VydmUiPgo8c3R5bGUgdHlwZT0idGV4dC9jc3MiPgoJLnN0MHtmaWxsOm5vbmU7c3Ryb2tlOiNGRkZGRkY7c3Ryb2tlLXdpZHRoOjI7c3Ryb2tlLWxpbmVqb2luOmJldmVsO3N0cm9rZS1taXRlcmxpbWl0OjEwO30KPC9zdHlsZT4KPGc+Cgk8cG9seWdvbiBjbGFzcz0ic3QwIiBwb2ludHM9IjIxLjYsMyAxLjcsMzcuNCA0MS41LDM3LjQgCSIvPgoJPGxpbmUgY2xhc3M9InN0MCIgeDE9IjIxLjYiIHkxPSIzIiB4Mj0iMjEuNiIgeTI9IjI3LjMiLz4KCTxwb2x5bGluZSBjbGFzcz0ic3QwIiBwb2ludHM9IjEyLjIsMTkuNCAyNC42LDMwLjEgMjQuNiwzNy40IAkiLz4KCTxsaW5lIGNsYXNzPSJzdDAiIHgxPSIxNy42IiB5MT0iMTYuNyIgeDI9IjE3LjYiIHkyPSIyNC4xIi8+Cgk8bGluZSBjbGFzcz0ic3QwIiB4MT0iMjguNiIgeTE9IjE1LjIiIHgyPSIyMS43IiB5Mj0iMjIuMSIvPgoJPHBvbHlsaW5lIGNsYXNzPSJzdDAiIHBvaW50cz0iNi44LDI4LjcgMTkuNSwzNC40IDE5LjUsMzcuNCAJIi8+Cgk8bGluZSBjbGFzcz0ic3QwIiB4MT0iMzQuOCIgeTE9IjI1LjgiIHgyPSIyNC42IiB5Mj0iMzYuMSIvPgoJPGxpbmUgY2xhc3M9InN0MCIgeDE9IjI5LjciIHkxPSIyMi4yIiB4Mj0iMjkuNyIgeTI9IjMwLjkiLz4KPC9nPgo8L3N2Zz4K)](https://doi.org/10.57844/arcadia-fe2a-711e)


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

As described in the [pub](https://doi.org/10.57844/arcadia-fe2a-711e), the motility data was derived from processing brightfield time-lapse microscopy data of _C. reinhardtii_ cells swimming in a 384-well plate. The image dataset underlying the pub is ____ (either 244 GB or 101 GB depending on whether 18 hr dataset is included) and has been uploaded to the BioImage Archive (DOI: ______).

> TODO: Add details about the description of image data (that will ultimately be) uploaded to the BioImage Archive. Main thing relevant for documentation here is that the dataset is divided into two subdirectories: `20240425_174057_487` and `20240426_095610_676`. The first contains time-lapse data of cells swimming in drugs for 2 hours while the cells were immersed in drugs for 18 hours in the second.

While the image data is too large to be included in this repository, CSV files of the detected cell trajectories can be found in [`data/cell_trajectories/`](data/cell_trajectories/). The CSV files contain time series of x, y coordinates of tracked cells, from which summary motility statistics are calculated and output to [`data/`](data/) as described in [Methods](#computing-summary-motility-statistics).

Raw images from the v-bottom motility assay are present as zipped files in ['data/vbottom_avi/'](data/vbottom_avi). The ZIP files contain single frame AVI files of either 96- or 384-well v-bottom plates containing *C. reinhardtii* cultures. Additionally, the final frame from these data acquisitions were cropped in FIJI and are available in ['data/vbottom_avi/cropped_final_frame/'](data/vbottom_avi/cropped_final_frame). 


## Overview

### Description of the folder structure

This repository is organized into the following top-level directories.
- **data**: CSV files containing cell trajectories as well as summary CSV files of computed motility metrics. There are two datasets of cell trajectories from two rounds of imaging: 2 hours post-treatment and 18 hours post-treatment. For each dataset there is also a CSV file of summary motility metrics. This folder also contains a list of experimental parameters related to the sample preparation, `experimental_parameters.json`. Finally, this folder includes AVI files of single-frame images of 96- or 384- well plates imaged on the Phenotype-o-mat
- **envs**: contains a conda environment YML file that lists the packages and dependencies used for creating the conda environment.
- **notebooks**: a collection of Jupyter notebooks for analyzing motility data.
- **src/scripts**: a Python script for computing summary motility statistics from cell trajectories.

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
- Figure 2: ____.ipynb
- Figure 3: ____.ipynb
- Figure 4: ____.ipynb

TODO: update list when finalized...


### Compute Specifications

Cell tracking was done on a Supermicro X12SPA-TF 64L running Ubuntu 22.04.1 with 512 GB RAM, 64 cores, and a 2 TB SSD.

The notebooks for statistical analysis were run on an Apple MacBook Pro with an Apple M3 Max chip running macOS Sonoma version 14.5 with 36 GB RAM, 14 cores, and 1 TB SSD.


## Contributing

See how we recognize [feedback and contributions to our code](https://github.com/Arcadia-Science/arcadia-software-handbook/blob/main/guides-and-standards/guide-credit-for-contributions.md).
