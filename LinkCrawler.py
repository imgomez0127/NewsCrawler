"""
    A module that contains the class for a webcrawler which finds all the Article 
    links on the News Site page
"""
from bs4 import BeautifulSoup
import os.path
from math import ceil
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from urllib.parse import urljoin
import time
class LinkCrawler(object):

    def __init__(self,index_url,filename,dirname,geckodriver_path):
        self.__index_url = index_url
        self.__filename = filename
        self.__dirname = dirname
        self.__geckodriver_path = geckodriver_path
        
    @property
    def index_url(self):
        return self.__index_url

    @index_url.setter
    def index_url(self,index_url):
        self.__index_url = index_url
        self.export_links()

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self,filename):
        self.__filename = filename
        self.export_links()

    @property
    def dirname(self):
        return self.__dirname

    @dirname.setter
    def dirname(self):
        return self.__dirname
        self.export_links()

    @property
    def full_filename(self):
        if self.__dirname == '/':
            return self.__filename
        return self.__dirname + self.__filename
    
    def __getPageHTML(self,url):
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options, 
                executable_path = self.__geckodriver_path)
        driver.set_page_load_timeout(20)
        driver.get(url) 
        page = driver.page_source
        driver.quit()
        return page

    def __constructFullURL(self,urlparams):
        if(urlparams == {}):
            return self.__index_url
        fullurl = self.__index_url if (self.__index_url[-1] == "/") else self.__index_url + "/"
        fullurl += "?"
        for key,value in urlparams.items():
            fullurl += key + "=" + value + "&" 
        return fullurl[:-1] 

    def __find_links(self,wrapper,wrapper_attrs,
                    a_tag_attrs,urlparams):
        a_tag_list = []
        links_list = []
        fullURL = self.__constructFullURL(urlparams)
        print(fullURL)
        index_page = self.__getPageHTML(fullURL)
        index_page_soup = BeautifulSoup(index_page,"lxml")
        wrapper_lst = index_page_soup.find_all(wrapper,attrs=wrapper_attrs)
        for a_tag in wrapper_lst: 
            a_tag_list += a_tag.find_all("a",attrs = a_tag_attrs)
        for a_tag in a_tag_list:
            link_url = urljoin(self.__index_url, a_tag.get('href'))
            if(link_url not in links_list):
                links_list.append(link_url)
        return links_list

    def export_links(self,wrapper,wrapper_attrs={},a_tag_attrs={},urlparams={}):
        links_list = self.__find_links(wrapper,wrapper_attrs, a_tag_attrs,urlparams)
        if not os.path.exists(self.__dirname):
            os.makedirs(self.__dirname)
        f = open(self.full_filename,'w')
        f.write('\n'.join(links_list))
        f.close()

    def append_links(self,a_tag_attrs={},urlparams={}):
        links_list = self.__find_links(a_tag_attrs,urlparams)
        if not os.path.exists(self.__dirname):
            os.makedirs(self.__dirname)
        if not os.path.isfile(self.__filename):
            f = open(self.full_filename, "w")
            f.close()
        f = open(self.full_filename, "a")
        f.write('\n'.join(links_list))
        f.close()

    def read_links(self):
        f = open(self.full_filename,"r")
        links_list = []
        for line in f:
            links_list.append(line.replace('\n',''))
        f.close()
        return links_list

if __name__ == "__main__":
    url = "https://www.washingtonpost.com/newssearch/"
    crawler = LinkCrawler(url,"links.txt","links/","/usr/bin/geckodriver") 
    crawler.export_links("div",wrapper_attrs={"class":"pb-feed-headline"},a_tag_attrs={"class":"ng-binding"},urlparams={"query":"bitcoin"})
