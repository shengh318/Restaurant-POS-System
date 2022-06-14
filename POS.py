import os
import tkinter as tk
from sections import *
import useful_functions

main_window = tk.Tk()
main_window.title("POS System")
main_window.geometry("1700x600")
directed_path_to_file = os.path.dirname(__file__)

make_sections_dictionary = {
        'appetizers': lambda:  appetizers(import_items_from_file('appetizers.txt')),
        
        'soup': lambda:  soup(import_items_from_file('soup.txt')),
        
        'fried_rice': lambda: fried_rice(import_items_from_file('fried_rice.txt')),
        
        'lo_mein': lambda: lo_mein(import_items_from_file('lo_mein.txt')),
        
        'chow_mein': lambda: chow_mein(import_items_from_file('chow_mein.txt')),
        
        'chop_suey': lambda: chop_suey(import_items_from_file('chop_suey.txt')),
        
        'sweet_and_sour': lambda: sweet_and_sour(import_items_from_file('sweet_and_sour.txt')),
        
        'vegetables': lambda: vegetables(import_items_from_file('vegetables.txt')),
        
        'egg_foo_young': lambda: egg_foo_young(import_items_from_file('egg_foo_young.txt')),
        
        'moo_shu_dish': lambda: moo_shu_dish(import_items_from_file('moo_shu_dish.txt')),
        
        'mei_fun': lambda: mei_fun(import_items_from_file('mei_fun.txt')),
        
        'pork': lambda: pork(import_items_from_file('pork.txt')),
        
        'beef': lambda: beef(import_items_from_file('beef.txt')),
        
        'chicken': lambda: chicken(import_items_from_file('chicken.txt')),
        
        'side_order': lambda: side_order(import_items_from_file('side_order.txt')),
        
        'seafood': lambda: seafood(import_items_from_file('seafood.txt')),
        
        'special_combo_plates': lambda: special_combo_plates(import_items_from_file('special_combo_plates.txt')),
        
        'diet_food': lambda: diet_food(import_items_from_file('diet_food.txt')),
        
        'chef_special': lambda: chef_special(import_items_from_file('chef_special.txt')),

        'lunch_special': lambda: lunch_special(import_items_from_file('lunch_special.txt')),
              
}


def make_nessary_sections():
        '''
        Makes all of the nessary sections on the menu for the internal representation of the code
        '''
        sections_dictionary = {}
        for key in make_sections_dictionary:
                sections_dictionary[key] = make_sections_dictionary[key]()
        return sections_dictionary


def import_items_from_file(file_name):
        '''
        Taking in a file_name that contains the information about the items in that section on the menu, it returns a list of items that has already been converted into the menu_items objects for internal uses
        
        '''
        abs_path_file_path = directed_path_to_file + '\\sections\\' + file_name
        file_1 = open(abs_path_file_path, 'r', encoding='utf-8')
        
        lines = file_1.readlines()
        list_of_items = []
        for line in lines:
                item = useful_functions.convert_txt_line_to_item(line)
                list_of_items.append(item)
        file_1.close()
        return list_of_items

# print(make_nessary_sections()['lunch_special'])

def convert_to_format(string):
        '''
        Taking in an old format like so:
        
        old_format_1 = 40. House Special Lo Mein (本樓撈麵) $5.20
        
        or 
        
        old for_mat_2 = 79. Beef w. Mushroom 蘑菇牛 $9.45
        
        it returns lines like so
        
        79, Beef w. Mushroom, 蘑菇牛, 9.45, 0
        '''
        alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ&\' '
        pass_char = '()$.- '
        period_index = string.find('.')
        item_number = string[0:period_index]
        item_en_name = ''
        item_chinese_name = ''
        item_price = ''
        for i in range (period_index+1, len(string)):
                current_char = string[i]
                if current_char in alphabet:
                        item_en_name += current_char
                elif current_char in pass_char:
                        pass
                elif current_char.isdigit():
                        item_price += current_char
                else:
                        item_chinese_name += current_char
        
        format_item_price = item_price[:-2] + '.' + item_price[-2:]
        return_string = item_number.strip() +  ', ' + item_en_name.strip() + ', ' + item_chinese_name.strip() + ', ' +  format_item_price.strip()
        return return_string


def rewrite_old_to_new(old_file_path, new_file_path):
        old_file = open(old_file_path, 'r', encoding='utf-8')
        new_file = open(new_file_path, 'w', encoding='utf-8')
        old_lines = old_file.readlines()
        for line in old_lines:
                new_line = convert_to_format(line)
                new_file.write(new_line + '\n')
        old_file.close()
        new_file.close()
        

sections_dict = make_nessary_sections()

pos_sys = POS_SYS(main_window, sections_dict)


main_window.mainloop()