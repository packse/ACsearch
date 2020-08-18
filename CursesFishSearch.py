import curses
from curses import wrapper
import FishSearch as fs

query = ""

# Todo
# Proper Confirm/Cancel and going back to the previous screen should be implemented
# Could replace the entering of data one by one and instead have multiple fields and being able to tab between them
# Resize error needs to be handled either by exception or using the os library to resize the terminal before crash
# When pressing enter the currently selected row is remembered so it doesn't start at the top of the list



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
    global query
    # Remove box around the mainscr
    scr.clear()
    scr.refresh()
    # Current screen begin as the left screen
    current_screen = "left"
    # rscreen starts empty but is filled depending on the selection by the user.
    rscreen_fish_array = []

    # Draw the left and right screens with header data and footer text
    lscreen = lhalf_box_create(scr)
    rscreen = rhalf_box_create(scr)
    while 1:
        if current_screen == "left":
            fish_selected, key_pressed = lscreen_fish_menu(scr, lscreen, 0)
            if key_pressed == curses.KEY_ENTER or key_pressed in [10, 13]:
                rscreen_fish_array.append(fish_selected)
                rscreen_fish_menu(scr, rscreen, rscreen_fish_array)
            # If the right key is pressed and there are fish displayed on the right screen to select from
            elif key_pressed == curses.KEY_RIGHT and len(rscreen_fish_array) > 0:
                # Set the current usable screen to right
                query = ""
                current_screen = "right"
        elif current_screen == "right":
            fish_name, skip_num, key_pressed = rscreen_fish_menu(scr, rscreen, rscreen_fish_array, 0)
            # If enter pressed remove selected fish from right screen
            if key_pressed == curses.KEY_ENTER or key_pressed in [10, 13]:
                # Removes fish from the array using the name and how many increments it is.
                # E.g. A skip_num of 1 would mean that it needs to skip 1 fish with the same fish_name and delete the
                # next fish with the value of fish name
                array_index = 0
                while skip_num != -1:
                    if rscreen_fish_array[array_index].name == fish_name:
                        skip_num -= 1
                    array_index += 1
                rscreen_fish_array.pop(array_index-1)
                # Need to clear and redraw the entire screen to remove list items
                rscreen.clear()
                rscreen = rhalf_box_create(scr)
                # If the size of the fish array for the right screen is empty change usable screen to the left screen
                if len(rscreen_fish_array) <= 0:
                    current_screen = "left"
            # If left key is pressed when on the right screen
            elif key_pressed == curses.KEY_LEFT:
                # Change the current usable screen to left
                query = ""
                current_screen = "left"

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
        #If the key is a character or spacebar
        elif 97 <= key <= 122 or key == 32:
            selected_row = 0
            return selected_row, key
        #If the key is backspace
        elif key == curses.KEY_BACKSPACE or 8:
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
def lscreen_fish_menu(mainscr, scr, selected_row=None):
    global query
    # Get the full number of fish that exist into an array
    full_fish_array = fs.get_fish_objects()
    # The starting position that the loop will read from when going through fish array. Required to allow for scrolling
    fish_array_start = 0
    # The position of the selected fish in relation to the whole array as opposed to the array of fish being displayed
    fish_array_position = 0
    # Creates search screen window with the proper dimensions
    searchscreen = search_box_create(mainscr)
    # Query begins empty
    search_box_fill(searchscreen)

    while 1:
        lhalf_box_create(mainscr)
        search_box_fill(searchscreen)
        fish_array = full_fish_array
        # Depending on the search query change which fish are now displayed
        if len(query) > 0:
            fish_array = [fish for fish in fish_array if fish.name[0:len(query)].lower() == query]

        fish_displayed = fill_box(scr, selected_row, fish_array, fish_array_start, "left")

        # Determines if the list is read only or if it can be navigated through
        if selected_row is not None:
            selected_row, key = keyboard_movement_ud(mainscr, selected_row)
            # If the enter key or right key is pressed return the selected fish with the key
            if key == curses.KEY_ENTER or key in [10, 13] and len(fish_displayed) > 0:
                # Return the selected fish along with the row data to clear highlight and the key pressed
                return fish_displayed[selected_row], key
            elif key == curses.KEY_RIGHT:
                # Refills the left box with all the items in the array
                fill_box(scr, None, full_fish_array, 0, "left")
                # Returns something for the fish_selected to prevent missing data errors
                return None, key
            elif 97 <= key <= 122 or key == 32:
                query += get_character(key)
                fish_array_position = 0
                fish_array_start = 0
            elif key == curses.KEY_BACKSPACE or key == 8 and query != "":
                query = query[:-1]
            # If up or down key is pressed determine how it should be handled
            elif key == curses.KEY_UP or key == curses.KEY_DOWN:
                selected_row, fish_array_position, fish_array_start = keyboard_selection(key, fish_array_position,
                                                                                         selected_row, fish_array_start,
                                                                                         fish_array, fish_displayed)
        # If the list doesn't react to user input exit the loop and therefore the function
        else:
            break


# Returns the selected fish after pressing enter. Selected row can be none for when the screen shouldn't be controllable
def rscreen_fish_menu(mainscr, scr, fish_array, selected_row=None):
    global query
    # rscreen will show fish received through the function parameter based on user selection
    # The starting position that the loop will read from when going through fish array. Required to allow for scrolling
    fish_array_start = 0
    # The position of the selected fish in relation to the whole array as opposed to the array of fish being displayed
    fish_array_position = 0
    full_fish_array = fish_array
    # Creates search screen window with the proper dimensions
    searchscreen = search_box_create(mainscr)
    # Query begins empty
    search_box_fill(searchscreen)

    while 1:
        rhalf_box_create(mainscr)
        search_box_fill(searchscreen)
        fish_array = full_fish_array
        # Depending on the search query change which fish are now displayed as long as the right screen is being used
        if len(query) > 0 and selected_row is not None:
            fish_array = [fish for fish in fish_array if fish.name[0:len(query)].lower() == query]

        create_footer_row(fish_array, scr)
        # The fish currently being shown on the screen since the screen size can vary. Clears itself when loop restarts
        fish_displayed = fill_box(scr, selected_row, fish_array, fish_array_start, "right")

        # Determines if the list is read only or if it can be navigated through
        if selected_row is not None:
            selected_row, key = keyboard_movement_ud(mainscr, selected_row)
            # If the enter key is pressed return the selected fish
            if key == curses.KEY_ENTER or key in [10, 13]:
                # This function is required to get the correct position when the search menu is being used
                # How many times the loop in profit_menu must continue in order to get the correct position of which
                # fish to delete
                num_fish_before = 0
                fish_name = fish_displayed[selected_row].name
                i = 0
                while i != selected_row:
                    # If the name of the selected fish is the same as the current then there exists one additional fish
                    if fish_displayed[i].name == fish_name:
                        # Increment the number of same name fish before the selected fish by one
                        num_fish_before += 1
                    i += 1
                # Return the position the fish to be deleted is in the array, the fish displayed data which contains
                # information on the row to clear highlighting and the key pressed
                return fish_name, num_fish_before, key
            elif key == curses.KEY_LEFT:
                # Refills the right box with all the items in the array and the array sum
                fill_box(scr, None, full_fish_array, 0, "right")
                create_footer_row(full_fish_array, scr)
                # Returns something for the fish_selected to prevent missing data errors
                return None, None, key
            elif 97 <= key <= 122 or key == 32:
                query += get_character(key)
                fish_array_start = 0
                fish_array_position = 0
            elif key == curses.KEY_BACKSPACE or key == 8 and query != "":
                query = query[:-1]
            # If up or down was pressed determine how it should be handled
            elif key == curses.KEY_UP or key == curses.KEY_DOWN:
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


# Creates the search window by setting up the dimensions and returns it as an object
def search_box_create(scr):
    maxh, maxw = scr.getmaxyx()
    begin_y = 3; begin_x = 0
    smaxh = 2; smaxw = maxw//3
    searchscreen = curses.newwin(smaxh, smaxw, begin_y, begin_x)

    return searchscreen


# Fills the search box with the current search query. Returns the updated query for when its size needs to be reduced
def search_box_fill(scr):
    global query
    scr.clear()
    maxy, maxx = scr.getmaxyx()
    box_start_x = 1
    box_start_y = 1
    prompt = "Search: "
    available_space = maxx - len(prompt) - box_start_x
    scr.addstr(box_start_y, box_start_x, prompt, curses.A_BOLD)
    # Ensures there is enough space in the search box to add another character
    if len(query) < available_space:
        scr.addstr(query)
        scr.refresh()
    else:
        query = query[:-1]
    return query


# Draws the left window and draws a visible box for its outline. Returns the window object
def lhalf_box_create(scr):
    maxh, maxw = scr.getmaxyx()
    begin_y = 5; begin_x = 0
    lmaxh = maxh - begin_y; lmaxw = maxw // 2
    lscreen = curses.newwin(lmaxh, lmaxw, begin_y, begin_x)
    lscreen.box()
    lscreen.refresh()

    # The width of each row window
    row_scr_width = get_row_width(lmaxw)

    # x positions that the text on the screen starts at
    name_pos = 0
    price_pos = row_scr_width // 2
    location_pos = row_scr_width - (row_scr_width // 4)
    # The heading items in the array and the position that they will be on the screen
    heading_and_pos = [["Name", name_pos], ["Price", price_pos], ["Location", location_pos]]

    # Creates the heading row and heading data
    create_heading_row(heading_and_pos, lscreen)

    return lscreen


# Creates the right window and draws a visible box for its outline. Returns the window object
def rhalf_box_create(scr):
    maxh, maxw = scr.getmaxyx()
    begin_y = 5; begin_x = maxw // 2
    # Width needs to be divided by two otherwise it would be the size of a whole screen
    rmaxh = maxh - begin_y; rmaxw = maxw // 2
    rscreen = curses.newwin(rmaxh, rmaxw, begin_y, begin_x)
    rscreen.box()
    rscreen.refresh()

    # The size of each row window leaving space for the footer
    row_scr_width = rmaxw - 2

    # x positions that the text on the screen starts at
    name_pos = 0
    price_pos = row_scr_width - (row_scr_width // 7)
    # The heading items in the array and the position that they will be on the screen sent as a 2d array
    heading_and_pos = [["Name", name_pos], ["Price", price_pos]]

    # Creates the heading row and heading data
    create_heading_row(heading_and_pos, rscreen)

    return rscreen

# Fills the box with all fish that can fit the display and sets the selected row
def fill_box(scr, selected_row, fish_array, fish_array_start, scr_side):
    # The fish currently being shown on the screen since the screen size can vary.
    fish_displayed = []

    maxh, maxw = scr.getmaxyx()
    beginy, beginx = scr.getbegyx()
    # The last row that text can be placed in
    # The size of each row window
    row_scr_height = get_row_height()
    row_scr_width = get_row_width(maxw)
    name_pos = 0
    price_pos = 0
    location_pos = 0
    ending_row = 0

    if scr_side == "left":
        # x positions that the text on the screen starts at
        name_pos = 0
        price_pos = row_scr_width // 2
        location_pos = row_scr_width - (row_scr_width // 4)
        ending_row = maxh + beginy - 1
    elif scr_side == "right":
        name_pos = 0
        price_pos = row_scr_width - (row_scr_width//7)
        ending_row = maxh + beginy - 2

    # Each row has a height of 1 so row_y being the start position of the item in relation to y is always 0
    row_y = 0

    # Loops through the array from the start of what is displayed to the end of what is displayed
    for idx, row in enumerate(fish_array[fish_array_start:len(fish_array)]):
        # The position the new window starts getting created from
        start_y = beginy + 2 + idx
        start_x = beginx + 1
        # Only adds next row if it won't overflow off screen
        if start_y < ending_row:
            # Creates a new window that will store a row's worth of fish data including name, price, location
            scr_row = curses.newwin(row_scr_height, row_scr_width, start_y, start_x)

            # Checking if the menu is selectable to decide if highlighting the row is valid
            if selected_row is not None:
                if selected_row == idx:
                    scr_row.bkgd(' ', curses.color_pair(1))

            if scr_side == "left":
                scr_row.addstr(row_y, name_pos, row.name)
                scr_row.addstr(row_y, price_pos, row.price)
                scr_row.addstr(row_y, location_pos, row.location)
            elif scr_side == "right":
                scr_row.addstr(row_y, name_pos, row.name)
                scr_row.addstr(row_y, price_pos, row.price)

            scr_row.refresh()
            fish_displayed.append(row)
        else:
            break

    return fish_displayed

# Creates the heading parts of a row that is placed above the actual fish list
def create_heading_row(heading_array, scr):
    maxh, maxw = scr.getmaxyx()
    beginy, beginx = scr.getbegyx()
    # Each row has a height of 1 so row_y being the start position of the item in relation to y is always 0
    row_y = 0
    # Start coordinates of the heading section of the screen
    heading_start_y = beginy + 1
    heading_start_x = beginx + 1

    heading_row = curses.newwin(get_row_height(), get_row_width(maxw), heading_start_y, heading_start_x)

    for heading_col in heading_array:
        heading_row.addstr(row_y, heading_col[1], heading_col[0], curses.A_BOLD)

    heading_row.refresh()


# Create the sum data appended to the bottom of the footer with all of the selected fish
def create_footer_row(fish_array, scr):
    maxh, maxw = scr.getmaxyx()
    fish_total = 0

    if len(fish_array) > 0:
        fish_prices = [int(item.price) for item in fish_array]
        fish_total = fs.sum_fish(fish_prices)

    footer_start_y = maxh + 3
    footer_start_x = maxw + 1

    # Each row has a height of 1 so row_y being the start position of the item in relation to y is always 0
    row_y = 0

    footer_row = curses.newwin(get_row_height(), get_row_width(maxw), footer_start_y, footer_start_x)

    maxhf, maxwf = footer_row.getmaxyx()

    footer_row.addstr(row_y, maxwf-(maxwf//4), "Sum", curses.A_BOLD)
    footer_row.addstr(row_y, maxwf-(maxwf//7), str(fish_total), curses.A_BOLD)
    footer_row.refresh()



# Gets the height of a single row of data. Used to prevent it being a global variable
def get_row_height():
    return 1


# Gets the width of a single row of data being the width of the box - 2. Used to prevent it being a global variable
def get_row_width(max_w):
    return max_w - 2

# Gets the corresponding value of key and returns its actual character
def get_character(key):
    key_dict = {
        32: " ", 97: "a", 98: "b", 99: "c", 100: "d", 101: "e", 102: "f", 103: "g", 104: "h",
        105: "i", 106:"j", 107: "k", 108: "l", 109: "m", 110: "n", 111: "o", 112: "p",
        113: "q", 114: "r", 115: "s", 116: "t", 117: "u", 118: "v", 119: "w",
        120: "x", 121: "y",  122: "z"
    }
    return key_dict[key]





# Wrapper improves and prevents some issues when running the curses terminal
wrapper(main)