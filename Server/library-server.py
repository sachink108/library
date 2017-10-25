#!python
import sys
import os
import argparse
import tornado.ioloop
import tornado.web
import tornado.websocket
import logging
from LoginHandler import *
from NewUserHandler import *
from AddBookHandler import *
from GetBooksHandler import *
from SearchHandler import *
from DeleteBookHandler import *
from UpdateBookHandler import *
from AuthCodeHandler import *

parser=argparse.ArgumentParser("Library backend")
parser.add_argument("--project-root", required=True)
parser.add_argument("--mode", default="local")
parser.add_argument("--serverport", type=int, default=9000)
args=parser.parse_args()
logging.basicConfig(level=logging.INFO)
sys.path.append(args.project_root)

database_dir = "C:\\databases"
# /
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write({'message':'Library backend. GET /quit to quit. Other information being added'})

class QuitHandler(tornado.web.RequestHandler):
    def get(self):
        tornado.ioloop.IOLoop.instance().stop()
        self.write("quit library backend")

# use a config file here to set the env variables
if (args.mode == "local"):
    os.environ['LIBRARY_IMAGE_STORE'] = 'LOCAL_STORE'

if (args.mode == 'aws'):
    os.environ['LIBRARY_IMAGE_STORE'] = 'AWS_STORE'

# -- start
logging.info("Library web server starting up on port %d" % args.serverport)
logging.info("Library web server mode is %s" % args.mode)
logging.info("Library image store is %s" % os.environ['LIBRARY_IMAGE_STORE'])
logging.getLogger("requests").setLevel(logging.CRITICAL)
logging.info ("Library web server is up and running")

#<img src="http://localhost:8888/static/the_visitor.jpg" />
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), database_dir),
}

application = tornado.web.Application([
    (r"/"                    , MainHandler)
    ,(r"/quit"               , QuitHandler)
    # LoginHandler.py
    ,(r"/auth/(.*)"          , LoginHandler)
    
    # NewUserHandler.py
    ,(r"/newuser/(.*)"       , NewUserHandler)
    
    # AddBookHandler.py
    ,(r"/addbook"            , AddBookHandler)
    
    # GetBooksHandler.py
    ,(r"/getbooks/(.*)"      , GetBooksHandler)

    # SearchHandler.py
    ,(r"/search/(.*)"        , SearchHandler)
    ,(r"/delete/(.*)"        , DeleteBookHandler)
    ,(r"/update/(.*)"        , UpdateBookHandler)
    ,(r"/storeauthcode"      , AuthCodeHandler)

    #(r"/upload"             , Upload),
], **settings)

application.listen(args.serverport)
tornado.ioloop.IOLoop.instance().start()

#useful links
'''
https://technobeans.com/2012/09/17/tornado-file-uploads/
http://www.encodedna.com/angularjs/tutorial/angularjs-file-upload-using-http-post-formdata-webapi.htm
http://stackoverflow.com/questions/16483873/angularjs-http-post-file-and-form-data
http://tutsnare.com/post-form-data-using-angularjs/
'''
