# -*- coding: utf-8 -*-
import re,sys,os
import json
import collections
import redis

class node:
    desc=[]

def makeNetwork(filename):
    with open(filename) as f:
        content = f.read()
        pair_list = getPairs(content)
        grouped = groupByKeys(pair_list) #outputs {'word' : [list, of, all, found, next, words]}
        counted = countKeys(grouped) #outputs {'word' : [ {'another_word' : 'counted_appearances'}]}
        return counted

def groupByKeys(inp):
    output={}
    for pair in inp:
        tmp=[]
        for p in inp:
            if list(pair.keys())[0] in p:
                tmp.append(p[list(pair.keys())[0]])
        output.update({list(pair.keys())[0] : tmp})
    return output

def countKeys(inp):
    output={}
    for item in inp.keys():
        counted=collections.Counter(inp[item])
        output.update({item : counted})
    return output

def getPairs(inp):
    stack=[]
    lines = json.loads(inp)
    for line in lines:
        words=line["quote"].split(" ")
        for i in range(len(words)):
            if (i+1)<len(words):
                stack.append({words[i] : words[i+1]})
            else:
                stack.append({words[i] : None})
    return stack



network = makeNetwork(sys.argv[1])
#addr=os.environ["REDIS_URL"].split(":")
#hostname=":".join(addr[:-1])
#print(hostname)
r = redis.from_url(os.environ.get("REDIS_URL"))
for net in network:
    r.set(str(net),str(json.dumps(network[net])),ex=86400) #setting keys to expire in a day
