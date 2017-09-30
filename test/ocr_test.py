from PIL import Image
import pytesseract

'''
#http://stackoverflow.com/questions/21955465/ocr-doesnt-recognize-phone-numbers-with-the-sign
from PIL import Image
from pyocr import pyocr
import pyocr.builders
import cStringIO
import os
os.putenv("TESSDATA_PREFIX", "/usr/share/tesseract-ocr/")
tools = pyocr.get_available_tools()
tool = tools[0]
langs = tool.get_available_languages()
lang = langs[0]
file = "test.png"
txt = tool.image_to_string(Image.open(file),
                           lang=lang,
                            builder=pyocr.builders.TextBuilder())
print txt
'''
imgfile = "C:/Users/sachinsk/Documents/personal/progs/library/Server/test.jpeg"
print (pytesseract.image_to_string(Image.open(imgfile)))
