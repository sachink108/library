import os,fnmatch
import sys
from PIL import Image
from pytesseract import image_to_string


imgdir = "c:\databases\sachin"

files = os.listdir(imgdir)

for file in fnmatch.filter(os.listdir(imgdir), '*.jpeg'):
    filepath = os.path.join(imgdir, file)
    imagetext = image_to_string(Image.open(filepath))
    print (filepath + "=>" + imagetext)

#print (pytesseract.image_to_string(Image.open(imgfile)))
