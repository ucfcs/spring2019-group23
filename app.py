import time
import sys
import requests
import cv2
import numpy as np
import socketio

from os import listdir
from os.path import isfile, join

from opticalFlow import opticalDense
from coverage import coverage
from fisheye_mask import create_mask
current_milli_time = lambda: int(round(time.time() * 1000))

# FLAGS -- used to test different functionalities
display_images = True
send_images = False
do_mask = True
sock = None

# Initialize socket io stuff
def initialize_socketio(url):
    sio = socketio.Client()

    @sio.event
    def connect():
        print("Connected to Application Server")

    sio.connect(url)
    return sio

# send_flow but socket io
def send_flow(frame, alert):
    if send_images is False or sock is None:
        return

    new_frame = black2transparent(frame)
    success, im_buffer = cv2.imencode(".png", new_frame)
    
    byte_image = im_buffer.tobytes()
    sock.emit('image', byte_image)

# Make all black pixels transparent
def black2transparent(bgr):
    bgra = cv2.cvtColor(bgr, cv2.COLOR_BGR2BGRA)
    bgra[np.where((bgra == [0, 0, 0, 1]).all(axis = 2))] = [0, 0, 0, 0]
    return bgra

def experiment_step(prev, next):
    before = current_milli_time()
    mask = create_mask.create_mask(prev)
    prev = create_mask.apply_mask(prev, mask)
    next = create_mask.apply_mask(next, mask)

    # Find the flow image for the prev and next images
    flow = opticalDense.calculate_opt_dense(prev, next)
    clouds = coverage.cloud_recognition(next)
    
    after = current_milli_time()
    print('Experiment step took: %s ' % (after - before))
    # Return experiment step
    return (prev, next, flow, clouds)

def experiment_display(prev, next, flow):
    if display_images is False:
        return
    # Resize the images for visibility
    flow_show = cv2.resize(flow, (400, 400))
    prev_show = cv2.resize(prev, (400, 400))
    next_show = cv2.resize(next, (400, 400))

    # Show the images
    cv2.imshow('flow?', flow_show)
    cv2.imshow('previous', prev_show)
    cv2.imshow('next', next_show)

    # Wait 30s for ESC and return false if pressed
    k = cv2.waitKey(30) & 0xff
    if (k == 27):
        return False
    return True

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

        # Break if ESC key was pressed
        if (experiment_display(prev, next, flow) == False):
            break

        prev_img = next_img

# Run experiment on folder of images
def experiment_images(folder_name):
    # TODO: Fix this, is actually getting file list out of order
    test_images = [f for f in listdir(folder_name) if isfile(join(folder_name, f))]

    # Get the first image 
    prev_img = cv2.imread(join(folder_name, test_images[0]))

    # Iterate through the rest of the images
    for next in test_images[1:]:
        next_img = cv2.imread(join(folder_name, next))

        (prev, next, flow) = experiment_step(prev_img, next_img)

        # Break if ESC key was pressed
        if (experiment_display(prev, next, flow) == False):
            break

        prev_img = next_img

# sock = initialize_socketio('http://localhost:3001')
# experiment_images("test_images/2019-09-29/")
# experiment_video('opticalFlow/Clouds.mp4')
experiment_video('test_images/2019-10-19/test10sec.mp4')