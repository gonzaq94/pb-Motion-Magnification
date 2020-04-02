<h1>Phase Based video Motion Magnification</h1>

A Python source code implementation of motion magnification based on the paper: [Phase Based Video Motion Processing](http://people.csail.mit.edu/mrub/papers/phasevid-siggraph13.pdf) by Neal Wadhwa, Michael Rubinstein, Frédo Durand, William T. Freeman, ACM Transactions on Graphics, Volume 32, Number 4 (Proc. SIGGRAPH), 2013. [project](http://people.csail.mit.edu/nwadhwa/phase-video/). 

This code also include some demos and some scripts that you can execute in order to do the experiments yourself.

__Authors: Tales Marra and Gonzalo Quintana.__

### Requirements:

 - python 2.7
 - numpy
 - [perceptual](https://github.com/andreydung/Steerable-filter) (Complex steerable pyramid, install with: sudo pip install perceptual) 
     
### Example video

    ./media/guitar.mp4
    
When you run the code 'python phasebasedMoMag.py' it expects an example video in the 'media' folder. Here we use the [http://people.csail.mit.edu/mrub/evm/video/guitar.mp4](guitar.mp4) video from the motion magnification website.

 
### About

This implementation may include some differences in terms of results then the original git repository, as we developed new experiments.
 
Based on the implementation of:Joao Bastos, Elsbeth van Dam, Coert van Gemeren, Jan van Gemert, Amogh Gudi, Julian Kooij, Malte Lorbach, Claudio Martella, Ronald Poppe.

