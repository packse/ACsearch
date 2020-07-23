import curses
from curses import wrapper
import FishSearch as fs


#Todo
# Better interface using Curses (List all fish nicely in grid like format)


def main(stdscr):
    # Clear screen
    stdscr.clear()
    begin_x = 0
    begin_y = 0
    height = 5
    width = 40
    win = curses.newwin(height, width, begin_y, begin_x)
    win.box()

    # Refreshes the screen. Must be called each time a new event needs to be rendered
    stdscr.refresh()
    win.refresh()




    # Basically python input() for the next key pressed by the user
    stdscr.getkey()
    stdscr.getkey()




# Wrapper improves and prevents some issues when running the curses terminal
wrapper(main)








# Wrapper performs the functions in here as well as other fixes to prevent issues when returning to the normal terminal
def what_wrapper_does():
    # Initialises the screen
    stdscr = curses.initscr()

    # Used to turn off the echoing(printing) of keys so that you read keys and only display them when you let them
    curses.noecho()
    # Allows the program to react to key presses instantly without needing to click enter
    curses.cbreak()
    # Allows usage of the keypad
    stdscr.keypad(True)

    # Should be run before the  program is terminated to reset the options
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    # This terminates curses and returns the terminal to its normal operating mode
    curses.endwin()
