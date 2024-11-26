'''
OOP database system project
#Todo: Fix console output formatting
#Todo: Testing and Bugfixes
#Todo: Remove Category if empty?
'''

class InventoryManagementSystem:
    '''
    Class of the system
    '''

    def __init__(self):
        '''
        Class Constructor
        '''

        self.categories: set[str] = set()
        self.inventory: dict[str,dict[str,list[int|float]]] = dict()
        self.transactions: list[str] = list()

    def main_loop(self) -> None:
        '''
        Main Function of the program
        '''

        while True:
            print("""
Inventory Management System
    1. Add Item
    2. Edit Item Quantity
    3. Delete Item
    4. Display Inventory by Category
    5. Summary Report
    6. Transaction History
    7. Exit
""")
            choice : str = input("\t Choose an option (1-7): ")

            if choice == '1':
                self.add_item()
            elif choice == '2':
                self.edit()
            elif choice == '3':
                self.delete()
            elif choice == '4':
                self.display()
            elif choice == '5':
                self.summary()
            elif choice == '6':
                self.show_transactions()
            elif choice == '7':
                break
            else:
                print("Invalid option. Please choose a valid option.")

    def is_int(self, num: str) -> bool:
        '''
        Check if an argumnt can be converted to type `int` 
        and returns a boolean
        '''

        try:
            int(num)
            return True
        except ValueError:
            return False

    def is_float(self, num: str) -> bool:
        '''
        Check if an argumnt can be converted to type `float` 
        and returns a boolean
        '''

        try:
            float(num)
            return True
        except ValueError:
            return False

    def is_valid_name(self, string: str) -> bool:
        '''
        Helper function that checks if inputted string is valid 
        '''

        #! Empty string input
        if string.strip() == "":
            print("Name cannot be empty")
            return False

        #! First letter is not alnum
        if string[0].isalnum():
            print("Name must start with an alphanumeric character")
            return False

        return True


    def add_item(self) -> None:
        '''
        Prompts the user to input the necessary params 
        create/add items in the inventory system
        '''

        item: str = input("Enter item name: ")

        #! Item name errors
        if not self.is_valid_name(item):
            item = item.rstrip()
            return None


        category: str = input("Enter category: ")

        #! Category name errors
        if not self.is_valid_name(category):
            category = category.rstrip()
            return None

        #! Item already exists in the categry error
        if (category in self.categories) and (item in self.inventory[category]):
            choice: str = input("No duplicate items(enter `y` to update instead): ").lower()
            if choice == 'y':
                self.item_edit(category,item)
            return None

        quantity_input:str = input("Enter quantity: ")

        #! Quantity not an integer input error
        if not self.is_int(quantity_input):
            print("Invalid quantity. Please enter a number")
            return None

        quantity:int = int(quantity_input)

        #! Quantity is less than 0 error
        if quantity < 0:
            print("Quantity must be equal to or greater than 0")
            return None

        price_input:str = input("Enter price: ")

        #! Price not float type input error
        if not self.is_float(price_input):
            print("Invalid quantity. Please enter a number")
            return None
        price:float = float(price_input)

        #! Price is less than 0 error
        if price < 0:
            print("Price must be equal to or greater than 0")
            return None

        #* Adding item to inventory based if item is already known
        if category not in self.categories:
            self.categories.add(category)
            self.inventory[category] = {item: [quantity, price]}
            transaction: str  = (
f"Created `{category}` with item: `{item}` that has quantity: {quantity} and price: {price} "                                 
                                 )
        else:
            self.inventory[category][item] = [quantity,price]
            transaction = (
f"Added `{item}` to `{category}` with a quantity: {quantity} and price: {price} " 
                           )

        self.update_transactions(transaction)


    def item_edit(self,category:str, item:str):
        '''
        Helper function that chanages quantity of an item
        '''

        update_input: str = input(
            "Enter the quantity change (positive to add, negative to remove): ")

        #! Check if input is int
        if not self.is_int(update_input):
            print("Invalid quantity. Please enter a number")
            return None

        update:int = int(update_input)

        #! Input results to negative quantity
        if self.inventory[category][item][0] + update < 0:
            choice:str = input("Quantity must be equal to or greater than 0.\n"
                               "Delete instead? (enter `y` to contiue): "
                               ).lower()
            if choice == 'y':
                self.item_deleter(category,item)
            return None

        #* Updates the quantity of the item
        self.inventory[category][item][0] += update
        transaction: str = f"Item `{item}` quantity updated to {self.inventory[category][item][0]}"
        self.update_transactions(transaction)

    def edit(self) -> None:
        '''
        Prompts the user to enter the necessary params and
        updates the quantity by adding the `update` input
        to the existing data
        '''

        category: str = input("Enter the category of the item to update: ")

        #! Category not found error
        if category not in self.categories:
            print("Category not found in the inventory")
            return None

        #! Item not found error
        item: str = input("Enter the name of the item to update: ")
        if item not in self.inventory[category]:
            print("Item not found in the inventory")
            return None

        self.item_edit(category,item)

    def item_deleter(self,category: str, item: str) -> None:
        '''
        Helper function that removes an item from the data structure
        '''

        #! Error for item not found in inventory
        if item not in self.inventory[category]:
            print("Item is not in the inventory")

        #* Remove the item from the inventory
        self.inventory[category].pop(item)
        transaction: str = f"{item} removed from the inventory"
        self.update_transactions(transaction)


    def delete(self) -> None:
        '''
        Function that prompts the user to delete a specific item
        '''

        category: str = input("Enter the category of the item to delete: ")

        #! category not found error
        if category not in self.categories:
            print("Category not found in the inventory")
            return None

        item: str = input("Enter the name of the item to delete: ")
        #! item not found error
        if not item in self.inventory[category]:
            print("Item not found in the inventory")
            return None

        self.item_deleter(category,item)

    def display(self) -> None:
        '''
        Function that shows the data structure in this format:
            Category A:
                {Item 1}  Quality = {value}     Price = {value}
            Category B:
                {Item 1}  Quality = {value}     Price = {value}
            
        and so on
        '''
        for category, s_value in self.inventory.items():
            print(f"Category: {category}")
            for item_name, item_value in s_value.items():
                print(f"\t{item_name}:\tQuatity = {item_value[0]},\tPrice = {item_value[1]}")
            print()

    def summary(self) -> None:
        '''
        Function that prints out all of the unique elements of the data structure based on;
        1. No. of categories
        2. No. of items in each category
        '''

        print("Inventory summary report:")
        print(f"Total unique categories: {len(self.categories)}",end="\n\n")
        # print(self.inventory)

        for key,value in self.inventory.items():
            print(f"Category `{key}`: {len(value)} unique items")

    def update_transactions(self, transaction: str):
        '''
        Prints out and update the transaction history
        '''

        print(transaction)
        self.transactions.append(transaction)

    def show_transactions(self) -> None:
        '''
        Show all transaction history
        '''

        print("Transaction history:")
        for i, transaction in enumerate(self.transactions):
            print(f"\t{i+1}. {transaction}")


if __name__ == "__main__":
    print("\033c") #? Hide filepath when running script
    x = InventoryManagementSystem()
    x.main_loop()
