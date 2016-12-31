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
        self.SPICLK = 18
        self.SPIMISO = 23
        self.SPIMOSI = 24
        self.SPICS = 25
        self.mq135Pin = 0
        self.mq138Pin = 1
         
        # set up the SPI interface pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SPIMOSI, GPIO.OUT)
        GPIO.setup(self.SPIMISO, GPIO.IN)
        GPIO.setup(self.SPICLK, GPIO.OUT)
        GPIO.setup(self.SPICS, GPIO.OUT)

    def readadc(self, adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
            return -1
        GPIO.output(cspin, True)
 
        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low
 
        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
            if (commandout & 0x80):
                    GPIO.output(mosipin, True)
            else:
                    GPIO.output(mosipin, False)
            commandout <<= 1
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)
 
        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)
            adcout <<= 1
            if (GPIO.input(misopin)):
                adcout |= 0x1
 
        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout
     
    def readSensors(self):
        mq135 = self.readadc(self.mq135Pin, self.SPICLK, self.SPIMOSI, self.SPIMISO, self.SPICS)
        mq138 = self.readadc(self.mq138Pin, self.SPICLK, self.SPIMOSI, self.SPIMISO, self.SPICS)
        return { 'mq135': mq135, 'mq138': mq138 }
