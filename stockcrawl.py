#!/usr/bin/env python3

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import json

class StockInfo(scrapy.Item):
    stock_name  = scrapy.Field()
    stock_id    = scrapy.Field()
    stock_pe    = scrapy.Field()
    stock_pb    = scrapy.Field()
    stock_price = scrapy.Field()
    stock_mcap = scrapy.Field()

class StockSpider(scrapy.Spider):
    name = "StockSpider"
    def __init__(self,stock_id,stock_name):
        self.sid = stock_id
        self.sname = stock_name
        self.allowed_domains = ["eastmoney.com"]
        if stock_id[0] == '6':
            self.tailstr = "1"
        else:
            self.tailstr = "2"
        self.start_urls = ['http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=' + self.sid + self.tailstr]
    def parse(self, response):
        stock = StockInfo()
        stock["stock_id"] = self.sid
        stock["stock_name"] = self.sname
        dump = response.xpath('//body/p/text()').extract()[0].split('[')[2].split(',')
        if len(dump) > 50:
            stock["stock_pe"] = dump[38].split('"')[1]
            stock["stock_pb"] = dump[43].split('"')[1]
            stock["stock_price"] = dump[25].split('"')[1]
            stock["stock_mcap"] = dump[46].split('"')[1]
            return stock 

settings = Settings()
settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36")
settings.set("ITEM_PIPELINES" , {'pipelines.StockInfoJsonPipeline':1})
process = CrawlerProcess(settings)

jfile = open("stocklist.json","r")
for jline in jfile.readlines():
    stockitem = dict(json.loads(jline))
    if stockitem["sid"][0] == '0' or stockitem["sid"][0] == '6':
        process.crawl(StockSpider,stockitem["sid"],stockitem["name"])
process.start()

