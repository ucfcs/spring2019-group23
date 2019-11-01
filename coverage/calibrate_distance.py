import cv2
import numpy as np
import matplotlib.pyplot as plt
  
img = cv2.imread('testing-images/IMG_1077.jpg')

# OpenCV opens images as GBR. We need to change it to RGB, convert it to a numpy array
# and then normalize all the values
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = np.asarray(img).astype(np.double)
img /= 255

plt.imshow(img)
plt.show()
