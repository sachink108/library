# make sure ES is up and running
import requests
import os
import sys
import uuid
import base64
import json
from elasticsearch import Elasticsearch

''''
payload = { 'username': 'test', 
            'title': 'test_title', 
            'author': 'test_author',
            'category' : 'test_category',
          }
c2cf9258-7418-4a7e-b8ea-e22535eda898
image_file = os.path.join(database_dir, 'f866bc97-3068-488d-b48f-22cf6007a203.jpg')

files = {'0': open(image_file, 'rb')}
'''
catWiseBooks = {
                "Action": [
                            {"author" : "Lee Child",
                             "title" : "The Visitor",
                             "img": "f866bc97-3068-488d-b48f-22cf6007a203.jpg"
                            },
                            {"author" : "Sidney Sheldon",
                             "title" : "Master of the Game",
                             "img": "0576b851-89b6-4d82-ae3a-8b28d53613fd.jpg"
                            },
                                {"author" : "Agatha Christie",
                                "title" : "And There Were None",
                                "img": "and-then-there-were-none-original-imadat8yqkjjftxt.jpeg"
                                },
                                {"author" : "Lee Child",
                                "title" : "Echo Burning",
                                "img": "echo-burning-original-imadgmgsynzunmug.jpeg"
                                },
                                {"author" : "Lee Child",
                                "title" : "Killing Floor",
                                "img": "killing-floor-original-imaenf7htjntettw.jpeg"
                                },
                                {"author" : "Lee Child",
                                "title" : "Never Go Back",
                                "img": "0f96e5f9-4cdc-49fe-85c4-dac6c973539e.jpg"
                                },
                            ],
                       "Biography": [
                                {"author" : "Stephen Hawkin",
                                "title" : "A Brief History of Time",
                                "img": "a-brief-history-of-time-original-imadxzr6ygdrtzpf.jpeg"
                                },
                                {"author" : "Andy Marino",
                                "title" : "Narendra Modi - A Political Biography",
                                "img": "narendra-modi-a-political-biography-original-imae27kczeehwyxz.jpeg"
                                },
                                {"author" : "A P J Abdul Kalam",
                                "title" : "Turning Points",
                                "img": "turning-points-a-journey-through-challanges-original-imaehzburu3vecqe.jpeg"
                                },
                                {"author" : "Kuldip Nayar",
                                "title" : "Life Without Fear",
                                "img": "without-fear-the-life-trial-of-bhagat-singh-original-imad6szctheuchsh.jpeg"
                                },
                                {"author" : "Jon Krakuer",
                                "title" : "Into the Wild",
                                "img": "into-the-wild-original-imad8bzvqzy5rfsp.jpeg"
                                },
                            ],
                       "Spiritual" : [
                                {"author" : "Paramahamsa Yogananda",
                                "title" : "Autobiography of a Yogi",
                                "img": "autobiography-of-a-yogi-original-imadryp23yqgfjyz.jpeg"
                                },
                                {"author" : "Sadhguru",
                                "title" : "More than a life",
                                "img": "sadhguru-more-than-a-life-pb-original-imadpv45eycrgngz.jpeg"
                                },
                                {"author" : "Om Swami",
                                "title" : "If Truth Be Told",
                                "img": "if-truth-be-told-original-imaeyvpuufsarhez.jpeg"
                                },
                       ],
                       "Health and Fitness" : [
                                {"author" : "B K S Iyengar",
                                "title" : "Light on Yoga",
                                "img": "light-on-yoga-original-imadgawzy6tys8hp.jpeg"
                                },
                                {"author" : "Rujuta Diwekar",
                                "title" : "Don't Lose Your Mind, Lose Your Weight",
                                "img": "don-t-lose-your-mind-lose-your-weight-original-imaeqcgmmzyg27qk.jpeg"
                                },
                       ],
         };

res = requests.get('http://localhost:9200')
#print(res.content)
#exit(1)
images_dir = "c:\\databases\sachin\\bkup"
client = Elasticsearch([{'host': 'localhost', 'port':9200}])

_id = 0
elasticIndex = 'books'
doc_type = 'sachinbooks'
user = "sachin"

def addBooks():
    if client.indices.exists(index="books"):
        if client.indices.exists_type(index="books", doc_type=user+".books"):
            print ("index and mapping both exist") #add content
        else:
            print ("index exists, adding mapping")
            request_body = {
                    user+".books": {
                        "properties": {
                            "title": {"type": "string"},
                            "author": {"type": "string"},
                            "category": {"type": "list"},
                            "image": {"type": "string", "index": "no"},
                            "date_added": {"type": "string"}
                        }
                }
            }
            client.indices.put_mapping(index="books", doc_type="sachin.books", body=request_body)
    else: #index does not exist, create index and mapping
        print("Adding index and mapping")
        request_body = {
            "settings": {
                "number_of_shards": 5,
                "number_of_replicas": 1
            },
            'mappings': {
                user+".books": {
                    "properties": {
                        "title": {"type": "string"},
                        "author": {"type": "string"},
                        "image": {"type": "string", "index": "no"},
                        "date_added": {"type": "string"}
                    }
                }}
        }
        client.indices.create(index='books', body=request_body)

    return
    for cat in catWiseBooks:
        print (cat)
        for book in catWiseBooks[cat]:
            image_file = os.path.join(images_dir, book['img'])
            with open(image_file, "rb") as imageFile:
                rawImage = base64.b64encode(imageFile.read())

            _body = {'id': 'f00b5f7c17534d22ab5cfb950bea972c',
                     'image': str(rawImage),
                     'username': 'sachin',
                     'title': book['title'],
                     'author': book['author'],
                     'category': cat,
                     }
            elasticResp = client.index(index=elasticIndex, doc_type=doc_type, id=_id, body=_body)
            print (elasticResp)
            _id = _id + 1

def getBooks():
    _body = {
                "query": {
                    "match": {
                        "author" : "Lee Child"
                    }
                }
            }
    _body = {
        "sort": {"timestamp": "asc"},
        "size": 5
    }
    _body = {
        "sort": {"timestamp": "asc"},
        "query": {
            "query_string": {
                "query": "crime,drama",
                "fields": ["category"]
            }
        }
    }

    database_dir = "C:\\databases"
    elasticResp = client.search(index=elasticIndex, doc_type=doc_type, body=_body)
    print(elasticResp)
    if (elasticResp['hits']['total']):
        for book in elasticResp['hits']['hits']:
            print (book)
            print (book['_source']['title'])
            imagePath = book['_source']['image_filepath']
            print (os.path.relpath(imagePath, database_dir))
            print(imagePath)
            imagePath.replace(database_dir, '')
            print (imagePath)

            # get count of all categories (not handling multi category
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
    elasticResp = client.search(index=elasticIndex, doc_type=doc_type, body=_body)
    print (elasticResp)
    for cat in elasticResp["aggregations"]["distinct_categories"]["buckets"]:
        print (cat["key"] + "\t" + str(cat["doc_count"]))

def search():
    _body = {
        "sort": {"timestamp": "asc"},
        "query": {
            "query_string": {
                "query": "lee"
            }
        }
    }
    elasticResp = client.search(index=elasticIndex, doc_type=doc_type, body=_body)
    if (elasticResp['hits']['total']):
        for book in elasticResp['hits']['hits']:
            print (book)

def update():
    _body = {
        "doc": {
            "favourite": False
        }
    }
    elasticResp = client.update(index=elasticIndex, doc_type="sachinbooks", body=_body, id="AV73l6og5hb-It3wc-3b")


#addBooks()
#getBooks()
#search()
update()


