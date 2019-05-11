# -*- coding:UTF-8 -*-
 # load library

import urllib.request
import os



  # image url to download

url = "https://img-api.neople.co.kr/df/items/39181fcc8264aa1bb3efbbfc1125d998"


  # file path and file name to download

outpath = "images/"
outfile = "test.png"


  # Create when directory does not exist

if not os.path.isdir(outpath):

    os.makedirs(outpath)


  # download

urllib.request.urlretrieve(url,  outpath + outfile)

print("complete!")
