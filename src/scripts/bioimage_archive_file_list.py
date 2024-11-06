import json
from pathlib import Path

import click
import pandas as pd
from natsort import natsorted

ASSAY_DATA_DIRECTORY = Path(__file__).parents[2] / "data/single-cell-motility-assay/"
SAMPLE_PREP_PARAMETERS_JSON = ASSAY_DATA_DIRECTORY / "experimental_parameters.json"

COLUMN_NAMES_SAMPLE_PREP_PARAMETERS = [
    "well_id",
    "strain",
    "drug",
    "concentration",
]
COLUMN_NAMES = ["Files", "file_content"] + COLUMN_NAMES_SAMPLE_PREP_PARAMETERS

FILE_CONTENT_BLURBS = {
    ".nd2": "raw brightfield time-lapse microscopy data",
    ".csv": "coordinates from cell tracking",
    ".tiff": "segmented time lapse",
    ".mp4": "movie of tracked cells with animated trajectories",
}

input_directory_argument = click.argument(
    "input_directory",
    type=Path,
)


def generate_dataframe(study_component_directory):
    """Generate a DataFrame from which to create the file list."""
    sample_prep_parameters = json.loads(SAMPLE_PREP_PARAMETERS_JSON.read_text())

    # glob all raw + processed data files
    filepaths = natsorted(study_component_directory.glob("*.nd2")) + natsorted(
        study_component_directory.glob("processed/*")
    )

    file_list_data = []
    for path in filepaths:
        # extract `well_id` from filename
        well_id = path.name[:7]

        row = {
            "Files": Path(*path.parts[5:]),  # this is tricky // relies on the absolute path
            "file_content": FILE_CONTENT_BLURBS[path.suffix],
            "well_id": well_id,
            "strain": sample_prep_parameters[well_id]["strain"],
            "drug": sample_prep_parameters[well_id]["drug"],
            "concentration": sample_prep_parameters[well_id]["concentration"],
        }
        file_list_data.append(row)

    dataframe = pd.DataFrame(file_list_data, columns=COLUMN_NAMES)
    return dataframe


@click.command()
@input_directory_argument
def main(input_directory):
    """Create a file list to accompany data upload to BioImage Archive.

    BioImage Archive requires a File List [1] to accompany each study component [2] you upload.
    According to their website,
    > A File List is used to describe all the files that you wish to include in your submission,
      both image files and other supporting files e.g., analysis results. It contains file level
      metadata.

    The full list of rules regarding the File List is available via their website, but the ones
    that are relevant for programmatically generating the File List are
    > * File lists are File lists are tabular data, either in tsv or Excel (.xlsx) format.
      * The first column of the header has to be the word “Files”.
      * File path separator must be forward slash “/”.
      * Allowed characters :: a-z A-Z 0-9 !-_.*'()

    References
    ----------
    [1] https://www.ebi.ac.uk/bioimage-archive/help-file-list/
    [2] https://www.ebi.ac.uk/bioimage-archive/rembi-help-examples/
    """
    # assume subdirectories of input directory correspond to study components
    study_component_directories = natsorted(
        [directory for directory in input_directory.glob("*") if directory.is_dir()]
    )

    for directory in study_component_directories:
        study_component_name = directory.name

        if "" in study_component_name:
            dataframe = generate_dataframe(directory)
        else:
            msg = "Unknown study component '{study_component_name}'."
            raise ValueError(msg)

        tsv_filename = ASSAY_DATA_DIRECTORY / f"{study_component_name}_file-list.tsv"
        dataframe.to_csv(tsv_filename, sep="\t", index=False)


if __name__ == "__main__":
    main()
