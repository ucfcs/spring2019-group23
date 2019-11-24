import numpy as np
from pysolar.solar import *
from _datetime import datetime
# from datetime import timedelta
# import pytz
import tzlocal
import cv2
from matplotlib import pyplot as plt


# also ignore leap second warnings
# the lat, long will be of the camera
def get_sun(lat, long, date):
	print("The date:", date)
	altitude = get_altitude(lat, long, date)
	print("altitude:", altitude)
	azimuth = get_azimuth(lat, long, date)
	print("azimuth:", azimuth)
	return azimuth, altitude


def mask_sun():
	lat = 28.6073098
	long = -81.2037086
	cam = cv2.VideoCapture('video1.mp4')

	# date = tzlocal.get_localzone().localize(datetime.now())
	date = datetime(2019, 11, 5, 10, 9, 18, tzinfo=tzlocal.get_localzone())

	while(1):
		# 1.) load frame
		ret, frame1 = cam.read()
		frame = cv2.resize(frame1, (640, 480))

		# 2.) Find sun using (azimuth, altitude)
		azimuth, altitude = get_sun(lat, long, date)

		# *************** Creating the polar grid ****************
		# To convert degrees to radian for plotting
		rad = np.pi / 180
		fig = plt.figure()
		ax1 = fig.add_subplot(111, projection='polar')
		ax1.grid(True)
		ax1.set_theta_zero_location("N")
		ax1.set_theta_direction(-1)
		ax1.grid(linewidth=1)
		ax1.set_ylim(0, 90)
		ax1.set_yticks(np.arange(0, 90, 10))
		yLabel = ['90', '', '', '60', '', '', '30', '', '', '']
		ax1.set_yticklabels(yLabel)

		# *************** PLOTTING DIRECTLY ONTO POLAR GRID WITH AZIMUTH, ALTITUDE input ***************
		# original: single center point
		plt.polar((azimuth)*rad, 90-altitude, 'ro', markersize=1)
		# changed: larger sun area mask; center needs to be extracted
		# plt.polar((360 - azimuth) * rad, 90 - altitude, 'ro', markersize=18)
		plt.savefig('sunPos.png')

		# *************** Show image under grid to check accuracy ***************
		axes_coords = [0.12, 0.1, 0.8, 0.8]
		ax_image = fig.add_axes(axes_coords)
		ax_image.imshow(frame, alpha=0.75)
		ax_image.axis('off')
		# plt.show()

		# 3.) Mask the sun in the image, store the masked area as 'sunPixels'
		# load sunPos image to create mask
		sun_image = cv2.imread('sunPos.png')
		mask = np.zeros_like(sun_image)
		mask[np.where((sun_image == [0, 0, 255]).all(axis=2))] = [0, 0, 255]
		# cv2.imshow('mask', mask)
		# cv2.waitKey(0)
		# Store the plotted center point
		point = np.where((mask == [0, 0, 255]).all(axis=2))
		sun_center = (point[1][0], point[0][0])
		# draw circle with radius=18 around the center point
		cv2.circle(mask, sun_center, 18, (0, 0, 255), -1, 8, 0)
		# cv2.imshow('mask', mask)
		# cv2.waitKey(0)
		points = np.where((mask == [0, 0, 255]).all(axis=2))
		sun_pixels = list(zip(points[1][:], points[0][:]))

		# print(len(sun_pixels))
		# exit(0)

		# 4.) Send 'sun_center' to motion estimation and coverage
		return sun_center, sun_pixels
