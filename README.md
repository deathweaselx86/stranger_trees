To install:

Prerequirements:
* Python 2.7+
* Raspberry Pi 3
* Linux

1. `apt-get install build-essential python-dev git scons swig mesa-common-dev freeglut3-dev`
1. `pip install virtualenvwrapper` and follow instructions for virtualenvwrapper initial setup
1. `mkvirtualenv zebratwitter`
1. `workon zebratwitter` to use zebratwitter virtualenv
1. `pip install -Ur requirements.txt`
1. `git clone https://github.com/jgarff/rpi_ws281x.git`
1. `cd rpi_ws281x && scons` to compile the rpi\_ws381x library
1. Carefully follow the instructions to disable BCM2835 sound!
1. `cd python && sudo python setup.py install` to install the python wrapper
1. `git clone https://github.com/zestyping/openpixelcontrol.git && cd openpixelcontrol`
1.
