# This file is not part of the project, but may be useful if you use a push scheme (e.g. using an ESP8266 chip)

from utilities import *
import argparse
import tornado
import tornado.ioloop
import tornado.web
import os
import logging

# Global models
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
AIR_QUALITY_FN = 'kitchenAirQuality.txt'

class SensorReadHandler(APIRequestHandler):
    def get(self):
        self.write({ 'status': 'success', 'result': { 'mq135': AirQualityHandler.g_kitchenAirQuality }})

class AirQualityHandler(APIRequestHandler):
    g_kitchenAirQuality = 0
    def get(self):
        self.write({ 'status': 'success', 'result': AirQualityHandler.g_kitchenAirQuality })
    def post(self):
        AirQualityHandler.g_kitchenAirQuality = self.get_argument("air", 0)
        open(AIR_QUALITY_FN, 'w').write(str(AirQualityHandler.g_kitchenAirQuality))
        self.write({ 'status': 'success', 'result': AirQualityHandler.g_kitchenAirQuality })
if os.path.exists(AIR_QUALITY_FN):
    AirQualityHandler.g_kitchenAirQuality = int(open(AIR_QUALITY_FN).read().strip())

class HomePageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', title='Analog Sensor Recording')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A test website using Tornado.")
    parser.add_argument('-d', '--debug', help="enable debug mode", action='store_true', default=False)
    parser.add_argument('-p', '--port', help="which port to serve content on", type=int, default=3000)
    args = parser.parse_args()

    settings = {
        'debug': args.debug, 
        'template_path': os.path.join(os.getcwd(), 'views'),
        'static_path': os.path.join(os.getcwd(), 'static')
    }

    logging.info('static path = {0}'.format(os.path.join(os.getcwd(), 'static', r'\1')))
    handlers = [
        (r'/', HomePageHandler),
        (r'/api/v1/sensors', SensorReadHandler),
        (r'/api/v1/air', AirQualityHandler),
    ]

    application = tornado.web.Application(handlers, **settings)
    if args.debug:
        logging.info('Entering debug mode...')
    logging.info('Listening on port {0}...'.format(args.port))
    application.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()
