import numpy as np
import cv2
import math
import matplotlib.pyplot as plt

# Load an color image in grayscale
img = cv2.imread('pictures/pretty.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

rows = len(img)
cols = len(img[0])

out = [None] * rows

for i in range(rows):
    out[i] = [None] * cols

cloud = 0
for i in range(rows):
    for j in range(cols):
        r = int(img[i][j][0])
        g = int(img[i][j][1])
        b = int(img[i][j][2])

        # ins = 1/3 * (r + g + b)

        # num = .5 * (r + r - g - b)
        # den = np.sqrt((r - g)**2 + (r - g)*(g - b))
        # hue = np.arccos(num / den)

        sat = 1 - 3 / (r + g + b) * min(r, g, b)
        if abs(sat) < 0.1:
            out[i][j] = 255
            cloud += 1
        else:
            out[i][j] = 0

print(cloud / (rows * cols))
plt.imshow(out, cmap='gray')
plt.show()