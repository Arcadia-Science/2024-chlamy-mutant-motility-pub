import json
import re
from pathlib import Path

import click
import pandas as pd
from chlamytracker.tracking_metrics import TrajectoryCSVParser
from natsort import natsorted
from tqdm import tqdm

INPUT_DIRECTORY = Path(__file__).parents[2] / "data/cell_trajectory_csvs/"
INPUT_JSON = Path(__file__).parents[2] / "data/experimental_parameters.json"
OUTPUT_CSV = Path(__file__).parents[2] / "data/summary_motility_metrics.csv"

input_directory_option = click.option(
    "--input-directory",
    "input_directory",
    default=INPUT_DIRECTORY,
    show_default=True,
    type=click.Path(file_okay=False, exists=True),
    help="File path to directory containing csv files of cell trajectories.",
)

input_json_option = click.option(
    "--input-json",
    "input_json",
    default=INPUT_JSON,
    show_default=True,
    type=click.Path(dir_okay=False, exists=True),
    help="File path to input json file containing experimental parameters.",
)

output_csv_option = click.option(
    "--output-csv",
    "output_csv",
    default=OUTPUT_CSV,
    show_default=True,
    type=click.Path(dir_okay=False, writable=True),
    help="File path to output csv file of summary motility metrics.",
)


@output_csv_option
@input_json_option
@input_directory_option
@click.command()
def main(input_directory, input_json, output_csv):
    """"""

    print("input_directory ::", input_directory)
    print("input_json ::", input_json)
    print("output_csv ::", output_csv)


    # experimental_parameters = json.loads

    # glob csvs

    # filter

    # export


if __name__ == "__main__":
    main()
