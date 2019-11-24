import cv2
import math
import numpy as np
from opticalFlow import opticalDense

# return predicted times unil sun occlusion
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

def forecast(sun_pixels, prev, next, fps):
	# Sun center (x, y) from the mask produced by sun tracker

	prev = cv2.resize(prev, (640, 480))
	next = cv2.resize(next, (640, 480))
	flow = opticalDense.calculate_opt_dense(prev, next)
	__, x_i, x_f = opticalDense.draw_arrows(next, flow, 10)

	return get_time(x_i, x_f, sun_pixels, 18, fps)