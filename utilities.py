import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '.'))
#from config import *
from datetime import datetime
import json
import tornado
import tornado.web

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
