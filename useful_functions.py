import sections
import os

def convert_txt_line_to_item(line):
        '''
        Taking in a line formatted like so: 1, Spring Roll, 上海春卷, 1.10
        
        returns a menu_item object which in the repr looks like this: 
        
        Number: 1
        English Name: Spring Roll
        Chinese Name: 上海春卷   
        Small: 1.1
        Large: 0
        Spicy: None
        
        '''
        splitted_line = line.replace('\n', '').split(',')
        stripped_line = [item.strip() for item in splitted_line]
        item_number = stripped_line[0]
        item_en_name = stripped_line[1]
        item_chinese_name = stripped_line[2]
        item_small_price = float(stripped_line[3])
        item_large_price = 0
        item_spicy = None
        if len(stripped_line) == 5:
                fifth_item = stripped_line[4]
                try:
                        item_large_price = float(fifth_item)
                except:
                        item_spicy = True
        elif len(stripped_line) == 6:
                item_large_price = stripped_line[4]
                item_spicy = True
        
        return sections.menu_item(item_number, item_en_name, item_chinese_name, item_small_price, item_large_price, item_spicy)


def write_to_file(file_path, list_of_strings):
        '''
        Taking in a filepath of the file that you want to write to and a list of string, it writes all the strings from the list to that file. txt files only
        '''
        new_file = open(file_path, 'w', encoding='utf-8')
        for string in list_of_strings:
                new_file.write(string+"\n")
        new_file.close()

#BELOW ARE FUNCTIONS ONLY USED TO FORMAT TXT FILES

def convert_all_txt_to_menu_items(all_items_list):
        '''
        Taking in a list of items written in txt format, it returns a list of menu_items that are made from these txt lines
        '''
        return_list = []
        for i in range(len(all_items_list)):
                item = convert_txt_line_to_item(all_items_list[i])
                #print(f"{i}: {item.chinese_name}")
                return_list.append(item)
        return return_list
        
def make_strings_from_menu_items(list_of_menu_items):
        '''
        Taking in a list of menu items, it takes each one and makes string in this format:
        
        1.fried_dumplings-------5.2
        '''
        return_strings = []
        for item in list_of_menu_items:
                item_name = item.en_name
                item_small_price = item.small_price
                add_string = item.number + '.' + item_name + '-------' + str(item_small_price) 
                if item.spicy != None:
                        add_string += f"--{item.spicy}"
                
                return_strings.append(add_string)
                if item.large_price != 0:
                        add_string = item.number + '.' + item_name + "-------" + str(item.large_price)
                        
                        if item.spicy != None:
                                add_string += f"--{item.spicy}"
                        return_strings.append(add_string)
        return return_strings

def read_text_file(file_path, list_of_items):
        '''
        Takes in a filepath and a list of items that will bhe mutated, it reads each line from the file and adds it to the list of items
        '''
        with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                        list_of_items.append(line.replace('\n', ''))
       
def read_all_files_from_folder():
        '''
        Looks through a folder and finds all of the txt files. Reads them, saves each line in the txt file to a list and return that list
        '''
        directed_path_to_file = os.path.dirname(__file__)
        
        folder_path = directed_path_to_file + "\\sections"
        
        os.chdir(folder_path)
        list_of_items = []
        for file in os.listdir():
                if file.endswith(".txt"):
                        file_path = f"{folder_path}\{file}"
                        read_text_file(file_path, list_of_items)
        
        return list_of_items