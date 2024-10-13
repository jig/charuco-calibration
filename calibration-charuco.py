#!/usr/bin/env python

import cv2 # Import the OpenCV library to enable computer vision
import numpy as np # Import the NumPy scientific computing library
import glob # Used to get retrieve files that have a specified pattern
import os

# ------------------------------
# ENTER YOUR REQUIREMENTS HERE:
ARUCO_DICT = cv2.aruco.DICT_6X6_50
SQUARES_VERTICALLY = 7
SQUARES_HORIZONTALLY = 5
# size in meters
SQUARE_LENGTH = 0.03
MARKER_LENGTH = 0.015
# ...
PATH_TO_YOUR_IMAGES = '.'
# ------------------------------

def calibrate_and_save_parameters():
    # Define the aruco dictionary and charuco board
    dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
    board = cv2.aruco.CharucoBoard((SQUARES_VERTICALLY, SQUARES_HORIZONTALLY), SQUARE_LENGTH, MARKER_LENGTH, dictionary)
    params = cv2.aruco.DetectorParameters()

    # Load PNG images from folder
    image_files = [os.path.join(PATH_TO_YOUR_IMAGES, f) for f in os.listdir(PATH_TO_YOUR_IMAGES) if f.endswith(".jpg")]
    image_files.sort()  # Ensure files are in order

    all_charuco_corners = []
    all_charuco_ids = []

    counter = 0
    for image_file in image_files:
        image = cv2.imread(image_file)
        image_copy = image.copy()
        marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(image, dictionary, parameters=params)

        # If at least one marker is detected
        if marker_ids is not None and len(marker_ids) > 0:
            cv2.aruco.drawDetectedMarkers(image_copy, marker_corners, marker_ids)
            charuco_retval, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(marker_corners, marker_ids, image, board)
            if charuco_retval:
                all_charuco_corners.append(charuco_corners)
                all_charuco_ids.append(charuco_ids)
                print(counter, image_file, "used")
                counter += 1
            else:
                print("   ", image_file, "not ret val")
        else:
            print("   ", image_file, "no markers")

    # Calibrate camera
    print("start calibration")
    retval, camera_matrix, distortion_coefficients, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(all_charuco_corners, all_charuco_ids, board, image.shape[:2], None, None)
    print("calibration done")

    # Save parameters to a file
    cv_file = cv2.FileStorage('calibration_chessboard.yaml', cv2.FILE_STORAGE_WRITE)
    cv_file.write('K', camera_matrix)
    cv_file.write('D', distortion_coefficients)
    cv_file.release()

    # Load the parameters from the saved file
    cv_file = cv2.FileStorage('calibration_chessboard.yaml', cv2.FILE_STORAGE_READ)
    camera_matrix = cv_file.getNode('K').mat()
    distortion_coefficients = cv_file.getNode('D').mat()
    cv_file.release()

    # Display key parameter outputs of the camera calibration process
    print("Camera matrix:")
    print(camera_matrix)

    print("\n Distortion coefficient:")
    print(distortion_coefficients)

    # Iterate through displaying all the images
    for image_file in image_files:
        image = cv2.imread(image_file)
        undistorted_image = cv2.undistort(image, camera_matrix, distortion_coefficients)
        print("comparing", image_file)
        cv2.imshow('Distorted Image', image)
        cv2.imshow('Undistorted Image', undistorted_image)
        cv2.waitKey(0)

    cv2.destroyAllWindows()

calibrate_and_save_parameters()
