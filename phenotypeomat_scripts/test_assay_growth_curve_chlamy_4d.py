import sys as sys

sys.path.insert(
    0, "/home/arcadia/git/arcadia-phenotypomat/phenotyper/"
)  # Add the path for phenotyper tools to the system path
import time as tm  # Import to handle delays (e.g., between frames)

import cam_tools as ct  # Import camera tools for interacting with the Blackfly camera
import serial as ser  # Import for serial communication (to control the LED and grow lights)
from pyzbar.pyzbar import decode  # Import to decode barcodes from the images

# Establish serial communication with the microcontroller to control the LEDs
dev = ser.Serial("/dev/ttyACM0")  # Set up a serial connection to the microcontroller

# Turn off the LED before beginning imaging
dev.write(b"SET LED_TRANS_STATUS 1;")

# Check if any cameras are connected; if not, exit the program
if not ct.detect_cams():
    sys.exit()

# Start communication with the camera system (Blackfly cameras)
system = ct.ps.System.GetInstance()

# Get a list of all connected cameras
cam_list = system.GetCameras()

# Select the first camera (index 0)
cam = cam_list[0]

# Initialize the selected camera
cam.Init()

# Set the exposure time of the camera to 500 ms for imaging
ct.set_expos_time(cam, 500)

# Turn on the white LED for transmitted light imaging
dev.write(b"SET LED_TRANS_STATUS 0;")

# Turn on grow lights (460 nm and 670 nm LEDs) for algae growth
dev.write(b"SET LED_460_STATUS 0;")
dev.write(b"SET LED_670_STATUS 0;")

# Capture an image from the camera and extract the timestamp
image, timestamp = ct.grab_images(cam, n_frames=1)

# Attempt to read a barcode from the first image to identify the sample
bcode = decode(image[0])
if not bcode:  # If no barcode is detected, use a default value '00000'
    bcode = "00000"
else:  # Otherwise, use the decoded barcode data
    bcode = bcode.data

# Loop through 96 cycles (for each well in the plate)
for _ in range(0, 96):
    # Reset the exposure time for the camera
    ct.set_expos_time(cam, 500)

    # Turn off grow lights (460 nm and 670 nm LEDs) before imaging
    dev.write(b"SET LED_460_STATUS 1;")
    dev.write(b"SET LED_670_STATUS 1;")

    # Turn on the transmitted LED for imaging
    dev.write(b"SET LED_TRANS_STATUS 0;")

    # Wait for 5 seconds to stabilize the lighting conditions
    tm.sleep(5)

    # Capture a single image with the camera and get timestamps
    images, timestamps = ct.grab_images(cam, n_frames=1)

    # Save the captured image as an AVI video using the barcode for identification
    ct.save_avi(images, barcode=bcode, prefix="algae_growth_curve")

    # Turn the grow lights (460 nm and 670 nm LEDs) back on for algae growth
    dev.write(b"SET LED_460_STATUS 0;")
    dev.write(b"SET LED_670_STATUS 0;")

    # Wait for 1 hour (60 minutes * 60 seconds) before the next cycle
    tm.sleep(60 * 60)

    # Turn off the transmitted LED after the image capture
    dev.write(b"SET LED_TRANS_STATUS 1;")

# Print the total imaging time (difference between the first and last timestamps)
print(str(timestamps[-1] - timestamps[0]))

# Print the time between the last two captured frames
print(str(timestamps[-1] - timestamps[-2]))

# Turn off the transmitted LED at the end of the process
dev.write(b"SET LED_TRANS_STATUS 1;")

# Release the camera and clean up
del cam  # Delete the camera object to turn off the camera
cam_list.Clear()  # De-initialize the cameras
system.ReleaseInstance()  # Release the camera system handler
