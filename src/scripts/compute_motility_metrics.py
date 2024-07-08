import json
from pathlib import Path

import click
import pandas as pd
from chlamytracker.tracking_metrics import TrajectoryCSVParser
from natsort import natsorted
from tqdm import tqdm

INPUT_DIRECTORY = Path(__file__).parents[2] / "data/cell_trajectory_csvs/"
INPUT_JSON = Path(__file__).parents[2] / "data/experimental_parameters.json"
OUTPUT_CSV = Path(__file__).parents[2] / "data/summary_motility_metrics.csv"

trajectory_time_threshold_option = click.option(
    "--time-threshold",
    "time_threshold",
    default=10.0,
    show_default=True,
    help=(
        "Minimum trajectory duration (in seconds). Motility metrics from cells with a shorter "
        "trajectory duration than this threshold will be discarded."
    ),
)

trajectory_distance_threshold_option = click.option(
    "--distance-threshold",
    "distance_threshold",
    default=20.0,
    show_default=True,
    help=(
        "Minimum trajectory distance (in microns). Motility metrics from cells that traverse a "
        "shorter distance than this threshold will be discarded."
    ),
)


@trajectory_distance_threshold_option
@trajectory_time_threshold_option
@click.command()
def main(time_threshold, distance_threshold):
    """Script for computing summary motility metrics from cell trajectory data.

    Parses cell trajectory coordinates from CSV files and computes a variety of motility metrics
    for each cell trajectory. Methodology for computing motility metrics is provided in [1].
    Outputs a summary CSV file in which the columns are the various motility metrics (total
    distance, mean curvilinear speed, mean angular speed, etc.), and each row corresponds to the
    summary motility metrics for one particular cell trajectory. Cell trajectories with a duration
    shorter than `time_threshold` or distance traversed shorter than `distance_threshold` are
    discarded.

    References
    ----------
    [1] https://doi.org/10.57844/arcadia-2d61-fb05
    """
    # handle missing file paths
    if not INPUT_DIRECTORY.exists():
        msg = "Input directory for CSV files of cell trajectories not found."
        raise FileNotFoundError(msg)

    if not INPUT_JSON.exists():
        msg = "Input json file for experimental parameters not found."
        raise FileNotFoundError(msg)

    # load experimental parameters
    experimental_parameters = json.loads(INPUT_JSON.read_text())
    framerate = experimental_parameters["framerate"]
    pixelsize = experimental_parameters["pixelsize"]

    # collect CSV files to process
    trajectory_csvs = natsorted(INPUT_DIRECTORY.glob("*.csv"))
    # initialize dataframe of summary motility metrics
    motility_metrics_dataframe = pd.DataFrame()

    for csv in tqdm(trajectory_csvs):
        # extract well ID from CSV filename
        well_id = csv.name.split("_")[0]

        # parse motility data from CSV
        cell_trajectories = TrajectoryCSVParser(csv, framerate, pixelsize)

        # estimate cell count and compute motility measurements for a batch of cell trajectories
        cell_count = cell_trajectories.estimate_cell_count()
        motility_metrics = cell_trajectories.compute_summary_statistics()
        dataframe = pd.DataFrame(motility_metrics)

        # build up dataframe
        dataframe["cell_count"] = cell_count
        dataframe["strain"] = experimental_parameters[well_id]["strain"]
        dataframe["drug"] = experimental_parameters[well_id]["drug"]
        dataframe["concentration"] = experimental_parameters[well_id]["concentration"]
        dataframe["well_ID"] = well_id

        # concatenate batch of motility metrics
        motility_metrics_dataframe = pd.concat([motility_metrics_dataframe, dataframe])

    # clean up dataframe and apply thresholds
    motility_metrics_dataframe = motility_metrics_dataframe.drop("cell_id", axis=1).reset_index(
        drop=True
    )
    motility_metrics_dataframe_filtered = motility_metrics_dataframe.loc[
        (motility_metrics_dataframe["total_time"] >= time_threshold)
        & (motility_metrics_dataframe["total_distance"] >= distance_threshold)
    ]

    # export to CSV
    motility_metrics_dataframe_filtered.to_csv(OUTPUT_CSV, index=False)


if __name__ == "__main__":
    main()
