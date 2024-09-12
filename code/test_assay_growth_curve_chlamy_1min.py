# Import necessary modules
import sys as sys
sys.path.insert(0, '/home/arcadia/git/arcadia-phenotypomat/phenotyper/')  # Add the path for phenotyper tools to the system path
import cam_tools as ct  # Import camera tools for interacting with the Blackfly camera
import matplotlib.pyplot as plt  # Import for potential plotting, though not used in this code
import serial as ser  # Import for serial communication (to control the LED and grow lights)
import time as tm  # Import to handle delays (e.g., between frames)
from pyzbar.pyzbar import decode  # Import to decode barcodes from the images

# Establish serial communication with the microcontroller (controls the LEDs and grow lights)
dev = ser.Serial('/dev/ttyACM0')  

# Turn off the transmitted light (LED) before starting the imaging process
dev.write(b'SET LED_TRANS_STATUS 1;')

# Ensure that Blackfly cameras are connected to the system
if not ct.detect_cams():  
    sys.exit()

# Start communication with the Blackfly camera system
system = ct.ps.System.GetInstance()

# Get the list of all connected cameras
cam_list = system.GetCameras()

# Select the first camera (index 0)
cam = cam_list[0]

# Initialize the selected camera
cam.Init()

# Set the exposure time of the camera to 500 ms
ct.set_expos_time(cam, 500)

# Turn on the transmitted light (LED) and grow lights (460 nm and 670 nm LEDs)
dev.write(b'SET LED_TRANS_STATUS 0;')  # Turn on the transmitted light
dev.write(b'SET LED_460_STATUS 0;')  # Turn on 460 nm grow light
dev.write(b'SET LED_670_STATUS 0;')  # Turn on 670 nm grow light

# Capture the first image and get the timestamp
image, timestamp = ct.grab_images(cam, n_frames=1)

# Attempt to decode a barcode from the first image to identify the sample
bcode = decode(image[0])
if not bcode:  # If no barcode is found, use a default value '00000'
    bcode = '00000'
else:  # Otherwise, use the decoded barcode data
    bcode = bcode.data

# Loop through 96 cycles (for each well in the 96-well plate)
for n in range(0, 96):
    # Reset the exposure time for the camera to 500 ms
    ct.set_expos_time(cam, 500)
    
    # Turn off grow lights (460 nm and 670 nm) before imaging
    dev.write(b'SET LED_460_STATUS 1;')  # Turn off 460 nm grow light
    dev.write(b'SET LED_670_STATUS 1;')  # Turn off 670 nm grow light
    
    # Turn on the transmitted light (LED) for imaging
    dev.write(b'SET LED_TRANS_STATUS 0;')  
    
    # Wait for 5 seconds to stabilize lighting
    tm.sleep(5)
    
    # Capture an image with the camera and get the timestamps
    images, timestamps = ct.grab_images(cam, n_frames=1)
    
    # Save the captured images as an AVI video, using the barcode for file identification
    ct.save_avi(images, barcode=bcode, prefix='algae_growth_curve')
    
    # Turn the grow lights (460 nm and 670 nm LEDs) back on after imaging
    dev.write(b'SET LED_460_STATUS 0;')  
    dev.write(b'SET LED_670_STATUS 0;')
    
    # Wait for 1 minute before capturing the next image
    tm.sleep(60 * 1)
    
    # Turn off the transmitted light (LED) after each imaging cycle
    dev.write(b'SET LED_TRANS_STATUS 1;)

# Print the total imaging time (difference between the first and last timestamps)
print(str(timestamps[-1] - timestamps[0]))

# Print the time between the last two captured frames
print(str(timestamps[-1] - timestamps[-2]))

# Turn off the transmitted light (LED) at the end of the experiment
dev.write(b'SET LED_TRANS_STATUS 1;)

# Clean up: release the camera and the system handlers
del cam  # De-initialize the camera
cam_list.Clear()  # De-initialize the list of cameras
system.ReleaseInstance()  # Release the camera system handlers