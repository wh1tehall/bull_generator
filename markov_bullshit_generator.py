import json
import random
import sys
import redis

class network:

    words=[]
    r = None

    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.words=list(self.r.scan_iter())
        print self.words

    def selectRandomWord(self):
        return self.words[random.randrange(len(self.words))]

    def selectNextWord(self,word):

        redisreturn = self.r.get(word)
        if redisreturn!=None:
            candidates=json.loads(self.r.get(word))
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

net=network()
starting_word=net.selectRandomWord()
words=[starting_word]
while words[-1]!=None:
    words.append(net.selectNextWord(words[-1]))

print " ".join(words[:-2])
