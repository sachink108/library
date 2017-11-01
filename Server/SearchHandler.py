import os
import tornado.websocket
import logging
import sqlite3
from URIParser import *
from elasticsearch import Elasticsearch

database_dir = "C:\\databases"
users_db = os.path.join(database_dir, "users.db")
gClient = Elasticsearch([{'host': 'localhost', 'port': 9200}])
gElasticIndex = "books"

class SearchHandler(tornado.web.RequestHandler):
    def get(self, info):
        self.set_header("Access-Control-Allow-Origin", "*")
        logging.info("GET /search")
        uriparser = URIParser()
        r = uriparser.parse(info)['dict']
        username = r['user']
        query_string = r['query_string']
        print("Searching for %s of category " % (query_string))
        docType = username + gElasticIndex
        _body = {
                "sort": {"timestamp": "desc"},
                "query": {
                    "query_string": {
                        "query": query_string,
                    }
                }
            }
        elasticResp = gClient.search(index=gElasticIndex, doc_type=docType, body=_body)
        ret = []
        if elasticResp['hits']['total']:
            for book in elasticResp['hits']['hits']:
                ret.append({"author": book['_source']['author'],
                                      "title": book['_source']['title'],
                                      "img": book['_source']['image_filepath'],
                                      })
        self.write({'books': ret})