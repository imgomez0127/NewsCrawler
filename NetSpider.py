""" 
A module that contains the class for a webcrawler which finds all the CryptoCurrency data hosted on coinmarketcap
    By Ian Gomez
"""
from bs4 import BeautifulSoup
import os.path
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from LinkCrawler import LinkCrawler
import csv
import json

class NetSpider(object):

    link_file = "links.txt"
    link_file_directory = "links/"
    queue_set = set()
    article_count = 1
    index_url = ""
    article_file = "articles.json"
    query = {}
    geckdriver_path = "/usr/bin/geckodriver"
    def __init__(self, spider_id, data_directory,queue_link):
        self.__spider_id = spider_id
        self.__data_directory = data_directory
        self.__queue_link = queue_link
    @property
    def spider_id(self):
        return self.__spider_id

    @spider_id.setter
    def spider_id(self,spider_id):
        self.__spider_id = spider_id
        
    @property
    def queue_link(self):
        return self.__queue_link

    @property
    def data_directory(self):
        return self.__data_directory

    @staticmethod
    def startup(articles_per_page,a_tag_attrs = {}):
        if(NetSpider.index_url == ""):
            raise ValueError("There is no URL to request from")
        full_filename = NetSpider.link_file_directory + NetSpider.link_file
        if not os.path.exists(NetSpider.link_file_directory):
            os.makedirs(NetSpider.link_file_directory)
        if not os.path.isfile(full_filename):
            f = open(full_filename, 'w')
            f.close()
        LinkCrawler(
                    NetSpider.index_url,NetSpider.article_count,\
                    NetSpider.link_file,NetSpider.link_file_directory,
                    NetSpider.geckodriver_path,NetSpider.query
                    ).export_links(articles_per_page,a_tag_attrs)
        with open(full_filename,'rt') as f:
            for line in f:
                NetSpider.queue_set.add(line.replace('\n',''))

    def crawl_page(self,title_html_tags,body_html_tags,title_attrs = {}, body_attrs = {}):
        page = requests.get(self.__queue_link)
        page_soup = BeautifulSoup(page.text,"lxml")
        title = page_soup.find_all(title_html_tags,attrs = title_attrs) 
        body = page_soup.find_all(body_html_tags,body_attrs) 
        if(title == []):
            raise ValueError("The title has no values returned")  
        if(body == []):
            raise ValueError("The body has no values returned")
        dataJson = json.dumps({"title": title, "body":body})
        return dataJson 

    def getArticleAsJSON(self,title_html_tags,body_html_tags,title_attrs = {},
                    body_attrs = {}):
        jsonData = self.crawl_page(title_html_tags,body_html_tags,
                                    title_attrs,body_attrs) 
        return jsonData                
    
