# charuco-calibration
Script to find the distortion parameters of a Raspberry Pi Camera Module 3

Adapted from [Using ChArUco boards in OpenCV](https://medium.com/@ed.twomey1/using-charuco-boards-in-opencv-237d8bc9e40d)

Grab a bunch of images at high resolution on the Raspberry Pi Camera. This command will result in about 60 images.

´´´bash
rpicam-still --timeout 120000 --timelapse 2000 -o image%04d.jpg
´´´

and move it to a fast computer (Python script tested on MacOS Sequoia):

´´´bash
python ./calibration-charuco.py
´´´

If the scripts fails at some image number, find the image file name for that number (marked with # prefix) and start over.

After a successful execution will end up with a YAML file similar to this [calibration_chessboard.yaml](./calibration_chessboard.yaml) and open two windows to show the comparison between original and undistorted image.
