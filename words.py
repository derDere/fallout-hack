import os
import json
import random
import curses
import screen as s


def likeliness(a, b):
  sum = 0
  for i in range(len(a)):
    c1 = a[i]
    c2 = (b + '      ')[i]
    if c1 == c2:
      sum += 1
  return sum


class Words:
  def __init__(self, path, screen):
    self.winWidth = 46
    self.winHeight = 6
    h, w, x, y = screen.center(self.winHeight, self.winWidth)
    self.loadWin = curses.newwin(h, w, x, y)
    self.loadWin.attron(curses.color_pair(1))
    self.loadWin.border()
    self.loadWin.refresh()
    self.path = path
    self.screen = screen
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
      self.loadWin.addstr(2, 2, "Hacking into system ...")
      s.progressBar(self.loadWin, self.winHeight - 2, 2, 0, 100, self.winWidth - 4, "0%")
      self.loadWin.refresh()
      global count
      count = 0
      def hook(obj):
        global count
        count += 1
        s.progressBar(self.loadWin, self.winHeight - 2, 2, count, len(self.list), self.winWidth - 4, "%i%%" % (round(count / len(self.list) * 100)) )
        self.loadWin.refresh()
        return obj
      with open('relations.json', 'r') as f:
        self.relations = json.load(f, object_hook=hook)
    else:
      self.loadWin.addstr(1, 2, "Generating word relation database.")
      self.loadWin.addstr(2, 2, "Don't worry this only has to be done once.")
      s.progressBar(self.loadWin, self.winHeight - 2, 2, 0, 100, self.winWidth - 4, "0%")
      self.loadWin.refresh()
      for i in range(len(self.list)):
        s.progressBar(self.loadWin, self.winHeight - 2, 2, i, len(self.list), self.winWidth - 4, "%i%%" % (round(i / len(self.list) * 100)) )
        self.loadWin.refresh()
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
