# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 18:42:05 2018

@author: Melissa
"""

import requests as rs, bs4, re
import time, datetime, random
import urllib
import os
from pathlib import Path

# Create New Folder
def createNewFolder(path):
    if os.path.exists(path):
        print("folder exists")
    else:
        os.mkdir(path)
        print("create folder success")

# Download File
def downloadFile(src_url, destPath):
    filename = src_url.split('/')[-1]
    target_path = destPath / filename
    urllib.request.urlretrieve(src_url, target_path)

# Access URL to get download link    
def getDownloadLink():
    
    # target page URL
    url='https://www.amazon.com/'
    
    # request header
    headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'content-type':'application/x-www-form-urlencoded; charset=UTF-8'
    }
    
    html = rs.get(url, headers = headers)
    html.encoding = 'utf8'
    
    if html.status_code == rs.codes.ok:
        soup = bs4.BeautifulSoup(html.text, 'lxml')
        lst = soup.find_all("img", class_="product-image", src=re.compile("http"))
    elif html.status_code == rs.codes.not_found:
        print("Page Not Found")
    else:
        print("Other status code", html.status_code, sep=": ")
        
    link_list = []
    for obj in lst:
        try:
            src = obj["src"]
            
        except:
            print(obj)
            
        else:
            link_list.append(src)
    
    return link_list

# timestamp
timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')

# dest Path
#destPath = Path("D:/")
destPath = Path(os.getcwd() + "/" + timeStamp)

# Create folder
createNewFolder(destPath)

# do Download
link_list = getDownloadLink()
for link in link_list:
    if link != '':
        downloadFile(link, destPath)
        time.sleep(2 + random.random())
