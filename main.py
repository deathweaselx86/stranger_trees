import lib.opc
import settings
import os, time, copy, json
import boto.sqs

import logging
import argparse

logger = logging.getLogger(__name__)

class QueueWrapper(object):

    def __init__(self, debug=False):
        self.region = os.environ.get('AWS_REGION', 'us-east-1')
        self.access_key = os.environ.get('AWS_ACCESS_KEY', 'XXX')
        self.secret = os.environ.get('AWS_SECRET_KEY', 'XXX')
        self.queue_name = os.environ.get('SQS_QUEUE', 'stranger_trees')

    def get_queue(self):
        connection = boto.sqs.connect_to_region(self.region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret)
        return connection.get_queue(self.queue_name)
 

class StrangerTreeDisplay(object):
    DEFAULT_MESSAGE = "HAPPY HOLIDAYS FROM THE ZEBRA"
    OFF_PIXEL = (0,0,0)
    GREEN = (255,0,0)
    RED = (0,255,0)
    # here is a table matching ASCII characters to
    # pixels in our string, channels, and colors
    # These will all show up on the first string right now
    # start at 50 and 300
    ASCII_PIXEL_TABLE = {
        'A': (333, (255,255,255)), # white
        'B': (337, (255,245,255)),
        'C': (324, (255,235,255)),
        'D': (69, (255,225,255)),
        'E': (340, (255,215,255)),
        'F': (318, (255,205,255)),
        'G': (349, (255,195,255)),
        'H': (315, (255,185,255)),
        'I': (85, (255,175,255)),
        'J': (90, (255,165,255)),
        'K': (347, (255,155,255)),
        'L': (52, (255,145,255)),
        'M': (72, (255,135,255)),
        'N': (311, (255,125,255)),
        'O': (83, (255,115,255)),
        'P': (87, (255,105,255)),
        'Q': (50, (255,95,255)),
        'R': (335, (255,85,255)),
        'S': (320, (255,75,255)),
        'T': (326, (255,65,255)),
        'U': (89, (255,55,255)),
        'V': (304, (255,45,255)),
        'W': (301, (255,35,255)),
        'X': (66, (255,25,255)),
        'Y': (309, (255,15,255)),
        'Z': (342, (255,5,255)),
        " ": (94, (255,0,190))
    }

    def __init__(self, debug=False):
        settings.init()
        host = os.environ.get('FADECANDY_HOST', 'localhost')
        port = os.environ.get('FADECANDY_PORT', '7890')
        self.client = lib.opc.Client('%s:%s' % (host, port))
        self.client.verbose = debug
        self.queue_wrapper = QueueWrapper()
        self.queue = None

    def start(self):
        if self.connected() is False:
            raise StandardError, "Cannot connect to server."
        self.queue = self.queue_wrapper.get_queue()
        while True:
            msg = self.get_sqs_msg()
            self.display_msg(msg)
            time.sleep(5)

    def connected(self):
        return self.client.can_connect()

       
    def get_sqs_msg(self):
        if self.queue:
            results = self.queue.get_messages(wait_time_seconds=5, num_messages=1)
            if len(results) > 0:
                message = results[0]
                text = json.loads(results[0].get_body())['text']
                message.delete()
                return text.upper()
            else:
                return StrangerTreeDisplay.DEFAULT_MESSAGE 

    def display_msg(self, msg):
        logger.info("Displaying %s" % (msg))
        for i in range(len(msg)):
            pixels = self._get_reset_pixels()
            try:
                index = StrangerTreeDisplay.ASCII_PIXEL_TABLE[msg[i]][0]
                value = StrangerTreeDisplay.ASCII_PIXEL_TABLE[msg[i]][1]
                pixels[index] = [StrangerTreeDisplay.RED,StrangerTreeDisplay.GREEN][i%2]
                self.client.put_pixels(pixels)
            except KeyError:
                self.client.put_pixels(pixels) # this is probably a space; no pixels at all
            time.sleep(1)
        pixels = self._get_reset_pixels()
        self.client.put_pixels(pixels) # defaults to all channels

    def _get_reset_pixels(self):
        return [copy.deepcopy(StrangerTreeDisplay.OFF_PIXEL) for i in xrange(512)]

def setup_logger(debug):
    level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(level)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def send_message(message):
    queue = QueueWrapper().get_queue()
    queue.write(queue.new_message(body=json.dumps({"text": message})))

def purge_queue():
    queue = QueueWrapper().get_queue()
    queue.purge()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Light up the stranger_tree based on text messages.')
    parser.add_argument('--debug', action='store_true', help='do you want verbose debugging messages?')
    parser.add_argument('--purge', action='store_true', help='clear all messages from queue before processing')
    parser.add_argument("--message", help="puts a message on the queue before running")
    args = parser.parse_args()
    setup_logger(args.debug)

    display = StrangerTreeDisplay(args.debug)
    if args.purge:
        purge_queue()
    if args.message:
        send_message(args.message)
    display.start()
