"""
    A module that contains the class for a webcrawler which finds all the Article 
    links on an HTML page
    
    Usage:
        $python LinkCrawler.py
    By Ian Gomez
"""
from math import ceil
import os.path
import sys
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options

class LinkCrawler(object):
    """
        Args:
            index_url(str):The str that contains the url where to query
            filename(str):The file where the url for the article to be
                          parsed will be found  
            dirname(str):The directory name where the file specified in
                         filename will be saved
            geckodriver_path(str):The path for the Firefox webdriver
    """
    def __init__(self,index_url,filename,dirname,geckodriver_path):
        self.__index_url = index_url
        self.__filename = filename
        self.__dirname = dirname
        self.__geckodriver_path = geckodriver_path
        
    @property
    def index_url(self):
        #The str that contains the url where to query
        return self.__index_url

    @index_url.setter
    def index_url(self,index_url):
        self.__index_url = index_url
        self.export_links()

    @property
    def filename(self):
        #The file where the url for the article to be parsed will be found  
        return self.__filename

    @filename.setter
    def filename(self,filename):
        self.__filename = filename
        self.export_links()

    @property
    def dirname(self):
        #The directory name where the file specified in filename will be saved
        return self.__dirname

    @dirname.setter
    def dirname(self):
        return self.__dirname
        self.export_links()

    @property
    def full_filename(self):
        #the full filename for where the article links will be saved
        if self.__dirname == '/':
            return self.__filename
        return self.__dirname + self.__filename
    
    def __getPageHTML(self,url):
        """
            Args:
                url(str):The url that contains links which need to be parsed
            Returns:
                page(str): A string that contains the html data of the webpage
    
            This function takes in a url and outputs the html of the page
        """ 
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options, 
        executable_path = self.__geckodriver_path)
        driver.set_page_load_timeout(20)
        try:
            driver.get(url) 
        except TimeoutException as e:
            driver.quit()
            print("Error %s" % e) 
            sys.exit(1)
        page = driver.page_source
        driver.quit()
        return page

    def __constructFullURL(self,urlparams):
        """
            Args:
                urlparams(dict):The query parameters to be placed in the url
            Returns:
                fullurl(str):The url formatted to contain the url params

            This function takes in query parameters for a url and returns
            the url string that make a GET request using those parameters
        """
        if(urlparams == {}):
            return self.__index_url
        fullurl = self.__index_url if (self.__index_url[-1] == "/") else self.__index_url + "/"
        fullurl += "?"
        for key,value in urlparams.items():
            fullurl += key + "=" + value + "&" 
        return fullurl[:-1] 

    def __get_links(self,wrapper,wrapper_attrs,a_tag_attrs,urlparams):
        """
            Args:
                wrapper(str): The html tag for the tag that wraps around
                              the <a> tag to be selected
                wrapper_attrs(dict): The different tag attributes for the 
                                     wrapper
                a_tag_attrs(dict): The different tag attribute for the <a> tag
                urlparams(dict): The query parameters for the url
            Returns:
                links_set(set): A set that contains all the article links 

                This function takes in a wrapper tag, the wrapper tag's 
                attributes the a tag's attributes and the url query parameters,
                and returns all the links that are in the html page
        """
        a_tag_list = []
        fullURL = self.__constructFullURL(urlparams)
        index_page = self.__getPageHTML(fullURL)
        links_set = set()
        index_page_soup = BeautifulSoup(index_page,"lxml")
        wrapper_lst = index_page_soup.find_all(wrapper,attrs=wrapper_attrs)
        for a_tag in wrapper_lst: 
            a_tag_list += a_tag.find_all("a",attrs = a_tag_attrs)
        for a_tag in a_tag_list:
            link_url = urljoin(self.__index_url, a_tag.get('href'))
            links_set.add(link_url)
        return links_set

    def export_links(self,wrapper,wrapper_attrs={},a_tag_attrs={},urlparams={}):
        """
             Args:
                wrapper(str): The html tag for the tag that wraps around
                              the <a> tag to be selected
                wrapper_attrs(dict): The different tag attributes for the 
                                     wrapper
                a_tag_attrs(dict): The different tag attribute for the <a> tag
                urlparams(dict): The query parameters for the url
                
                This function takes in the parameters used to parse
                the article links and writes them to a file specified
                by dirname/filename.txt
        """  
        links_set = self.__get_links(wrapper,wrapper_attrs, a_tag_attrs,urlparams)
        if not os.path.exists(self.__dirname):
            os.makedirs(self.__dirname)
        f = open(self.full_filename,'w')
        f.write('\n'.join(links_set))
        f.close()

    def append_links(self,a_tag_attrs={},urlparams={}):
        links_set = self.__get_links(a_tag_attrs,urlparams)
        if not os.path.exists(self.__dirname):
            os.makedirs(self.__dirname)
        if not os.path.isfile(self.__filename):
            f = open(self.full_filename, "w")
            f.close()
        f = open(self.full_filename, "a")
        f.write('\n'.join(links_set))
        f.close()

    def readLinksAsSet(self):
        """
            Returns:
                links_set(set): A list of links to articles to be parsed

            This function uses the file specified by dirname/filename.txt
            and reads all the links in the file and exports them as a list
        """
        f = open(self.full_filename,"r")
        links_set = set()
        for line in f:
            links_set.add(line.replace('\n',''))
        f.close()
        return links_set

if __name__ == "__main__":
    url = "https://www.washingtonpost.com/newssearch/"
    crawler = LinkCrawler(url,"links.txt","links/","/usr/bin/geckodriver") 
    crawler.export_links("div",wrapper_attrs={"class":"pb-feed-headline"},a_tag_attrs={"class":"ng-binding"},urlparams={"query":"bitcoin"})
