import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '.'))
#from config import *
from datetime import datetime
import json
import tornado
import tornado.web
import time
import os
import RPi.GPIO as GPIO
import spidev

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

class APIRequestHandler(tornado.web.RequestHandler):
    def writeJson(self, obj):
        text = json.dumps(obj, default=json_serial)
        self.write(text)

class GPIOHelper:
    def __init__(self):
        self.mq135Pin = 0
        self.mq138Pin = 1
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
    def readadc(self, adcnum):
        if ((adcnum > 7) or (adcnum < 0)):
            return -1
        r = self.spi.xfer2([1,(8+adcnum)<<4,0])
        adcout = ((r[1]&3) << 8) + r[2]
        return adcout
     
    def readSensors(self):
        mq135 = self.readadc(self.mq135Pin)
        mq138 = self.readadc(self.mq138Pin)
        return { 'mq135': mq135, 'mq138': mq138 }
