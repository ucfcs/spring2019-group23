import subprocess as sp
import base64
import time
import sys
import requests
import cv2
import numpy as np
import matplotlib.pyplot as plt
import socketio

from os import listdir
from os.path import isfile, join

from opticalFlow import opticalDense
from coverage import coverage
from fisheye_mask import create_mask

current_milli_time = lambda: int(round(time.time() * 1000))

# Constants
# URL_APP_SERVER          = 'http://localhost:3001/'
URL_APP_SERVER          = 'http://cloudtrackingcloudserver.herokuapp.com'
CALC_IM_COVERAGE_SIZE   = (1024, 768)
DISPLAY_SIZE            = (512, 384)
MASK_RADIUS_RATIO       = 3.5

# FLAGS -- used to test different functionalities
display_images = False
send_images = True
do_coverage = True
do_mask = True
sock = None

# Initialize socket io
def initialize_socketio(url):
    sio = socketio.Client()

    @sio.event
    def connect():
        print("Connected to Application Server")

    sio.connect(url)
    return sio

# send coverage image
def send_coverage(frame):
    if send_images is False or sock is None:
        return

    # frame = black2transparent(frame)
    success, im_buffer = cv2.imencode('.png', frame)
    
    if success is False:
        print("couldnt encode png image")
        return

    byte_image = im_buffer.tobytes()
    sock.emit('coverage', byte_image)

# send optical flow image
def send_optflow(frame):
    if send_images is False or sock is None:
        return

    frame = black2transparent(frame)
    success, im_buffer = cv2.imencode('.png', frame)
    
    if success is False:
        print("couldnt encode png image")
        return

    byte_image = im_buffer.tobytes()
    sock.emit('flow', byte_image)

# Make all black pixels transparent
def black2transparent(bgr):
    bgra = cv2.cvtColor(bgr, cv2.COLOR_BGR2BGRA)
    bgra[(bgra[:, :, 0:3] == [0, 0, 0]).all(2)] = (0, 0, 0, 0)
    return bgra

def experiment_step(prev, next):
    before = current_milli_time()

    clouds = None
    if do_mask is True:
        mask = create_mask.create_mask(prev, MASK_RADIUS_RATIO)
        prev = create_mask.apply_mask(prev, mask)
        next = create_mask.apply_mask(next, mask)

    # Find the flow image for the prev and next images
    flow = opticalDense.calculate_opt_dense(prev, next)

    if do_mask is True:
        flow = create_mask.apply_mask(flow, mask)

    if do_coverage is True:
        small = cv2.resize(next, CALC_IM_COVERAGE_SIZE)
        clouds = coverage.cloud_recognition(small)
        
    after = current_milli_time()
    elapsed = (after - before)
    print('Experiment step took: %s ms' % elapsed)

    # Return experiment step
    return (prev, next, flow, clouds)

def experiment_display(prev, next, flow, coverage):
    if display_images is False:
        return
    # Resize the images for visibility
    flow_show = cv2.resize(flow, DISPLAY_SIZE)
    prev_show = cv2.resize(prev, DISPLAY_SIZE)
    next_show = cv2.resize(next, DISPLAY_SIZE)
    # if do_coverage is True:
    #     cvg_show = cv2.resize(coverage, DISPLAY_SIZE)

    # Show the images
    cv2.imshow('flow?', flow_show)
    cv2.imshow('previous', prev_show)
    cv2.imshow('next', next_show)
    
    # if do_coverage is True:
    #     cv2.imshow('coverage', cvg_show)

    # Wait 30s for ESC and return false if pressed
    k = cv2.waitKey(30) & 0xff
    if (k == 27):
        return False
    return True

# Run experiment on a live stream rtsp
# DEPRECARTED ('does not really work')
# def experiment_livestream(url):
#     cam = cv2.VideoCapture(url)

#     count = 0
#     while 1:
#         before = current_milli_time()
#         # Get the first image
#         ret, prev_img = cam.read()
#         ret, next_img = cam.read()
        
#         (prev, next, flow, coverage) = experiment_step(prev_img, next_img)
#         send_coverage(coverage)

#         # Break if ESC key was pressed
#         if (experiment_display(prev, next, flow, coverage) == False):
#             break
        
#         after = current_milli_time()
#         elapsed = (after - before)
#         print('Experiment step took: %s ms' % elapsed)
#         ret = True

#         while ( count < (elapsed / 1000) * 50 ):
#             count += 1
#             # Get the first image
#             ret = cam.grab()
#         count = 0

def experiment_ffmpeg_pipe():
    command = [ 'ffmpeg',
            '-rtsp_transport', 'tcp',
            '-i', 'rtsp://192.168.0.10:8554/CH001.sdp',
            '-s', '1024x768',
            '-f', 'image2pipe',
            '-pix_fmt', 'rgb24',
            '-vf', 'fps=fps=1/8',
            '-vcodec', 'rawvideo', '-']

    pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)

    while True:
        raw_image = pipe.stdout.read(1024*768*3)
        # transform the byte read into a numpy array
        prev =  np.fromstring(raw_image, dtype='uint8')
        prev = prev.reshape((768,1024,3))
        prev = cv2.cvtColor(prev, cv2.COLOR_RGB2BGR)
        
        # throw away the data in the pipe's buffer.

        pipe.stdout.flush()

        raw_image = pipe.stdout.read(1024*768*3)
        # transform the byte read into a np array
        next =  np.fromstring(raw_image, dtype='uint8')
        next = next.reshape((768,1024,3))
        next = cv2.cvtColor(next, cv2.COLOR_RGB2BGR)
        # throw away the data in the pipe's buffer.
        pipe.stdout.flush()    

        (prev, next, flow, coverage) = experiment_step(prev, next)
        send_coverage(coverage)
        send_optflow(flow)

        # Break if ESC key was pressed
        if (experiment_display(prev, next, flow, coverage) == False):
            break

# Run experiment on a video file
def experiment_video(video_filename):
    cam = cv2.VideoCapture(video_filename)

    # Get the first image
    ret, prev_img = cam.read()

    # Loop forever
    while 1:
        # Get the next image
        ret, next_img = cam.read()

        # If there is no next image, break the forever loop
        if (next_img is None):
            break
        
        (prev, next, flow, coverage) = experiment_step(prev_img, next_img)
        send_coverage(coverage)
        send_optflow(flow)

        # Break if ESC key was pressed
        if (experiment_display(prev, next, flow, coverage) == False):
            break

        prev_img = next_img

# Run experiment on folder of images
def experiment_images(folder_name):
    # Get the first image 

    # Iterate through the rest of the images
    while True:
        prev_img = cv2.imread(join(folder_name, 'frame1.jpg'))
        next_img = cv2.imread(join(folder_name, 'frame2.jpg'))

        (prev, next, flow, coverage) = experiment_step(prev_img, next_img)

        # Break if ESC key was pressed
        if (experiment_display(prev, next, flow, coverage) == False):
            break

sock = initialize_socketio(URL_APP_SERVER)
# experiment_video('opticalFlow/Clouds.mp4')
# experiment_video('test_images/20191105-134549.117.mp4')
# experiment_video('test_images/2019-10-19/test10sec.mp4')
# experiment_livestream('rtsp://192.168.0.10:8554/CH001.sdp')
experiment_ffmpeg_pipe()