import numpy as np
import cv2

# Reads video frames by frame and outputs the optical flow as a BGR image
def calculate_opt_dense(frame1, frame2):
    # Convert the images to Grayscale
    prev = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
    # Prepare HSV
    hsv = np.zeros_like(frame1)
    hsv[..., 1] = 255

    # Calculate the optical flow
    flow = cv2.calcOpticalFlowFarneback(prev, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    # Populate HSV image with optical flow values
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] = ang*180/np.pi/2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)

    # Return the optical flow in BGR, as it was inputted
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)