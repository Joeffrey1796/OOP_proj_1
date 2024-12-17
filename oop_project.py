'''
OOP database system project
#Todo: Testing and Bugfixes
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
    7. Delete Category
    8. Exit
""")
            # choice : str = input("\t Choose an option (1-8): ")

            # if choice == '1':
            #     self.add_item()
            # elif choice == '2':
            #     self.edit()
            # elif choice == '3':
            #     self.delete_item()
            # elif choice == '4':
            #     self.display()
            # elif choice == '5':
            #     self.summary()
            # elif choice == '6':
            #     self.show_transactions()
            # elif choice == '7':
            #     self.delete_category()
            # elif choice == '8':
            #     print("Exiting Inventory Management System.")
            #     break
            # else:
            #     print("Invalid option. Please choose a valid option.")

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

    def is_valid_name(self, string: str,variable:str = "Name") -> tuple[bool,str]:
        '''
        Helper function that checks if inputted string is valid 
        '''

        #! Empty string input
        if string.strip() == "":
            return (False,f"{variable} name cannot be empty")

        #! First letter is not alnum
        if not string[0].isalnum():
            return (False,f"{variable} must start with an alphanumeric character")

        return (True,f"{variable} is valid")


    def add_item(self,category,item,quantity_input,price_input):
        '''
        Prompts the user to input the necessary params 
        create/add items in the inventory system
        '''

        category: str = category.rstrip()

        #! Category name errors
        r_value,r_msg  = self.is_valid_name(category,"Category")
        if not r_value:
            return r_msg
        
        item: str = item.rstrip()

        #! Item name errors
        r_value,r_msg  = self.is_valid_name(item,"Item")
        if not r_value:
            return r_msg


        # quantity_input:str = input("Enter quantity: ")

        #! Quantity not an integer input error
        if not self.is_int(quantity_input):
            return "Invalid quantity. Please enter a number"

        quantity:int = int(quantity_input)

        #! Quantity is less than 0 error
        if quantity < 0:
            return "Quantity must be equal to or greater than 0"

        # price_input:str = input("Enter price: ")

        #! Price not float type input error
        if not self.is_float(price_input):
            return "Invalid price. Please enter a number"
        price:float = float(price_input)

        #! Price is less than 0 error
        if price < 0:
            return "Price must be equal to or greater than 0"
                #! Item already exists in the categry error

        if (category in self.categories) and (item in self.inventory[category]):
            return "No duplicate items(enter `y` to update instead): "
            # choice: str = input("No duplicate items(enter `y` to update instead): ").lower()
            # if choice == 'y':
            #     self.item_edit(category,item)
            # return None

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
        return transaction


    def item_edit(self,category:str, item:str,update_input: str) -> str:
        '''
        Helper function that chanages quantity of an item
        '''

        # update_input: str = input(
        #     "Enter the quantity change (positive to add, negative to remove): ")

        #! Check if input is int
        if not self.is_int(update_input):
            return "Invalid quantity. Please enter a number"

        update:int = int(update_input)

        #! Input results to negative quantity
        if self.inventory[category][item][0] + update < 0:
            return ("Quantity must be equal to or greater than 0.\n"
                    "Delete instead? (enter `y` to contiue): ")
            # choice:str = input("Quantity must be equal to or greater than 0.\n"
            #                    "Delete instead? (enter `y` to contiue): "
            #                    ).lower()
            # if choice == 'y':
            #     self.item_deleter(category,item)
            # return None

        #* Updates the quantity of the item
        self.inventory[category][item][0] += update
        transaction: str = f"Item `{item}` quantity updated to {self.inventory[category][item][0]}"
        self.update_transactions(transaction)

        return transaction

    def edit(self,category,item) -> str:
        '''
        Prompts the user to enter the necessary params and
        updates the quantity by adding the `update` input
        to the existing data
        '''

        # category: str = input("Enter the category of the item to update: ")

        #! Category not found error
        if category not in self.categories:
            return "Category not found in the inventory"

        #! Item not found error
        # item: str = input("Enter the name of the item to update: ")
        if item not in self.inventory[category]:
            return "Item not found in the inventory"

        # self.item_edit(category,item)


    def deleting_item(self, category: str, item:str) -> None:
        self.inventory[category].pop(item)
        transaction = f"{item} removed from the inventory"
        self.update_transactions(transaction)

    def item_deleter(self,category: str, item: str) -> str:
        '''
        Helper function that removes an item from the data structure
        '''
        # #! Error for item not found in inventory
        # if item not in self.inventory[category]:
        #     print("Item is not in the inventory")

        #? Prompts the user to delete a category if empty after deletion
        if len(self.inventory[category]) == 1:
            return "Category will have 0 unique items. Delete it?"
            # # .lower()
            # if choice == 'y':
            #     #* Remove category from the inventory
            #     self.delete_category(category)
            # else:
            #     #* Remove the item from the inventory
            #     self.deleting_item(category,item)
        else:
            #* Remove the item from the inventory
            self.deleting_item(category,item)


    def delete_item(self,category,item) -> None|str:
        '''
        Function that prompts the user to delete a specific item
        '''

        # category: str = input("Enter the category of the item to delete: ")

        #! category not found error
        if category not in self.categories:
            return "Category not found in the inventory"

        item: str = input("Enter the name of the item to delete: ")
        #! item not found error
        if not item in self.inventory[category]:
            return "Item not found in the inventory"

        self.item_deleter(category,item)

    def display(self) -> list[str]:
        '''
        Function that shows the data structure in this format:
            Category A:
                {Item 1}   Quantity = {value}    Price = {value}
            Category B:
                {Item 1}   Quantity = {value}    Price = {value}
        '''
        texts = []
        # max_item_length = max(
        #     len(item) for category in self.inventory.values() for item in category
        # )

        max_item_length = 0 

        for category in self.inventory.values():  
            for item in category.keys():          
                item_length = len(item)          
                max_item_length = max(max_item_length, item_length)

        column_width_item = max_item_length + 5     

        for category, s_value in self.inventory.items():
            texts.append(f"Category: {category}")
            for item_name, item_value in s_value.items():
                
                item_text = item_name.ljust(column_width_item)
                quantity_text = f"Quantity = {item_value[0]}".ljust(20)
                price_text = f"Price = {item_value[1]}".ljust(20)
                texts.append("    " + item_text + quantity_text + price_text)
            texts.append("")  # Blank line for spacing
        
        return texts

    def summary(self) -> list[str]:
        '''
        Function that prints out all of the unique elements of the data structure based on;
        1. No. of categories
        2. No. of items in each category
        '''
        text = []
        text.append("Inventory summary report:")
        text.append(f"Total unique categories: {len(self.categories)}\n\n")
        # print(self.inventory) #? Debugging

        for key,value in self.inventory.items():
            text.append(f"Category `{key}`: {len(value)} unique items".ljust(50))
        
        return text

    def update_transactions(self, transaction: str) -> None :
        '''
        Prints out and update the transaction history
        '''

        # print(transaction)
        self.transactions.append(transaction)

    def show_transactions(self) -> list[str]:
        '''
        Show all transaction history
        '''
        texts = []
        texts.append("Transaction history:")
        for i, transaction in enumerate(self.transactions):
            texts.append(f"\t{i+1}. {transaction}")
        return texts

    def delete_category(self,category: str|None = None) -> str|None:
        '''
        Function that deletes a category
        '''

        # if not category:
        #     return "Enter the category to delete:"

        if category not in self.categories:
            return "Category not found in the inventory"

        transaction: str = (
f"category: `{category}` with {len(self.inventory[category])} unique item/s deleted"
                           )
        self.categories.remove(category)
        self.inventory.pop(category)
        self.update_transactions(transaction)
        
        return transaction


# def main() -> None:
#     print("\033c") #? Hide filepath when running script
#     x = InventoryManagementSystem()
#     x.main_loop()

# if __name__ == "__main__":
#     main()
