import re
import zipfile
from datetime import timedelta
from pathlib import Path

import click
import cv2
import imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT_DIRPATH = Path(__file__).parents[2]
DEFAULT_ZIPFOLDER_FILEPATH = (
    REPO_ROOT_DIRPATH / "data/vbottom_motility_assay/vbottom_motility_strains.zip"
)
DEFAULT_OUTPUT_GIF_FILEPATH = REPO_ROOT_DIRPATH / "results/vbottom_strain_output_video.gif"

zipfolder_filepath_option = click.option(
    "--zipfolder",
    "zipfolder_filepath",
    type=Path,
    default=DEFAULT_ZIPFOLDER_FILEPATH,
    show_default=True,
    help="Filepath location to zip folder.",
)

extracted_folder_filepath_option = click.option(
    "--extract-to",
    "extracted_folder_filepath",
    type=Path,
    default=None,
    show_default=False,
    help="Filepath location for where to extract contents of zip folder.",
)

output_gif_filepath_option = click.option(
    "--gif",
    "output_gif_filepath",
    type=Path,
    default=DEFAULT_OUTPUT_GIF_FILEPATH,
    show_default=True,
    help="Filepath location for where to output GIF.",
)


def add_timestamp(img, timestamp):
    pil_img = Image.fromarray(img)
    draw = ImageDraw.Draw(pil_img)
    font_path = "/Library/Fonts/Arial.ttf"
    font_size = 32
    try:
        font = ImageFont.truetype(font_path, font_size)
    except OSError:
        font = ImageFont.load_default(font_size)
    text_position = (10, 10)
    text_color = (255, 255, 255)
    draw.text(text_position, timestamp, font=font, fill=text_color)
    return np.array(pil_img)


def extract_timestamp(filename):
    match = re.search(r"_(\d+)\.avi$", filename.as_posix())
    if match:
        return int(match.group(1))
    else:
        raise ValueError(f"No numeric timestamp found in filename: {filename}")


def process_videos(input_folder, output_gif):
    video_files = sorted(input_folder.glob("*.avi"))
    if not video_files:
        print("No .avi files found in the directory.")
        return

    video_files.sort(key=extract_timestamp)

    print(f"Processing {len(video_files)} files...")

    gif_frames = []
    base_time = extract_timestamp(video_files[0])

    for filename in video_files:
        current_time = extract_timestamp(filename)
        timestamp_diff = current_time - base_time
        timestamp = str(timedelta(seconds=timestamp_diff))

        cap = cv2.VideoCapture(filename)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_with_timestamp = add_timestamp(frame, timestamp)
            gif_frames.append(frame_with_timestamp)
        cap.release()

    # Save as GIF
    imageio.mimsave(output_gif, gif_frames, fps=20)
    print("GIF creation complete.")


@output_gif_filepath_option
@extracted_folder_filepath_option
@zipfolder_filepath_option
@click.command()
def main(zipfolder_filepath, extracted_folder_filepath, output_gif_filepath):
    """This script processes a set of AVI video files, adds timestamps based on the file names,
    and combines them into an animated GIF for visualization.

    Key Steps:

        1. Timestamp Extraction: Extracts timestamps from video filenames using regex to calculate
        time differences between frames.

        2. Video Processing: Reads each video file, applies a timestamp to each frame, and collects
        frames for GIF creation.

        3. GIF Creation: Combines processed frames into a single animated GIF and saves the output.

        4. ZIP File Handling: Extracts video files from a specified ZIP archive before processing.

    Outputs:

        Animated GIF: A GIF created from the processed video frames, saved to the specified output
        path.
    """

    # Ensure the output directory exists
    output_dir = output_gif_filepath.parent
    if not output_dir.exists():
        output_dir.mkdir(exist_ok=True)

    # Set default extracted folder if not provided
    if extracted_folder_filepath is None:
        extracted_folder_filepath = zipfolder_filepath.parent / zipfolder_filepath.stem

    # Extract the .zip file
    with zipfile.ZipFile(zipfolder_filepath, "r") as zip_ref:
        zip_ref.extractall(extracted_folder_filepath)
        print(f"Files extracted to: {extracted_folder_filepath}")

    # Process the videos from the extracted folder
    print(f"Outputting GIF to: {output_gif_filepath}")
    process_videos(extracted_folder_filepath, output_gif_filepath)


if __name__ == "__main__":
    main()
