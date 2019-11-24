# Creates an image with only clouds in them from a BGR image
import numpy as np
from scipy import signal
import cv2

# A few constants that are used in this program
SUN_RADIUS    = 50   # Used to block the sun
SAT_THRESHOLD = 0.08  # Used for cloud detection
SUN_THRESHOLD = 2.9375 # Used for sun detection
FILTER_SIZE   = 25    # Used for noise reduction and locating the sun

# Formula for caluclating saturation
def _calc_sat(r, g, b):
    try:
        if (r < g < b):
            return 1 - (3 * r) / (r + b + g)
        elif (g < b):
            return 1 - (3 * g) / (r + b + g)
        else:
            return 1 - (3 * b) / (r + b + g)
    except:
        return 1e9

# Vectorize the functions above so that we can use numpy to easily apply the functions
# to all pixels
v_sat = np.vectorize(_calc_sat)

# Calculate cloud-only image
def cloud_recognition(img):
    # OpenCV opens images as GBR. We need to change it to RGB, convert it to a numpy array
    # and then normalize all the values
    img = np.asarray(img).astype(np.double)
    img /= 255

    # Locate the brightest pixel in the image (i.e. the sun) and cover it up so it doesn't
    # f*ck with our coverage code
    intensity = img[:,:,0] + img[:,:,1] + img[:,:,2]

    # To eliminate noise and find the center of the sun, we're going to do a mean convolution
    mean_matrix = np.full(shape=(FILTER_SIZE, FILTER_SIZE), fill_value=1/FILTER_SIZE**2)
    convolved_intensity = signal.convolve2d(intensity, mean_matrix, mode='full', boundary='fill', fillvalue=0)

    # locate the brightest pixel in the image (aka the pixel with the highest intensity value)
    max_intensity = np.amax(convolved_intensity)

    # If the sun is in the image, the max_intensity should be greater than this threshold
    # If it's not, the that means that the sun is probably covered by a cloud (or not in frame)
    if max_intensity >= SUN_THRESHOLD:
        brightest = np.where(convolved_intensity == max_intensity)
        l = int(len(brightest[0]) / 2)

        x = brightest[1][l]
        y = brightest[0][l]
        r = SUN_RADIUS

        cv2.circle(img, (x, y), r, (255, 0, 0), -1)

    # Use the vectorized functions above and apply to every element of the matrix
    sat = v_sat(img[:,:,2], img[:,:,1], img[:,:,0])

    # Change values to make output prettier
    sat = np.where(sat > SAT_THRESHOLD, 0, 1)
    output = np.dstack((img, sat))

    output *= 255

    # Return the image in the same format, in which it was inputted
    return output