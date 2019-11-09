# Creates an image with only clouds in them from a BGR image
import numpy as np
import cv2
from PIL import Image

def _calc_hue(i, r, g, b):
    if (r < g < b):
        try:
            return ((b - r) / (i - (3 * r))) + 1
        except:
            return 1e9
    elif (g < b):
        try:
            return ((b - r) / (i - (3 * r))) + 2
        except:
            return 1e9
    else:
        try:
            return ((b - r) / (i - (3 * r)))
        except:
            return 1e9

def _calc_sat(i, h, r, g, b):
    if (h <= 1):
        return (i - (3 * b)) / i
    elif (1 < h <= 2):
        return (i - (3 * r)) / i
    else:
        if i == 0:
            return 1e9
        return (i - (3 * g)) / i

# Calculate cloud-only image
def cloud_recognition(img):
    # OpenCV opens images as GBR. We need to change it to RGB, convert it to a numpy array
    # and then normalize all the values
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.asarray(img).astype(np.double)
    img /= 255

    # Vectorize the functions above so that we can use numpy to easily apply the functions
    # to all pixels
    v_hue = np.vectorize(_calc_hue)
    v_sat = np.vectorize(_calc_sat)

    # Use the vectorized functions above and apply to every element of the matrix
    intensity = img[:,:,0] + img[:,:,1] + img[:,:,2]
    hue = v_hue(intensity, img[:,:,0], img[:,:,1], img[:,:,2])
    sat = v_sat(intensity, hue, img[:,:,0], img[:,:,1], img[:,:,2])

    # Change values to make output prettier
    sat = np.where(sat > 0.1, 0, sat * 2)

    sat = sat.astype(np.float32)

    # Return the image in the same format, in which it was inputted
    return cv2.cvtColor(sat, cv2.COLOR_GRAY2BGR)