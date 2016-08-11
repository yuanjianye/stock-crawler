#!/usr/bin/env python3
import json
def tofloat(fstr):
    if fstr == "-":
        return 100000
    else:
        return float(fstr)

class Stock(object):
    def __init__(self,info):
        self.name=info["stock_name"]
        self.sid=info["stock_id"]
        self.pb=tofloat(info["stock_pb"])
        self.pe=tofloat(info["stock_pe"])
        self.price=tofloat(info["stock_price"])
        self.mcap=tofloat(info["stock_mcap"])

stocklist=[]
jfile = open("stockinfo.json","r")
for I in jfile.readlines():
#    print(I)
    stocklist.append(Stock(dict(json.loads(I))))
stocklist.sort(key = lambda stock:stock.pe+(stock.pb*5))
for I in stocklist:
    print(I.name,"   \t",I.sid, "    %-10.2f %-10.2f %-10.2f"%(I.pe,I.pb,I.price))

