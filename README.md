# Stranger Trees

To use:

Prerequirements:
* Python 2.7+
* Raspberry Pi 3
* Linux
* AWS SQS
* Fadecandy Controller Board
* WS281x compatible LED strip(s)

This particular project uses three strips of 50 on 3 channels.

1. You will need to get an OPC server. Get Fadecandy. `cd .. && git clone https://github.com/scanlime/fadecandy.git`
1. Install the fcserver binary according to the instructions in the server directory of the fadecandy project.
1. `apt-get install build-essential python-dev git scons swig mesa-common-dev freeglut3-dev`
1. `pip install virtualenvwrapper` and follow instructions for virtualenvwrapper initial setup
1. `mkvirtualenv stranger_trees`
1. `workon stranger_trees` to use stranger_trees virtualenv
1. `pip install -Ur requirements.txt`
1. Copy `.env.example` to `.env` and put your Fadecandy server settings and AWS credentials, etc in it.
It will be picked up by settings.py when you run `main.py`
1. Run fcserver
1. `python main.py --debug`
