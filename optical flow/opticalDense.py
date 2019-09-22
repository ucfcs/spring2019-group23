import numpy as np
import cv2


# Change video file name here
cam = cv2.VideoCapture('Clouds.mp4')
ret, frame1 = cam.read()
prev = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[..., 1] = 255

# Reads video frame by frame and outputs the optical flow as bgr values
while(1):
    ret, frame2 = cam.read()
    next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(prev, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] = ang*180/np.pi/2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    cv2.imshow('frame2', bgr)
    k = cv2.waitKey(30) & 0xff

    # Press 'esc' to end process
    if k == 27:
        break
    # Press 's' to save a snapshot of the original video frame and its
    # corresponding optical flow image
    elif k == ord('s'):
        cv2.imwrite('opticalfb.png', frame2)
        cv2.imwrite('opticalhsv.png', bgr)

    prev = next
