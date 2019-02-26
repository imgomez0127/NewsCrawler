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
    index_url = ""
    article_file = "articles.json"
    query = {}
    geckodriver_path = "/usr/bin/geckodriver"

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
    def startup(wrapper,wrapper_attrs={},a_tag_attrs = {},urlparams={}):
        if(NetSpider.index_url == ""):
            raise ValueError("There is no URL to request from")
        full_filename = NetSpider.link_file_directory + NetSpider.link_file
        if not os.path.exists(NetSpider.link_file_directory):
            os.makedirs(NetSpider.link_file_directory)
        if not os.path.isfile(full_filename):
            f = open(full_filename, 'w')
            f.close()
        LinkCrawler(
                    NetSpider.index_url,\
                    NetSpider.link_file,NetSpider.link_file_directory,
                    NetSpider.geckodriver_path
                    ).export_links(wrapper,wrapper_attrs,a_tag_attrs,urlparams)
        with open(full_filename,'rt') as f:
            for line in f:
                NetSpider.queue_set.add(line.replace('\n',''))

    def __getPageHTML(self,url):
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options, 
                executable_path = NetSpider.geckodriver_path)
        driver.set_page_load_timeout(20)
        driver.get(url) 
        page = driver.page_source
        driver.quit()
        return page

    def crawl_page(self,title_html_tags,body_html_tags,title_attrs = {}, 
                    body_attrs = {}):
        page = self.__getPageHTML(self.__queue_link)
        page_soup = BeautifulSoup(page,"lxml")
        title = page_soup.find_all(title_html_tags,attrs = title_attrs)
        body = page_soup.find_all(body_html_tags,body_attrs)
        article = ""
        for tag in body:
            article += tag.get_text()        
        print(article)
        if(title == []):
            raise ValueError("The title has no values returned") 
        if(body == []):
            raise ValueError("The body has no values returned")
        dataJson = json.dumps({"title": title[0].get_text(), "article":article})
        return dataJson 

    def getArticleAsJSON(self,title_html_tags,body_html_tags,title_attrs = {},
                        body_attrs = {}):
        jsonData = self.crawl_page(title_html_tags,body_html_tags,
                                    title_attrs,body_attrs) 
        return jsonData                
    
if __name__ == "__main__":
    url = "https://www.washingtonpost.com/newssearch/"
    query = {"query":"bitcoin"}
    NetSpider.index_url = url
    NetSpider.startup("div",wrapper_attrs={"class":"pb-feed-headline"},a_tag_attrs={"class":"ng-binding"},urlparams={"query":"bitcoin"})
    print(NetSpider.queue_set)
    spider = NetSpider(1,"data/",NetSpider.queue_set.pop())
    print(json.loads(spider.crawl_page("h1","p",title_attrs = {"itemprop":"headline"})))
