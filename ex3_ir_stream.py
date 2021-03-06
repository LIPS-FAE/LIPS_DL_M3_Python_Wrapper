#!/usr/bin/env python
'''
Created on 19Jun2015
Stream depth video using openni2 opencv-python (cv2)
Requires the following libraries:
    1. OpenNI-Linux-<Platform>-2.2 <Library and driver>
    2. primesense-2.2.0.30 <python bindings>
    3. Python 2.7+
    4. OpenCV 2.4.X
Current features:
    1. Convert primensense oni -> numpy
    2. Stream and display depth 
    3. Keyboard commands    
        press esc to exit
        press s to save current screen and distancemap
NOTE: 
    1. On device streams:  IR and RGB streams do not work together
       Depth & IR  = OK
       Depth & RGB = OK
       RGB & IR    = NOT OK
    2. Do not synchronize with rgb or stream will feeze
@author: Carlos Torres <carlitos408@gmail.com>
'''

import numpy as np
import cv2
from openni import openni2#, nite2
from openni import _openni2 as c_api

## Path of the OpenNI redistribution OpenNI2.so or OpenNI2.dll
# Windows
dist = 'C:\Program Files\OpenNI2\Tools'
# OMAP
#dist = '/home/carlos/Install/kinect/OpenNI2-Linux-ARM-2.2/Redist/'
# Linux
#dist ='/home/carlos/Install/openni2/OpenNI-Linux-x64-2.2/Redist'

## Initialize openni and check
openni2.initialize(dist) #
if (openni2.is_initialized()):
    print "openNI2 initialized"
else:
    print "openNI2 not initialized"

## Register the device
dev = openni2.Device.open_any()

## Create the streams stream
ir_stream = dev.create_ir_stream()

## Configure the depth_stream -- changes automatically based on bus speed
#print 'Get b4 video mode', ir_stream.get_video_mode() # Checks depth video configuration
ir_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_GRAY16, resolutionX=320, resolutionY=240, fps=30))

## Check and configure the mirroring -- default is True
# print 'Mirroring info1', ir_stream.get_mirroring_enabled()
ir_stream.set_mirroring_enabled(False)


## Start the streams
ir_stream.start()

## Use 'help' to get more info
# help(dev.set_image_registration_mode)

def get_ir():
    """
    Returns numpy ndarrays representing the raw and ranged depth images.
    Outputs:
        dmap:= distancemap in mm, 1L ndarray, dtype=uint16, min=0, max=2**12-1
        d4d := depth for dislay, 3L ndarray, dtype=uint8, min=0, max=255    
    Note1: 
        fromstring is faster than asarray or frombuffer
    Note2:     
        .reshape(120,160) #smaller image for faster response 
                OMAP/ARM default video configuration
        .reshape(240,320) # Used to MATCH RGB Image (OMAP/ARM)
                Requires .set_video_mode
    """
    irmap = np.fromstring(ir_stream.read_frame().get_buffer_as_uint16(),dtype=np.uint16).reshape(240,320)  # Works & It's FAST
    ir4d = np.uint8(irmap.astype(float) *255/ 2**12-1) # Correct the range. Depth images are 12bits
    #d4d = cv2.cvtColor(d4d,cv2.COLOR_GRAY2RGB)
    # Shown unknowns in black
    #ir4d = 255 - ir4d    
    return irmap, ir4d
#get_ir


## main loop
s=0
done = False
while not done:
    key = cv2.waitKey(1)
    ## Read keystrokes
    key = cv2.waitKey(1) & 255
    ## Read keystrokes
    if key == 27: # terminate
        print "\tESC key detected!"
        done = True
    elif chr(key) =='s': #screen capture
        print "\ts key detected. Saving image and distance map {}".format(s)
        cv2.imwrite("ex1_"+str(s)+'.png', d4d)
        np.savetxt("ex1dmap_"+str(s)+'.out',dmap)
        #s+=1 # uncomment for multiple captures   
    #if
    
    ## Streams    
    #IR
    irmap,ir4d = get_ir()
    #print 'Center pixel is {}mm away'.format(dmap[119,159])

    ## Display the stream syde-by-side
    cv2.imshow('ir', ir4d)
# end while

## Release resources 
cv2.destroyAllWindows()
ir_stream.stop()
openni2.unload()
print ("Terminated")