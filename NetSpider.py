""" 
    A module that contains the class for a webcrawler framework
    Which parses the article off of a News website
    
    Usage:
        $python NetSpider.py

    By Ian Gomez
"""
import json
import os.path 
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from LinkCrawler import LinkCrawler
class NetSpider(object):
    """
        Args:
            spider_id(int): Id for the spider (which is used for threading)
            data_directory(str): Directory where to store the json articles
            queue_link(str): Link for the article to scrape
    """
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
        """
            Args:
                wrapper(str): The html tag for the tag that wraps around
                              the <a> tag to be selected
                wrapper_attrs(dict): The different tag attributes for the 
                                     wrapper
                a_tag_attrs(dict): The different tag attribute for the <a> tag
                urlparams(dict): The query parameters for the url
                
            This function takes in all the parameters required to parse
            the article links on a website and then adds each article
            to a set. Thus readying the NetSpider for gathering
            News articles.
        """  
        if(cls.index_url == ""):
            raise ValueError("There is no URL to request from")
        full_filename = cls.link_file_directory + cls.link_file
        crawler = LinkCrawler(
                    cls.index_url,\
                    cls.link_file,cls.link_file_directory,
                    cls.geckodriver_path
                    )
        crawler.export_links(wrapper,wrapper_attrs,a_tag_attrs,urlparams)
        cls.queue_set = crawler.readLinksAsSet()

    def __getPageHTML(self,url):
        """
            Args:
                url(str): url for the article that is going to be parsed
            Returns:
                page_html(str): The html for the inserted news article
            
        """
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options, 
                executable_path = NetSpider.geckodriver_path)
        driver.set_page_load_timeout(20)
        try:
            driver.get(url) 
        except TimeoutException as e:
            driver.quit()
            print("Error %s" % e) 
            sys.exit(1)
        page_html = driver.page_source
        driver.quit()
        return page_html
    
    def _getTitle(self, title_html,title_attrs = {}):
        """
            Args: 
                title_html(str): html tag for the article title
                title_attrs(dict): tag attributes for the article title
            Returns:
                title_text(str): The text inside of the specified html tag
            
        """
        page_soup = BeautifulSoup(self.__page_html,"lxml")
        title = page_soup.find_all(title_html,attrs = title_attrs)
        return title[0].get_text()
    
    def _getArticle(self,wrapper,body,wrapper_attrs={},body_attrs={}):
        """
            Args:
                wrapper(str): HTML tag for the article body wrapper
                body(str): HTML tag for the article
                wrapper_attrs(dict): Tag attributes for the body wrapper
                body_attrs(dict): Tag attributes for the article
            Returns:
                article_str(str): The string that contains the article text
        """
        page_soup = BeautifulSoup(self.__page_html,"lxml")
        wrappers = page_soup.find_all(wrapper,attrs=wrapper_attrs)
        body_lst = []
        for wrapper_tag in wrappers:
            body_lst += wrapper_tag.find_all(body,body_attrs)
        body_lst = [tag.get_text() for tag in body_lst] 
        return " ".join(body_lst) 
    
    def _getAuthor(self,author_tag,author_attrs = {}):
        """
            Args:
                author_tag(str): HTML tag that contains the author
                author_attrs(dict): Tag attributes for the author tag
            Returns:
                author_name(str):Author's Name
        """
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

