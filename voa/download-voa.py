# coding: utf-8 
import sys
import argparse
from argparse import ArgumentDefaultsHelpFormatter
from bs4 import BeautifulSoup
import requests
import bs4
import re
import os

import urllib.request
from header.replheader import *
 
#base_url = 'https://www.voanews.com/podcast/?zoneId=6932'
base_arrays = [
               'https://www.voanews.com/podcast/?zoneId=6932',
               'https://www.voanews.com/podcast/?zoneId=6951',
               'https://www.voanews.com/podcast/?zoneId=5082',
               'https://www.voanews.com/podcast/?zoneId=1469'
              ]

def downloadFiles(url,filename):
    if url == None: 
        return

    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename,'wb') as f:
                f.write(response.content)
                f.close()
        return None
    except requests.exceptions.RequestException:
        return None  

#
# get html content
#
def get_html(url):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        return None
    except requests.exceptions.RequestException:
        return None     

def parseHtml(html,filename):
    bStart = False
    urls = re.findall(r'url="([a-zA-z]+://[^\s]*)"', str(html))
    for url in urls:
        name = url[url.rfind('/')+1:]

        if name in dict_rep:
            continue
    
        path = 'e:/voa/' + name
        if os.path.exists(path) == False:
            downloadFiles(url,path)
            print(url)
"""
    soup = BeautifulSoup(html, 'lxml')
    titles = soup.select('channel > item')
    for n in titles:
        encls = n.find_all('enclosure')
        if encls != None:
            print(str(encls))
"""            


def getAllMp3():
    filename = 'cradiointer'   
    for url in base_arrays:
        print(url+'\n')    
        html = get_html(url)
        if html != None :
            parseHtml(html,filename)

def main():
    getAllMp3()
 
if __name__ == "__main__":
    main()