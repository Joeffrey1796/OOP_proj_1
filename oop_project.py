'''
OOP database system proj
'''

import typing as tp


# inventory: tp.Dict[tp.Any,tp.Any] = dict()
# transactions: tp.List[tp.Any] = list()

categories: tp.Set[tp.Any] = set()
structure: tp.Dict[str,tp.List[tp.Dict[str,tp.List[int|float]]]] = dict()

def main() -> None:
    '''Main function'''

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
 
        choice = input("    Choose an option (1-6): ")

        if choice == '1':
            add_item()
        elif choice == '2':
            edit()
        elif choice == '3':
            delete()            
        elif choice == '4':
            display()
        elif choice == '5':
            summary()
        elif choice == '6':
            break
        else:
            print("Invalid option. Please choose a valid option")




def is_int(num) -> bool:
    try:
        int(num)
        return True
    except Exception:
        return False

def is_float(num) -> bool:
    try:
        float(num)
        return True
    except Exception:
        return False

def add_item() -> None:
    item_name : str = input("Enter item name: ")
    category : str = input("Enter category: ")

    if category in categories:
        for i in structure[category]:
            if item_name in i:
                print("No duplicate items(update instead of add?)")
                return


    quantity : str|int = input("Enter quantity: ")
    if is_int(quantity):
        quantity = int(quantity)
    else:
        print("Invalid quantity. Please enter a number")
        return

    price : str|float = input("Enter price: ")
    if is_float(price):
        price = float(price)
    else:
        print("Invalid quantity. Please enter a number")
        return


    

    # print(structure)
    # print(categories)

    if category not in categories:
        categories.add(category)
        structure[category] = [{item_name: [quantity, price]}]
    else:
        structure[category].append({item_name:[quantity,price]})
    

def edit() -> None:
    category : str = input("Enter the category of the item to update: ")
    if category not in categories:
        print("Category not found in the system")
        return
    
    item : str = input("Enter the name of the item to update: ")
    if not any((item in s_v_dict) for s_v_dict in structure[category]):
        print("Item not found in the system")
        return
    

    update : str|int = input("Enter the quantity change(positive to add, negative to remove): ")
    if is_int(update):
        update = int(update)
        for s_v_dict in structure[category]:
            if item in s_v_dict:
                s_v_dict[item][0] += update
                print(f"Item '{item}' quantity updated to {s_v_dict[item][0]}")
            else:
                print("Item is not in the Inventory")
    else:
        print("Invalid quantity. Please enter a number")
        return
    
def delete() -> None :
    category : str = input("Enter the category of the item to delete: ")
    if category not in categories:
        print("Category not found in the system")
        return
    item : str = input("Enter the name of the item to delete: ")

    
    if not any((item in s_v_dict) for s_v_dict in structure[category]):
        print("Item not found in the system")
        return
        
    
    for s_v_dict in structure[category]:
        if item in s_v_dict:
            s_v_dict.pop(item)
            print(f"{item} removed from inventory")
        else:
            print("Item is not in the Inventory")


def display() -> None:
    for s_key, s_value in structure.items():
        print(f"Category: {s_key}")
        for s_v_list in s_value:
            for s_v_key, s_v_value in s_v_list.items():
                print(f"    {s_v_key}:\t Quantity = {s_v_value[0]},\t Price = {s_v_value[1]}")
        print()
    

def summary() -> None:
    print("Inventory summary report:")
    print(f"Total unique categories: {len(categories)}")

    for key in structure:
        print(f"Category: '{key}': {len(structure[key])} unique items")
    

if __name__ == "__main__":

    # category = {"belt"}
    # inventory = {"my belt":[12,12.0]}
    # add_item()
    # add_item()
    main()

    

