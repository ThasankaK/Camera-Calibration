# Camera-Calibration

A simple setup using OpenCV and Python to return the calibration parameters needed for your camera. 

## Step 1. Capture Images
Run the get_imgs_webcam.py file to create a OpenCV window displaying the live footage taken from your camera. From then on, press "P" with the window open to take snapshots of the current frame, these images will be saved in a images/directory inside the Camera-Calibration folder. Make sure you are capturing images of a **rectangular checkerboard pattern**, the size of the checkerboard does not matter too much, but try to not make it too small (e.g (3x3) or smaller) as larger checkerboards lead to better coverage, perspective variaton, etc. Also, make sure you take several images, 5-20 to be safe, as sometimes the checkerboard finder function from OpenCV may not find the checkerboard in your picture. 

## Step 2. Adjust Calibration Settings
Before running the camera_calibration.py file, take a look inside the file and change around the following variables at the top of the file:

**board_size** (tuple): This is the board size of the checkerboard you will use, specified with 0-based indexing. For example, a 8x8 checkerboard with 8 squares on each side should be declared as (7, 7) tuple

**image_size** (tuple): This will be the size of the image that is taken from your camera, usually 640x480. Declare this variable as (Width, Height) tuple

**square_size_mm** (tuple): This is the size of the individual checkerboard squares in **millimeters**.

## Step 3. Run Calibration

Run the camera_calibration.py file and you will see which of the captured images are succesfully by the checkerboard detector function by OpenCV. If too little images got detected, it might be a good idea to rerun the capturing of the images. There will be some example images inside this repo that you can take a look at to see how you can rotate or tilt around the checkerboard to get good images for calibration. After the calibration process is completed, you will given a file called calibration_parameters.npz, and inside will be the saved calibration settings of your camera. These parameters can be useful in scenarios where camera calibration is required, such as for solving Perspective-n-Point (PnP) problems.

Inside the calibration_parameters file will be:

**Camera Matrix (camera_matrix)**: 
**Distortion Coefficients (dist_coeffs)**
**Rotational Vectors (rvecs)**:
**Translational Vectors (tvecs)**:
**Root-Mean Squared Error (rms_error)**:

## Important Notes
If get_imgs_webcam.py is not detecting your specific webcam, take a look inside and change the value where cv2.VideoCapture( ) is called. 0 is usually your main webcam device.

The calibration_parameters.npz file holds data in NumPy's compressed array format. To get these parameters from the file, the following code can be used to easily extract it.

```
import numpy as np

calibration_data = np.load("calibration_parameters.npz")
camera_matrix = calibration_data["camera_matrix"]
dist_coeffs = calibration_data["dist_coeffs"]
```
