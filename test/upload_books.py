import os
import sys
import requests

database_dir = "C:\\databases"

url = 'http://localhost:9000/addbook'
'''
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

images_dir = "c:\\databases\sachin\\bkup"
for cat in catWiseBooks:
    print (cat)
    for book in catWiseBooks[cat]:
        payload = { 'username': 'sachin',
                    'title': book['title'], 
                    'author': book['author'],
                    'category' : cat
                  } 
        image_file = os.path.join(images_dir, book['img'])
        files = {'0': open(image_file, 'rb')}
        print ("Sending book")
        r = requests.post("http://localhost:9000/addbook", data=payload, files=files)
        print (r)
        input()
