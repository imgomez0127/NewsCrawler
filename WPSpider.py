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
    testurl = "https://www.washingtonpost.com/technology/2019/02/19/password-managers-have-security-flaw-you-should-still-use-one/?utm_term=.9805c84d7273"
    query = {"query":"bitcoin"}
    WPSpider.startup("div",wrapper_attrs={"class":"pb-feed-headline"},a_tag_attrs={"class":"ng-binding"},urlparams=query)
    print(WPSpider.queue_set)
    spider = WPSpider(1,"data/",testurl)
    print(spider.getArticleAsJSON())

