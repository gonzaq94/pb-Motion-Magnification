from perceptual.filterbank import *
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb

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


def phaseBasedMagnify(vidFname, vidFnameOut, maxFrames, windowSize, factor, fpsForBandPass, lowFreq, highFreq):
    # initialize the steerable complex pyramid
    steer = Steerable(5)
    steer.nbands = 8
    pyArr = Pyramid2arr(steer)

    print "Reading:", vidFname,

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

    print ' %d frames' % vidFrames,
    print ' (%d x %d)' % (width, height),
    print ' FPS:%d' % fps

    # video Writer
    fourcc = func_fourcc('M', 'J', 'P', 'G')
    vidWriter = cv2.VideoWriter(vidFnameOut, fourcc, int(fps), (width, height), 1)
    print 'Writing:', vidFnameOut

    # how many frames
    nrFrames = min(vidFrames, maxFrames)

    # read video
    # print steer.height, steer.nbands

    # setup temporal filter
    filter = IdealFilterWindowed(windowSize, lowFreq, highFreq, fps=fpsForBandPass, outfun=lambda x: x[0])
    # filter = ButterBandpassFilter(1, lowFreq, highFreq, fps=fpsForBandPass)

    print 'FrameNr:',
    for frameNr in range(nrFrames + windowSize): #nrFrames + windowSize
        print frameNr,
        sys.stdout.flush()

        if frameNr < nrFrames:
            # read frame
            _, im = vidReader.read()

            if im is None:
                # if unexpected, quit
                break
            # convert to gray image
            if len(im.shape) > 2:
                #plt.imshow(im)
                #plt.show()
                im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
                grayIm = np.array(im[:, :, 2])
            else:
                # already a grayscale image?
                grayIm = im

            # We decompose the image within the pyramid's coefficients. This refers to the first column in the figure 2 of the paper.
            coeff = steer.buildSCFpyr(grayIm)
            # coeff = steer.buildSCFpyr(HSV_img[:,:,2])

            # add image pyramid to video array
            # NOTE: on first frame, this will init rotating array to store the pyramid coeffs
            arr = pyArr.p2a(coeff)

            # We take the phase of the decomposition (second column of figure 2) for every coefficient.
            phases = np.angle(arr)

            # add to temporal filter
            filter.update([phases])

            # try to get filtered output to continue
            try:
                filteredPhases = filter.next()
            except StopIteration:
                continue

            print '*',

            # motion magnification
            magnifiedPhases = phases + filteredPhases * factor
            # create new array
            newArr = np.abs(arr) * np.exp(magnifiedPhases * 1j)

            # create pyramid coeffs
            newCoeff = pyArr.a2p(newArr)

            # reconstruct pyramid
            out = steer.reconSCFpyr(newCoeff)

            # clip values out of range
            out[out > 255] = 255
            out[out < 0] = 0

            # make a RGB image
            hsvIm = np.empty((out.shape[0], out.shape[1], 3))
            hsvIm[:, :, 0] = np.array(im[:,:,0])
            hsvIm[:, :, 1] = np.array(im[:,:,1])
            hsvIm[:, :, 2] = out

            rgbIm = cv2.cvtColor((hsvIm/255).astype(np.float32), cv2.COLOR_HSV2BGR)

            res = (rgbIm*255).astype('uint8')
            plt.imshow(res)
            plt.show()

            vidWriter.write(res)

    # free the video reader/writer
    vidReader.release()
    vidWriter.release()

################# main script

# vidFname = 'media/baby.mp4';
# vidFname = 'media/WIN_20151208_17_11_27_Pro.mp4.normalized.avi'
# vidFname = 'media/embryos01_30s.mp4'
vidFname = 'media/guitar.mp4'

# maximum nr of frames to process
maxFrames = 60000
# the size of the sliding window
windowSize = 30
# the magnifaction factor
factor = 50
# the fps used for the bandpass
fpsForBandPass = 600  # use -1 for input video fps
# low ideal filter
lowFreq = 72
# high ideal filter
highFreq = 92
# output video filename
vidFnameOut = vidFname + '-Mag%dIdeal-lo%d-hi%d-color-hsv.avi' % (factor, lowFreq, highFreq)

phaseBasedMagnify(vidFname, vidFnameOut, maxFrames, windowSize, factor, fpsForBandPass, lowFreq, highFreq)
