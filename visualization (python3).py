from perceptual.filterbank import *
import numpy as np
import matplotlib.pyplot as plt

import pyrtools as pt

import scipy.signal as sps


import cv2

# determine what OpenCV version we are using
try:
    import cv2.cv as cv
    USE_CV2 = True
except ImportError:
    # OpenCV 3.x does not have cv2.cv submodule
    USE_CV2 = False
    
import sys
import numpy as np

from pyr2arr import Pyramid2arr
from temporal_filters import IdealFilterWindowed, ButterBandpassFilter


def visualize(vidFname, maxFrames, windowSize, factor, fpsForBandPass, lowFreq, highFreq):
    filters = pt.steerable_filters('sp3_filters')

    fsz = int(np.round(np.sqrt(filters['bfilts'].shape[0])))
    fsz = np.array([fsz, fsz])
    nfilts = filters['bfilts'].shape[1]
    nrows = int(np.floor(np.sqrt(nfilts)))


    # Look at the oriented bandpass filters:
    filtList = []
    for f in range(nfilts):
        filtList.append(sps.convolve2d(filters['bfilts'][:,f].reshape(fsz), filters['lo0filt']))

    filt = pt.imshow(filtList, vrange='auto', zoom=20)
    filt.savefig('Visualization_results/spatial_filters.png')
    # initialize the steerable complex pyramid
    steer = Steerable(5)
    steer.nbands = 8
    pyArr = Pyramid2arr(steer)

    print ("Reading:", vidFname)

    # get vid properties
    vidReader = cv2.VideoCapture(vidFname)
    if USE_CV2:
        # OpenCV 2.x interface
        vidFrames = int(vidReader.get(cv.CV_CAP_PROP_FRAME_COUNT))    
        width = int(vidReader.get(cv.CV_CAP_PROP_FRAME_WIDTH))
        height = int(vidReader.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
        fps = int(vidReader.get(cv.CV_CAP_PROP_FPS))
        func_fourcc = cv.CV_FOURCC
    else:
        # OpenCV 3.x interface
        vidFrames = int(vidReader.get(cv2.CAP_PROP_FRAME_COUNT))    
        width = int(vidReader.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vidReader.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(vidReader.get(cv2.CAP_PROP_FPS))
        func_fourcc = cv2.VideoWriter_fourcc

    if np.isnan(fps):
        fps = 30

    # video Writer
    fourcc = func_fourcc('M', 'J', 'P', 'G')

    # how many frames
    nrFrames = min(vidFrames, maxFrames)

    # read video
    #print steer.height, steer.nbands

    # setup temporal filter
    filter = IdealFilterWindowed(windowSize, lowFreq, highFreq, fps=fpsForBandPass, outfun=lambda x: x[0])
    #filter = ButterBandpassFilter(1, lowFreq, highFreq, fps=fpsForBandPass)

    for frameNr in range( nrFrames + windowSize ):
        sys.stdout.flush() 

        if frameNr < nrFrames:
            # read frame
            _, im = vidReader.read()
               
            if im is None:
                # if unexpected, quit
                break
			
            # convert to gray image
            if len(im.shape) > 2:
                HSV_img = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
                grayIm = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
            else:
                # already a grayscale image?
                grayIm = im


            filt = 'sp3_filters' # There are 4 orientations for this filter
            pyr = pt.pyramids.SteerablePyramidSpace(grayIm, height=4, order=3)
            a = pt.pyrshow(pyr.pyr_coeffs)
            
            a.savefig('Visualization_results/pyramid.png')

            break

################ main script

#vidFname = 'media/baby.mp4';
#vidFname = 'media/WIN_20151208_17_11_27_Pro.mp4.normalized.avi'
#vidFname = 'media/embryos01_30s.mp4'
vidFname = 'media/guitar.mp4'

# maximum nr of frames to process
maxFrames = 60000
# the size of the sliding window
windowSize = 30
# the magnifaction factor
factor = 2
# the fps used for the bandpass
fpsForBandPass = 600 # use -1 for input video fps
# low ideal filter
lowFreq = 72
# high ideal filter
highFreq = 92


visualize(vidFname, maxFrames, windowSize, factor, fpsForBandPass, lowFreq, highFreq)

