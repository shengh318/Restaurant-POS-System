import tkinter as tk
import os
import useful_functions

class search_bar():
        def __init__(self, parent_frame, pos_class):
                self.parent_frame = parent_frame
                self.search_frame = tk.Frame(self.parent_frame)
                self.search_results_frame = tk.Frame(self.parent_frame)
                self.add_frame = tk.Frame(self.parent_frame)
                
                self.search_frame.pack()
                self.search_results_frame.pack()
                self.add_frame.pack()
                
                self.add_button = tk.Button(self.add_frame, text = "Add Item", command = lambda pos_class = pos_class: self.add_item_to_receipt(pos_class))
                
                self.add_button.pack()
                
                self.search_label = tk.Label(self.search_frame, text="Search")
                self.search_label.grid(row=0, column=0)
                self.search_bar = tk.Entry(self.search_frame)
                self.search_bar.grid(row=0, column=1)
                
                
                self.all_items = []
                directed_path_to_file = os.path.dirname(__file__)
                all_items_txt_file = directed_path_to_file + "\\sections\\all_items.txt"
                
                useful_functions.read_text_file(all_items_txt_file, self.all_items)

                self.string_var = tk.StringVar(value = self.all_items)
                self.scroll_bar = tk.Scrollbar(self.search_results_frame, orient='vertical')
                self.search_box = tk.Listbox(
                        self.search_results_frame,
                        listvariable= self.string_var,
                        height = 15,
                        width = 45,
                        selectmode='extended',
                        yscrollcommand=self.scroll_bar.set
                )
                
                self.scroll_bar.config(command  = self.search_box.yview)
                self.scroll_bar.pack(side='right', fill = 'y')
                self.search_box.pack()
                
                self.search_bar.bind("<KeyRelease>", self.check_box)
        
        
        def add_item_to_receipt(self, pos_class):
                '''
                Adds the selected item to the receipt page
                '''
                selected_indices = self.search_box.curselection()
                selected_item = self.search_box.get(selected_indices)
                
                #selected_item = 3.Shrimp Egg Roll-------1.4
                item_en_name, item_price = self.get_name_and_price(selected_item)
                item_class = "PLACEHOLDER"
                
                receipt_class = pos_class.receipt_page
                if item_en_name in receipt_class.items:
                        receipt_class.items[item_en_name].append((item_price,item_class))
                else:
                        receipt_class.items[item_en_name] = [(item_price,item_class)]
                #print(receipt_class.items)
                receipt_class.listbox.insert('end', item_en_name + "---------" + str(item_price))
                receipt_class.total += item_price
                receipt_class.tax = receipt_class.total*1.08
                receipt_class.total_label.config(text=f"Total (before tax): ${round(receipt_class.total,2)}")
                receipt_class.total_label_2.config(text=f"(after tax): ${round(receipt_class.tax,2)}")
                return item_price
                
        def get_name_and_price(self, string):
                dot_index = string.find('.')
                first_hyphen_index = string.find('-')
                last_hyphen_index = string.rfind('-')
                item_name = string[dot_index+1:first_hyphen_index]
                item_price = float(string[last_hyphen_index+1:])
                return (item_name, item_price)
                
        def update(self, data):
                '''
                Updates the list_box with the new data
                '''
                self.search_box.delete(0, tk.END)
                for item in data:
                        self.search_box.insert(tk.END, item)
                
        def check_box(self, e):
                '''
                Goes through the items and checks each one to see if there are any strings inside of them. If there are, then we add it to the data and update the listbox accordingly
                '''
                typed = self.search_bar.get()
                if typed == '':
                        data = self.all_items
                else:
                        data = []
                        for item in self.all_items:
                                if typed.lower() in item.lower():
                                        data.append(item)
                self.update(data)
                

                