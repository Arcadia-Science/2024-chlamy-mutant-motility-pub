import sys as sys
import time

# Replace with path to local clone of Arcadia-Science/arcadia-phenotypeomat-protocol repo
sys.path.insert(0, "/path/to/arcadia-phenotypeomat-protocol/flir_camera_tools")

import cam_tools
import click
import serial
from pyzbar.pyzbar import decode

num_cycles_option = click.option(
    "--num-cycles",
    "num_cycles",
    type=int,
    default=96,
    show_default=True,
    help="Number of imaging cycles to run through.",
)

duration_option = click.option(
    "--pause",
    "pause_duration_min",
    type=int,
    default=1,
    show_default=True,
    help="Number of minutes to pause between imaging cycles",
)


@duration_option
@num_cycles_option
@click.command()
def main(num_cycles, pause_duration_min):
    """A script to periodically acquire images from the phenotype-o-mat.

    This script has been adapted from
    https://github.com/Arcadia-Science/arcadia-phenotypeomat-protocol/blob/main/test_assay_growth_curve_chlamy.py
    """
    # Establish serial communication with the microcontroller to control the LEDs
    dev = serial.Serial("/dev/ttyACM0")

    # Turn off the LED before beginning imaging
    dev.write(b"SET LED_TRANS_STATUS 1;")

    # Check if any cameras are connected; if not, exit the program
    if not cam_tools.detect_cams():
        sys.exit()

    # Start communication with the Blackfly camera system
    system = cam_tools.ps.System.GetInstance()
    cam_list = system.GetCameras()
    cam = cam_list[0]
    cam.Init()

    # Set the exposure time of the camera to 500 ms for imaging
    cam_tools.set_expos_time(cam, 500)

    # Turn on the transmitted light (LED) and grow lights (460 nm and 670 nm LEDs)
    dev.write(b"SET LED_TRANS_STATUS 0;")
    dev.write(b"SET LED_460_STATUS 0;")
    dev.write(b"SET LED_670_STATUS 0;")

    # Capture the first image and get the timestamp
    image, timestamp = cam_tools.grab_images(cam, n_frames=1)

    # Attempt to read a barcode from the first image to identify the sample
    bcode = decode(image[0])
    if not bcode:  # If no barcode is detected, use a default value '00000'
        bcode = "00000"
    else:  # Otherwise, use the decoded barcode data
        bcode = bcode.data

    # Loop through 96 cycles
    for _ in range(0, num_cycles):
        # Reset the exposure time for the camera
        cam_tools.set_expos_time(cam, 500)

        # Turn off grow lights before imaging
        dev.write(b"SET LED_460_STATUS 1;")
        dev.write(b"SET LED_670_STATUS 1;")

        # Turn on the transmitted LED for imaging
        dev.write(b"SET LED_TRANS_STATUS 0;")

        # Wait for 5 seconds to stabilize the lighting conditions
        time.sleep(5)

        # Capture a single image with the camera and get timestamps
        images, timestamps = cam_tools.grab_images(cam, n_frames=1)

        # Save the captured images as an AVI, using the barcode for file identification
        cam_tools.save_avi(images, barcode=bcode, prefix="algae_growth_curve")

        # Turn the grow lights back on for algae growth
        dev.write(b"SET LED_460_STATUS 0;")
        dev.write(b"SET LED_670_STATUS 0;")

        # Pause duration before the next cycle
        time.sleep(60 * pause_duration_min)

        # Turn off the transmitted LED after the image capture
        dev.write(b"SET LED_TRANS_STATUS 1;")

    # Print the total imaging time (difference between the first and last timestamps)
    print(str(timestamps[-1] - timestamps[0]))
    # Print the time between the last two captured frames
    print(str(timestamps[-1] - timestamps[-2]))

    # Turn off the transmitted LED at the end of the process
    dev.write(b"SET LED_TRANS_STATUS 1;")

    # Release the camera and clean up
    del cam
    cam_list.Clear()
    system.ReleaseInstance()


if __name__ == "__main__":
    main()
