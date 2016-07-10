import string
import csv
import fileinput
import re
import os

from PIL import Image

newpath = 'SLFiles/'
if not os.path.exists(newpath):
    os.makedirs(newpath)

path = os.path.dirname('PreSLFiles/')
count = 1
for spec in os.listdir(path):
    img = Image.open(os.path.join(path, spec))
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] < 60 and item[1] < 60 and item[2] < 60:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    temp = 'A' + '_' + str(count) + '.png'
    #print(temp)
    count +=1
    img.save(os.path.join(newpath, temp), "JPEG")