# Conviniently outputs all the pyplots to a certain directory
import numpy as np
from scipy import misc
import sys
import imageio
import matplotlib.pyplot as plt

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

# Load an color image in grayscale
# img = imageio.imread('image.png')
# pix = np.array(img).astype(np.double)
# pix /= 255

# # Vectorize the saturation funciton to speed things up
# v_sat = np.vectorize(calc_sat)

# # Use the vectorized functions above and apply to every element of the matrix
# sat = v_sat(pix[:,:,0], pix[:,:,1], pix[:,:,2])

# # Change values to make output and give it a transparent background
# sat = np.where(sat > 0.05, 0, .9)
# # pix = np.dstack((pix, sat))
# pix[:,:,3] = sat

# # Output image
# imageio.imwrite('trans.png', pix)
f = misc.face()
plt.imshow(f)
plt.show()