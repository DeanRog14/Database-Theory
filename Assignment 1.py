filename = 'part.tbl'

def open_data():
    dataset = []

    with open(filename, "r") as file:
        # Splits the file apart to make easier to change
        for line in file: 
            values = line.strip().split("|")
            # Adds all information to a dictionary to make changes to the dataset easier
            dataset.append({
                "PARTKEY" : values[0],
                "NAME" : values[1],
                "MFGR" : values[2],
                "BRAND" : values[3],
                "TYPE" : values[4],
                "SIZE" : values[5],
                "CONTAINER" : values[6],
                "RETAILPRICE" : values[7],
                "COMMENT" : values[8]
            })

    return dataset


def add_item(dataset):
    new_item = {}

    # Iterates through each selection to add new information to the item
    for selection in ["PARTKEY", "NAME", "MFGR", "BRAND", "TYPE", "SIZE", "CONTAINER", "RETAILPRICE", "COMMENT"]:
        new_item[selection] = input(f'Enter {selection}: ')

    # Adds the item to dataset
    dataset.append(new_item)

def search_item(dataset):
    # Searches for item based on attribute, looks for item, then checks if it matches attribute, then prints
    searched_attribute = input("What attribute would you like to search for? (PARTKEY, NAME, BRAND, or TYPE) ")
    searched_value = input(f'Enter value from {searched_attribute} that you want: ')
    for item in dataset:
       if item.get(searched_attribute, "").lower() == searched_value.lower():
            print(item)

def update_item(dataset):
    # Finds the specified PARTKEY in the dataset
    partkey_searched = input("What PARKTEY would like to update the information from?")
    for item in dataset:
        if item["PARTKEY"] == partkey_searched:
            # Prompts user to update each selection if they would like
            for selection in ["PARTKEY", "NAME", "MFGR", "BRAND", "TYPE", "SIZE", "CONTAINER", "RETAILPRICE", "COMMENT"]:
                new_selection = input("Enter " + selection + ": ")
                # If this is in fact a new selection then add the new selection as an item to the dataset
                if new_selection:
                    item[selection] = new_selection

def delete_item(dataset):
    # Finds the specified PARTKEY in the dataset
    partkey_searched = input("What PARKTEY would like to delete the information from?")
    for item in dataset:
        # Removes the item from the dataset based on the specified PARTKEY
        if item["PARTKEY"] == partkey_searched:
            dataset.remove(item)

def save_dataset(dataset):
    # Re-opens the file for writing
    with open(filename, "w") as file:
        for item in dataset:
            # Creates a row by joining each piece of information together with the pipe-sign 
            row = "|".join([
                str(item["PARTKEY"]),
                str(item["NAME"]),
                str(item["MFGR"]),
                str(item["BRAND"]),
                str(item["TYPE"]),
                str(item["SIZE"]),
                str(item["CONTAINER"]),
                str(item["RETAILPRICE"]),
                str(item["COMMENT"])
            ])
            # Writes the created row back to the file
            file.write(row + "\n")

def main():
    dataset = open_data()

    while True:
        # Prompts the user to pick which action they want to be done
        print(" Actions able to be completed ")
        print(" 1. Insert new Item")
        print(" 2. Search for am Item")
        print(" 3. Update an Item")
        print(" 4. Delete an Item")
        print(" 5. Exit the program ")
        answer = input("Enter the number of the action you want to complete? ")

        # Based on the user input the selection action will be perfromed 
        if (answer == "1"):
            add_item(dataset)
        elif (answer == "2"):
            search_item(dataset)        
        elif (answer == "3"):
            update_item(dataset)
        elif (answer == "4"):
            delete_item(dataset)
        else:
            save_dataset(dataset)
            break

main()