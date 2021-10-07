import random
import curses
import math
from curses import *


def selection2xy(selection, halfBufferSize):
  y = math.floor(selection / 12)
  x = selection % 12
  if selection >= halfBufferSize:
    y -= 16
    x += 20
  return (x, y)


def screen(stdscr, words):
  curs_set(0)
  start_color()
  use_default_colors()
  color = 10
  init_pair(1, color, 0)
  init_pair(2, 0, color)
  stdscr.attron(color_pair(1))

  chars = "°^!\"§$%%&/=?@€|,;.:-_+#*'~²³\\¢£¥©«±µ¶"
  halfBufferSize = 12 * 16
  bufferSize = halfBufferSize * 2
  buffer = [random.choice(chars) for i in range(bufferSize)]
  startAddress = random.randint(0x6000, 0xFFFF - bufferSize)

  target, decoys = words.getWords()
  attempts = 4
  selection = 0

  stdscr.addstr("Welcome to ROBCO Industries (TM) Termlink\n\n")
  stdscr.addstr("Password Required\n\n")
  stdscr.addstr("Attempts Remaining:%s" % (" ■" * attempts))
  y = 6
  for addr in range(startAddress, startAddress + halfBufferSize, 12):
    stdscr.addstr(y, 0, "0x" + ("0000" + hex(addr)[2:])[-4:].upper())
    stdscr.addstr(y, 20, "0x" + ("0000" + hex(addr + halfBufferSize)[2:])[-4:].upper())
    y += 1
  i = 0
  for y in range(6, 6 + 16):
    for x in range(7, 7 + 12):
      stdscr.addstr(y, x, buffer[i])
      stdscr.addstr(y, x + 20, buffer[i + halfBufferSize])
      i += 1

  key = ''
  oldSelection = 0
  while not key in [ord('q'), 27]:
    #y = math.floor(selection / 12)
    #x = selection % 12
    #if selection >= halfBufferSize:
    #  y -= 16
    #  x += 20
    x,y = selection2xy(oldSelection, halfBufferSize)
    stdscr.addstr(y + 6, x + 7, buffer[oldSelection], color_pair(1))
    x,y = selection2xy(selection, halfBufferSize)
    stdscr.addstr(y + 6, x + 7, buffer[selection], color_pair(2))

    key = stdscr.getch()
    oldSelection = selection
    if key in [ord('w'), curses.KEY_UP]:
      selection -= 12
    elif key in [ord('a'), curses.KEY_LEFT]:
      if (selection % 12) == 0:
        selection -= halfBufferSize - 11
      else:
        selection -= 1
    elif key in [ord('s'), curses.KEY_DOWN]:
      selection += 12
    elif key in [ord('d'), curses.KEY_RIGHT]:
      if (selection % 12) == 11:
        selection += halfBufferSize - 11
      else:
        selection += 1
    while selection < 0:
      selection += bufferSize
    selection %= bufferSize
