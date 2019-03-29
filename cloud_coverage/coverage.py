# Creates a pyplot of images with only clouds in them

import numpy as np
import cv2
import matplotlib.pyplot as plt

# Load an color image in grayscale
img = cv2.imread('results/03282019/in/1.jpg')

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = np.asarray(img).astype(np.int)

# Using numpy to calculate Intensity, Hue, and Saturation
# Intensity  = 1/3 * (r + g + b) / 3
# Hue        = arccos(((r - g) + (r - b)) / (sqrt((r - g)^2 + (r - g)*(g - b))))
# Saturation = 1 - (3 / (r + g + b)) * min(r, g, b) 
# ins = (r + g + b) / 3
# num = .5 * (r + r - g - b)
# den = np.sqrt((r - g)**2 + (r - g)*(g - b))
# hue = np.arccos(num / den)
sat = 1 - (3 / (img[:,:,0] + img[:,:,1] + img[:,:,2])) * np.minimum(np.minimum(img[:,:,0], img[:,:,1]), img[:,:,2])
sat = np.where(abs(sat) > 0.15, 0, sat * 2)

# To make the output image grayscale
plt.imshow(sat, cmap='gray')
plt.show()
