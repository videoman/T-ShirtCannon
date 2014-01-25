
# Camera time?
import picamera
import io
import sys
import time
from select import select
from datetime import datetime
photodir = "/home/pi/photos/"

def circular_video():
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        stream = picamera.PiCameraCircularIO(camera, seconds=10)
        camera.start_recording(stream, format='h264')
        print('Enter <w> to write the stream to disk')
        print('Enter <q> to stop recording and exit')
        while camera.recording:
            while True:
                camera.wait_recording(0.5)
                # Wait half a second for a key press
                r, w, x = select([sys.stdin], [], [], 0.5)
                if r:
                    break
            c = input()
            if c == 'q':
                print('Exiting...')
                camera.stop_recording()
            elif c == 'w':
                #print('Writing the video to foo.h264...', end='')
                # Lock the stream to prevent the camera mutating it while we
                # read from it
                with stream.lock:
                    # Find the first header frame in the video
                    for frame in stream.frames:
                        if frame.header:
                            stream.seek(frame.position)
                            break
                    # Write the rest of the stream to a disk file using read1
                    # for speed
                    with io.open('foo.h264', 'wb') as output:
                        while True:
                            buf = stream.read1()
                            if not buf:
                                break
                            output.write(buf)
                print('done')
            else:
                print('Unrecognized input: %s' % c)
    
def take_video():
        with picamera.PiCamera() as camera:
                camera.resolution = (800, 600)
                camera.start_preview()
                camera.start_recording('/home/pi/MNRG.h264')
                camera.wait_recording(5)
                camera.stop_recording()

#LMODE=9
#print "Launcher Mode in camera module is: {}".format(LMODE)

def filenames(MODE):
    frame = 0
    LMODE=MODE
    while frame < frames:
        #yield '%02dimage%02d%02d.jpg' % photodir, str(datetime.now()), frame, 
        #yield "{}image{}{}.jpg".format(photodir, str(datetime.now()), frame) 
        #yield '/home/pi/photos/image%02d%02d.jpg' % frame, 
        yield "{}image-B{}-{}-{}.jpg".format(photodir, LMODE, time.strftime('%Y_%m_%d-%H:%M:%S'), frame) 
        frame += 1

def take_pictures(frames_n,MODE):
    global frames
    LMODE = MODE
    frames = frames_n
    with picamera.PiCamera() as camera:
       camera.resolution = (1024, 768)
       camera.framerate = 15
       camera.start_preview()
       # Capture several pictures
       start = time.time()
       camera.capture_sequence(filenames(LMODE), use_video_port=True)
       finish = time.time()
    print('Captured %d frames at %.2ffps' % (
       frames,
       frames / (finish - start)))

