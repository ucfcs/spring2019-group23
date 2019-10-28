import numpy as np
import sys
import cv2

# You should replace these 3 lines with the output in calibration step

### SCALED DOWN RESOLUTION ###
# DIM=(1280, 1200)
# K=np.array([[406.39342736565584, 0.0, 652.6119887090737], [0.0, 399.55972721953697, 602.5131856594861], [0.0, 0.0, 1.0]])
# D=np.array([[-0.03413702116213987], [0.010472077619485693], [-0.005912796816307453], [0.0005101722646145202]])

### FULL SCALE CHECKERBOARD ###
DIM=(2048, 1536)
K=np.array([[506.931058126675, 0.0, 1031.7299405018123], [0.0, 504.31186855001533, 754.621311351006], [0.0, 0.0, 1.0]])
D=np.array([[-0.028326866079378912], [9.965299485583218e-05], [0.006078527291122385], [-0.0031642322992292073]])



def undistort(img_path):
    img = cv2.imread(img_path)
    h,w = img.shape[:2]

    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    
    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    for p in sys.argv[1:]:
        undistort(p)