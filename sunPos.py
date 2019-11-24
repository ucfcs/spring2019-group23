import numpy as np
from pysolar.solar import get_azimuth, get_altitude
from _datetime import datetime
import tzlocal
import cv2
from matplotlib import pyplot as plt
import os


# also ignore leap second warnings
# the lat, long will be of the camera
def get_sun(lat, long, date):
	altitude = get_altitude(lat, long, date)
	azimuth = get_azimuth(lat, long, date)
	return azimuth, altitude

def mask_sun(lat, long):
	# date = tzlocal.get_localzone().localize(datetime.now())
	date = datetime(2019, 11, 24, 13, 17, 00, tzinfo=tzlocal.get_localzone())
	# frame = cv2.resize(frame1, (640, 480))

	# 2.) Find sun using (azimuth, altitude)
	azimuth, altitude = get_sun(lat, long, date)
	# print(azimuth, altitude)
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
	plt.savefig('sunPos.png')

	# 3.) Mask the sun in the image, store the masked area as 'sunPixels'
	# load sunPos image to create mask
	sun_image = cv2.imread('sunPos.png')

	mask = np.zeros_like(sun_image)
	mask[np.where((sun_image == [0, 0, 255]).all(axis=2))] = [0, 0, 255]

	# Store the plotted center point
	point = np.where((mask == [0, 0, 255]).all(axis=2))

	# TODO: check if the sun is not out return
	#return None, None

	sun_center = (point[1][0], point[0][0])

	# draw circle with radius=18 around the center point
	cv2.circle(mask, sun_center, 18, (0, 0, 255), -1, 8, 0)
	
	points = np.where((mask == [0, 0, 255]).all(axis=2))
	sun_pixels = list(zip(points[1][:], points[0][:]))

	# clean up after ourselves
	# os.remove('sunPos.png')

	# 4.) Send 'sun_center' to motion estimation and coverage
	return sun_center, sun_pixels
