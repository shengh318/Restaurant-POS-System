import os

class already_in_system_customers():
        def __init__(self, address, phone_number, order_list, total):
                self.address = address
                self.phone_number = phone_number
                self.order_list = order_list
                self.total = total
                self.tax = self.total*1.08
        
        def __repr__(self) -> str:
                return f"{self.phone_number}: {self.total}"
                
        def update_address(self, new_address):
                self.address = new_address

def order_list_to_string(already_customer_class):
        '''
        Taking the order list from the already_customer_class and basically returning a string that has all items in the order list seperated by ","
        '''
        return_string = ""
        for item in already_customer_class.order_list:
                return_string  += item + ","
        return return_string

def write_to_customer_folder(customer_folder_path, already_customer_class):
        '''
        Writes all of the nessary information that we need for the customer in the receipt
        '''
        new_customer_path = f"{customer_folder_path}\{already_customer_class.phone_number}.txt"
        
        with open(new_customer_path, 'w', encoding='utf-8') as f:
                f.write(str(already_customer_class.phone_number) + '\n')
                f.write(already_customer_class.address + '\n')
                
                order_string = order_list_to_string(already_customer_class)
                
                f.write(order_string + '\n')
                f.write(str(already_customer_class.total) + '\n')


def convert_txt_to_already_customer_class(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                information_list = []
                for line in lines:
                        information_list.append(line.strip())
                
                customer_phone_number = int(information_list[0])
                customer_address = information_list[1]
                
                
                customer_order_list = information_list[2].split(',')
                
                filtered_list = []
                for item in customer_order_list:
                        if item != '':
                                filtered_list.append(item)

                customer_total = float(information_list[3])
                
                new_customer_class = already_in_system_customers(customer_address, customer_phone_number, filtered_list, customer_total)
                
                return new_customer_class

def import_from_folder(pos_class, folder_path):
        '''
        Going into the customer folder path, and it adds the phone number and the already_customer class into the pos_class.already_customers
        
        ex.
        pos.already_csutomers = {
                
           1234: already_customer_class     

        }
        '''
        customer_dictionary = pos_class.already_customers
        customer_folder_path = f"{folder_path}\customer"
        os.chdir(customer_folder_path)
        for file in os.listdir():
                if file.endswith(".txt"):
                        file_path = f"{customer_folder_path}\{file}"
                        new_customer_class = convert_txt_to_already_customer_class(file_path)
                        new_customer_phone = new_customer_class.phone_number
                        customer_dictionary[new_customer_phone] = new_customer_class
                        
                
        

        
        
        
                
                