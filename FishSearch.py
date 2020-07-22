import csv
import curses
#Todo
# Option to Delete/Edit Fish
# Can calculate multiple fish to get a sum of all fish for selling
# Better interface using Curses (List all fish nicely in grid like format)
#
LOCATIONS_CONST = [("1", 'River'), ("2", "Sea"), ("3", "Pond"),("4", "Pier")]


def main():
    # Curses stuff


    if __name__ == '__main__':
        while 1:
            selection = input("Select an Option:\n1.Find Fish\n2.Add Fish\n3.Show All Fish\n4.Delete Fish\n")
            if selection == '1':
                find_fish()
                break
            elif selection == '2':
                add_fish()
                break
            elif selection == '3':
                print(numbered_printable())
                break
            elif selection == '4':
                print(numbered_printable())
                break
            else:
                print("Invalid Input")
        #Add in checking with else and while loop


class Fish:
    def __init__(self, name, price, location):
        self.name = name
        self.price = price
        self.location = location


def add_all_fish(fish_arr):
    arr_length = len(fish_arr)
    with open('testfile.csv','w') as a:
        a.write("Name,Price,Location\n")
        for i in range (0, arr_length):
            a.write(fish_arr[i].name + ',' + str(fish_arr[i].price) + ',' + fish_arr[i].location)
            a.write('\n')


def add_fish():
    valid = 0
    f_name = input("Enter Fish Name: ")
    all_fish = get_all_fish()
    while valid == 0:
        if not f_name.isdigit() and f_name.upper() not in [f_name.upper() for f_name in all_fish[0]]:
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
                          if item[0] == f_location or item[1].upper()== f_location.upper()]

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


def write_fish(fish_obj):
    with open('fishfile.csv', 'a') as a:
        a.write(fish_obj.name + ',' + str(fish_obj.price) + ',' + fish_obj.location)
        a.write('\n')
    return 1


def get_all_fish():
    with open('fishfile.csv','r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        next(csvreader)
        fish_list = list(csvreader)
    return fish_list


def find_fish():
    fish_array = get_all_fish()
    fish_search = 1
    while not fish_search == "0":
        fish_found = 0
        fish_search = input("Enter Fish Name: ")
        print("Search Results:")
        print("----------------------------------------------------------------")
        for fish in fish_array:
            if fish[0].upper().startswith(fish_search.upper()):
                print(fish[0] + " | Price: " + "{:,}".format(int(fish[1])) + " | Location: " + fish[2])
                fish_found = 1
        if fish_found == 0:
            print("No Fish with that name")


def numbered_printable():
    fish_array = get_all_fish()
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
f4 = Fish('Crucian Carp', 120, 'River')
main()