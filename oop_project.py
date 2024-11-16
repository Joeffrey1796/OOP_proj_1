'''
OOP database system proj
'''

import typing as tp

class InventoryManagementSystem:

    def __init__(self):
        '''
        Class Constructor
        '''
        self.categories: tp.Set[tp.Any] = set()
        self.structure: tp.Dict[str,tp.List[tp.Dict[str,tp.List[int|float]]]] = dict()
  
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
        try:
            int(num)
            return True
        except ValueError:
            return False

    def is_float(self, num: str) -> bool:
        try:
            float(num)
            return True
        except ValueError:
            return False

    def add_item(self) -> None:
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
        else:
            print("Invalid quantity. Please enter a number")
            return None

        price_input:str = input("Enter price: ")
        if self.is_float(price_input):
            price:float = float(price_input)
        else:
            print("Invalid quantity. Please enter a number")
            return None


        if category not in self.categories:
            self.categories.add(category)
            self.structure[category] = [{item_name: [quantity, price]}]
        else:
            self.structure[category].append({item_name:[quantity,price]})

    def edit(self) -> None:
        category: str = input("Enter the category of the item to update: ")
        if category not in self.categories:
            print("Category not found in the system")
            return None

        item: str = input("Enter the name of the item to update: ")
        if not any((item in s_v_dict) for s_v_dict in self.structure[category]):
            print("Item not found in the system")
            return None

        update_input: str = input("Enter the quantity change (positive to add, negative to remove): ")
        if self.is_int(update_input):
            update:int = int(update_input)
            for s_v_dict in self.structure[category]:
                if item in s_v_dict:
                    s_v_dict[item][0] += update
                    print(f"Item '{item}' quantity updated to {s_v_dict[item][0]}")
                else:
                    print("Item is not in the inventory")
        else:
            print("Invalid quantity. Please enter a number")
            return None

    def delete(self) -> None:
        category: str = input("Enter the category of the item to delete: ")
        if category not in self.categories:
            print("Category not found in the system")
            return None
        item: str = input("Enter the name of the item to delete: ")

        if not any((item in s_v_dict) for s_v_dict in self.structure[category]):
            print("Item not foudn in the system")
            return None

        for s_v_dict in self.structure[category]:
            if item in s_v_dict:
                s_v_dict.pop(item)
                print(f"{item} removed from the inventory")
            else:
                print("Item is not in the inventory")

    def display(self) -> None:
        for s_key, s_value in self.structure.items():
            print(f"Categofy: {s_key}")
            for s_v_list in s_value:
                for s_v_key, s_v_value in s_v_list.items():
                    print(f"\t{s_v_key}:\tQuatity = {s_v_value[0]},\tPrice = {s_v_value[1]}")
            print()

    def summary(self) -> None:
        print("Inventory summary report:")
        print(f"Total unique categories: {len(self.categories)}")

        for key in self.structure:
            print(f"Category: '{key};: {len(self.structure[key])} unique items")


if __name__ == "__main__":
    x = InventoryManagementSystem()
    x.main_loop()
