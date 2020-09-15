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

# define this as a lambda func. we will use throughout
current_milli_time = lambda: int(round(time.time() * 1000))

###########################################################################
#######          Constant Variables                          ##############
###########################################################################
# Engineering II
LAT = 28.601722
LONG = -81.198545

# LAT  = 28.603865
# LONG = -81.199273

# Lake Claire
# LAT = 28.607334
# LONG = -81.203706

# Garage C
# LAT = 28.601985
# LONG = -81.195806

# Path to socket.io app server
URL_APP_SERVER          = 'http://cloud-track.herokuapp.com'

# This mask radius is  the ratio of image width to how big the mask radius should be, 
# it is a very close approximation for calculating a mask that selects only the inner
# circle of the image without needing to do heavy computation
MASK_RADIUS_RATIO       = 3.5

CAPTURE_RESOLUTION = (1024, 768)

#                                                 \/ 2 bc prev, next (2 iterations)
# What the camera FPS is to feed to cloud motion (2 * SECONDS_PER_PREDICTION) / 60 = 2 * 30 / 60 = 1
SECONDS_PER_FRAME       = 1
# How often we calculate cloud motion vector predictions (remember it is expensive proc)
SECONDS_PER_PREDICTION  = 30

# Declare the socket.io
sock = None

###########################################################################
#######          Debugging (visual) Variables                          ####
###########################################################################
DISPLAY_SIZE            = (512, 384)
display_images = True
send_images = True
do_coverage = True
do_mask = True
do_crop = True


# Initialize socket io client
# @params url: socket.io server path
def initialize_socketio(url):
    sio = socketio.Client()

    # Define an event to let us know when we connect
    @sio.event
    def connect():
        print("Connected to Application Server")

    # Connect the socket io client to app server
    sio.connect(url)
    return sio

# Send the cloud motion updates
# @params data: a frequency map of cloud segments mapped to eta
def send_predictions(data):
    if sock is None:
        return
        
    # unpack the map to a json object
    payload = {
        'cloudPrediction': {int(a) : int(b) for a,b in data}
    }

    # emit the message as a "predi" message
    sock.emit('predi', payload)

# Send the cloud coverage percentage
# @params coverage: an opencv image where the sky has been removed (set to 0,0,0)
def send_coverage(coverage):
    if sock is None:
        return

    # count cloud pixels (where the pixel val > 0)
    cloud = np.count_nonzero(coverage[:, :, 3] > 0)
    not_cloud = np.count_nonzero(coverage[:, :, 3] == 0)

    # calculate the percentage
    coverage = np.round((cloud / (cloud + not_cloud)) * 100, 2)
    
    # ship the coverage as a json object under the msg type 'coverage data'
    sock.emit('coverage_data', { "cloud_coverage": coverage })


# Send an image
# @params image: an opencv image with (hopefully) 4 channels
# @params event_name: event name to emit it under
def send_image(image, event_name):
    if send_images is False or sock is None:
        return

    # encode our image to png so we can ship it
    success, im_buffer = cv2.imencode('.png', image)
    
    if success is False:
        print("couldnt encode png image")
        return

    # once we have the image bytes, pass it to emit who will encode it to base64 under the hood
    # https://github.com/miguelgrinberg/python-socketio/blob/7365799a970591910502379aac2378ba5e814f58/socketio/client.py#L458
    byte_image = im_buffer.tobytes()

    # emit the image under event_name
    sock.emit(event_name, byte_image)

# send coverage image
# @params event_name: event name to emit it under
def send_cloud(frame):
    send_image(frame, 'coverage')

# send a shadow image (only where the pixels are 50% opacity and up)
# @params event_name: event name to emit it under
def send_shadow(coverage):
    shadow = coverage.copy()
    shadow[(shadow[:, :, 3] > 0)] = (0, 0, 0, 127)
    send_image(shadow, 'shadow')

# forecast cloud motion
# @params queue: queue of predictions (we async here)
# @params prev: prev frame
# @params next: next frame
def forecast_(queue, prev, next):
    # record when we started execution
    before_ = current_milli_time()

    # run the mask_sun func. inside sunpos.py with our current LAT, LONG
    # and get the center of the sun (plus surrounding sun pixels)
    sun_center, sun_pixels = mask_sun(LAT, LONG)

    # record when we finished calculating sun position
    after_mask_sun = current_milli_time()

    # run the forecast func. inside of forecast.py with the sun pixels (where we're checking),
    # prev, next frames, and our current FPS which lets it know the speed at which these images are recorded (estimate)
    times = forecast.forecast(sun_pixels, prev, next, 1/SECONDS_PER_FRAME)

    # record when we finished calculating the frequencies
    after_forecast = current_milli_time()

    # do some ugly rounding and unique-ing to round out the frequency array
    prediction_frequencies = np.array(np.unique(np.round(times), return_counts=True)).T
    
    # add it to our multithreadded queue (we are not running on the same thread that has ffmpeg pipe / sock.io right now)
    queue.put(prediction_frequencies)
    
    # print out how expensive this op was
    elapsed_mask = (after_mask_sun - before_)
    print('SUN MASK TOOK: %s ms' % elapsed_mask)

    elapsed_forecast = (after_forecast - after_mask_sun)
    print('FORECAST TOOK: %s ms' % elapsed_forecast)

# Make all black pixels transparent
# @params bgr: BGR image we are then making BGRA (for all pix in bgr: if pix === (0,0,0): newPix = (0,0,0, 0))
def black2transparent(bgr):
    bgra = cv2.cvtColor(bgr, cv2.COLOR_BGR2BGRA)
    bgra[(bgra[:, :, 0:3] == [0, 0, 0]).all(2)] = (0, 0, 0, 0)
    return bgra

# Run an iteration of experiments using our collected frames
# @params prev: prev frame (opencv BGR image)
# @params next: next frame
def experiment_step(prev, next):
    before = current_milli_time()
    clouds = None
    if do_mask is True:
        # run create_mask func. inside create_mask.py using the MASK_RADIUS_RATIO
        mask = create_mask.create_mask(prev, MASK_RADIUS_RATIO)

        # Apply the mask to our images
        prev = create_mask.apply_mask(prev, mask)
        next = create_mask.apply_mask(next, mask)

    if do_crop is True:
        # get the resolution of the images
        w = prev.shape[0]
        h = prev.shape[1]


        # get the edges of the circle mask (using the MASK_RADIUS_RATIO) and crop
        s = w / MASK_RADIUS_RATIO

        top_edge = int(h/2-s)
        bottom_edge = int(h/2 + s)

        left_edge = int(w/2-s)
        right_edge = int (w/2 + s)
        # Slice our image
        prev = prev[ left_edge:right_edge  ,  top_edge:bottom_edge , :]
        next = next[ left_edge:right_edge  ,  top_edge:bottom_edge , :]

    # Find the flow vectors for the prev and next images
    flow_vectors = opticalDense.calculate_opt_dense(prev, next)

    if do_coverage is True:
        # Select all cloud pixels on our last frame
        # ( arrows begin on the first frame and point to the second frame )
        clouds = coverage.cloud_recognition(next)

    # draw the arrows on a copy of the cloud-only image
    flow, _, __ = opticalDense.draw_arrows(clouds.copy(), flow_vectors)

    after = current_milli_time()
    elapsed = (after - before)
    print('Experiment step took: %s ms' % elapsed)

    # Return experiment step data (potentially cropped prev/next)
    return (prev, next, flow, clouds)

# Display the set of images generated by every iteration
# @params prev: prev image
# @params next: next image
# @params flow: flow (optical dense) image
# @params coverage: coverage image
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

# Create a piped subprocess utilizing python subprocess module
# https://docs.python.org/3/library/subprocess.html#subprocess.Popen
# The idea of using a pipe is essentially solving the problem of feeding video from camera to our python scripts
# we use FFMPEG to re-encode our feed (which we are already comfortable with) and essentially write it to an a
# "temporary" file in memory (https://en.wikipedia.org/wiki/Named_pipe) and then we get that buffer and we can read from it
# @params video_path: (default None) path of video to feed ffmpg else use camera
def create_ffmpeg_pipe(video_path = None):
    if video_path is None:
        command = [ 'ffmpeg',
            # we don't really want output
            '-loglevel', 'panic',
            '-nostats',
            # RTSP over TCP (camera-specific)
            '-rtsp_transport', 'tcp',
            '-i', 'rtsp://192.168.0.10:8554/CH001.sdp',
            # output resolution and FPS (SCALE THIS AS NEEDED)
            '-s', CAPTURE_RESOLUTION.join(','),
            '-vf', 'fps=fps=1/8',
            # format
            '-f', 'image2pipe',
            '-pix_fmt', 'rgb24',
            # note the '-' argument, we're telling ffmpeg that we're piping to another program (use stdout to output)
            # http://zulko.github.io/blog/2013/10/04/read-and-write-audio-files-in-python-using-ffmpeg/
            '-vcodec', 'rawvideo', '-']
    else:
        command = [ 'ffmpeg',
            '-loglevel', 'panic',
            '-nostats',
            # similar to above but utilizing a video
            '-i', video_path,
            '-s', CAPTURE_RESOLUTION.join(','),
            '-f', 'image2pipe',
            '-pix_fmt', 'rgb24',
            '-vcodec', 'rawvideo', '-']

    # open a subprocess using PIPE, writing to stdout
    pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
    return pipe

def read_from_pipe(pipe):
    # read a 1024x768x3 RGB image byte array (one long array)
    raw_img = pipe.stdout.read(CAPTURE_RESOLUTION[0]*CAPTURE_RESOLUTION[1]*3)
    # transform the bytes read into a numpy array
    img =  np.fromstring(raw_img, dtype='uint8')
    # reshape it so that it's a nice WxHx(RGB)
    img = img.reshape((CAPTURE_RESOLUTION[1], CAPTURE_RESOLUTION[0], 3))
    # convert it to BGR
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # mirror it since the camera is mirrored
    img = np.fliplr(img)

    # throw away the data in the pipe's buffer. (we want the freshest frame)
    pipe.stdout.flush()

# Run our experiments using an ffmpeg pipe stream
# @params pipe: the ffmpeg pipe
def experiment_ffmpeg_pipe(pipe):
    last_run = current_milli_time()

    ## BRONZE SOLUTION (of handling expensive computation of sunpos)
    # record that this is the first iteration
    First = True

    # are we blocking sunpos from running?
    BLOCK = False

    # create a queue of predictions so we don't clog up the main process (and send as we please)
    prediction_queue = Queue()

    while True:
        try:
            # fetch two images from the buffer
            prev = read_from_pipe(pipe)
            next = read_from_pipe(pipe)

            # run our experiments with prev, next images
            (prev, next, flow, coverage) = experiment_step(prev, next)
            
            # check if we are ready to run cloud motion predictions
            current_run = current_milli_time()
            if (current_run - last_run > (1000 * SECONDS_PER_PREDICTION)
                or First is True) and BLOCK is False:
                # set our process lock
                BLOCK = True
                # create a python process with the queue (we multiprocess remember?) and the frames
                p = Process(target=forecast_, args=(prediction_queue, prev, next))
                p.start()
                # flip First
                First = False

                # reset our last run time
                last_run = current_run
            
            # if we have data to push
            if(prediction_queue.empty() != True):
                # get data and push
                prediction_frequencies = prediction_queue.get()
                print("Sending predictions", np.shape(prediction_frequencies))
                send_predictions(prediction_frequencies)

                # unblock the queue
                BLOCK = False
                
            # as normal, send our data via socket.io
            send_cloud(flow)
            send_shadow(coverage)
            send_coverage(coverage)

            # show our experiments and break if ESC was pressed
            if (experiment_display(prev, next, flow, coverage) == False):
                break
        except Exception as inst:
            print(inst)
            break
    return


# [1] __Entry point__
if __name__ == "__main__":
    # Initialize a GLOBAL var for the socket io client (we're going to use it a lot)
    global sock
    sock = initialize_socketio(URL_APP_SERVER)

    # Initialize the pipe from running an ffmpeg python process (https://docs.python.org/3/library/multiprocessing.html)
    # @param video_path: when None, will use camera, otherwise use file located at video_path
    pipe = create_ffmpeg_pipe(video_path=None)

    # Run our experiments (cloud coverage, sun detection, cloud motion, etc. etc. etc.) on the ffmpeg (video/camera) pipe
    experiment_ffmpeg_pipe(pipe)

    # When we are done, make sure we close our connection (no one likes danlging connections)
    if sock is not None:
        sock.disconnect()