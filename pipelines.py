#!/usr/bin/env python3

import json

class StockListJsonPipeline(object):
    def __init__(self,jfile='stocklist.json'):
        self.file = open(jfile, 'w')

    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False,sort_keys=True) + "\n"
        self.file.write(line)
        return item

class StockInfoJsonPipeline(object):
    def __init__(self,jfile='stockinfo.json'):
        self.file = open(jfile, 'a')

    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False,sort_keys=True) + "\n"
        self.file.write(line)
        return item
