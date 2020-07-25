import curses
from curses import wrapper
import FishSearch as fs


#Todo
# Better interface using Curses (List all fish nicely in grid like format)
# Proper Confirm/Cancel and going back to the previous screen should be implemented
# Being able to repeat the same operation multiple times (add/edit/delete) would also be ideal
# Could replace the entering of data one by one and instead have multiple fields and being able to tab between them
# Periodically check for resize issues where you will need to clear and refresh the screen to fit correctly

# Outline
# Program should work primarily with keyboard controls, using arrow keys and enter to move between different selections
# and letters to for use in the search bar. For screens that use it search should be dynamic and enter shouldn't need
# to be clicked for it to register. An empty search field should display all
# ud = Up/Down lf = Left/Right




def main(stdscr):
    startup(stdscr)
    opening_menu(stdscr)


# Sets up dimensions of win1 screen based on stdscr
def header_scr_setup(stdscr):
    # Returns a tuple (y, x) of the height and width of the screen.
    h, w = stdscr.getmaxyx()
    begin_x = 0; begin_y = 0
    height = h // 5     # // is floor division which removes the decimal points
    width = w
    win1 = curses.newwin(height, width, begin_y, begin_x)
    # Draws border around box
    win1.box()
    # Refreshes the screen. Must be called each time a new event needs to be rendered
    win1.refresh()
    return win1


# Keyboard movement when using up and down directions. Returns the row selected by enter
def menu_screen(scr, menu_items, header_text=""):
    centered_menu_ud(scr, menu_items, 0)
    selected_row = 0
    while 1:
        header_display(scr, menu_items, header_text)
        selected_row, key = keyboard_movement_ud(scr, menu_items, selected_row)
        centered_menu_ud(scr, menu_items, selected_row, key)
        if key == curses.KEY_ENTER or key in [10, 13]:
            return selected_row


# Returns the currently selected row and the key pressed as a tuple
def keyboard_movement_ud(scr, menu_items,selected_row):
    while 1:
        key = scr.getch()
        if key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
            return selected_row, key
        elif key == curses.KEY_DOWN and selected_row < len(menu_items) - 1:
            selected_row += 1
            return selected_row, key
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return selected_row, key


def centered_menu_ud(scr, menu_items, selected_row, key=None):
    # 1 is the key used as because variables don't store it
    box_reset(scr)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_YELLOW)
    h, w = scr.getmaxyx()
    for idx, row in enumerate(menu_items):
        y = (h//2) - (len(menu_items)//2) + idx  # // is floor division which removes the decimal points
        x = (w//2) - (len(row)//2)
        if idx == selected_row:
            scr.addstr(y, x, row, curses.color_pair(1))
        else:
            scr.addstr(y, x, row)

# Initialisation of the primary screen
def startup(stdscr):
    curses.curs_set(0)
    box_reset(stdscr)

def header_display(scr, menu_items, text):
    h, w = scr.getmaxyx()
    y = h//2 - len(menu_items)//2 - 2
    x = w//2 - len(text)//2
    scr.addstr(y, x, text)


def box_reset(scr):
    # Clear screen
    scr.clear()
    # Draw box outline of screen
    scr.box()
    # Refresh the elements on the screen
    scr.refresh()

def opening_menu(scr):
    start_menu_items = ["Find Fish", "Add Fish", "Show All Fish", "Delete Fish", "Edit Fish", "Sum Fish", "Exit"]
    menu_selection = menu_screen(scr, start_menu_items, "Animal Crossing Fish Search")

    if menu_selection == 6:
        exit_menu(scr)

def exit_menu(scr):
    exit_menu_items = ["Yes", "No"]
    box_reset(scr)
    menu_selection = menu_screen(scr, exit_menu_items, "Are you sure you want to quit?")
    if menu_selection == 0:
        curses.endwin()
    else:
        scr.getch()

# Wrapper improves and prevents some issues when running the curses terminal
wrapper(main)