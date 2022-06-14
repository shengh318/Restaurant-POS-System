import tkinter as tk
from tkinter import ttk
import already_customer
import os

class receipt_window():
        def __init__(self, parent_frame, pos_class):
                self.parent_frame = parent_frame
                
                self.customer_address_frame = tk.LabelFrame(self.parent_frame, text="Customer")
                self.customer_address_frame.pack(fill='both', expand="yes")
                
                self.receipt_items_frame = tk.LabelFrame(self.parent_frame, text="Receipt Items")
                self.receipt_items_frame.pack(fill='both', expand="yes")
                
                self.info_frame = tk.LabelFrame(self.parent_frame, text="Information")
                self.info_frame.pack(fill='both', expand='yes')
                
                self.customer_number_label = tk.Label(self.customer_address_frame, text=f"Phone Number: {pos_class.customer}")
                self.customer_number_label.pack()
                
                self.customer_address_label = tk.Label(self.customer_address_frame, text=f"Address: {pos_class.customer_address}")
                
                self.customer_address_label.pack()
                
                self.chart = ttk.Treeview(self.receipt_items_frame, columns=(1,2), show='headings', height=8)
                self.chart.pack()
                
                self.chart.heading(1, text="Item")
                self.chart.heading(2, text="Price")
                
                # self.chart.insert(parent="", index = 0, values=("stuff", 1.9))

                self.add_to_chart(pos_class)
                self.customer_profile = make_customer_profile(pos_class)
                
                pos_class.already_customers[int(pos_class.customer)] = self.customer_profile
                
                customer_folder_path =  f"{os.path.dirname(__file__)}\customer"
                
                already_customer.write_to_customer_folder(customer_folder_path, self.customer_profile)
                
                
                self.total_label = tk.Label(self.info_frame, text = f"Total: ${round(pos_class.receipt_page.tax,2)}")
                self.total_label.pack()
        
        def add_to_chart(self, pos_class):
                '''
                Adds all of the items from the receipt page into the table view of the pos_class
                '''
                look_at_dictionary = pos_class.receipt_page.items
                list_of_keys = list(look_at_dictionary.keys())
                
                parent = ""
                for i in range (len(list_of_keys)):
                        index = i
                        item_name = list_of_keys[i]
                        number_of_item_tuples = look_at_dictionary[item_name]
                        
                        for stuff in number_of_item_tuples:
                                item_price = stuff[0]
                                tuple_for_chart = (item_name, item_price)
                                self.chart.insert(parent = parent, index = index, values = tuple_for_chart)
                

def make_dictionary_into_list(order_dictionary):
        '''
        Takes every thing in the order dictionary format and translate them into a string like so: 
        
        Spring Roll-------1.1
        
        then return a list of these strings
        '''
        return_list = []
        for key in order_dictionary:
                for item in order_dictionary[key]:
                        price = item[0]
                        add_string = f"{key}-------{price}"
                        return_list.append(add_string)
        return return_list

def make_customer_profile(pos_class):
        '''
        Makes a customer profile of the current customer and return that an instance of that class
        '''
        order_dictionary = pos_class.receipt_page.items
        order_list = make_dictionary_into_list(order_dictionary)
        phone_number = pos_class.customer
        address = pos_class.customer_address
        total = pos_class.receipt_page.total
        
        return already_customer.already_in_system_customers(address, phone_number, order_list, total)
                
        