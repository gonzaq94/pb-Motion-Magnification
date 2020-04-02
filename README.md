<h1>Phase Based video Motion Magnification</h1>

A Python source code implementation of motion magnification based on the paper: [Phase Based Video Motion Processing](http://people.csail.mit.edu/mrub/papers/phasevid-siggraph13.pdf) by Neal Wadhwa, Michael Rubinstein, Frédo Durand, William T. Freeman, ACM Transactions on Graphics, Volume 32, Number 4 (Proc. SIGGRAPH), 2013. [project](http://people.csail.mit.edu/nwadhwa/phase-video/). 

This code also includes some demos and some scripts that you can execute in order to do the experiments yourself.

__Authors: Tales Marra and Gonzalo Quintana.__

### Requirements:

 - python 2.7
 - numpy
 - [perceptual](https://github.com/andreydung/Steerable-filter) (Complex steerable pyramid. If you install it with pip you will find and old version that doesn't work. Use the version of this repository or download from the previous github link)
 
 
### Demo

The file demo.py is a console application that allows you to generate a motion magnified version of an input video. Arguments:

`-i --input-video`: Path to the input video.  

`-c / --color-video-flag`: if used, the output video will be a color video. If not, it will be in grayscale.

`-f / --mag-factor`: Magnification factor (default 20).

`-n / --noise-type`: Type of noise added. Possible values: 'gaussian', 'uniform' and 's&p' (salt and pepper). Default: no noise

`-np / --noise-param`: noise parameter. The standard deviation for Gaussian noise, the maximum value for uniform noise and the noise probability for salt and pepper noise. Default values: 20 (gaussian), 60 (uniform) and 0.01 (salt and pepper).

### Color video

Output color video can be generated with two different methods: by applying the MoMag algorithm to all the coordinates of an RGB representation of the frames (phasebasedMoMagColor.py) or by applying it to the VALUE field of an HSV representation (phasebasedMoMagColorHSV.py). In the demo file, the HSV representation is the one used

The RGB method preserves better the colors but creates artifacts for small magnification factors and is three times more computationally costly than the other one. The HSV has better performances (it doesn't create more artifacts than the clasical method and can be used with relatively big amplification factors) and doesn't add any complexity to the classic algorithm, but doesn't preserve the colors perfectly. 
     
### Example video

    ./media/guitar.mp4
    
For all the experiments, we use the [http://people.csail.mit.edu/mrub/evm/video/guitar.mp4](guitar.mp4) video from the motion magnification website.

 
### About

This implementation may include some differences in terms of results with the original git repository, as we developed new experiments. We added the possibility of creating a magnified color video and of adding different kinds of noise.
 
Based on the implementation of:Joao Bastos, Elsbeth van Dam, Coert van Gemeren, Jan van Gemert, Amogh Gudi, Julian Kooij, Malte Lorbach, Claudio Martella, Ronald Poppe.

