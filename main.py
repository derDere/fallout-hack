import curses
import screen
from words import Words


def main(argv):
  words = Words('words.txt')
  curses.wrapper(screen.screen, words)


if __name__=="__main__":
  import sys
  if len(sys.argv) > 1:
    main(sys.argv[1:])
  else:
    main([])
