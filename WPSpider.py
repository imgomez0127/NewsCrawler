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
    testurl = "https://www.washingtonpost.com/opinions/global-opinions/china-is-racing-ahead-of-the-united-states-on-blockchain/2019/03/07/c1e7776a-4116-11e9-9361-301ffb5bd5e6_story.html?utm_term=.5fbe8b97e648"
    query = {"query":"bitcoin"}
    spider = WPSpider(1,"data/",testurl)
    print(json.loads(spider.getArticleAsJSON()))

