import time
import sys
import requests
import cv2
import numpy as np

from os import listdir
from os.path import isfile, join

from opticalFlow import opticalDense
from coverage import coverage
current_milli_time = lambda: int(round(time.time() * 1000))

# FLAGS -- used to test different functionalities
display_images = True
send_images = False

def send_flow(frame, alert):
    if send_images is False:
        return

    # Encode our frame into a JPG
    _, encoded_img = cv2.imencode(".jpg", frame)
    
    # Generate payload
    file = { 'file': ('flow.jpg', encoded_img, 'image/jpeg') }
    payload = { 'alert': alert }

    # POST payload to /motion route
    res = requests.post('http://localhost:3000/motion', payload, files=file)

    # for fun
    print(res.content)


def experiment_step(frame1, frame2):
    # Run cloud detection (grayscale image)
    prev = coverage.cloud_recognition(frame1)
    next = coverage.cloud_recognition(frame2)

    # Find the flow image for the prev and next images
    flow = opticalDense.calculate_opt_dense(prev, next)

    # TODO: Generate alert... here?
    alert = "for fun"
    send_flow(flow, alert)

    # Return experiment step
    return (prev, next, flow)

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
        
        (prev, next, flow) = experiment_step(prev_img, next_img)

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

# experiment_images("test_images/")
# experiment_video('opticalFlow/Clouds.mp4')