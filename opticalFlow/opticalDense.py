import numpy as np
import cv2

# Constants
ARROW_STEP = 16

# Flags
DRAW_COLORS = False
DRAW_ARROWS = True

def draw_colors(optflow):
    # Prepare HSV
    hsv = np.zeros_like(frame1)
    hsv[..., 1] = 255

    # Populate HSV image with optical flow values
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] = ang*180/np.pi/2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)

    # Return the optical flow in BGR, as it was inputted
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def draw_arrows(frame, flow, step=ARROW_STEP):
    h, w = frame.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T
    
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)

    nonzero_lines = []
    x_f = []
    x_i = []

    for (x1, y1), (x2, y2) in lines:
        if (x1 != x2) and (y1 != y2):
            #nonzero_lines.append(np.array( [[x1, y1], [x2, y2]] ))
            cv2.arrowedLine(frame, (x1, y1), (x2, y2), (0,255,0,255), thickness=1, tipLength=0.3)
            x_i.append((x1, y1))
            x_f.append((x2, y2))

    #cv2.polylines(frame, nonzero_lines, False, (0, 255, 0, 255))


    return frame, x_i, x_f

# Reads video frames by frame and outputs the optical flow as a BGR image
def calculate_opt_dense(frame1, frame2):
    # Convert the images to Grayscale
    prev = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Calculate the optical flow
    return cv2.calcOpticalFlowFarneback(prev, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)