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

def addNoiseToVideo(vidFname, vidFnameOut, maxFrames, noise_type, noise_param):

    # for Gaussian noise
    mean = 0

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

            if noise_type == 'gaussian':
                noise = cv2.randn(np.zeros(im.shape), (mean, mean, mean), (noise_param, noise_param, noise_param))
                # noise_param is the STD
                im = im + noise
            elif noise_type == 's&p':
                im = sp_noise(im, noise_param/2)
                # noise_param is the noise probability
            elif noise_type == 'uniform':
                noise = cv2.randu(np.zeros(im.shape), (-noise_param,-noise_param,-noise_param), (noise_param,noise_param,noise_param))
                # noise_param is the maximal value of the uniform             
                im = im + noise

            im[im>255] = 255
            im[im<0] = 0

            # write to disk
            res = cv2.convertScaleAbs(im)
            vidWriter.write(res)

    # free the video reader/writer
    vidReader.release()
    vidWriter.release()

################# main script
def main():

    # vidFname = 'media/baby.mp4';
    # vidFname = 'media/WIN_20151208_17_11_27_Pro.mp4.normalized.avi'
    # vidFname = 'media/embryos01_30s.mp4'
    vidFname = 'guitar.mp4'
    vidFolder = 'media/'

    # maximum nr of frames to process
    maxFrames = 60000

    # noise parameters
    noise_type = 'uniform' #possible values 'gaussian', 'uniform' and 's&p'
    # gaussian
    std = 50
    mean = 0
    # salt and pepper
    prob = 0.1 # for salt and pepper noise
    #uniform
    max_u = 1

    # output video filename
    output_folder = 'media/noisy videos/'
    if noise_type == 'gaussian':
        vidFnameOut = output_folder + vidFname + '-noisy-%s-%d.avi' % (noise_type, std)
    elif noise_type == 's&p':
        vidFnameOut = output_folder + vidFname + '-noisy-%s-%1.2f.avi' % (noise_type, prob)
    elif noise_type == 'uniform':
        vidFnameOut = output_folder + vidFname + '-noisy-%s-%d.avi' % (noise_type, max_u)

    addNoiseToVideo(vidFolder + vidFname, vidFnameOut, maxFrames, noise_type, max_u)

if __name__ == "__main__":
    main()
