""" 
    A module that contains the class for a webcrawler framework
    Which parses the article off of a News website
    By Ian Gomez
"""
from bs4 import BeautifulSoup
import os.path 
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from LinkCrawler import LinkCrawler
import csv
import json
import time
class NetSpider(object):

    link_file = "links.txt"
    link_file_directory = "links/"
    queue_set = set()
    index_url = ""
    article_file = "articles.json"
    geckodriver_path = "/usr/bin/geckodriver"
    
    def __init__(self, spider_id, data_directory,queue_link):
        self.__spider_id = spider_id
        self.__data_directory = data_directory
        self.__queue_link = queue_link
        self.__page_html = self.__getPageHTML(self.__queue_link)
    @property
    def spider_id(self):
        #id of the spider thread
        return self.__spider_id

    @spider_id.setter
    def spider_id(self,spider_id):
        self.__spider_id = spider_id
        
    @property
    def queue_link(self):
        #url of the article that is going to be parsed
        return self.__queue_link

    @property
    def data_directory(self):
        #directory for which the article is to be stored
        return self.__data_directory

    @classmethod
    def startup(cls,wrapper,wrapper_attrs={},a_tag_attrs = {},urlparams={}):
        print(cls)
        print(cls.index_url)
        if(cls.index_url == ""):
            raise ValueError("There is no URL to request from")
        full_filename = cls.link_file_directory + cls.link_file
        if not os.path.exists(cls.link_file_directory):
            os.makedirs(cls.link_file_directory)
        if not os.path.isfile(full_filename):
            f = open(full_filename, 'w')
            f.close()
        LinkCrawler(
                    cls.index_url,\
                    cls.link_file,cls.link_file_directory,
                    cls.geckodriver_path
                    ).export_links(wrapper,wrapper_attrs,a_tag_attrs,urlparams)
        with open(full_filename,'rt') as f:
            for line in f:
                cls.queue_set.add(line.replace('\n',''))
    def __getPageHTML(self,url):
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options, 
                executable_path = NetSpider.geckodriver_path)
        driver.set_page_load_timeout(20)
        driver.get(url) 
        page_html = driver.page_source
        driver.quit()
        return page_html
    
    def _getTitle(self, title_html,title_attrs = {}):
        page_soup = BeautifulSoup(self.__page_html,"lxml")
        title = page_soup.find_all(title_html,attrs = title_attrs)
        return title[0].get_text()
    
    def _getArticle(self,wrapper,body,wrapper_attrs={},body_attrs={}):
        page_soup = BeautifulSoup(self.__page_html,"lxml")
        wrappers = page_soup.find_all(wrapper,attrs=wrapper_attrs)
        body_lst = []
        for wrapper_tag in wrappers:
            body_lst += wrapper_tag.find_all(body,body_attrs)
        body_lst = [tag.get_text() for tag in body_lst] 
        return " ".join(body_lst) 
    
    def _getAuthor(self,author_tag,author_attrs = {}):
        page_soup = BeautifulSoup(self.__page_html,"lxml")
        author_html = page_soup.find_all(author_tag,attrs=author_attrs)
        return author_html[0].get_text() 

if __name__ == "__main__":
    url = "https://www.washingtonpost.com/newssearch/"
    query = {"query":"bitcoin"}
    NetSpider.index_url = url
    NetSpider.startup("div",wrapper_attrs={"class":"pb-feed-headline"},a_tag_attrs={"class":"ng-binding"},urlparams={"query":"bitcoin"})
    print(NetSpider.queue_set)
    spider = NetSpider(1,"data/",NetSpider.queue_set.pop())

