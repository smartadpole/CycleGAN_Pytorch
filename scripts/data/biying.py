#!/usr/bin/python3 python
# encoding: utf-8
'''
@author: 孙昊
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: smartadpole@163.com
@file: biying.py
@time: 19-5-8 下午4:24
@desc: 
'''
import sys, os

CURRENT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(CURRENT_DIR, '../../'))

import os
import re
import urllib.request

import requests


def get_one_page(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if (response.status_code == 200):
        return response.text
    return None


def download(url, filename):
    dst = "/media/hao/DS/OTHER/CODE/GAN/CycleGAN/Pytorch/pytorch-CycleGAN-and-pix2pix/datasets/horse"
    filepath = os.path.join(dst, filename + '.jpg')
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    if os.path.exists(filepath):
        return
    with open(filepath, 'wb')as f:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        f.write(response.read())


def parse(html):
    pattern = re.compile('data-progressive="(.*?)".*?<h3>(.*?)</h3>')
    items = re.findall(pattern, html)
    for item in items:
        try:
            url = item[0].replace('800', '1920').replace('480', '1080')
            imagename = item[1].strip()
            rule = re.compile(r'[a-zA-z1-9()-/]')
            imagename = rule.sub('', imagename)
            download(url, imagename.strip())
            print(imagename, "正在下载")
        except Exception:
            continue


if __name__ == '__main__':
    for page in range(1, 97):
        url = 'https://bing.ioliu.cn/ranking?p=' + str(page)
        print("Page", page, " ", url)
        html = get_one_page(url)
        parse(html)


def main():
    pass


if __name__ == '__main__':
    main()