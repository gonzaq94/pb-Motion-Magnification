import cv2
import matplotlib.pyplot as plt

# determine what OpenCV version we are using
try:
    import cv2.cv as cv

    USE_CV2 = True
except ImportError:
    # OpenCV 3.x does not have cv2.cv submodule
    USE_CV2 = False

import sys
import numpy as np

def sp_noise(image,prob):
    '''
    Add salt and pepper noise to image
    prob: Probability of the noise
    '''
    output = np.zeros(image.shape, np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = np.random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

def addNoiseToVideo(vidFname, vidFnameOut, maxFrames, noise_type):
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
    for frameNr in range(nrFrames):
        print frameNr,
        sys.stdout.flush()

        if frameNr < nrFrames:
            # read frame
            _, im = vidReader.read()

            if im is None:
                # if unexpected, quit
                break

            if noise_type == 'wgn':

                im = cv2.add(im, cv2.randn(np.zeros(im.shape), (mean, mean, mean), (std, std, std)).astype('uint8'))
            elif noise_type == 's&p':
                im = sp_noise(im, prob)
            elif noise_type == 'uniform':
                im = cv2.add(im, cv2.randu(np.zeros(im.shape), -max_u, max_u).astype('uint8'))

            #noise = np.random.randn(im.shape[0],im.shape[1],im.shape[2])#randint(0, 255, size=c, dtype=np.uint8)

            #im = im + noise


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

# noise parameters
noise_type = 's&p'
# gaussian
std = 1
mean = 0
# salt and pepper
prob = 0.05 # for salt and pepper noise
#uniform
max_u = 200

# output video filename
output_folder = 'media/noisy videos/'
if noise_type == 'wgn':
    vidFnameOut = output_folder + vidFname + '-noisy-%s-%d.avi' % (noise_type, std)
elif noise_type == 's&p':
    vidFnameOut = output_folder + vidFname + '-noisy-%s-%1.2f.avi' % (noise_type, prob)
elif noise_type == 'uniform':
    vidFnameOut = output_folder + vidFname + '-noisy-%s-%d.avi' % (noise_type, max_u)

addNoiseToVideo(vidFolder + vidFname, vidFnameOut, maxFrames, noise_type)
