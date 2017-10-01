import os
import sys
import uuid
import json
import tornado.ioloop
import time
import tornado.web
import logging
import sqlite3
import base64
import datetime
from URIParser import *
from elasticsearch import Elasticsearch

database_dir = "C:\\databases"
gClient = Elasticsearch([{'host': 'localhost', 'port': 9200}])
gElasticIndex = "books"

class AddBookHandler(tornado.web.RequestHandler):
    def _saveImage(self, request):
        username = self.get_body_argument("username", default=None, strip=False)
        userdir = username + "_es"
        userdir = os.path.join(database_dir, userdir)

        if not os.path.exists(userdir):
            os.makedirs(userdir)

        if (len(self.request.files.keys()) > 0): #desktop
            fileinfo = self.request.files['0'][0]
            filename = fileinfo['filename']
            imgData = fileinfo['body']
        else: #mobile
            filename = str(uuid.uuid4()) + ".jpg"
            imgData = self.get_body_argument("0", default=None, strip=False)
            imgData = base64.decodebytes(bytes(imgData, 'utf-8'))

        ofile = os.path.join(userdir, filename)
        fh = open(ofile, 'wb')
        fh.write(imgData)

        return ofile

    def _createIndexDocTypeMapping(self, username):
        docType = username + gElasticIndex
        properties = {"title": {"type": "text"},
                      "author": {"type": "text"},
                      "image_filepath": {"type": "text", "index": "false"},
                      "timestamp": {"type": "date", "format" : "epoch_millis"},
                      "h_timestamp": {"type": "text"}
                      }
        if gClient.indices.exists(index="books"):
            if not gClient.indices.exists_type(index=gElasticIndex, doc_type=docType):
                print("index exists, adding mapping")
                request_body = { docType: {
                                    "properties": properties
                                    }
                                }
                gClient.indices.put_mapping(index="books", doc_type=docType, body=request_body)
        else:  # index does not exist, create index and mapping
            print("Adding index and mapping")
            request_body = { "settings": {"number_of_shards": 5, "number_of_replicas": 1},
                             'mappings': { docType: {
                                            "properties": properties
                                            }
                                         }
                            }
            gClient.indices.create(index='books', body=request_body)
        return docType

    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        username = self.get_body_argument("username", default=None, strip=False)
        title = self.get_body_argument("title", default=None, strip=False)
        author = self.get_body_argument("author", default=None, strip=False)
        category = self.get_body_argument("category", default=None, strip=False)

        filepath = self._saveImage(self.request) # should return an error is image is not provided, can chck this in js?
        docType = self._createIndexDocTypeMapping(username)
        current_milli_time = lambda: int(round(time.time() * 1000))
        curTime = current_milli_time()
        #hCurTime =  datetime.datetime.fromtimestamp(curTime/1000.0).strftime('%Y-%m-%dT%H:%M:%S')
        hCurTime = datetime.datetime.fromtimestamp(curTime / 1000.0).strftime("%A, %d. %B %Y %I:%M %p")

        _body = {'title': title,
                 'author': author,
                 'category': category,
                 'image_filepath': filepath,
                 #'timestamp': datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
                 'timestamp':curTime,
                 "h_timestamp": hCurTime
                 }
        elasticResp = gClient.index(index=gElasticIndex, doc_type=docType, id=uuid.uuid4(), body=_body)
        print(elasticResp)
        self.finish({"status": "OK", "resp" : elasticResp})

'''
class AddBookHandler(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        username = self.get_body_argument("username", default=None, strip=False)
        title = self.get_body_argument("title", default=None, strip=False)
        author = self.get_body_argument("author", default=None, strip=False)
        category = self.get_body_argument("category", default=None, strip=False)
        
        if (len(self.request.files.keys()) > 0):
            fileinfo = self.request.files['0'][0]
            filename = fileinfo['filename']
            extn = os.path.splitext(filename)[1]
            cname = str(uuid.uuid4()) + extn
            user_dir = os.path.join(database_dir, username)
            ofile = os.path.join(user_dir, cname)
            fh = open(ofile, 'wb')
            fh.write(fileinfo['body'])
            # finished saving image
        else:
            cname = str(uuid.uuid4()) + ".jpg"
            user_dir = os.path.join(database_dir, username)
            ofile = os.path.join(user_dir, cname)
            fh = open(ofile, 'wb')
            img_data = self.get_body_argument("0", default=None, strip=False)
            print (img_data)
            #img = base64.decodestring(img_data)
            img = base64.decodestring(bytes(img_data,'utf-8'))
            fh.write(img)
            
        status = '';
        user_db = os.path.join(user_dir, "%s.db" % username)
        conn = sqlite3.connect(user_db)
        create_books_table = """ CREATE TABLE IF NOT EXISTS books (
                                        id INTEGER PRIMARY KEY,
                                        author TEXT NOT NULL,
                                        title TEXT NOT NULL,
                                        category TEXT NOT NULL,
                                        img_filename TEXT NOT NULL,
                                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                        ); """ 
        conn.cursor().execute(create_books_table)
        if conn is not None:
            q = "INSERT INTO books (title, author, category, img_filename) VALUES (?,?,?,?);"
            print (q)
            conn.cursor().execute(q,(title,author,category,cname))
            conn.commit()
            status = "OK"
        else:
            status = "NOK"
        self.finish({"status" : status})
'''