import os
import sys
import uuid
import json
import tornado.web
import logging
from URIParser import *
from elasticsearch import Elasticsearch

database_dir = "C:\\databases"
gClient = Elasticsearch([{'host': 'localhost', 'port': 9200}])
gElasticIndex = "books"

class UpdateBookHandler(tornado.web.RequestHandler):
    def post(self, info):
        self.set_header("Access-Control-Allow-Origin", "*")
        logging.info("POST /update")
        uriparser = URIParser()
        r = uriparser.parse(info)['dict']
        username = r['user']
        book_id = r['book_id']
        field = r['field']
        value = r['value']
        print (field + "\t" + value)
        _body = {
            "doc": {
                field: value
            }
        }
        docType = username + gElasticIndex
        elasticResp = gClient.update(index=gElasticIndex, doc_type=docType, body=_body, id=book_id)
        print(elasticResp)
        self.finish({"status": "OK", "resp": elasticResp})
