import tkinter as tk
from tkinter import messagebox
import already_customer
import search_bar
import os
import receipt_window

class POS_SYS():
        def __init__(self, parent_frame, sections_dictionary):
                self.parent_frame = parent_frame
                self.sections_dict = sections_dictionary
                
                self.section_frame = tk.Frame(self.parent_frame)
                self.section_frame.grid(row=0, column=0)
                
                self.receipt_frame = tk.Frame(self.parent_frame)
                self.receipt_frame.grid(row=0, column=1)
                
                self.list_of_sections = list(self.sections_dict.keys())
                
                self.customer = 0000
                self.customer_address = "Eat In"
                self.receipt_page = receipt(self.receipt_frame, self)
                self.search_frame = tk.Frame(self.parent_frame)
                self.search_frame.grid(row=0, column=2)
                self.search_bar = search_bar.search_bar(self.search_frame, self)
                self.already_made_buttons = {}
                
                self.already_customers = {}
                self.directed_path_to_file = os.path.dirname(__file__)
                already_customer.import_from_folder(self, self.directed_path_to_file)
                

class customer_info():
        def __init__(self, parent_frame, pos_sys_class):
                self.parent_frame = parent_frame
                
                self.phone_label = tk.Label(self.parent_frame, text="Last 4 digits")
                self.phone_label.grid(row=0, column=0)
                
                self.user_entry = tk.Entry(self.parent_frame)
                self.user_entry.grid(row=0, column=1)
                
                self.customer_address_label = tk.Label(self.parent_frame, text="Address")
                self.customer_address_label.grid(row=1, column=0)
                
                self.customer_address_entry = tk.Entry(self.parent_frame)
                self.customer_address_entry.grid(row=1, column=1)
                
                self.order_button = tk.Button(self.parent_frame, text="Begin Order", command = lambda pos_sys_class = pos_sys_class: self.begin_order(pos_sys_class))
                self.order_button.grid(row=2, column=0)

        
        def change_address_command(self, new_address, already_customer_class, window, pos_class):
                '''
                Gets the new address and updates the receipt page accordingly
                '''
                address = new_address.get()
                already_customer_class.update_address(address)
                pos_class.customer_address = address
                self.update_everything(already_customer_class, pos_class)
                self.show_sections_page(pos_class)
                window.destroy()
        
        def same_address_command(self, already_customer_class, window, pos_class):
                '''
                Since the address did not change for the customer, we simply takes the order list and adds it to the receipt page, we do not need to change anything else
                '''
                self.update_everything(already_customer_class, pos_class)
                self.show_sections_page(pos_class)
                window.destroy()
                
        def get_item_name_price(self, string):
                '''
                Given a string like so: Spring Roll-------1.1
                
                returns (Spring Roll, 1.1)
                '''
                hyphen_index = string.find('-')
                last_index = string.rfind('-')
                item_name = string[:hyphen_index]
                item_price = float(string[last_index+1:])
                return(item_name, item_price)
        
        def add_already_information(self, already_customer_class, pos_class):
                '''
                Creates a window to see if the customer needs to change his or her address from the last time he or she came in
                '''
                address_window = tk.Tk()
                address_window.title("Address")
                
                same_address = tk.Button(
                        address_window, 
                        text="Same Address", 
                        command= lambda already_customer_class = already_customer_class, window = address_window, pos_class = pos_class: self.same_address_command(already_customer_class, window, pos_class)
                )
                
                same_address.grid(row=0, column=0)
                
                different_address_label = tk.Label(address_window, text="New Address (leave blank if not changed)")
                different_address_label.grid(row=1, column=0)
                
                different_address_entry = tk.Entry(address_window)
                different_address_entry.grid(row=1, column=1)
                
                change_address_button = tk.Button(
                        address_window, 
                        text = "Change", 
                        command = lambda new_address = different_address_entry, already_customer_class = already_customer_class, window = address_window, pos_class = pos_class: self.change_address_command(new_address, already_customer_class, window, pos_class)
                )
                
                change_address_button.grid(row=2)
                
                address_window.mainloop()
                
        def update_everything(self, already_customer_class, pos_class):
                '''
                Takes in the already customer and updates the receipt page with information that we already have about the last time the customer came to the restaurant
                '''
                phone_number = already_customer_class.phone_number
                address = already_customer_class.address
                order_list = already_customer_class.order_list
                
                receipt_class = pos_class.receipt_page
                
                pos_class.customer = phone_number
                pos_class.customer_address = address
                
                receipt_class.customer_last_4_digits.config( text=f"Phone Number: {pos_class.customer}")
                
                receipt_class.customer_address_label.config(text=f"Address: {pos_class.customer_address}")
                
                for item in order_list:
                        item_class = "PLACEHOLDER"
                        item_en_name, item_price = self.get_item_name_price(item)
                        if item_en_name in receipt_class.items:
                                receipt_class.items[item_en_name].append((item_price,item_class))
                        else:
                                receipt_class.items[item_en_name] = [(item_price,item_class)]
                        receipt_class.listbox.insert('end', item_en_name + "---------" + str(item_price))
                        receipt_class.total += item_price
                        receipt_class.tax = receipt_class.total*1.08
                        
                receipt_class.total_label.config(text=f"Total (before tax): ${round(receipt_class.total,2)}")
                receipt_class.total_label_2.config(text=f"(after tax): ${round(receipt_class.tax,2)}")
                
                
        def show_sections_page(self, pos_sys_class):
                '''
                Displays the section page for the user
                
                If there already is a section page that was previously made, then it uses that page
                
                otherwise, it makes a completely new page
                '''
                if not hasattr(pos_sys_class, 'section_buttons_dict'):
                        clear_frame(self.parent_frame)
                        pos_sys_class.section_buttons_dict = make_button_grid(pos_sys_class.list_of_sections, 3, pos_sys_class.section_frame)

                        for key in pos_sys_class.section_buttons_dict:
                                current_button = pos_sys_class.section_buttons_dict[key]
                                current_button.config(command = lambda pos_class=pos_sys_class, parent_frame=pos_sys_class.section_frame, section_title = key: section_button_command(pos_class, parent_frame, section_title))
                else:
                        return_to_homepage(pos_sys_class, pos_sys_class.section_frame)
        
        def begin_order(self, pos_sys_class):
                user_input = self.user_entry.get()
                phone_number = int(user_input)
                if phone_number in pos_sys_class.already_customers:
                        customer_class = pos_sys_class.already_customers[phone_number]
                        self.add_already_information(customer_class, pos_sys_class)
                else:
                        user_address = self.customer_address_entry.get().split()
                        if len(user_input) != 4:
                                messagebox.showerror("Error Window", "Input Error")
                                return 
                        else:
                                for i in range (len(user_input)):
                                        if not user_input[i].isdigit():
                                                messagebox.showerror("Error Window", "Input Error")
                                                return
                                if len(user_address) == 0:
                                        pos_sys_class.customer_address = "Eat In"
                                else:
                                        pos_sys_class.customer_address = user_address
                                        pos_sys_class.receipt_page.customer_address_label.config(text=f"Address: {pos_sys_class.customer_address}")
                                
                                pos_sys_class.customer = user_input
                                pos_sys_class.receipt_page.customer_last_4_digits.config(text=f"Phone Number: {pos_sys_class.customer}")
                                #print(pos_sys_class.customer)
                        
                        self.show_sections_page(pos_sys_class)

def return_to_customer_page(customer_class, parent_frame, pos_class):
        '''
        Basically resets everything to how it was like at the beginning
        '''        
        receipt_show = tk.Tk()
        receipt_show.title("Receipt")
        
        receipt_class = receipt_window.receipt_window(receipt_show, pos_class)
        

        
        
        clear_frame(parent_frame)
        receipt = pos_class.receipt_page
        
        receipt.total = 0
        receipt.tax = receipt.total*1.08
        pos_class.customer = 0000
        pos_class.customer_address = "Eat In"
        
        
        receipt.total_label.config(text=f"Total (before tax): ${receipt.total}")
        
        receipt.total_label_2.config(text=f" (after tax): {receipt.tax}")
        
        receipt.customer_last_4_digits.config(text=f"Phone Number: {pos_class.customer}")
        
        receipt.customer_address_label.config( text=f"Address: {pos_class.customer_address}")
        
        receipt.items = {}
        
        receipt.listbox.delete(0, tk.END)
        
        customer_class.phone_label.grid(row=0, column=0)
        customer_class.user_entry.grid(row=0, column=1)
        customer_class.user_entry.delete(0, tk.END)
        customer_class.customer_address_label.grid(row=1, column=0)
        customer_class.customer_address_entry.grid(row=1, column=1)
        customer_class.order_button.grid(row=2, column=0)
        
        receipt_show.mainloop()
      
def clear_frame(frame):
        '''
        Takes in a tkinter frame and clear it, just forgets the widgets and not destroy them
        '''
        for widgets in frame.winfo_children():
                try:
                        widgets.grid_forget()
                except:
                        widgets.pack_forget()
                        
                        
def get_all_buttons(pos_sys_sections_dict):
        '''
        Given a pos_sys_sections_dict, it returns a list that contains all of the buttons instead of using the dictionary
        '''
        
        return_list = []
        for key in pos_sys_sections_dict:
                return_list.append(pos_sys_sections_dict[key])
        return return_list



def return_to_homepage(pos_class, parent_frame):
        '''
        Returns to the homepage using existing buttons
        '''
        clear_frame(parent_frame)
        buttons_list = get_all_buttons(pos_class.section_buttons_dict)
        row=0
        for i in range (len(buttons_list)):
                if i%3== 0:
                        row += 1
                buttons_list[i].grid(row = row, column = i%3)


def get_already_made_buttons(pos_class, section_title):
        '''
        Gets the current section title of the premade buttons and returns a tuple in this order:
        
        return (return_button_frame, return_button, menu_items_frame, menu_buttons)
        
        This is made for the efficiency of the program. We don't have to keep forgetting buttons then remake new ones. We can just use the ones that we already made that we keep in a dictionary called already_made_buttons in the pos_class
        '''
        dictionary = pos_class.already_made_buttons[section_title]
        return_button_frame = dictionary['return_button_frame']
        return_button= dictionary['return_button']
        menu_items_frame = dictionary['menu_items_frame']
        
        menu_buttons = []
        skip_keys = ['return_button_frame','return_button', 'menu_items_frame']
        for key in dictionary:
                if key not in skip_keys:
                        menu_buttons.append(dictionary[key])
        
        return (return_button_frame, return_button, menu_items_frame, menu_buttons)

def section_button_command(pos_class,parent_frame, section_title):
        '''
        Clears the frame, and remake the corresponding section from the section title
        '''
        clear_frame(parent_frame)
        if section_title in pos_class.already_made_buttons:
                all_buttons = get_already_made_buttons(pos_class, section_title)
                return_button_frame = all_buttons[0]
                return_button= all_buttons[1]
                menu_items_frame = all_buttons[2]
                menu_buttons = all_buttons[3]
                
                return_button_frame.grid(row=0, column=0)
                return_button.grid(row=0, column=0)
                menu_items_frame.grid(row=1, column=0)
                
                row=0
                for i in range (len(menu_buttons)):
                        if i%4== 0:
                                row += 1
                        menu_buttons[i].grid(row = row, column=i%4)
                
        else:
                pos_class.current_page = make_one_section_page(pos_class.sections_dict[section_title], pos_class.section_frame, pos_class.receipt_page, pos_class)
                pos_class.already_made_buttons[section_title] = pos_class.current_page


class receipt():
        def __init__(self, parent_frame, pos_sys_class) -> None:
                pos_sys_class.customer_page = customer_info(pos_sys_class.section_frame, pos_sys_class)
                
                self.items = {}
                
                self.parent_frame = parent_frame
                self.receipt_frame = tk.Frame(self.parent_frame)
                self.customer_info_and_total_frame = tk.Frame(self.parent_frame)
                
                self.button_frame = tk.Frame(self.parent_frame)
                
                self.receipt_frame.grid(row=0, column=0)
                self.customer_info_and_total_frame.grid(row=1, column=0)
                self.button_frame.grid(row=2, column=0)
                
                self.total_frame = tk.Frame(self.customer_info_and_total_frame)
                self.total_frame.grid(row=0, column=0)
                
                self.customer_info_frame = tk.Frame(self.customer_info_and_total_frame)
                self.customer_info_frame.grid(row=0, column=1)
                
                
                self.string_var = tk.StringVar(value = list(self.items.keys()))
                self.scrollbar = tk.Scrollbar(self.receipt_frame, orient='vertical')
                
                self.listbox = tk.Listbox(
                        self.receipt_frame, 
                        listvariable=self.string_var, 
                        height=20,
                        width=100,
                        selectmode='extended', 
                        yscrollcommand=self.scrollbar.set
                )
                
                self.scrollbar.config(command=self.listbox.yview)
                self.scrollbar.pack(side='right', fill='y')
                self.listbox.pack()
                
                self.total = 0
                self.tax = self.total*1.08
                
                self.total_label = tk.Label(self.total_frame, text=f"Total (before tax): ${self.total}")
                self.total_label.pack()
                
                self.total_label_2 = tk.Label(self.total_frame, text=f" (after tax): {self.tax}")
                self.total_label_2.pack()
                
                self.customer_last_4_digits = tk.Label(self.customer_info_frame, text=f"Phone Number: {pos_sys_class.customer}")
                self.customer_last_4_digits.pack()
                
                self.customer_address_label = tk.Label(self.customer_info_frame, text=f"Address: {pos_sys_class.customer_address}")
                self.customer_address_label.pack()
                
                self.print_button = tk.Button(
                        self.button_frame, 
                        text="PRINT", 
                        command= lambda customer_class = pos_sys_class.customer_page, parent_frame = pos_sys_class.section_frame, pos_sys_class = pos_sys_class: return_to_customer_page(customer_class, parent_frame, pos_sys_class),
                                
                        )
                
                self.print_button.grid(row=1, column=0)
                
                self.delete_item = tk.Button(self.button_frame, text="DELETE", command = lambda : remove_selected_item(self))
                self.delete_item.grid(row=1, column=1)

def remove_selected_item(receipt_class):
        '''
        Gets the selected item from the listbox and deletes it from the listbox
        
        updates the total and the total after tax
        
        '''
        selected_indices = receipt_class.listbox.curselection()
        selected_item = (receipt_class.listbox.get(selected_indices))
        item_name = get_item_from_receipt_page(selected_item)
        receipt_class.listbox.delete(selected_indices)
        item_price = receipt_class.items[item_name].pop(-1)[0]
        
        if receipt_class.items[item_name] == []:
                del receipt_class.items[item_name]
        receipt_class.total = receipt_class.total - item_price
        receipt_class.tax = receipt_class.total * 1.08
        receipt_class.total_label.config(text=f"Total (before tax): ${round(receipt_class.total,2)}")
        receipt_class.total_label_2.config(text=f"(after tax): ${round(receipt_class.tax,2)}")
        return item_price
         
def get_item_from_receipt_page(string):
        '''
        Taking in a string format like so: fried_dumplings-------5.2
        
        returns:
        fried_dumplings
        '''
        split_index = string.find('-')
        return string[:split_index]

def make_one_section_page(section_class, parent_frame, receipt_class, pos_class):
        '''
        taking in a sections class intance and a parent frame, it creates buttons that corresponds to the items that are in that section on that parent frame.
        
        returns a dictionary that contains these buttons
        '''
        return_button_frame = tk.Frame(parent_frame)
        return_button_frame.grid(row=0, column=0)

        return_button = tk.Button(return_button_frame, text="Return", command= lambda pos_class = pos_class, parent_frame = parent_frame: return_to_homepage(pos_class, parent_frame))
        return_button.grid(row=0, column=0)
        
        
        menu_items_frame = tk.Frame(parent_frame)
        menu_items_frame.grid(row=1, column=0)
        
        list_of_items = section_class.get_list_of_items()
        overall_dictionary = get_item_names(list_of_items)
        list_of_items_name = list(overall_dictionary.keys())
        return_dict = make_button_grid(list_of_items_name, 4, menu_items_frame)
        
        #add commands for all keys for this one section
        for key in return_dict:
                button = return_dict[key]
                button.config(command=lambda value = key, price_dictionary=overall_dictionary: add_price_button_command(price_dictionary, value, receipt_class))
                
        return_dict['return_button_frame'] = return_button_frame
        return_dict['return_button'] = return_button
        return_dict['menu_items_frame'] = menu_items_frame
        
        return return_dict

def add_price_button_command(price_dictionary, dictionary_key, receipt_class):
        '''
        Gets the price of the item from the menu button that was clicked and add it to the receipt and total
        '''
        #print(price_dictionary[dictionary_key])
        item_price = price_dictionary[dictionary_key][0]
        item_class = price_dictionary[dictionary_key][1]
        item_en_name = item_class.en_name
        
        if item_en_name in receipt_class.items:
                receipt_class.items[item_en_name].append((item_price,item_class))
        else:
                receipt_class.items[item_en_name] = [(item_price,item_class)]
        #print(receipt_class.items)
        receipt_class.listbox.insert('end', item_class.en_name + "---------" + str(item_price))
        receipt_class.total += item_price
        receipt_class.tax = receipt_class.total*1.08
        receipt_class.total_label.config(text=f"Total (before tax): ${round(receipt_class.total,2)}")
        receipt_class.total_label_2.config(text=f"(after tax): ${round(receipt_class.tax,2)}")
        return item_price

def get_item_names(list_of_menu_items):
        '''
        Taking in a list of menu_items objects, it returns a list of strings that contains the information needed to be displayed on the buttons.
        
        ex.
        returns
        
        {
                '15. Chicken Teriyaki Stick\n(雞肉串)\n$4.8' : [4.8, menu_item_class],
                
                '14. Pu Pu Platter\n(寶賓船)\n$5.7': [5.7, menu_item_class]
        }
        '''
        return_list = {}
        for item in list_of_menu_items:
                item_number = item.get_number()
                item_en_name = item.get_en_name()
                item_chinese_name = item.get_chinese_name()
                item_small_price = item.get_small_price()
                item_large_price = item.get_large_price()
                
                small_string =item_number + '. '+ item_en_name + '\n(' + item_chinese_name + ')\n$' + str(item_small_price)
                #return_list.append(small_string)
                return_list[small_string] = [item_small_price, item]
                
                if float(item_large_price) != 0.0:
                        large_string =item_number + '. '+ item_en_name + '\n(' + item_chinese_name + ')\n$' + str(item_large_price)
                        #return_list.append(large_string)
                        return_list[large_string] = [item_large_price,item]
                        
        return return_list

                
def make_button_grid(list_of_keys, button_count_col, parent_frame):
        '''
        Given a list of keys, the number of buttons that you want in each row, and a parent frame,
        
        this puts the buttons into the parent frame and returns a dictionary that contaisn pointers to each button just in case if the user wants to config anything about these buttons later on
        '''
        row=0
        return_button_dict= {}
        for i in range (len(list_of_keys)):
                button = tk.Button(parent_frame, text=list_of_keys[i], width = 25, height=4)
                
                return_button_dict[list_of_keys[i]] = button
                
                if i%button_count_col == 0:
                        row += 1
                button.grid(row = row, column = i%button_count_col )

        return return_button_dict

class menu_item():
        def __init__(self, number, en_name, chinese_name, small_price, large_price=0, spicy = None):
                self.number = number
                self.en_name = en_name
                self.chinese_name = chinese_name
                self.small_price = small_price
                self.large_price = large_price
                self.spicy = spicy
        
        def get_number(self):
                return self.number
        
        def get_small_price(self):
                return self.small_price
        
        def get_large_price(self):
                return self.large_price
        
        def get_en_name(self):
                return self.en_name
        
        def get_chinese_name(self):
                return self.chinese_name
        
        # def __repr__(self):
        #         if self.spicy != None:  
        #                 return  self.number + '| ' + self.en_name + ' ( '  + self.chinese_name + ') ' + str(self.small_price) + ', ' + str(self.large_price) + ',' + ' Spicy: ' + str(self.spicy) + '\n'
        #         else:
        #                 return  self.number + '| ' + self.en_name + ' ( '  + self.chinese_name + ') ' + str(self.small_price) + ', ' + str(self.large_price) + '\n'
        

class section():
        def __init__(self, list_of_items):
                items_dictionary = {}
                self.list_of_items = list_of_items
                for item in list_of_items:
                        item_en_name = item.get_en_name()
                        item_chinese_name = item.get_chinese_name()
                        items_dictionary[item_en_name] = item
                        items_dictionary[item_chinese_name] = item
                self.items_dictionary = items_dictionary  
        
        
        def get_list_of_items(self):
                return self.list_of_items
        
        def get_items_dictionary(self):
                return self.items_dictionary
        
        def get_item(self, item_name):
                try:
                        return self.items_dictionary[item_name]
                except:
                        return "Item does not exist in this section!!"
        
        def __repr__(self):
                return repr(self.items_dictionary)
        

class appetizers(section):
        pass
        
class soup(section):
        pass

class fried_rice(section):
        pass
        
class lo_mein(section):
        pass

class chow_mein(section):
        pass

class chop_suey(section):
        pass

class sweet_and_sour(section):
        pass

class vegetables(section):
        pass

class egg_foo_young(section):
        pass

class moo_shu_dish(section):
        pass

class mei_fun(section):
        pass

class pork(section):
        pass

class beef(section):
        pass

class chicken(section):
        pass

class side_order(section):
        pass

class seafood(section):
        pass

class special_combo_plates(section):
        pass

class diet_food(section):
        pass

class chef_special(section):
        pass

class lunch_special(section):
        pass