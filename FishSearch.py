import csv
#Todo
# For more extensibility make use of fish.__getattribute("name") rather than fish.name so an array can be used in case
# more attributes are added to the class which would result in more exponential growth of coding

LOCATIONS_CONST = [("1", 'River'), ("2", "Sea"), ("3", "Pond"), ("4", "Pier")]


def main():

    if __name__ == '__main__':
        while 1:
            selection = input("Select an option:\n1.Find Fish\n2.Add Fish\n3.Show All Fish\n4.Delete Fish"
                              "\n5.Edit Fish\n6.Sum Fish\n")
            if selection == '1':
                find_fish()
                break
            elif selection == '2':
                add_fish()
                break
            elif selection == '3':
                print_fish()
                break
            elif selection == '4':
                delete_text_menu()
                break
            elif selection == '5':
                edit_text_menu()
                break
            elif selection == '6':
                select_fish()
                break
            else:
                print("Invalid Input")


class Fish:

    def __init__(self, name=None, price=None, location=None):
        # Must use a different name for the attribute otherwise you get a recursion problem when using the setters
        self._name = name
        self._price = price
        self._location = location

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not new_name.isnumeric():
            self._name = new_name

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if new_price.isdigit() and " " not in new_price and int(new_price) >= 0:
            self._price = new_price

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, new_location):
        # Checking if the set location of the fish is in LOCATIONS_CONST variable
        if new_location in [locations[1] for locations in LOCATIONS_CONST]:
            self._location = new_location


# Method used primarily for testing
def add_all_fish(fish_arr):
    arr_length = len(fish_arr)
    with open('testfile.csv', 'w') as a:
        a.write("Name,Price,Location\n")
        for i in range(0, arr_length):
            a.write(fish_arr[i].name + ',' + str(fish_arr[i].price) + ',' + fish_arr[i].location)
            a.write('\n')


# Text based add menu inputting from user to create a fish in order to be added
def add_fish():
    # Retrieves all fish in  from the most current file
    fish_array = get_fish_objects()
    new_fish = Fish()
    # An array of fish names in uppercase to check against them later to prevent duplicate additions
    checking_array = [fish.name.upper() for fish in fish_array]
    print_fish()
    f_name = input("Enter Fish Name: ")
    while new_fish.name is None:
        # Checks for duplicate names
        if f_name.upper() not in checking_array:
            new_fish.name = f_name
        # Checks that validation in the setter was successful resulting in a name being set
        if new_fish.name is None:
            f_name = input("Fish either exists or invalid name. Please enter a valid fish name: ")

    f_price = input("Enter Fish Price: ")
    while new_fish.price is None:
        new_fish.price = f_price
        if new_fish.price is None:
            f_price = input("Please enter a valid fish price: ")

    # This section is used to display the menu of location options correctly with no hanging comma

    input_text = locations_text()

    f_location = input(input_text)

    while new_fish.location is None:
        new_fish.location = f_location
        if new_fish.location is None:
            f_location = input("Please enter a valid location as either " + input_text)

    if write_fish(new_fish):
        print("----------------------------------------------------------------")
        print("Fish Added Successfully ")
        print("----------------------------------------------------------------")
        
    repeat = input("Would you like to add another fish?: ")
    if repeat == "1" or repeat.upper() == "YES":
        add_fish()


# Code to add a fish to the csv file
# Assumes completed validation
def write_fish(fish_obj):
    with open('fishfile.csv', 'a') as a:
        a.write(fish_obj.name + ',' + str(fish_obj.price) + ',' + fish_obj.location)
        a.write('\n')
    return 1


# Gets the csv file of all fish in 2d array format
def get_fish_array():
    with open('fishfile.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        next(csvreader)
        fish_array = list(csvreader)
    return fish_array


# Translates fish array into the object counterpart and returns an array of objects
def get_fish_objects():
    fish_array = get_fish_array()
    fish_objects = []
    for fish in fish_array:
        fish_objects.append(Fish(fish[0], fish[1], fish[2]))
    return fish_objects


# Searches for a fish based on user input and can search using only the start of the name
def find_fish():
    fish_array = get_fish_objects()
    fish_search = 1
    while not fish_search == "0":
        fish_found = 0
        fish_search = input("Enter Fish Name: ")
        print("Search Results:")
        print("----------------------------------------------------------------")
        for fish in fish_array:
            if fish.name.upper().startswith(fish_search.upper()):
                print(fish.name + " | Price: " + "{:,}".format(int(fish.price)) + " | Location: " + fish.location)
                fish_found = 1
        if fish_found == 0:
            print("No Fish with that name")


# Text based delete menu
def delete_text_menu():
    valid = False
    print_fish()
    fish_array = get_fish_objects()
    # Loops until a valid fish is deleted
    while not valid:
        fish_name = input("Enter the name of the fish you wish to delete: ")
        # Checks if the fish exists in the file using the name given
        for fish in fish_array:
            if fish.name.upper() == fish_name.upper():
                valid = 1
                break
        # If valid run the delete code and loop will complete
        if valid:
            delete_fish(fish_name)
            print("Fish was deleted successfully")
        else:
            print("Fish by that name does not exist")


# Delete Command
# Deletes fish from file by taking fish_name from user input and recreating the file. Assumes validation completed
def delete_fish(fish_name):
    fish_array_cur = get_fish_objects()
    fish_array_new = []
    # Creates array of all existing fish except fish to be removed
    for fish in fish_array_cur:
        if fish.name.upper() != fish_name.upper():
            fish_array_new.append(fish)

    # Writes to file using updated array of fish
    arr_length = len(fish_array_new)
    with open('fishfile.csv', 'w') as a:
        a.write("Name,Price,Location\n")
        for i in range(0, arr_length):
            a.write(fish_array_new[i].name + ',' + str(fish_array_new[i].price) + ',' + fish_array_new[i].location)
            a.write('\n')


# Text based edit menu for selecting a fish and editing their values
def edit_text_menu():
    fish_array = get_fish_objects()
    checking_array = [fish.name.upper() for fish in fish_array]
    chosen_fish = Fish()
    valid = False
    print_fish()
    old_name = input("Please enter the name of the fish you wish to change: ")
    while not valid:
        if old_name.upper() in checking_array:
            valid = True
        else:
            old_name = input("Fish doesn't exist. Please try again: ")

    f_name = input("Enter New Fish Name: ")
    while chosen_fish.name is None:
        # Checks that the same name is valid as long as it does not match the name of other fish as long as
        if f_name.upper() not in checking_array or f_name.upper() == old_name.upper():
            chosen_fish.name = f_name
        # If chosen fish name is still none then some error must have occured during setter validation
        if(chosen_fish.name is None):
            f_name = input("Fish either exists or invalid name. Please enter a valid fish name: ")

    f_price = input("Enter New Fish Price: ")
    while chosen_fish.price is None:
        chosen_fish.price = f_price
        # Only validation required is performed in the setter
        if chosen_fish.price is None:
            f_price = input("Please enter a valid fish price: ")

    input_text = locations_text()

    f_location = input(input_text)

    while chosen_fish.location is None:
        chosen_fish.location = f_location
        # Only validation required is performed in the setter
        if chosen_fish.location is None:
            f_location = input("Please enter a valid location as either " + input_text)

    # Since all previous checks have been valid then edit fish
    edit_fish(old_name, f_name, f_price, f_location)


# Edits fish in file by taking fish_name and new values from user input and recreating the file.
# Assumes validation completed
def edit_fish(fish_name, new_name, new_price, new_location):
    fish_array = get_fish_objects()
    for fish in fish_array:
        if fish.name.upper() == fish_name.upper():
            fish.name = new_name
            fish.price = new_price
            fish.location = new_location
            break

    # Writes to file using updated array of fish
    arr_length = len(fish_array)
    with open('fishfile.csv', 'w') as a:
        a.write("Name,Price,Location\n")
        for i in range(0, arr_length):
            a.write(fish_array[i].name + ',' + str(fish_array[i].price) + ',' + fish_array[i].location)
            a.write('\n')


# Sums together the price of fish using a numeric array of values and returns total profit
def sum_fish(fish_prices):
    total_profit = 0
    for prices in fish_prices:
        total_profit += int(prices)

    return total_profit


# Text based function to allow user to select which fish to add for summing the total amount of fish
def select_fish():
    fish_array = get_fish_objects()
    print_fish()
    finished = 0
    fish_name = input("Choose which fish to sum together: ")
    fish_selected_array = []
    # Continue looping until user has finished choosing all fish they wish to sum
    while finished == 0:
        valid = False
        while not valid:
            for fish in fish_array:
                if fish_name.upper() == fish.name.upper():
                    valid = True
                    fish_selected_array.append(fish)
            if not valid:
                fish_name = input("Fish doesn't exist. Please try again: ")

        print("Current Fish:")
        for i in range(0, len(fish_selected_array)):
            print(fish_selected_array[i].name)

        fish_name = input("Add another fish (Type 0 if finished): ")
        if fish_name == '0':
            finished = 1

    sum_display(fish_selected_array)


# Displays all fish that were part of the calculation along with the total profit
def sum_display(fish_array):
    # Test array used. In practice they should be able to choose which fish/how many of that fish, etc
    # Gets only the prices of the fish from the array
    fish_prices = [fish.price for fish in fish_array]
    total_profit = sum_fish(fish_prices)
    print("---------------------------------------------\nFish List")
    for fish in fish_array:
        print(fish.name + " " + fish.price)
    print("---------------------------------------------\nTotal Profit: " + str(total_profit))


# Prints out all of the fish in a nice format
def print_fish():
    fish_array = get_fish_array()
    fish_text = ""
    for idx, listed in enumerate(fish_array):
        fish_text += str(idx+1) + ". "
        counter = 0
        for data in listed:
            if counter == 0:
                fish_text += "Name: "
                fish_text += data + " | "
            elif counter == 1:
                fish_text += "Price: "
                fish_text += data + " | "
            elif counter == 2:
                fish_text += "Location: "
                fish_text += data
            counter += +1
        fish_text += "\n"
    print(fish_text)


# Used to print out all locations in the proper format (No trailing comma)
def locations_text():
    text = ""
    for idloc, location in LOCATIONS_CONST:
        text += str(idloc) + "." + location
        if int(idloc) < len(LOCATIONS_CONST):
            text += ", "
        else:
            text += ": "
    return text


f1 = Fish('Dorado', 15000, 'River')
f2 = Fish('Sweetfish', 900, 'River')
f3 = Fish('Pufferfish', 250, 'Sea')
fish_test_array = [f1, f2, f3]
get_fish_objects()
main()
