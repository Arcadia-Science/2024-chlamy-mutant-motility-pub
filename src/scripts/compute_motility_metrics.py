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


@click.command()
def main():
    """"""

    print("input_directory ::", INPUT_DIRECTORY)
    print("input_json ::", INPUT_JSON)
    print("output_csv ::", OUTPUT_CSV)

    # experimental_parameters = json.loads

    # glob csvs

    # filter

    # export


if __name__ == "__main__":
    main()
