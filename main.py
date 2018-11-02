import re,sys
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
        print grouped
        counted = countKeys(grouped) #outputs {'word' : [ {'another_word' : 'counted_appearances'}]}
        return counted

def groupByKeys(inp):
    output={}
    for pair in inp:
        tmp=[]
        for p in inp:
            if p.has_key(pair.keys()[0]):
                tmp.append(p[pair.keys()[0]])
        output.update({pair.keys()[0] : tmp})
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
r = redis.StrictRedis(host='localhost', port=6379, db=0)
for net in network:
    r.set(net,json.dumps(network[net]),ex=86400) #setting keys to expire in a day
