import os
import json
import random


def likeliness(a, b):
  sum = 0
  for i in range(len(a)):
    c1 = a[i]
    c2 = (b + '      ')[i]
    if c1 == c2:
      sum += 1
  return sum


class Words:
  def __init__(self, path):
    self.list = []
    self.byLen = {
      3: [],
      4: [],
      5: [],
      6: []
    }
    with open(path, 'r') as f:
      for word in f:
        word = word.replace("\n","")
        l = len(word)
        index = len(self.list)
        self.list.append(word.upper())
        if l in self.byLen:
          self.byLen[l].append(index)
    self.relations = {}
    if os.path.isfile('relations.json'):
      print("Loading word relations ...")
      with open('relations.json', 'r') as f:
        self.relations = json.load(f)
    else:
      print("Generating word relations\nDon't worry this only has to be done once.")
      for i in range(len(self.list)):
        print("%i / %i - %i%%" % (i, len(self.list), round(100 * i / len(self.list))), end="\r")
        word = self.list[i]
        data = {}
        for n in range(1, len(word)):
          data[str(n)] = []
        for j in self.byLen[len(word)]:
          wordB = self.list[j]
          if word != wordB and len(word) == len(wordB):
            likns = likeliness(word, wordB)
            if likns > 0:
              data[str(likns)].append(j)
        self.relations[str(i)] = data
      print("\n")
      with open('relations.json', 'w') as f:
        jj = json.dumps(self.relations)
        f.write(jj)

  def getWords(self):
    index = random.randint(0, len(self.list))
    target = self.list[index]
    indexD = random.randint(0, len(self.list))
    while indexD == index:
      indexD = random.randint(0, len(self.list))
    decoy = self.list[indexD]
    false = [decoy]
    length = random.randint(10, 20)
    while len(false) < length:
      if len(false) < 6:
        rndLikns = random.randint(1, len(target) - 1)
        options = self.relations[str(index)][str(rndLikns)]
        if len(options) > 0:
          i = random.choice(options)
          f = self.list[i]
          if not f in false:
            false.append(f)
      elif len(false) < 10:
        rndLikns = random.randint(1, len(decoy) - 1)
        options = self.relations[str(indexD)][str(rndLikns)]
        if len(options) > 0:
          i = random.choice(self.relations[str(indexD)][str(rndLikns)])
          f = self.list[i]
          if not f in false:
            false.append(f)
      else:
        f = random.choice(self.list)
        if not f in false:
          false.append(f)
    return (target, false)
