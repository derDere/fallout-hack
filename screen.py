import random
from curses import *

def screen(stdscr, words):
  chars = "0123456789abcdefghijklmnopqrstuvwxyz"
  curs_set(0)
  start_color()
  init_pair(7, 1, -1)
  halfBufferSize = 12 * 16
  bufferSize = halfBufferSize * 2
  buffer = [chars[i % len(chars)] for i in range(bufferSize)] # * bufferSize
  attempts = 4
  startAddress = 0 #random.randint(0x1000, 0xFFFF - bufferSize)
  target, decoys = words.getWords()
  stdscr.addstr("Welcome to ROBCO Industries (TM) Termlink\n\n", color_pair(1))
  stdscr.addstr("Password Required\n\n", color_pair(1))
  stdscr.addstr("Attempts Remaining:%s" % (" ■" * attempts), color_pair(1))
  y = 6
  for addr in range(startAddress, startAddress + halfBufferSize, 12):
    stdscr.addstr(y, 0, "0x" + ("0000" + hex(addr)[2:])[-4:].upper(), color_pair(1))
    stdscr.addstr(y, 20, "0x" + ("0000" + hex(addr + halfBufferSize)[2:])[-4:].upper(), color_pair(1))
    y += 1
  i = 0
  for y in range(6, 6 + 16):
    for x in range(7, 7 + 12):
      stdscr.addstr(y, x, buffer[i], color_pair(1))
      stdscr.addstr(y, x + 20, buffer[i + halfBufferSize], color_pair(1))
      i += 1
  stdscr.getch()
