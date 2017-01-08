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
import wiringpi
import struct
import serial

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
        self.pm10Pin = 2
        self.ILEDPin = 18
        self.samplingTime = 280
        self.deltaTime = 40
        self.sleepTime = 9680
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        # Uncomment this when you need to read from the Nova PM25 sensor.
        # self.serial = serial.Serial(port='/dev/serial0')
        
        # Initialize wiringpi
        wiringpi.wiringPiSetupGpio() 
        wiringpi.pinMode(self.ILEDPin, 1)
        wiringpi.digitalWrite(self.ILEDPin, 0) # turn the LED off

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
    def readadc(self, adcnum):
        if ((adcnum > 7) or (adcnum < 0)):
            return -1
        r = self.spi.xfer2([1,(8+adcnum)<<4,0])
        adcout = ((r[1]&3) << 8) + r[2]
        return adcout

    def readNovaPM25Sensor(self):
        data = self.serial.read(10)
        # Parse the data and convert it to the unit of ug/m^3
        pm25 = (data[3] * 256 + data[2]) / 10
        pm10 = (data[5] * 256 + data[4]) / 10
        return { 'pm25': pm25, 'pm10': pm10 }
     
    def readSharpPM10Sensor(self):
        voMeasured = 0
        for i in range(10):
            wiringpi.digitalWrite(self.ILEDPin, 1) # power on the LED
            wiringpi.delayMicroseconds(self.samplingTime)
            wiringpi.delayMicroseconds(self.deltaTime)
            voMeasured = self.readadc(self.pm10Pin) # read the dust value
            wiringpi.digitalWrite(self.ILEDPin, 0) # turn the LED off
            wiringpi.delayMicroseconds(self.sleepTime)

            # 0 - 5V mapped to 0 - 1023 integer values
            # recover voltage
            calcVoltage = voMeasured * (5.0 / 1024)
            
            # linear eqaution taken from http://www.howmuchsnow.com/arduino/airquality/
            # Chris Nafis (c) 2012
            dustDensity = 0.17 * calcVoltage - 0.1
            #print("{0}, {1}, {2}".format(voMeasured, calcVoltage, dustDensity))
        return voMeasured
     
    def readSensors(self):
        mq135 = self.readadc(self.mq135Pin)
        #mq138 = self.readadc(self.mq138Pin)
        pm10 = self.readSharpPM10Sensor()
        return { 'mq135': mq135, 'pm10': pm10 }

if __name__ == '__main__':
    helper = GPIOHelper()
    while True:
        wiringpi.delay(500)
        print(helper.readSharpPM10Sensor())
