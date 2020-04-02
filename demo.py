import os
import argparse

from phasebasedMoMag import phaseBasedMagnify
from phasebasedMoMagColorHSV import phaseBasedMagnifyColor
from noisyVideoGenerator import addNoiseToVideo

args = None
parser = argparse.ArgumentParser(description='Motion Magnification demo')
parser.add_argument('-i', '--input-video',
                    type=str, help='path to input video')
parser.add_argument('-c', '--color-video-flag',
                    action='store_true', help='If activated, output is color video')
parser.add_argument('-f', '--mag-factor',
                    default=20,
                    type=int, help='Magnification factor')
parser.add_argument('-n', '--noise_type',
                    default='', type=str,
                    help="Type of noise added, possible values are 'gaussian', 'uniform' and 's&p'")
parser.add_argument('-np', '--noise_param',
                    default=None, type=float,
                    help="Noise parameters: STD for 'gaussian', MAX_VALUE for 'uniform' and PROBABILITY for 's&p'")

# output folder
output_folder = 'demo'
# maximum nr of frames to process
maxFrames = 60000
# the size of the sliding window
windowSize = 30
# the fps used for the bandpass
fpsForBandPass = 600 # use -1 for input video fps
# low ideal filter
lowFreq = 72
# high ideal filter
highFreq = 92

default_noise_param = {

    'gaussian': 20,
    'uniform': 60,
    's&p': 0.01,
}

def main(args):

    vidFname = args.input_video

    directory, filename = os.path.split(args.input_video)
    output_dir = os.path.join(directory,output_folder)

    # Create target Directory if don't exist
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        print "Directory" , output_dir ,  "created"
    else:
        print "Directory" , output_dir ,  "already exists" 

    if args.noise_type:

        print("Adding noise to video")

        # if not specified, use the default noise parameters

        if not args.noise_param:

            noise_param = default_noise_param.get(args.noise_type, 'Invalid type')

        else:

            noise_param = args.noise_param

        if int(noise_param) == float(noise_param):
            decimals = 0
        else:
            decimals = 2

        noisy_video = output_dir +'/' + filename + '-noisy-%s'  % (args.noise_type) + '-{0:.{1}f}.avi'.format(noise_param, decimals)

        addNoiseToVideo(vidFname, noisy_video, maxFrames, args.noise_type, noise_param)

        vidFname = noisy_video
        filename = os.path.split(vidFname)[1]

    if args.color_video_flag:

        vidFnameOut = output_dir +'/' + filename + '-Mag%dIdeal-lo%d-hi%d-color-hsv.avi' % (args.mag_factor, lowFreq, highFreq)
        phaseBasedMagnifyColor(vidFname, vidFnameOut, maxFrames, windowSize, args.mag_factor, fpsForBandPass, lowFreq, highFreq)

    else:

        vidFnameOut = output_dir +'/' + filename + '-Mag%dIdeal-lo%d-hi%d.avi' % (args.mag_factor, lowFreq, highFreq)
        phaseBasedMagnify(vidFname, vidFnameOut, maxFrames, windowSize, args.mag_factor, fpsForBandPass, lowFreq, highFreq)

if __name__ == "__main__":

    args = parser.parse_args()
    main(args)

