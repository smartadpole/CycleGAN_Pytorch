#!/usr/bin/python3 python
# encoding: utf-8
'''
@author: 孙昊
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: smartadpole@163.com
@file: spider.py
@time: 19-5-7 下午6:38
@desc: 
'''
import sys, os

CURRENT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(CURRENT_DIR, '../../'))

import argparse
import requests
import re
import urllib.request
from tqdm import tqdm

import requests
import urllib.request
from bs4 import BeautifulSoup
import os
import time

import re
import requests
import urllib

def getArgs():
    parser = argparse.ArgumentParser(description="",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--url", type=str, help="url")
    parser.add_argument("--dir", type=str, default="",
                        help="")

    args = parser.parse_args()
    return args

def getImgs(url):
    # response = urllib.request.urlopen(args.url).read().decode('utf-8')
    # items = re.findall('src="(.+?\.jpg)" pic_ext', response)
    # urllib.request.urlretrieve(item, file.format(image_num))

    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)  # overcome access restrictions
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('img')

    # items = re.findall('"objURL":"(.*?)",', response.text, re.S)

    return items

def main():
    args = getArgs()
    if not os.path.exists(args.dir):
        os.makedirs(args.dir)

    items = getImgs(args.url)
    image_num = 0
    headers = {'User-Agent': 'Mozilla/5.0'}

    for item in tqdm(items):
        image_num += 1

        try:
            img_request = urllib.request.Request(item, headers)
            fwws = urllib.request.urlopen(img_request, timeout=300)
            file = os.path.join(args.dir, "{}_{}".format(image_num, item.split("/")[-1]))

            with open(file, 'wb') as file:  # write image in byte
                file.write(fwws.read())
                # file.flush()
            file.close()

        except requests.exceptions.ConnectionError:
            continue

    print("end")




if __name__ == '__main__':
    main()