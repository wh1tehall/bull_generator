# -*- coding: utf-8 -*-
import json
import random
import sys,os
import redis

class network:

    words=[]
    r = None

    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        for w in self.r.scan_iter():
            self.words.append(w.decode('utf-8'))

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

    def generatePhrase(self):
        starting_word=self.selectRandomWord()
        phrase=[starting_word]
        while phrase[-1]!=None:
            phrase.append(self.selectNextWord(phrase[-1]))
        return u" ".join(phrase[:-2])
