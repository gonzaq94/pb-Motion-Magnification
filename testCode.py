from phasebasedMoMag import phaseBasedMagnify
from phasebasedMoMagColor import phaseBasedMagnifyColor

def main():

    vidFname = 'media/guitar.mp4'
    #vidFname = 'media/noisy videos/guitar.mp4-noisy-wgn-20.avi'
    #vidFname = 'media/noisy videos/guitar.mp4-noisy-s&p-0.00.avi'
    #vidFname = 'media/noisy videos/guitar.mp4-noisy-uniform-200.avi'
    factors = [2,5,10]

    # maximum nr of frames to process
    maxFrames = 60000
    # the size of the sliding window
    windowSize = 30
    # the magnification factor
    factor = 40
    # the fps used for the bandpass
    fpsForBandPass = 600 # use -1 for input video fps
    # low ideal filter
    lowFreq = 72
    # high ideal filter
    highFreq = 92


    for f in factors:

        # output video filename
        vidFnameOut = vidFname + '-Mag%dIdeal-lo%d-hi%d-color.avi' % (f, lowFreq, highFreq)

        phaseBasedMagnifyColor(vidFname, vidFnameOut, maxFrames, windowSize, f, fpsForBandPass, lowFreq, highFreq)


if __name__ == "__main__":
    main()
