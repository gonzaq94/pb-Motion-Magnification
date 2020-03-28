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


def addNoiseToVideo(vidFname, vidFnameOut, maxFrames):
    # initialize the steerable complex pyramid

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

    print 'FrameNr:',
    for frameNr in range(nrFrames + windowSize):
        print frameNr,
        sys.stdout.flush()

        if frameNr < nrFrames:
            # read frame
            _, im = vidReader.read()

            if im is None:
                # if unexpected, quit
                break

            im = cv2.add(im, cv2.randn(np.zeros(im.shape), 0, std).astype('uint8'))

            im[im>255] = 255
            im[im<0] = 0

            # write to disk
            res = cv2.convertScaleAbs(im)
            vidWriter.write(res)

    # free the video reader/writer
    vidReader.release()
    vidWriter.release()


################# main script

# vidFname = 'media/baby.mp4';
# vidFname = 'media/WIN_20151208_17_11_27_Pro.mp4.normalized.avi'
# vidFname = 'media/embryos01_30s.mp4'
vidFname = 'guitar.mp4'
vidFolder = 'media/'

# maximum nr of frames to process
maxFrames = 60000
# the size of the sliding window
windowSize = 30
# the magnifaction factor
factor = 2
# the fps used for the bandpass
fpsForBandPass = 600  # use -1 for input video fps
# low ideal filter
lowFreq = 72
# high ideal filter
highFreq = 92
# noise parameters
noise_type = 'wgn'
std = 5
# output video filename
output_folder = 'media/noisy videos/'
vidFnameOut = output_folder + vidFname + '-noisy-%s-%d.avi' % (noise_type, std)

addNoiseToVideo(vidFolder+vidFname, vidFnameOut, maxFrames)
