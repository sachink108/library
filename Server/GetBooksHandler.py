import os
import tornado.websocket
import logging
from URIParser import *
from elasticsearch import Elasticsearch

database_dir = "C:\\databases"
users_db = os.path.join(database_dir, "users.db")
gClient = Elasticsearch([{'host': 'localhost', 'port': 9200}])
gElasticIndex = "books"

class GetBooksHandler(tornado.web.RequestHandler):
    def _getCategoryCounts(self, docType):
        self.set_header("Access-Control-Allow-Origin", "*")
        _body = {
            "size": 0,
            "aggs": {
                "distinct_categories": {
                    "terms": {
                        "field": "category.keyword",
                        "size": 1000
                    }
                }
            }
        }
        elasticResp = gClient.search(index=gElasticIndex, doc_type=docType, body=_body)
        catret = []
        for cat in elasticResp["aggregations"]["distinct_categories"]["buckets"]:
            catret.append({'name': cat["key"], 'count': cat["doc_count"]})

    '''
    def _getBooks(self, category, docType):
        self.set_header("Access-Control-Allow-Origin", "*")
        if category == 'recent':
            _body = { "sort": {"timestamp": "asc"}, "size": 5 }
        else:
            _body = {
                "sort": {"timestamp": "asc"},
                "query": {
                    "query_string": {
                        "query": category,
                        "fields": ["category"] # search in this field
                    }
                }
            }
        elasticResp = gClient.search(index=gElasticIndex, doc_type=docType, body=_body)
        ret = {}
        if elasticResp['hits']['total']:
            for book in elasticResp['hits']['hits']:
                if category not in ret: # have to handle multi category
                    ret[category] = []

                #imagePath = book['_source']['image_filepath']
                #imagePath = os.path.relpath(imagePath, database_dir)
                #imagePath.replace("\\", "/")
                ret[category].append({"author": book['_source']['author'],
                                      "title": book['_source']['title'],
                                      #"img": "%s/%s" % (r['user'], row[4]),
                                      "img" : book['_source']['image_filepath']
                                    })
    '''

    def _checkIndexDocTypeMapping(self, docType):
        properties = {"title": {"type": "text"},
                      "author": {"type": "text"},
                      "image_filepath": {"type": "text", "index": "false"},
                      "favourite": {"type": "text" },
                      "current" : {"type": "text"},
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

    def get(self,info):
        self.set_header("Access-Control-Allow-Origin", "*")
        logging.info("GET /getbooks")
        uriparser = URIParser()
        r = uriparser.parse(info)['dict']
        username = r['user']
        category = r['cat']
        print("Getting books for %s of category %s" % (username, category))
        docType=username+gElasticIndex
        self._checkIndexDocTypeMapping(docType)
        #ret = self._getBooks(category, docType) #somehow this is not working
        if category == 'recent':
            _body = { "sort": {"timestamp": "desc"}, "size": 5 }
        elif category == 'favorite':
            _body = {
                "sort": {"timestamp": "desc"},
                "query": {
                    "query_string": {
                        "query": "true",
                        "fields": ["favourite"]  # search in this field
                    }
                }
            }
        elif category == 'current':
            _body = {
                "sort": {"timestamp": "desc"},
                "query": {
                    "query_string": {
                        "query": "true",
                        "fields": ["current"]  # search in this field
                    }
                }
            }
        else:
            _body = {
                "sort": {"timestamp": "desc"},
                "query": {
                    "query_string": {
                        "query": category,
                        "fields": ["category"] # search in this field
                    }
                }
            }
        elasticResp = gClient.search(index=gElasticIndex, doc_type=docType, body=_body)
        ret = {}
        if elasticResp['hits']['total']:
            for book in elasticResp['hits']['hits']:
                if category not in ret: # have to handle multi category
                    ret[category] = []
                #imagePath = book['_source']['image_filepath']
                #imagePath = os.path.relpath(imagePath, database_dir)
                #imagePath.replace("\\", "/")
                ret[category].append({"author": book['_source']['author'],
                                      "title": book['_source']['title'],
                                      "id" : book['_id'],
                                      "img" : book['_source']['image_filepath'],
                                      "favourite" : book['_source']['favourite'],
                                      "current": book['_source']['current']
                                    })
        #catret = self._getCategoryCounts(docType)
        # This part has to be sent everytime? is it necessary? seems so!
        _body = {
            "size": 0,
             "aggs": {
                "distinct_categories": {
                    "terms": {
                        "field": "category.keyword",
                        "size": 1000
                    }
                }
             }
        }
        elasticResp = gClient.search(index=gElasticIndex, doc_type=docType, body=_body)
        catret = []
        for cat in elasticResp["aggregations"]["distinct_categories"]["buckets"]:
            catret.append({'name': cat["key"], 'count': cat["doc_count"]})

        self.write({'status': 'OK',
                    'books': ret,
                    'categories': catret})
