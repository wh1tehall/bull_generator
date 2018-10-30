import json
import random
import sys

def impNetwork(inp):
    with open(inp) as f:
        return json.loads(f.read())

def selectRandomWord(net):
    keys=net.keys()
    return keys[random.randrange(len(keys))]

def selectNextWord(net,word):
    if net.has_key(word):
        candidates=net[word]
        keys=candidates.keys()
        den=0
        for key in keys:
            den+=candidates[key]
        i=random.randrange(den)
        den=0
        for key in keys:
            den+=candidates[key]
            if den>i:
                return key
    else:
        return None

network=impNetwork(sys.argv[1])
starting_word=selectRandomWord(network)
words=[starting_word]
while words[-1]!=None:
    words.append(selectNextWord(network,words[-1]))

print " ".join(words[:-1])
