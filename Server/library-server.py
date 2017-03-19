#!python
import sys
import argparse
import tornado.ioloop
import tornado.web
import tornado.websocket
import logging
import threading
from glob import glob
import threading
from LoginHandler import *
from NewUserHandler import *
from AddBookHandler import *

parser=argparse.ArgumentParser("Library backend")
parser.add_argument("--project-root", required=True)
parser.add_argument("--serverport", type=int, default=9000)
args=parser.parse_args()
logging.basicConfig(level=logging.INFO)
sys.path.append(args.project_root)

# /
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write({'message':'Library backend. GET /quit to quit. Other information being added'})

class QuitHandler(tornado.web.RequestHandler):
    def get(self):
        tornado.ioloop.IOLoop.instance().stop()
        self.write("quit library backend")

# -- start
logging.info("Library web server starting up on port %d" % args.serverport)
logging.getLogger("requests").setLevel(logging.CRITICAL)
print ("Library is ready\n")

application = tornado.web.Application([
    (r"/"                    , MainHandler)
    ,(r"/quit"                , QuitHandler)
    # LoginHandler.py
    ,(r"/auth/(.*)"           , LoginHandler)
    
    # NewUserHandler.py
    ,(r"/newuser/(.*)"        , NewUserHandler)
    
    # AddBookHandler.py
    ,(r"/addbook/(.*)"        , AddBookHandler)
])

application.listen(args.serverport)
tornado.ioloop.IOLoop.instance().start()
