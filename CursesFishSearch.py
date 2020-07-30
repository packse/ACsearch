import curses
from curses import wrapper
import FishSearch as fs


# Todo
# Better interface using Curses (List all fish nicely in grid like format)
# Proper Confirm/Cancel and going back to the previous screen should be implemented
# Could replace the entering of data one by one and instead have multiple fields and being able to tab between them
# Resize error needs to be handled either by exception or using the os library to resize the terminal before crash
# Add footer section for the right screen that will display sum of fish


def main(stdscr):
    # 1 is essentially the variable of the created colour pair
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_YELLOW)
    start_menu(stdscr)


# Run when the program is started
def start_menu(scr):
    curses.curs_set(0)
    start_menu_items = ["Calculate Profit", "Add Fish", "Delete Fish", "Edit Fish", "Exit"]
    menu_selection = centered_menu_ud(scr, start_menu_items, 0, "Animal Crossing Fish Search")

    if menu_selection == 0:
        profit_menu(scr)
    elif menu_selection == len(start_menu_items) - 1:
        exit_menu(scr)


# Run when the exit option is selected to confirm the decision
def exit_menu(scr):
    exit_menu_items = ["Yes", "No"]
    window_reset(scr)
    menu_selection = centered_menu_ud(scr, exit_menu_items, 0, "Are you sure you want to quit?")
    if menu_selection == 0:
        curses.endwin()
    else:
        start_menu(scr)


# Run when the calculate profit option is selected
def profit_menu(scr):
    window_reset(scr)
    # Current screen begin as the left screen
    current_screen = 0
    # rscreen starts empty but is filled depending on the selection by the user.
    rscreen_fish_array = []

    while 1:
        if current_screen == 0:
            fish_selected = lscreen_fish_menu(scr, 0)
            rscreen_fish_array.append(fish_selected)
            rscreen_fish_menu(scr, rscreen_fish_array)
        else:
            fish_selected = rscreen_fish_menu(scr, rscreen_fish_array, 0)


# Menu that displays information in the center of the screen. When enter is pressed it returns the selected row
def centered_menu_ud(scr, menu_items, selected_row, header_text=""):
    # Continues to operate as a selectable menu until a selection has been made by pressing enter
    while 1:
        window_reset(scr)
        h, w = scr.getmaxyx()
        header_display(scr, menu_items, header_text)
        # Displays all menu items from the array that is received by function parameter
        for idx, row in enumerate(menu_items):
            y = (h // 2) - (len(menu_items) // 2) + idx  # // is floor division which removes the decimal points
            x = (w // 2) - (len(row) // 2)
            # Highlights the text to have it displayed which row is selected
            if idx == selected_row:
                scr.addstr(y, x, row, curses.color_pair(1))
            else:
                scr.addstr(y, x, row, curses.color_pair(0))

        selected_row, key = keyboard_movement_ud(scr, selected_row)
        # Allows the menu selection to loop around
        if key == curses.KEY_UP and selected_row == -1:
            selected_row = len(menu_items) - 1
        elif key == curses.KEY_DOWN and selected_row == len(menu_items):
            selected_row = 0
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return selected_row


# Returns the currently selected row and the key pressed as a tuple
def keyboard_movement_ud(scr, selected_row):
    while 1:
        key = scr.getch()
        if key == curses.KEY_UP:
            selected_row -= 1
            return selected_row, key
        elif key == curses.KEY_DOWN:
            selected_row += 1
            return selected_row, key
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return selected_row, key
        # Checks if the screen is resized as this requires exiting the loop and redrawing the terminal
        elif curses.KEY_RESIZE:
            return selected_row, key


# Displays header text above the centered menu
def header_display(scr, menu_items, text):
    h, w = scr.getmaxyx()
    y = h // 2 - len(menu_items) // 2 - 2
    x = w // 2 - len(text) // 2
    scr.addstr(y, x, text)

    # For when the window needs to be reset


def window_reset(scr):
    # Clear screen
    scr.clear()
    # Turns off the cursor. Needs to be set every time the screen clears
    curses.curs_set(0)
    # Draw box outline of screen
    scr.box()
    # Refresh the elements on the screen
    scr.refresh()


# Returns the selected fish after pressing enter. Selected row can be none for when the screen shouldn't be controllable
def lscreen_fish_menu(mainscr, selected_row=None):
    # lscreen will show all of the the fish in the file but could change depending on search options
    fish_array = fs.get_fish_objects()
    scr = lhalf_box_draw(mainscr)
    # The starting position that the loop will read from when going through fish array. Required to allow for scrolling
    fish_array_start = 0
    # The position of the selected fish in relation to the whole array as opposed to the array of fish being displayed
    fish_array_position = 0
    while 1:
        # The fish currently being shown on the screen since the screen size can vary. Clears itself when loop restarts
        fish_displayed = []
        maxh, maxw = scr.getmaxyx()
        beginy, beginx = scr.getbegyx()
        # The last row that text can be placed in
        ending_row = maxh - 1
        # The size of each row window
        row_scr_height = get_row_height()
        row_scr_width = get_row_width(maxw)

        # x positions that the text on the screen starts at
        name_pos = 0
        price_pos = row_scr_width // 2
        location_pos = row_scr_width - row_scr_width // 4
        # The heading items in the array and the position that they will be on the screen
        heading_and_pos = [["Name", name_pos], ["Price", price_pos], ["Location", location_pos]]

        # Creates the heading row and heading data
        create_heading_row(heading_and_pos, scr)

        # Each row has a height of 1 so row_y being the start position of the item in relation to y is always 0
        row_y = 0

        for idx, row in enumerate(fish_array[fish_array_start:len(fish_array)]):
            # The position the new window starts getting created from
            start_y = beginy + 3 + idx
            start_x = beginx + 1
            # Only adds next row if it won't overflow off screen
            if start_y < ending_row:
                # Creates a new window that will store a row's worth of fish data including name, price, location
                scr_row = curses.newwin(row_scr_height, row_scr_width, start_y, start_x)

                # Checking if the menu is selectable to decide if highlighting the row is valid
                if selected_row is not None:
                    if selected_row == idx:
                        scr_row.bkgd(' ', curses.color_pair(1))

                scr_row.addstr(row_y, name_pos, row.name)
                scr_row.addstr(row_y, price_pos, row.price)
                scr_row.addstr(row_y, location_pos, row.location)

                scr_row.refresh()
                fish_displayed.append([row, scr_row])

        # Determines if the list is read only or if it can be navigated through
        if selected_row is not None:
            selected_row, key = keyboard_movement_ud(mainscr, selected_row)
            # If the enter key is pressed return the selected fish
            if key == curses.KEY_ENTER or key in [10, 13]:
                return fish_array[fish_array_position]
            # If another key is pressed determine how it should be handled
            else:
                selected_row, fish_array_position, fish_array_start = keyboard_selection(key, fish_array_position,
                                                                                         selected_row, fish_array_start,
                                                                                         fish_array, fish_displayed)
        # If the list doesn't react to user input exit the loop and therefore the function
        else:
            break


# Returns the selected fish after pressing enter. Selected row can be none for when the screen shouldn't be controllable
def rscreen_fish_menu(mainscr, fish_array, selected_row=None):
    # rscreen will show fish received through the function parameter based on user selection
    scr = rhalf_box_draw(mainscr)
    # The starting position that the loop will read from when going through fish array. Required to allow for scrolling
    fish_array_start = 0
    # The position of the selected fish in relation to the whole array as opposed to the array of fish being displayed
    fish_array_position = 0
    while 1:
        # The fish currently being shown on the screen since the screen size can vary. Clears itself when loop restarts
        fish_displayed = []
        maxh, maxw = scr.getmaxyx()
        beginy, beginx = scr.getbegyx()
        # The last row that text can be placed in
        ending_row = maxh - 1
        # The size of each row window
        row_scr_height = 1
        row_scr_width = maxw - 2

        # x positions that the text on the screen starts at
        name_pos = 0
        price_pos = row_scr_width // 2
        # The heading items in the array and the position that they will be on the screen sent as a 2d array
        heading_and_pos = [["Name", name_pos], ["Price", price_pos]]

        # Creates the heading row and heading data
        create_heading_row(heading_and_pos, scr)

        # Each row has a height of 1 so row_y being the start position of the item in relation to y is always 0
        row_y = 0

        for idx, row in enumerate(fish_array[fish_array_start:len(fish_array)]):
            # The position the new window starts getting created from
            start_y = beginy + 3 + idx
            start_x = beginx + 1
            # Only adds next row if it won't overflow off screen
            if start_y < ending_row:
                # Creates a new window that will store a row's worth of fish data including name and price
                scr_row = curses.newwin(row_scr_height, row_scr_width, start_y, start_x)

                # Checking if the menu is selectable to decide if highlighting the row is valid
                if selected_row is not None:
                    if selected_row == idx:
                        scr_row.bkgd(' ', curses.color_pair(1))

                scr_row.addstr(row_y, name_pos, row.name)
                scr_row.addstr(row_y, price_pos, row.price)

                scr_row.refresh()
                fish_displayed.append([row, scr_row])

        # Determines if the list is read only or if it can be navigated through
        if selected_row is not None:
            selected_row, key = keyboard_movement_ud(mainscr, selected_row)
            # If the enter key is pressed return the selected fish
            if key == curses.KEY_ENTER or key in [10, 13]:
                return fish_array[fish_array_position]
            # If another key is pressed determine how it should be handled
            else:
                selected_row, fish_array_position, fish_array_start = keyboard_selection(key, fish_array_position,
                                                                                         selected_row, fish_array_start,
                                                                                         fish_array, fish_displayed)
        # If the list doesn't react to user input exit the loop and therefore the function
        else:
            break


# Used for the profit_menu keyboard selection handling
def keyboard_selection(key, fish_array_position, selected_row, fish_array_start, fish_array, fish_displayed):
    # If the up key was pressed move up the list
    if key == curses.KEY_UP:
        fish_array_position -= 1
        # For when the up key is pressed at the very start of the list which loops it back around to the end
        if fish_array_position == -1:
            # Set all parameters to be the end of the list
            selected_row = len(fish_displayed) - 1
            fish_array_start = (len(fish_array) - 1) - (len(fish_displayed) - 1)
            fish_array_position = len(fish_array) - 1
        # When the up key is pressed at the top of the list then scroll up
        elif selected_row < 0 and fish_array_position != -1:
            fish_array_start -= 1
            # +1 to set it back to the top of the list making selected row 0
            selected_row += 1

    # If the down key was move down the list
    if key == curses.KEY_DOWN:
        fish_array_position += 1
        # For when the down key is pressed at the end of the list which sets it back to the start
        if fish_array_position > len(fish_array) - 1:
            # Reset all parameters to be the start of the list
            fish_array_start = 0
            selected_row = 0
            fish_array_position = 0
        # When the down key is pressed at the end of the visible list then scroll down
        elif selected_row > len(fish_displayed) - 1:
            fish_array_start += 1
            # -1 to have it keep highlighting the last entry in the list being len(fish_display) - 1
            selected_row -= 1

    return selected_row, fish_array_position, fish_array_start


# Draws the left window and draws a visible box for its outline. Returns the window object
def lhalf_box_draw(scr):
    y, x = scr.getmaxyx()
    begin_y = 0; begin_x = 0
    height = y; width = x // 2
    lscreen = curses.newwin(height, width, begin_y, begin_x)
    lscreen.box()
    lscreen.refresh()

    return lscreen


# Creates the right window and draws a visible box for its outline. Returns the window object
def rhalf_box_draw(scr):
    y, x = scr.getmaxyx()
    begin_y = 0; begin_x = x // 2
    # Width needs to be divided by two otherwise it would be the size of a whole screen
    height = y; width = x // 2
    rscreen = curses.newwin(height, width, begin_y, begin_x)
    rscreen.box()
    rscreen.refresh()

    return rscreen


# Creates the heading parts of a row that is placed above the actual fish list
def create_heading_row(heading_array, scr):
    maxh, maxw = scr.getmaxyx()
    beginy, beginx = scr.getbegyx()
    # Each row has a height of 1 so row_y being the start position of the item in relation to y is always 0
    row_y = 0
    # Start coordinates of the heading section of the screen
    heading_start_y = beginy + 2
    heading_start_x = beginx + 1

    heading_row = curses.newwin(get_row_height(), get_row_width(maxw), heading_start_y, heading_start_x)

    for heading_col in heading_array:
        heading_row.addstr(row_y, heading_col[1], heading_col[0], curses.A_BOLD)

    heading_row.refresh()


# Gets the height of a single row of data. Used to prevent it being a global variable
def get_row_height():
    return 1


# Gets the width of a single row of data being the width of the box - 2. Used to prevent it being a global variable
def get_row_width(max_w):
    return max_w - 2


# Wrapper improves and prevents some issues when running the curses terminal
wrapper(main)
