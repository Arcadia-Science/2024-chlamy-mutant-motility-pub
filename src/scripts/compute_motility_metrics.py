import json
from pathlib import Path

import click
import pandas as pd
from natsort import natsorted
from swimtracker.tracking_metrics import TrajectoryCSVParser
from tqdm import tqdm

REPO_ROOT_DIRECTORY = Path(__file__).parents[2]
DEFAULT_INPUT_DIRECTORY = REPO_ROOT_DIRECTORY / "data/single-cell-motility-assay/cell_trajectories/"
DEFAULT_INPUT_JSON_FILE = (
    REPO_ROOT_DIRECTORY / "data/single-cell-motility-assay/experimental_parameters.json"
)
DEFAULT_OUTPUT_DIRECTORY = DEFAULT_INPUT_DIRECTORY.parent

input_directory_option = click.option(
    "--input-directory",
    "input_directory",
    type=Path,
    default=DEFAULT_INPUT_DIRECTORY,
    show_default=True,
    help="File path to directory of CSV files of cell trajectories.",
)

input_json_option = click.option(
    "--json",
    "input_json_file",
    type=Path,
    default=DEFAULT_INPUT_JSON_FILE,
    show_default=True,
    help=(
        "File path to JSON file that maps each file in a dataset to a set of experimental "
        "parameters."
    ),
)

output_directory_option = click.option(
    "--output-directory",
    "output_directory",
    type=Path,
    default=DEFAULT_OUTPUT_DIRECTORY,
    show_default=True,
    help="File path for output CSV file of summary motility statistics.",
)

trajectory_time_threshold_option = click.option(
    "--time-threshold",
    "time_threshold",
    default=10.0,
    show_default=True,
    help=(
        "Minimum trajectory duration (in seconds). Motility measurements from cells with a shorter "
        "trajectory duration than this threshold will be discarded."
    ),
)

trajectory_distance_threshold_option = click.option(
    "--distance-threshold",
    "distance_threshold",
    default=20.0,
    show_default=True,
    help=(
        "Minimum trajectory distance (in microns). Motility measurements from cells that traverse "
        "a shorter distance than this threshold will be discarded."
    ),
)


@trajectory_distance_threshold_option
@trajectory_time_threshold_option
@output_directory_option
@input_json_option
@input_directory_option
@click.command()
def main(input_directory, input_json_file, output_directory, time_threshold, distance_threshold):
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
    dataset_name = input_directory.parent.name

    # handle missing file paths
    if not input_directory.exists():
        msg = f"Input directory for CSV files of cell trajectories not found: '{input_directory}'."
        raise FileNotFoundError(msg)
    if not input_json_file.exists():
        msg = f"Input json file for experimental parameters not found: '{input_json_file}'."
        raise FileNotFoundError(msg)
    if not output_directory.exists():
        output_directory.mkdir(exist_ok=True, parents=False)
    else:
        output_csv_file = output_directory / f"{dataset_name}_summary-statistics.csv"

    # collect CSV files to process
    trajectory_csvs = natsorted(input_directory.glob("*.csv"))
    if not trajectory_csvs:
        msg = f"No CSV files found in '{input_directory}'."
        raise FileNotFoundError(msg)

    # load experimental parameters
    experimental_parameters = json.loads(input_json_file.read_text())
    framerate = experimental_parameters[dataset_name]["framerate"]
    pixelsize = experimental_parameters[dataset_name]["pixelsize"]
    hours_in_drug = experimental_parameters[dataset_name]["hours_in_drug"]

    # initialize dataframe of summary motility metrics
    motility_metrics_dataframe = pd.DataFrame()

    for csv_filepath in tqdm(trajectory_csvs):
        # extract well ID from CSV filename
        well_id = csv_filepath.name.split("_")[0]

        # parse motility data from CSV
        cell_trajectories = TrajectoryCSVParser(csv_filepath, framerate, pixelsize)

        # estimate cell count and compute motility measurements for a batch of cell trajectories
        cell_count = cell_trajectories.estimate_cell_count()
        motility_metrics = cell_trajectories.compute_summary_statistics()
        dataframe = pd.DataFrame(motility_metrics)

        # build up dataframe
        dataframe["cell_count"] = cell_count
        dataframe["strain"] = experimental_parameters[well_id]["strain"]
        dataframe["drug"] = experimental_parameters[well_id]["drug"]
        dataframe["hours_in_drug"] = hours_in_drug
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
    motility_metrics_dataframe_filtered.to_csv(output_csv_file, index=False)


if __name__ == "__main__":
    main()
