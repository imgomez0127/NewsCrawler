from NetSpider import NetSpider
NetSpider.index_url = "https://www.washingtonpost.com"
NetSpider.query={"query":"bitcoin"}
spider = NetSpider.startup(20,{"class":"ng-binding"})

