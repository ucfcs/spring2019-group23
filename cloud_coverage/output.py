# Conviniently outputs all the pyplots to a certain directory
import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys

def calc_hue(i, r, g, b):
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


def calc_sat(i, h, r, g, b):
    if (h <= 1):
        return (i - (3 * b)) / i
    elif (1 < h <= 2):
        return (i - (3 * r)) / i
    else:
        return (i - (3 * g)) / i

# Load an color image in grayscale
for i in range(1, 24):
    if i < 13:
        img = cv2.imread('results/04042019/in/' + str(i) + '.jpg')
    else:
        img = cv2.imread('results/04042019/in/' + str(i) + '.png')

    # Exit if image was not opened (Probably due to a wrong file name)
    if (img.all() == None):
        print("Wrong file name/path, buddy.")
        sys.exit()

    # OpenCV opens images as GBR. We need to change it to RGB, convert it to a numpy array
    # and then normalize all the values
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.asarray(img).astype(np.double)
    img /= 255

    # Vectorize the functions above so that we can use numpy to easily apply the functions
    # to all pixels
    v_hue = np.vectorize(calc_hue)
    v_sat = np.vectorize(calc_sat)

    # Use the vectorized functions above and apply to every element of the matrix
    intensity = img[:,:,0] + img[:,:,1] + img[:,:,2]
    hue = v_hue(intensity, img[:,:,0], img[:,:,1], img[:,:,2])
    sat = v_sat(intensity, hue, img[:,:,0], img[:,:,1], img[:,:,2])

    # Change values to make output prettier
    sat = np.where(sat > 0.1, 0, sat * 2)

    # To make the output image grayscale
    plt.imshow(sat, cmap='gray')
    plt.savefig('results/04042019/out/out' + str(i) + '.png')
    print("Picture #",i," is done.")