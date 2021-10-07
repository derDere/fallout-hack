import curses
import screen
from words import Words


def printColors(stdscr):
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    try:
        for i in range(0, 255):
            stdscr.addstr("(%i,%i,%i)" % (i + 1, i, -1), curses.color_pair(i))
    except curses.ERR:
        # End of screen reached
        pass
    stdscr.addstr('#' * 200, curses.color_pair(11))
    stdscr.getch()


def main(argv):
  if 'pc' in argv:
    curses.wrapper(printColors)
  else:
    words = Words('words.txt')
    curses.wrapper(screen.screen, words)


if __name__=="__main__":
  import sys
  if len(sys.argv) > 1:
    main(sys.argv[1:])
  else:
    main([])
