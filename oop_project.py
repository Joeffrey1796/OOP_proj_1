'''
OOP database system project
#Todo: Fix console output formatting
#Todo: Add Category deleter
#Todo: Testing and Bugfixes
#//: //Fix bug on Summary Report
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
        self.structure: dict[str,list[dict[str,list[int|float]]]] = dict()

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
    6. Exit
""")
            choice : str = input("\t Choose an option (1-6): ")

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

    def add_item(self) -> None:
        '''
        Prompts the user to input the necessary params 
        create/add items in the inventory system
        '''

        item_name: str = input("Enter item name: ")
        category: str = input("Enter category: ")

        if category in self.categories:
            for s_dict in self.structure[category]:
                if item_name in s_dict:
                    print("No duplicate items(update instead of add?)")
                    return None

        quantity_input:str = input("Enter quantity: ")
        if self.is_int(quantity_input):
            quantity:int = int(quantity_input)
            if quantity < 0:
                print("Quantity must be equal to or greater than 0")
                return None
        else:
            print("Invalid quantity. Please enter a number")
            return None

        price_input:str = input("Enter price: ")
        if self.is_float(price_input):
            price:float = float(price_input)
            if price < 0:
                print("Price must be equal to or greater than 0")
                return None
        else:
            print("Invalid quantity. Please enter a number")
            return None


        if category not in self.categories:
            self.categories.add(category)
            self.structure[category] = [{item_name: [quantity, price]}]
        else:
            self.structure[category].append({item_name:[quantity,price]})

    def edit(self) -> None:
        '''
        Prompts the user to enter the necessary params and
        updates the quantity by adding the `update` input
        to the existing data
        '''

        category: str = input("Enter the category of the item to update: ")
        if category not in self.categories:
            print("Category not found in the system")
            return None

        item: str = input("Enter the name of the item to update: ")
        if not any((item in s_v_dict) for s_v_dict in self.structure[category]):
            print("Item not found in the system")
            return None

        update_input: str = input(
            "Enter the quantity change (positive to add, negative to remove): ")

        if not self.is_int(update_input):
            print("Invalid quantity. Please enter a number")
            return None

        update:int = int(update_input)
        for s_v_dict in self.structure[category]:
            if s_v_dict[item][0] + update < 0:
                choice:str = input("""
Quantity must be positive.
Delete instead? (enter `y` to contiue): """).lower()

                if choice == 'y':
                    self.item_deleter(category,item)
                else:
                    s_v_dict[item][0] += update
                    print(f"Item `{item}` quantity updated to {s_v_dict[item][0]}")

    def item_deleter(self,category: str, item: str) -> None:
        '''
        Helper function that removes an item from the data structure
        '''

        for s_v_dict in self.structure[category]:
            if item in s_v_dict:
                s_v_dict.pop(item)
                print(f"{item} removed from the inventory")
            else:
                print("Item is not in the inventory")

        #! Hot fix for empty list but counts 1 error
        if self.structure[category] == [{}]:
            self.structure[category].clear()

    def delete(self) -> None:
        '''
        Function that prompts the user to delete a specific item
        '''

        category: str = input("Enter the category of the item to delete: ")
        if category not in self.categories:
            print("Category not found in the system")
            return None
        item: str = input("Enter the name of the item to delete: ")

        if not any((item in s_v_dict) for s_v_dict in self.structure[category]):
            print("Item not foudn in the system")
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
        for s_key, s_value in self.structure.items():
            print(f"Category: {s_key}")
            for s_v_list in s_value:
                for s_v_key, s_v_value in s_v_list.items():
                    print(f"\t{s_v_key}:\tQuatity = {s_v_value[0]},\tPrice = {s_v_value[1]}")
            print()

    def summary(self) -> None:
        '''
        Function that prints out all of the unique elements of the data structure based on;
        1. No. of categories
        2. No. of items in each category
        '''

        print("Inventory summary report:")
        print(f"Total unique categories: {len(self.categories)}",end="\n\n")
        print(self.structure)

        for key,value in self.structure.items():
            print(f"Category `{key}`: {len(value)} unique items")


if __name__ == "__main__":
    x = InventoryManagementSystem()
    x.main_loop()
