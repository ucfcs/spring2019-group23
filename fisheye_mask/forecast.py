import cv2
import math
import numpy as np
from create_mask import create_mask, apply_mask
from sunPos import mask_sun


# Mask area far from the sun that we dont care about
def mask_im(frame):
	mask = create_mask(frame)
	masked = apply_mask(frame, mask)
	return masked

# return predicted times unil sun occlusion
# fps = 1 frame / 8 seconds
def get_time(x_i, x_f, sun_pixels, sun_radius, fps):
	# 1.) Calculate speed (pixels/sec.)
	# 2.) Calculate distance from pixel to sun
	times = []
	for i in range(len(x_i)):
		dist1 = euclid(x_i[i], x_f[i])
		speed = dist1 * fps

		temp = []
		for j in range(len(sun_pixels)):
			temp.append(euclid(x_f[i], sun_pixels[j], sun_radius))
		dist2 = min(temp)

		ab = np.subtract(x_f[i],x_i[i])
		# change sun_center to the selected min sun pixel ****
		# bc = np.subtract(sun_center, x_f[i])
		bc = np.subtract(sun_pixels[temp.index(dist2)], x_f[i])
		ang = get_angle(ab, bc, dist1, dist2)

		# Note: if time is neg., occlusion is happening currently ***********
		if(ang == 0):
			# print(x_i[i], x_f[i])
			t = dist2 / (speed * 60)
			# print("time:", round(t) , "minutes")
			times.append(t)
	# exit(0)
	return times


# Returns angle between two vectors
def get_angle(ab, bc, mag_ab, mag_bc):
	ang = math.acos(np.clip((np.dot(ab, bc) / (mag_ab * mag_bc)), -1.0, 1.0))
	return math.degrees(ang)


# Get euclidean distance; Radius is used when finding distance from point to sun
def euclid(p1, p2, r=0):
	a = np.array(p1)
	b = np.array(p2)
	distance = np.linalg.norm(b-a) - r
	return distance


# To display and extract the optical flow vectors
def draw_flow(img, flow, step=10):
	h, w = img.shape[:2]	# 768, 1024
	y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)

	fx, fy = flow[y,x].T

	lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
	lines = np.int32(lines + 1.5)

	vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
	cv2.polylines(vis, lines, 0, (0, 255, 0))

	x_f = []
	x_i = []
	for (x1, y1), (_x2, _y2) in lines:
		cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
		# If there was motion, store the start and end positions of that pixel
		if (_x2 !=  x1) and (_y2 != y1):
			x_i.append((x1, y1))
			x_f.append((_x2, _y2))

	return vis, x_i, x_f


def farne_flow(sun_pixels, fps):
	# Read a frame
	cam = cv2.VideoCapture('video1.mp4')
	ret, frame1 = cam.read()
	frame1 = cv2.resize(frame1, (640, 480))
	# cv2.imshow('frame', frame1)
	# cv2.waitKey(0)
	# exit(0)
	f1_mask = mask_im(frame1)
	prevgray = cv2.cvtColor(f1_mask, cv2.COLOR_BGR2GRAY)

	while True:
		_ret, img = cam.read()
		img = cv2.resize(img, (640, 480))
		f2_mask = mask_im(img)
		gray = cv2.cvtColor(f2_mask, cv2.COLOR_BGR2GRAY)

		flow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.1, 0)
		vis, x_i, x_f = draw_flow(gray, flow)

		# cv2.imshow('projected', vis)

		times = get_time(x_i, x_f, sun_pixels, 18, fps)

		prevgray = gray

		ch = cv2.waitKey(5)
		if ch == 27:
			break

	return times


def main():
	# Sun center (x, y) from the mask produced by sun tracker
	fps = 1/8
	sun_center, sun_pixels = mask_sun()
	times = farne_flow(sun_pixels, fps)
	cv2.destroyAllWindows()
	return times


main()
