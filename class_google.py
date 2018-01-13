# -*- coding:utf-8 -*-
import requests
import time

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import argparse
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from multiprocessing import Pool
from lxml.html import fromstring
import os, sys

class Collector:

    def __init__(self):
        self.ua = UserAgent()
        self.collect = []
        self.error_list = []

    def search(self, url):
        print("Search Result..")
        # Create a browser
        dir = '/Users/tw/Desktop/chromedriver'
        browser = webdriver.Chrome(dir)

        # Open the link
        browser.get(url)
        time.sleep(1)

        element = browser.find_element_by_tag_name("body")

        # # Scroll down
        for i in range(1):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)

        time.sleep(1)

        # Get page source and close the browser
        source = browser.page_source
        browser.close()

        return source

    def download(self, collects, dir='/'):
        print("Download Image..")
        if not dir.endswith("/"):
            dir += '/'


        for i in range(len(collects)):
            print("%d/%d"%(i, len(collects)))
            col = collects[i]
            if (col == '알림'):
                pass
            else:
                full_name = str(collects.index(col)) + ".jpg"
                save_path = os.path.join(dir, full_name)  # 저장폴더
                try:
                    urllib2.urlretrieve(col, save_path)
                except:
                    self.error_list.append(col)
                    pass

    def download_image(self, link):
        # Use a random user agent header
        headers = {"User-Agent": self.ua.random}
        # Get the image link
        try:
            r = requests.get("https://www.google.com" + link.get("href"), headers=headers)
        except:
            print("Cannot get link.")
        title = str(fromstring(r.content).findtext(".//title"))
        link = title.split(" ")[-1]
        self.collect.append(link)
        # Download the image

    def collectImage(self, keyword):
        url = "https://www.google.com/search?as_st=y&tbm=isch&as_q=" + keyword + \
              "&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=isz:lt,islt:svga,itp:photo,ift:jpg"
        source = self.search(url)

        # Parse the page source and download pics
        soup = bs(str(source), "html.parser")
        links = soup.find_all("a", class_="rg_l")
        print("%d개 이미지가 검색됨"%len(links))

        if not os.path.isdir(keyword):
            os.makedirs(keyword)

        dir = os.getcwd() + "/" + str(keyword)
        os.chdir(dir)
        print(dir)

        print("Collect Image URL..")
        for link in links:
            self.download_image(link)

        # print(collect)
        self.download(self.collect, dir)