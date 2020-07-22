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

