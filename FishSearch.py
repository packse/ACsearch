import csv
import curses
#Todo
# Can calculate multiple fish to get a sum of all fish for selling
# Better interface using Curses (List all fish nicely in grid like format)
# For more extensibility make use of fish.__getattribute("name") rather than fish.name so an array can be used in case
# more attributes are added to the class which would result in more exponential growth of coding

LOCATIONS_CONST = [("1", 'River'), ("2", "Sea"), ("3", "Pond"),("4", "Pier")]


def main():
    # Curses stuff

    if __name__ == '__main__':
        while 1:
            selection = input("Select an Option:\n1.Find Fish\n2.Add Fish\n3.Show All Fish\n4.Delete Fish\n5.Edit Fish\n")
            if selection == '1':
                find_fish()
                break
            elif selection == '2':
                add_fish()
                break
            elif selection == '3':
                print(print_fish())
                break
            elif selection == '4':
                delete_text_menu()
                break
            elif selection == '5':
                edit_text_menu()
                break
            else:
                print("Invalid Input")


class Fish:
    def __init__(self, name, price, location):
        self.name = name
        self.price = price
        self.location = location

# Method used primarily for testing
def add_all_fish(fish_arr):
    arr_length = len(fish_arr)
    with open('testfile.csv','w') as a:
        a.write("Name,Price,Location\n")
        for i in range (0, arr_length):
            a.write(fish_arr[i].name + ',' + str(fish_arr[i].price) + ',' + fish_arr[i].location)
            a.write('\n')

# Text based add menu inputting from user to create a fish in order to be added
def add_fish():
    valid = 0
    fish_array = get_fish_objects()
    # An array of fish names in uppercase to check against them later to prevent duplicate additions
    checking_array = [fish.name.upper() for fish in fish_array]
    print(print_fish())
    f_name = input("Enter Fish Name: ")
    while valid == 0:
        # Checks for digits in name or duplicate names
        if (f_name.isalpha()) and (f_name.upper() not in checking_array):
            valid = 1
        else:
            f_name = input("Fish either exists or invalid name. Please enter a valid fish name: ")

    valid = 0
    f_price = input("Enter Fish Price: ")
    while valid == 0:
        if f_price.isdigit() and " " not in f_price:
            valid = 1
        else:
            f_price = input("Please enter a valid fish price: ")

    valid = 0
    # This section is used to display the menu of location options correctly with no hanging comma
    input_text = ""
    for idloc, location in LOCATIONS_CONST:
        input_text += str(idloc) + "." + location
        if int(idloc) < len(LOCATIONS_CONST):
            input_text += ", "
        else:
            input_text += ": "

    f_location = input(input_text)

    while valid == 0:
        location_index = [item
                          for item in LOCATIONS_CONST
                          if item[0] == f_location or item[1].upper() == f_location.upper()]

        if not location_index == []:
            f_location = location_index[0][1]
            valid = 1
        else:
            f_location = input("Please enter a valid location as either " + input_text)

    if write_fish(Fish(f_name, f_price, f_location)):
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
    with open('fishfile.csv','r') as csvfile:
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
            if fish. upper().startswith(fish_search.upper()):
                print(fish.name + " | Price: " + "{:,}".format(int(fish.price)) + " | Location: " + fish.location)
                fish_found = 1
        if fish_found == 0:
            print("No Fish with that name")


# Text based delete menu
def delete_text_menu():
    valid = 0
    print(print_fish())
    fish_array = get_fish_objects()
    # Loops until a valid fish is deleted
    while valid == 0:
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
    with open('fishfile.csv','w') as a:
        a.write("Name,Price,Location\n")
        for i in range (0, arr_length):
            a.write(fish_array_new[i].name + ',' + str(fish_array_new[i].price) + ',' + fish_array_new[i].location)
            a.write('\n')


# Text based edit menu for selecting a fish and editing their values
def edit_text_menu():
    fish_array = get_fish_objects()
    checking_array = [fish.name.upper() for fish in fish_array]
    valid = 0
    print(print_fish())
    old_name = input("Please enter the name of the fish you wish to change: ")
    while valid == 0:
        if old_name.upper() in checking_array:
            valid = 1
        else:
            old_name = input("Fish doesn't exist. Please try again: ")

    valid = 0
    f_name = input("Enter New Fish Name: ")
    while valid == 0:
        # Checks that only letters are in name and that the new name does not match the name of other fish as long as
        # it matches the name of the fish to be edited
        if (f_name.isalpha()) and ((f_name.upper() not in checking_array) or f_name.upper() == old_name.upper()):
            valid = 1
        else:
            f_name = input("Invalid name. Please enter a valid fish name: ")

    valid = 0
    f_price = input("Enter New Fish Price: ")
    while valid == 0:
        if f_price.isdigit() and " " not in f_price:
            valid = 1
        else:
            f_price = input("Please enter a valid fish price: ")

    valid = 0
    # This is used to display the menu of location options correctly with no hanging comma
    input_text = ""
    for idloc, location in LOCATIONS_CONST:
        input_text += str(idloc) + "." + location
        if int(idloc) < len(LOCATIONS_CONST):
            input_text += ", "
        else:
            input_text += ": "

    f_location = input(input_text)

    while valid == 0:
        location_index = [item
                          for item in LOCATIONS_CONST
                          if item[0] == f_location or item[1].upper() == f_location.upper()]

        if not location_index == []:
            f_location = location_index[0][1]
            valid = 1
        else:
            f_location = input("Please enter a valid location as either " + input_text)

    # Since all previous checks have been valid then edit fish
    edit_fish(old_name,f_name,f_price,f_location)


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


# Sums together the values of multiple fish to get a total
def sum_fish(fish_sum_array):
    print("PLACEHOLDER")
    # Receives the prices of selected fish through an array and sums them together to get the total value
    # Want to display all of the fish chosen with their prices and the total profit at the bottom


#Prints out all of the fish in a nice format
def print_fish():
    fish_array = get_fish_array()
    fish_text = ""
    for idx, list in enumerate(fish_array):
        fish_text += str(idx+1) + ". "
        counter = 0
        for data in list:
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
    return(fish_text)


f1 = Fish('Dorado', 15000, 'River')
f2 = Fish('Sweetfish', 900, 'River')
f3 = Fish('Pufferfish', 250, 'Sea')
fish_test_array = [f1, f2, f3]
f4 = Fish('Crucian Carp', 120, 'River').__getattribute__("name")
print(f4)
get_fish_objects()
main()