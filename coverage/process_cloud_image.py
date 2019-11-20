# Conviniently outputs all the pyplots to a certain directory
import numpy as np
from scipy import signal
import imageio
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# Formula for caluclating saturation
def calc_sat(r, g, b):
    try:
        if (r < g < b):
            return 1 - (3 * r) / (r + b + g)
        elif (g < b):
            return 1 - (3 * g) / (r + b + g)
        else:
            return 1 - (3 * b) / (r + b + g)
    except:
        return 1e9

# A few constants that are used in this program
SIDE_LENGTH   = 525   # Used for cropping
SUN_RADIUS    = 100   # Used to block the sun
SAT_THRESHOLD = 0.1  # Used for cloud detection
SUN_THRESHOLD = 2.975 # Used for sun detection
FILTER_SIZE   = 10    # Used for noise reduction and locating the sun

# Load an color image in grayscale
unprocessed_image = Image.open('coverage_testing_images/12.jpg')

# Crop the image. To get rid of the really distorted edges (because of fisheye)
h, w = unprocessed_image.size
s    = SIDE_LENGTH
cropped_image = unprocessed_image.crop((h/2-s, w/2-s, h/2+s, w/2+s))

# Convert image to numpy array
array_image = np.array(cropped_image).astype(np.double)
array_image /= 255

# Locate the brightest pixel in the image (i.e. the sun) and cover it up so it doesn't
# f*ck with our coverage code
intensity = array_image[:,:,0] + array_image[:,:,1] + array_image[:,:,2]

# To eliminate noise and find the center of the sun, we're going to do a mean convolution
mean_matrix = np.full(shape=(FILTER_SIZE, FILTER_SIZE), fill_value=1/(FILTER_SIZE**2))
convolved_intensity = signal.convolve2d(intensity, mean_matrix, mode='full', boundary='fill', fillvalue=0)

# locate the brightest pixel in the image (aka the pixel with the highest intensity value)
max_intensity = np.amax(convolved_intensity)

# If the sun is in the image, the max_intensity should be greater than this threshold
# If it's not, the that means that the sun is probably covered by a cloud (or not in frame)
if max_intensity >= SUN_THRESHOLD:
    brightest = np.where(convolved_intensity == max_intensity)
    l = int(len(brightest[0]) / 2)

    draw = ImageDraw.Draw(cropped_image)
    x = brightest[1][l]
    y = brightest[0][l]
    r = SUN_RADIUS
    draw.ellipse((x-r, y-r, x+r, y+r), fill=(255,0,0,255))

# Now that the sun's blocked, convert the image to a numpy array
array_image = np.array(unprocessed_image).astype(np.double)
array_image /= 255

# # The sat. function above will be applied to every pixel. Vectorize the function for speed
v_sat = np.vectorize(calc_sat)
sat = v_sat(array_image[:,:,0], array_image[:,:,1], array_image[:,:,2])

# Change values to make output and give the clouds a transparent background
sat = np.where(sat > SAT_THRESHOLD, 0, .9)
output = np.dstack((array_image, sat))

# Output image
imageio.imwrite('../front_end/public/leaflet_cloud_image.png', output)

# Display image (for debugging)
plt.imshow(unprocessed_image)
plt.show()