from NetSpider import NetSpider
import json
class WPSpider(NetSpider):
    index_url = "https://www.washingtonpost.com/newssearch"
    def __init__(self, spider_id, data_directory,queue_link):
        super(WPSpider,self).__init__(spider_id,data_directory,queue_link)
    def getArticleAsJSON(self):
        title = self._getTitle("h1",{"itemprop":"headline"})
        author = self._getAuthor(["span","a"],{"class":"author-name"})
        article = self._getArticle("div","p",{"class":"article-body"})
        return json.dumps({"title":title,"author":author,"article":article}) 
            
if __name__ == "__main__":
    testurl = "https://www.washingtonpost.com/world/asia_pacific/mt-gox-head-convicted-of-manipulating-data-cleared-of-theft/2019/03/14/7678979e-46d1-11e9-94ab-d2dda3c0df52_story.html?utm_term=.5038d4a083e5"
    WPSpider.startup("div",wrapper_attrs={"class":"pb-feed-headline"},a_tag_attrs={"class":"ng-binding"},urlparams={"query":"bitcoin"})
    query = {"query":"bitcoin"}
    spider = WPSpider(1,"data/",testurl)
    print(json.loads(spider.getArticleAsJSON()))

