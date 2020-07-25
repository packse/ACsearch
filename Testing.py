array = (("1", 'A'),("3", 'B'),("2", 'C'))
tuple = ("1", 'A')
valido = ("YES", "2", "3")
location_index = [item for item in array if item[0] == "1" or item[1] == "1"]

print(location_index)
if "A" in location_index[0]:
    print(location_index[0][1])
else:
    print("no")

#     print(array[0].index("2"))


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
