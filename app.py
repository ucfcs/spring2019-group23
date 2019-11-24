import subprocess as sp
import base64
import time
import sys
import cv2
import numpy as np
import socketio
from multiprocessing import Process, Queue

import forecast
from opticalFlow import opticalDense
from coverage import coverage
from fisheye_mask import create_mask
from sunPos import mask_sun

current_milli_time = lambda: int(round(time.time() * 1000))

# Constants
# URL_APP_SERVER          = 'http://localhost:3001/'
URL_APP_SERVER          = 'http://cloudtrackingcloudserver.herokuapp.com'
DISPLAY_SIZE            = (512, 384)
MASK_RADIUS_RATIO       = 3.5
SECONDS_PER_FRAME       = 1
SECONDS_PER_PREDICTION  = 30

# 
# LAT  = 28.603865
# LONG = -81.199273

# Lake Claire
# LAT = 28.607334
# LONG = -81.203706

# Garage C
# LAT = 28.601985
# LONG = -81.195806

# Engineering II
LAT = 28.601722
LONG = -81.198545

# FLAGS -- used to test different functionalities
display_images = True
send_images = True
do_coverage = True
do_mask = True
do_crop = True
sock = None

# Initialize socket io
def initialize_socketio(url):
    sio = socketio.Client()

    @sio.event
    def connect():
        print("Connected to Application Server")

    sio.connect(url)
    return sio

def send_predictions(data):
    if sock is None:
        return
        
    payload = {
        'cloudPrediction': {int(a) : int(b) for a,b in data}
    }

    sock.emit('predi', payload)

def send_coverage(coverage):
    if sock is None:
        return

    cloud = np.count_nonzero(coverage[:, :, 3] > 0)
    not_cloud = np.count_nonzero(coverage[:, :, 3] == 0)

    coverage = np.round((cloud / (cloud + not_cloud)) * 100, 2)

    print(coverage)
    
    sock.emit('coverage_data', { "cloud_coverage": coverage })

def send_image(image, event_name):
    if send_images is False or sock is None:
        return
    success, im_buffer = cv2.imencode('.png', image)
    
    if success is False:
        print("couldnt encode png image")
        return

    byte_image = im_buffer.tobytes()
    sock.emit(event_name, byte_image)

# send coverage image
def send_cloud(frame):
    send_image(frame, 'coverage')

def send_shadow(coverage):
    shadow = coverage.copy()
    shadow[(shadow[:, :, 3] > 0)] = (0, 0, 0, 127)
    send_image(shadow, 'shadow')

def forecast_(queue, prev, next):
    before_ = current_milli_time()
    sun_center, sun_pixels = mask_sun(LAT, LONG)
    after_mask = current_milli_time()
    times = forecast.forecast(sun_pixels, prev, next, 1/SECONDS_PER_FRAME)
    after_forecast = current_milli_time()

    prediction_frequencies = np.array(np.unique(np.round(times), return_counts=True)).T
    
    queue.put(prediction_frequencies)
    
    elapsed_mask = (after_mask - before_)
    print('SUN MASK TOOK: %s ms' % elapsed_mask)

    elapsed_forecast = (after_forecast - after_mask)
    print('FORECAST TOOK: %s ms' % elapsed_forecast)

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

    if do_crop is True:
        w = prev.shape[0]
        h = prev.shape[1]
        s = w / MASK_RADIUS_RATIO

        top_edge = int(h/2-s)
        bottom_edge = int(h/2 + s)

        left_edge = int(w/2-s)
        right_edge = int (w/2 + s)
        prev = prev[ left_edge:right_edge  ,  top_edge:bottom_edge , :]
        next = next[ left_edge:right_edge  ,  top_edge:bottom_edge , :]

    # Find the flow vectors for the prev and next images
    flow_vectors = opticalDense.calculate_opt_dense(prev, next)

    if do_coverage is True:
        clouds = coverage.cloud_recognition(next)

    flow, _, __ = opticalDense.draw_arrows(clouds.copy(), flow_vectors)

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

    # Show the images
    cv2.imshow('flow?', flow_show)
    cv2.imshow('previous', prev_show)
    cv2.imshow('next', next_show)

    # Wait 30s for ESC and return false if pressed
    k = cv2.waitKey(30) & 0xff
    if (k == 27):
        return False
    return True

def create_ffmpeg_pipe(video_path = None):
    if video_path is None:
        command = [ 'ffmpeg',
            '-loglevel', 'panic',
            '-nostats',
            '-rtsp_transport', 'tcp',
            '-i', 'rtsp://192.168.0.10:8554/CH001.sdp',
            '-s', '1024x768',
            '-f', 'image2pipe',
            '-pix_fmt', 'rgb24',
            '-vf', 'fps=fps=1/8',
            '-vcodec', 'rawvideo', '-']
    else:
        command = [ 'ffmpeg',
            '-loglevel', 'panic',
            '-nostats',
            '-i', video_path,
            '-s', '1024x768',
            '-f', 'image2pipe',
            '-pix_fmt', 'rgb24',
            '-vcodec', 'rawvideo', '-']

    pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
    return pipe

def experiment_ffmpeg_pipe(pipe):
    before = current_milli_time()

    ## BRONZE SOLUTION
    First = True
    BLOCK = False

    
    prediction_queue = Queue()

    while True:
        try:
            prev_rawimg = pipe.stdout.read(1024*768*3)
            # transform the byte read into a numpy array
            prev =  np.fromstring(prev_rawimg, dtype='uint8')
            prev = prev.reshape((768,1024,3))
            prev = cv2.cvtColor(prev, cv2.COLOR_RGB2BGR)
            prev = np.fliplr(prev)
            
            # throw away the data in the pipe's buffer.
            pipe.stdout.flush()

            next_rawimg = pipe.stdout.read(1024*768*3)
            # transform the byte read into a np array
            next =  np.fromstring(next_rawimg, dtype='uint8')
            next = next.reshape((768,1024,3))
            next = cv2.cvtColor(next, cv2.COLOR_RGB2BGR)
            next = np.fliplr(next)

            # throw away the data in the pipe's buffer.
            pipe.stdout.flush()    

            (prev, next, flow, coverage) = experiment_step(prev, next)
            
            after = current_milli_time()
            if (after - before > (1000 * SECONDS_PER_PREDICTION)
                or First is True) and BLOCK is False:
                BLOCK = True
                p = Process(target=forecast_, args=(prediction_queue, prev, next))
                p.start()
                First = False
                before = after
            
            if(prediction_queue.empty() != True):
                prediction_frequencies = prediction_queue.get()
                print("Sending predictions", np.shape(prediction_frequencies))
                send_predictions(prediction_frequencies)
                BLOCK = False
                
            send_cloud(flow)
            send_shadow(coverage)
            send_coverage(coverage)

            # Break if ESC key was pressed
            if (experiment_display(prev, next, flow, coverage) == False):
                break
        except Exception as inst:
            print(inst)
            break
    return


def main():
    global sock
    sock = initialize_socketio(URL_APP_SERVER)
    pipe = create_ffmpeg_pipe(None)

    # pipe = create_ffmpeg_pipe('/home/jose/Desktop/cloud-tracking/20191123-120256.showcase.mp4')

    experiment_ffmpeg_pipe(pipe)
    if sock is not None:
        sock.disconnect()

main()
