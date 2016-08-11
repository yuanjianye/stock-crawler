#!/usr/bin/env python3

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import json

class StockItem(scrapy.Item):
        name  = scrapy.Field()
        sid   = scrapy.Field()
        url   = scrapy.Field()

class ListSpider(scrapy.Spider):
    name = "ListSpider"
    def __init__(self):
        self.allowed_domains = ["eastmoney.com"]
        self.start_urls = ['http://quote.eastmoney.com/stocklist.html']
    def parse(self, response):
        for I in response.xpath(".//*[@id='quotesearch']/ul/li/a"):
            sitem = StockItem()
            sitem['url']=I.xpath("@href")[0].extract()
            sitem['name'],sitem['sid']=I.xpath("text()")[0].extract().split('(')
            sitem['sid'] = sitem['sid'].replace(")","")
            if sitem['sid'][0] == '0' or sitem['sid'][0] == '6':
                yield(sitem)

settings = Settings()
settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36")
settings.set("ITEM_PIPELINES" , {'pipelines.StockListJsonPipeline':1})
process = CrawlerProcess(settings)

process.crawl(ListSpider)
process.start()
