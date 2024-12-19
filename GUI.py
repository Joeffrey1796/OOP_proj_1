import os
import tkinter as tk
from tkinter import messagebox
import oop_project as oop
import sampledata
from PIL import Image, ImageTk


#todo: remove global scope
#todo: PEP-8
#todo: class

FONT = ("Courier", 10)
BG_COLOR = "#CAD2C5"
FG_COLOR = "white"
BUTTON_COLOR = "#52796F"
ENTRY_COLOR = "#84A98C"
KULAY_NG_MAGANDA = "#f3e3d3"

def destroy_widget_children(master):
    for widget in master.winfo_children():
        widget.destroy()

    master.config(width= 1)

def exit_():
    pop_up = messagebox.askokcancel("Exit Program","Are you sure about exiting the program?")

    if pop_up == True:
        root.destroy()

def scrollable(master_root,width, height,row,collumn, **kwargs):

    def adjust_frame_size(event):
        '''
        Update the frame size 
        '''
        canvas.configure(scrollregion=(0, 0, event.width,event.height))

    def on_mouse_wheel(event):
        if event.state & 0x0001:
            canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas = tk.Canvas(master_root,width=width,height=height, bg=KULAY_NG_MAGANDA)
    canvas.grid(row=row, column=collumn, sticky="nsew", pady=(kwargs.get("pady", 0), 0), columnspan=kwargs.get("columnspan", 1))
    
    v_scroll = tk.Scrollbar(master_root, orient=tk.VERTICAL, command=canvas.yview)
    v_scroll.grid(row=row+1, column=collumn+1, sticky="ns", **kwargs)

    h_scroll = tk.Scrollbar(master_root, orient=tk.HORIZONTAL, command=canvas.xview)
    h_scroll.grid(row=row+1,column=collumn,sticky="ew")
    

    v_scroll.grid_remove()
    h_scroll.grid_remove()
    
    canvas.configure(yscrollcommand=v_scroll.set,xscrollcommand=h_scroll.set)
    
    scrollable_frame = tk.Frame(master=canvas, bg=KULAY_NG_MAGANDA)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
    scrollable_frame.bind("<Configure>", adjust_frame_size)
    
    canvas.bind("<Enter>", lambda event: canvas.bind_all("<MouseWheel>", on_mouse_wheel))  # Start binding on hover
    canvas.bind("<Leave>", lambda event: canvas.unbind_all("<MouseWheel>"))  # Stop binding when leaving
    
    return scrollable_frame

def add_item():

    def add_item_process():
        result = logic.add_item(category_entry.get(),item_entry.get(),quantity_entry.get(),price_entry.get())
        # print(result)
        add_item_errors = ("Item name cannot be empty", 
                           "Category name cannot be empty",
                           "Item must start with an alphanumeric character",
                           "Category must start with an alphanumeric character",
                           "Invalid quantity. Please enter a number",
                           "Quantity must be equal to or greater than 0",
                           "Invalid price. Please enter a number",
                           "Price must be equal to or greater than 0"
                           )
        if result in add_item_errors:
            messagebox.showerror("Fatal Error",result)
        elif result == "No duplicate items(enter `y` to update instead): ":
            choice = messagebox.askyesno("Duplicate Items",result)
            if choice is True:
                edit_item(category_entry.get(),item_entry.get())
        add_transaction(result)
        update_drop_menu(drop_var, f4, sorted(logic.categories))
    
    
    destroy_widget_children(f2)

    
    # Creating Widgets
    category_label = tk.Label(master=f2,text="Enter Cagetory:",width= 15, anchor="w",font=FONT, bg = KULAY_NG_MAGANDA)
    category_entry = tk.Entry(master=f2, width=58)
    item_label = tk.Label(master=f2, text="Enter Item:",width= 15, anchor="w",font=FONT, bg = KULAY_NG_MAGANDA)
    item_entry = tk.Entry(master=f2, width=58)
    quantity_label = tk.Label(master=f2,text="Enter Quantity:",width= 15, anchor="w",font=FONT, bg = KULAY_NG_MAGANDA)
    quantity_entry = tk.Entry(master=f2, width=58)
    price_label = tk.Label(master=f2,text="Enter Price:",width= 15, anchor="w",font=FONT, bg = KULAY_NG_MAGANDA)
    price_entry = tk.Entry(master=f2, width=58)
    
    # Packing widgets
    category_label.grid(row=0,column=0,pady=5,sticky="nw",padx=(10,15))
    category_entry.grid(row=0,column=1,pady=5,sticky="nw")
    item_label.grid(row=1,column=0,pady=5,sticky="nw",padx=(10,15))
    item_entry.grid(row=1,column=1,pady=5,sticky="nw")
    quantity_label.grid(row=2,column=0,pady=5,sticky="nw",padx=(10,15))
    quantity_entry.grid(row=2,column=1,pady=5,sticky="nw")
    price_label.grid(row=3,column=0,pady=5,sticky="nw",padx=(10,15))
    price_entry.grid(row=3,column=1,pady=5,sticky="nw")

    btn = tk.Button(master=f2, text="Confirm",font=FONT, command=add_item_process, height=3, bg=BUTTON_COLOR, fg=FG_COLOR)
    btn.grid(columnspan=2,row=4,pady=15,sticky="ew")



def edit_item(category=None,item=None):

    def edit_item_process():
        edit_item_errors = ("Category not found in the inventory",
                            "Item not found in the inventory",
                            "Invalid quantity. Please enter a number")
        
        result = logic.edit(category_entry.get(),item_entry.get())

        #! Category and Item errors
        if result in edit_item_errors:
            messagebox.showerror("Fatal Error",result)
            return

        #! Quantity Errrors
        result = logic.item_edit(category_entry.get(),item_entry.get(),quantity_entry.get())
        if result in edit_item_errors:
            messagebox.showerror("Fatal Error",result)
        elif result == ("Quantity must be equal to or greater than 0.\n"
                        "Delete instead? (enter `y` to contiue): "
                        ):
            choice = messagebox.askyesno("Duplicate Items",result)
            if choice is True:
                delete_item(category_entry.get(),item_entry.get())

        add_transaction(result)
            
    destroy_widget_children(f2)

    # Creating Widgets
    category_label = tk.Label(master=f2,text="Enter Cagetory:",width=37, anchor="w", font=FONT, bg = KULAY_NG_MAGANDA)
    category_entry = tk.Entry(master=f2, width=29 )
    item_label = tk.Label(master=f2, text="Enter Item:",width=37, anchor="w", font=FONT, bg = KULAY_NG_MAGANDA)
    item_entry = tk.Entry(master=f2, width=29 )
    quantity_label = tk.Label(master=f2,text="Enter the quantity change:",width=37, anchor="w", font=FONT, bg = KULAY_NG_MAGANDA)
    quantity_entry = tk.Entry(master=f2, width=29)

    


    # Passed as a function
    if category is not None and item is not None:
        category_entry.insert(0,category)
        item_entry.insert(0,item)

    # Packing widgets
    category_label.grid(row=0,column=0,pady=5, padx=(10,10))
    category_entry.grid(row=0,column=1,pady=5)
    item_label.grid(row=1,column=0,pady=5, padx=(10,10))
    item_entry.grid(row=1,column=1,pady=5)
    quantity_label.grid(row=2,column=0 ,pady=5, padx=(10,10))
    quantity_entry.grid(row=2,column=1 ,pady=5)

    quantity_entry.bind("<Enter>", show_prompt)  # Show the prompt when mouse enters
    quantity_entry.bind("<Leave>", hide_prompt)  # Hide the prompt when mouse leaves

    btn = tk.Button(master=f2,text="Confirm", command=edit_item_process, font=FONT, height=3, bg=BUTTON_COLOR, fg=FG_COLOR)
    btn.grid(columnspan=2,row=4,pady=15,sticky="ew")

def delete_item(category = None, item = None):

    def delete_item_process():
        delete_item_errors = ("Category not found in the inventory",
                              "Item not found in the inventory")
        result = logic.delete_item(category_entry.get(),item_entry.get())

        if result in delete_item_errors:
            messagebox.showerror("Fatal Error", result)
        elif result == "Category will have 0 unique items. Delete it?":
            choice = messagebox.askquestion("0 unique",result)
            if choice is True:
                logic.delete_category(category_entry.get())
                update_drop_menu(drop_var, f4, sorted(logic.categories))
            else:
                logic.deleting_item(category_entry.get(),item_entry.get())
        add_transaction(result)


    destroy_widget_children(f2)


    # Creating Widgets
    category_label = tk.Label(master=f2,text="Enter Cagetory:", anchor="w", font=FONT, width=20, bg = KULAY_NG_MAGANDA)
    category_entry = tk.Entry(master=f2, width=53 )
    item_label = tk.Label(master=f2, text="Enter Item:", anchor="w", font=FONT, width=20, bg = KULAY_NG_MAGANDA)
    item_entry = tk.Entry(master=f2, width=53 )

    # Passed as a function
    if category is not None and item is not None:
        category_entry.insert(0,category)
        item_entry.insert(0,item)

    # Packing Widgets
    category_label.grid(row=0,column=0,pady=5, padx=(10,0))
    category_entry.grid(row=0,column=1,pady=5)
    item_label.grid(row=1,column=0,pady=5, padx=(10,0))
    item_entry.grid(row=1,column=1,pady=5)

    btn = tk.Button(master=f2,text="Confirm", command=delete_item_process, height=3, font=FONT, bg=BUTTON_COLOR, fg=FG_COLOR)
    btn.grid(columnspan=2,row=4,pady=15,sticky="ew")


def delete_inventory_by_category():

    def delete_inventory_by_category_process():
        result = logic.delete_category(category_entry.get())
        add_transaction(result)


    destroy_widget_children(f2)

    #Creating Widgets
    category_label = tk.Label(master=f2,text="Enter Cagetory:", anchor="w", width=20, font=FONT, bg = KULAY_NG_MAGANDA)
    category_entry = tk.Entry(master=f2 , width=53)

    # Packing Widgets
    category_label.grid(row=0,column=0,pady=5, padx=(10,0))
    category_entry.grid(row=0,column=1,pady=5)

    btn = tk.Button(master=f2,text="Confirm", command=delete_inventory_by_category_process, height=3, bg=BUTTON_COLOR, fg=FG_COLOR)
    btn.grid(columnspan=2,row=4,pady=15,sticky="ew")


def show_prompt(event):
    # Create the tooltip label dynamically
    global tooltip
    tooltip = tk.Label(root, text="Positive to add, Negative to subtract", bg=BG_COLOR, fg="#2F3E46", relief="solid", borderwidth=1, font=("Arial", 9))
    tooltip.place(x=event.widget.winfo_rootx() - root.winfo_rootx(), 
                  y=event.widget.winfo_rooty() - root.winfo_rooty() - 25)

def hide_prompt(event):
    # Destroy the tooltip when mouse leaves
    global tooltip
    if tooltip:
        tooltip.destroy()



def display():
    destroy_widget_children(f2)

    texts = logic.display()


    for i, text in enumerate(texts):
        label = tk.Label(master=f2, text=text, anchor="w", font=FONT, bg = KULAY_NG_MAGANDA)
        label.grid(row=i, column=0, pady=5)
    

def summary_report():
    destroy_widget_children(f2)

    texts = logic.summary()


    for i, text in enumerate(texts):
        label = tk.Label(master=f2, text=text, anchor="w", font=FONT, bg = KULAY_NG_MAGANDA)
        label.grid(row=i, column=0, pady=5, padx=10)
        

def show_transactions():
    destroy_widget_children(f2)

    texts = logic.show_transactions()
    for text in texts:
        tk.Label(master=f2,text=text, anchor="w", font=FONT, bg = KULAY_NG_MAGANDA).pack()


def delete_category():

    def delete_category_process(category_entry):
        delete_category_process_errors = ("Category not found in the inventory")

        result = logic.delete_category(category_entry.get())
        
        
        if result in delete_category_process_errors:
            messagebox.showerror("Fatal Error", result)
        add_transaction(result)


    destroy_widget_children(f2)

    # Creating Widgets
    category_label = tk.Label(master=f2,text="Enter Cagetory:", anchor="w", font=FONT, width=20, bg = KULAY_NG_MAGANDA)
    category_entry = tk.Entry(master=f2, width=53 )

    # Packing Widgets   
    category_label.grid(row=0,column=0,pady=5, padx=(10,0))
    category_entry.grid(row=0,column=1,pady=5)

    btn = tk.Button(master=f2,text="Confirm", command=lambda:delete_category_process(category_entry), height=3, bg=BUTTON_COLOR, fg=FG_COLOR)
    btn.grid(columnspan=2,row=4,pady=15,sticky="ew")

def add_transaction(text):
    
    for widget in f3.winfo_children():
        widget.destroy()
    
    tk.Label(master=f3,text=text, font=FONT, bg = KULAY_NG_MAGANDA, width=61, wraplength=480).pack()

def show_search(search_term,master_root):
    global show_searched
    
    search_type, x = search(search_term)
    
    if 'show_searched' in globals():
        show_searched.config(text=x)
    else:
        show_searched = tk.Label(master=master_root, text=x, width=40, height=30,anchor="nw", font=FONT, bg = KULAY_NG_MAGANDA, justify="left", padx=10)
        show_searched.grid(row=5, column=0, columnspan=3, sticky="ew")
        


def search(search_term):

    for category, item in logic.inventory.items():
        if search_term in item:
            y = logic.inventory[category][search_term]
            return ("item", f"Quantity: {y[0]}\nPrice: {y[1]}")
        
    if search_term in logic.categories:
        text = ""  
        for i in logic.inventory[search_term].keys():
            text += f"{i}\n"  
        text = text.strip("\n")  
        
        return ("category", text)


    return (None, "404: Not found")

def update_drop_menu(drop_var, f4, new_categories):

    #? Destroy the old OptionMenu if it exists
    for widget in f4.winfo_children():
        if isinstance(widget, tk.OptionMenu):
            widget.destroy() 

     #? Create a new OptionMenu with updated categories
    search_drop = tk.OptionMenu(f4, drop_var, *new_categories)
    search_drop.grid(row=1, column=0, columnspan=2, sticky="ew") 


def main2():
    global logic
    global f1
    global f2
    global f3
    global f4
    global drop_var
    

    logic = oop.InventoryManagementSystem()
    # Create Database
    logic.inventory = sampledata.inventory
    logic.categories = sampledata.categories
    # Initialize Widgets
    f1 = tk.LabelFrame(master=root,text = "Choose your input",padx=20,pady=20,labelanchor="n", font=FONT, bg = KULAY_NG_MAGANDA)
    f2 = scrollable(root,500,100,0,1, pady=20)
    f3 = tk.LabelFrame(master=root,text="Last Transaction",labelanchor="n", font=FONT, bg = KULAY_NG_MAGANDA)
    f4 = tk.LabelFrame(master=root, width=50, height=100, font=FONT, bg = KULAY_NG_MAGANDA)

    # Pack Widgets
    f1.grid(row=0, column=0,padx=50, pady=20)
    f3.grid(row=2,column=1, columnspan=2,padx=0,pady=20)
    f4.grid(row=0,column=4, padx=45)

    


    btn_choices = [("Add Item", add_item),
                ("Edit Item Quantity", edit_item),
                ("Delete Item", delete_item),
                ("Delete Inventory by Category", delete_inventory_by_category),
                ("Display", display),
                ("Summary Report", summary_report),
                ("Transaction History", show_transactions),
                ("Delete Category", delete_category),
                ("Exit", exit_)]
    longest_text = max(btn_choices, key=lambda b: len(b[0]))

    for i, data in enumerate(btn_choices):
        tk.Button(master=f1,text=data[0], width=len(longest_text[0]) ,command=data[1],font=FONT, bg=BUTTON_COLOR, fg=FG_COLOR).grid(row=i, column=0, padx=5,pady=5)


    drop_var = tk.StringVar()
    entry_var = tk.StringVar()

    plotting = scrollable(f4,250,343,2,0, columnspan=3)
    search_label = tk.Label(master=f4,text="Search:", anchor="nw", font=FONT, bg = KULAY_NG_MAGANDA)
    search_entry = tk.Entry(master=f4,textvariable=entry_var)
    search_drop = tk.OptionMenu(f4,drop_var,*logic.categories)
    btn_confirm = tk.Button(master=f4, text="Confirm",command=lambda: show_search(search_entry.get(),plotting), font=FONT, bg=BUTTON_COLOR, fg=FG_COLOR)

    
    entry_var.set("")

    drop_var.trace_add("write", lambda *args: entry_var.set(drop_var.get()))

    search_label.grid(row=0,column=0)
    search_entry.grid(row=0,column=1)
    search_drop.grid(row=1,column=0,columnspan=2,sticky="ew")
    btn_confirm.grid(row=0,column=2,rowspan=2,sticky="nsew")

    update_drop_menu(drop_var, f4, sorted(logic.categories))


def main():
    global root
    

    

    global base_dir
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct paths for resources dynamically
    icon_path = os.path.join(base_dir, "Source", "OOP_icon.ico")
    image_path = os.path.join(base_dir, "Source", "Inventory_Management_System2.png")

    # Initialize the Tkinter window
    root = tk.Tk()
    root.geometry("1280x720")
    root.configure(bg=BG_COLOR)
    root.resizable(0, 0)
    root.iconbitmap(icon_path)  # Dynamically set the icon
    root.title("Inventory Management System")

    # Load the image dynamically
    image = Image.open(image_path)

    # Convert to Tkinter-compatible format
    photo = ImageTk.PhotoImage(image)

    
    
    def go_to_main2():
        
        proceed_button.grid_forget()

        main2()

    proceed_button = tk.Button(root, image=photo, command=go_to_main2)
    proceed_button.grid(row=0, column=0, sticky="nsew")
    




    root.mainloop()

main()