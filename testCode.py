from phasebasedMoMag import phaseBasedMagnify
from phasebased
+MoMagColor import phaseBasedMagnifyColor

def main():

    vidFname = 'media/guitar.mp4'
    vidFname = 'media/noisy videos/guitar.mp4-noisy-wgn-20.avi'
    #vidFname = 'media/noisy videos/guitar.mp4-noisy-s&p-0.00.avi'
    #vidFname = 'media/noisy videos/guitar.mp4-noisy-uniform-200.avi'
    files = []

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


    for f in files:

        # output video filename
        vidFnameOut = f + '-Mag%dIdeal-lo%d-hi%d.avi' % (factor, lowFreq, highFreq)

        phaseBasedMagnifyColor(f, vidFnameOut, maxFrames, windowSize, 2, fpsForBandPass, lowFreq, highFreq)
        phaseBasedMagnifyColor(f, vidFnameOut, maxFrames, windowSize, 5, fpsForBandPass, lowFreq, highFreq)
        phaseBasedMagnifyColor(f, vidFnameOut, maxFrames, windowSize, 10, fpsForBandPass, lowFreq, highFreq)
        phaseBasedMagnifyColor(f, vidFnameOut, maxFrames, windowSize, 40, fpsForBandPass, lowFreq, highFreq)

if __name__ == "__main__":
    main()
