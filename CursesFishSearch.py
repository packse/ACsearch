import curses
from curses import wrapper
import FishSearch as fs


#Todo
# Better interface using Curses (List all fish nicely in grid like format)
# Proper Confirm/Cancel and going back to the previous screen should be implemented
# Being able to repeat the same operation multiple times (add/edit/delete) would also be ideal
# Could replace the entering of data one by one and instead have multiple fields and being able to tab between them
# Periodically check for resize issues where you will need to clear and refresh the screen to fit correctly
# Resize error needs to be handled either by exception or using the os library to resize the terminal before crash

# Outline
# Program should work primarily with keyboard controls, using arrow keys and enter to move between different selections
# and letters to for use in the search bar. For screens that use it search should be dynamic and enter shouldn't need
# to be clicked for it to register. An empty search field should display all
# ud = Up/Down lf = Left/Right



def main(stdscr):
    startup(stdscr)
    start_menu(stdscr)

# Sets up dimensions of header screen based on stdscr
def header_scr_setup(stdscr):
    # Returns a tuple (y, x) of the height and width of the screen.
    h, w = stdscr.getmaxyx()
    begin_x = 0; begin_y = 0
    height = h // 5     # // is floor division which removes the decimal points
    width = w
    headerscr = curses.newwin(height, width, begin_y, begin_x)
    # Draws border around box
    headerscr.box()
    # Refreshes the screen. Must be called each time a new event needs to be rendered
    headerscr.refresh()
    return headerscr


# Determines which menu type/keyboard type will be used and passes it relevant information. Returns selected row
def menu_controller(scr, menu_items, header_text=""):
    selected_row = 0
    while 1:
        if 1:
            return centered_menu_ud(scr, menu_items, selected_row, header_text)



# Returns the currently selected row and the key pressed as a tuple
def keyboard_movement_ud(scr, menu_items, selected_row):
    while 1:
        key = scr.getch()
        if key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
            return selected_row, key
        elif key == curses.KEY_UP and selected_row == 0:
            selected_row = len(menu_items) - 1
            return selected_row, key
        elif key == curses.KEY_DOWN and selected_row < len(menu_items) - 1:
            selected_row += 1
            return selected_row, key
        elif key == curses.KEY_DOWN and selected_row == len(menu_items) - 1:
            selected_row = 0
            return selected_row, key
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return selected_row, key
        # Checks if the screen is resized as this requires exiting the loop and redrawing the terminal
        elif curses.KEY_RESIZE:
            return selected_row, key


# Returns array of all existing menu items
def centered_menu_ud(scr, menu_items, selected_row, header_text=""):
    # 1 is the key used as because variables don't store it
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_YELLOW)
    while 1:
        box_reset(scr)
        h, w = scr.getmaxyx()
        header_display(scr, menu_items, header_text)
        for idx, row in enumerate(menu_items):
            y = (h//2) - (len(menu_items)//2) + idx  # // is floor division which removes the decimal points
            x = (w//2) - (len(row)//2)
            if idx == selected_row:
                scr.addstr(y, x, row, curses.color_pair(1))
            else:
                scr.addstr(y, x, row, curses.color_pair(0))

        selected_row, key = keyboard_movement_ud(scr, menu_items, selected_row)

        if key == curses.KEY_ENTER or key in [10, 13]:
            return selected_row





# Initialisation of the primary screen
def startup(stdscr):
    curses.curs_set(0)

# Displays header text above the current menu
def header_display(scr, menu_items, text):
    h, w = scr.getmaxyx()
    y = h//2 - len(menu_items)//2 - 2
    x = w//2 - len(text)//2
    scr.addstr(y, x, text)


def box_reset(scr):
    # Clear screen
    scr.clear()
    # Turns off the cursor. Needs to be set every time the screen clears
    curses.curs_set(0)
    # Draw box outline of screen
    scr.box()
    # Refresh the elements on the screen
    scr.refresh()


def start_menu(scr):
    start_menu_items = ["Calculate Profit", "Add Fish", "Delete Fish", "Edit Fish", "Exit"]
    menu_selection = menu_controller(scr, start_menu_items, "Animal Crossing Fish Search")

    if menu_selection == 0:
        profit_menu(scr)
    elif menu_selection == len(start_menu_items) - 1:
        exit_menu(scr)


def exit_menu(scr):
    exit_menu_items = ["Yes", "No"]
    box_reset(scr)
    menu_selection = menu_controller(scr, exit_menu_items, "Are you sure you want to quit?")
    if menu_selection == 0:
        curses.endwin()
    else:
        start_menu(scr)


def profit_menu(scr):
    box_reset(scr)
    # Draws the left and right side screens
    lscreen = lhalf_box_draw(scr)
    rscreen = rhalf_box_draw(scr)
    scr.addstr("WOWOWOWOWOWOWOWOWOWOWOWOWOWOWOWOWOWOW")
    lscreen.addstr("HEYEEYEYEYE")
    rscreen.addstr("YOYOYOYOOYOYYYO")
    scr.refresh()
    lscreen.refresh()
    rscreen.refresh()
    scr.getch()

def lhalf_box_draw(scr):
    y, x = scr.getmaxyx()
    begin_y = 0; begin_x = 0
    height = y; width = x//2
    lscreen = curses.newwin(height, width, begin_y, begin_x)
    lscreen.box()
    lscreen.refresh()

    return lscreen

def rhalf_box_draw(scr):
    y, x = scr.getmaxyx()
    begin_y = 0; begin_x = x//2
    # Width needs to be divided by two otherwise it would be the size of a whole screen
    height = y; width = x//2
    rscreen = curses.newwin(height, width, begin_y, begin_x)
    rscreen.box()
    rscreen.refresh()

    return rscreen





# Wrapper improves and prevents some issues when running the curses terminal
wrapper(main)