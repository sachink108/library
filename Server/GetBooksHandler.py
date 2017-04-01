import os
import sys
import json
import time
import requests
import tornado.ioloop
import tornado.web
import tornado.websocket
import logging
import sqlite3
from URIParser import *

database_dir = "C:\\databases"
users_db = os.path.join(database_dir, "users.db")

class GetBooksHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        logging.info("GET /getbooks")
        # receiver category later
        global users_db
        
        recent = { 'recent' :[
                    {"author" : "Lee Child",
                     "title" : "The Visitor",
                     "img": "sachin/f866bc97-3068-488d-b48f-22cf6007a203.jpg"
                    },
                    {"author" : "Stephen Hawkin",
                     "title" : "A Brief History of Time",
                          "img": "sachin/a-brief-history-of-time-original-imadxzr6ygdrtzpf.jpeg"
                        },
                        {"author" : "Kuldip Nayar",
                         "title" : "Life Without Fear",
                         "img": "sachin/without-fear-the-life-trial-of-bhagat-singh-original-imad6szctheuchsh.jpeg"
                        },
                        {"author" : "Paramahamsa Yogananda",
                         "title" : "Autobiography of a Yogi",
                         "img": "sachin/autobiography-of-a-yogi-original-imadryp23yqgfjyz.jpeg"
                        },
                        {"author" : "B K S Iyengar",
                         "title" : "Light on Yoga",
                         "img": "sachin/light-on-yoga-original-imadgawzy6tys8hp.jpeg"
                        },
                        {"author" : "Rujuta Diwekar",
                         "title" : "Don't Lose Your Mind, Lose Your Weight",
                         "img": "sachin/don-t-lose-your-mind-lose-your-weight-original-imaeqcgmmzyg27qk.jpeg"
                        }
                      ] 
                    };
        catWiseBooks = {
                        "Action": [
                                {"author" : "Lee Child",
                                "title" : "The Visitor",
                                "img": "sachin/f866bc97-3068-488d-b48f-22cf6007a203.jpg"
                                },
                                {"author" : "Sidney Sheldon",
                                "title" : "Master of the Game",
                                "img": "sachin/0576b851-89b6-4d82-ae3a-8b28d53613fd.jpg"
                                },
                                {"author" : "Agatha Christie",
                                "title" : "And There Were None",
                                "img": "sachin/and-then-there-were-none-original-imadat8yqkjjftxt.jpeg"
                                },
                                {"author" : "Lee Child",
                                "title" : "Echo Burning",
                                "img": "sachin/echo-burning-original-imadgmgsynzunmug.jpeg"
                                },
                                {"author" : "Lee Child",
                                "title" : "Killing Floor",
                                "img": "sachin/killing-floor-original-imaenf7htjntettw.jpeg"
                                },
                                {"author" : "Lee Child",
                                "title" : "Never Go Back",
                                "img": "sachin/never_go_back.jpg"
                                },
                            ],
                       "Biography": [
                                {"author" : "Stephen Hawkin",
                                "title" : "A Brief History of Time",
                                "img": "sachin/a-brief-history-of-time-original-imadxzr6ygdrtzpf.jpeg"
                                },
                                {"author" : "Andy Marino",
                                "title" : "Narendra Modi - A Political Biography",
                                "img": "sachin/narendra-modi-a-political-biography-original-imae27kczeehwyxz.jpeg"
                                },
                                {"author" : "A P J Abdul Kalam",
                                "title" : "Turning Points",
                                "img": "sachin/turning-points-a-journey-through-challanges-original-imaehzburu3vecqe.jpeg"
                                },
                                {"author" : "Kuldip Nayar",
                                "title" : "Life Without Fear",
                                "img": "sachin/without-fear-the-life-trial-of-bhagat-singh-original-imad6szctheuchsh.jpeg"
                                },
                                {"author" : "Jon Krakuer",
                                "title" : "Into the Wild",
                                "img": "sachin/into-the-wild-original-imad8bzvqzy5rfsp.jpeg"
                                },
                            ],
                       "Spiritual" : [
                                {"author" : "Paramahamsa Yogananda",
                                "title" : "Autobiography of a Yogi",
                                "img": "sachin/autobiography-of-a-yogi-original-imadryp23yqgfjyz.jpeg"
                                },
                                {"author" : "Sadhguru",
                                "title" : "More than a life",
                                "img": "sachin/sadhguru-more-than-a-life-pb-original-imadpv45eycrgngz.jpeg"
                                },
                                {"author" : "Om Swami",
                                "title" : "If Truth Be Told",
                                "img": "sachin/if-truth-be-told-original-imaeyvpuufsarhez.jpeg"
                                },
                       ],
                       "Health and Fitness" : [
                                {"author" : "B K S Iyengar",
                                "title" : "Light on Yoga",
                                "img": "sachin/light-on-yoga-original-imadgawzy6tys8hp.jpeg"
                                },
                                {"author" : "Rujuta Diwekar",
                                "title" : "Don't Lose Your Mind, Lose Your Weight",
                                "img": "sachin/don-t-lose-your-mind-lose-your-weight-original-imaeqcgmmzyg27qk.jpeg"
                                },
                       ],
         };
            
        self.write({'catWiseBooks' : catWiseBooks,
                    'recent' : recent
                    })
