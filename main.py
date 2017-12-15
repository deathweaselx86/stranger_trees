import lib.opc
import settings
import os, time, copy, json
import boto.sqs

import logging
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

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
    DEFAULT_MESSAGE = "DEFAULT HOLIDAYS"
    OFF_PIXEL = (0,0,0)
    
    # here is a table matching ASCII characters to
    # pixels in our string, channels, and colors
    ASCII_PIXEL_TABLE = {
        'A': (0, (255,255,255), 0), # white
        'B': (1, (255,245,255), 0),
        'C': (2, (255,235,255), 0),
        'D': (3, (255,225,255), 0),
        'E': (4, (255,215,255), 0),
        'F': (5, (255,205,255), 0),
        'G': (6, (255,195,255), 0),
        'H': (7, (255,185,255), 0),
        'I': (8, (255,175,255), 0),
        'J': (9, (255,165,255), 0),
        'K': (10, (255,155,255), 0),
        'L': (11, (255,145,255), 0),
        'M': (12, (255,135,255), 0),
        'N': (13, (255,125,255), 0),
        'O': (14, (255,115,255), 0),
        'P': (15, (255,105,255), 0),
        'Q': (16, (255,95,255), 0),
        'R': (17, (255,85,255), 0),
        'S': (18, (255,75,255), 0),
        'T': (19, (255,65,255), 0),
        'U': (20, (255,55,255), 0),
        'V': (21, (255,45,255), 0),
        'W': (22, (255,35,255), 0),
        'X': (23, (255,25,255), 0),
        'Y': (24, (255,15,255), 0),
        'Z': (25, (255,5,255), 0),
        '@': (26, (255,0,255), 0),
        '!': (27, (255,0,245), 0),
        '.': (28, (255,0,235), 0),
        '#': (29, (255,0,225), 0),
        '"': (30, (255,0,215), 0),
        "'": (30, (255,0,215), 0)
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
                channel = StrangerTreeDisplay.ASCII_PIXEL_TABLE[msg[i]][2]
                pixels[index] = value
                self.client.put_pixels(pixels, channel=channel)
            except KeyError:
                self.client.put_pixels(pixels) # this is probably a space; no pixels at all
            time.sleep(1)
        pixels = self._get_reset_pixels()
        self.client.put_pixels(pixels) # defaults to all channels

    def _get_reset_pixels(self):
        return [copy.deepcopy(StrangerTreeDisplay.OFF_PIXEL) for i in xrange(64)]

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

def purge_queue(message):
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
        purge_queue(args.message)
    if args.message:
        send_message(args.message)
    display.start()
