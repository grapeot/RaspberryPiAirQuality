import argparse
import tornado
import tornado.ioloop
import tornado.web
import os
import logging

# Global models
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class APIJobHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({ 'status': 'success', 'result': [ 1, 2, 3 ] })

class APIPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('api.html', title='API Index')

class HomePageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', title='Index', items=[1, 2, 3])

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
        (r'/api', APIPageHandler),
        (r'/api/v1/jobs', APIJobHandler),
    ]

    application = tornado.web.Application(handlers, **settings)
    if args.debug:
        logging.info('Entering debug mode...')
    logging.info('Listening on port {0}...'.format(args.port))
    application.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()
