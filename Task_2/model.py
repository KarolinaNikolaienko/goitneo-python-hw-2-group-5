from collections import UserDict
import re

class PhoneNumError(Exception):
    pass

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            print( "No phone was found")
        except KeyError:
            print( "Record wasn't found")
        except IndexError: 
            print( "Index error")
        except PhoneNumError:
            print( "Phone must consist of 10 digits")
    return inner

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    
    @input_error
    def add_phone(self, phone):
        if re.findall(r"^\d{10}$", phone):
            self.phones.append(Phone(phone))
        else:
            raise PhoneNumError
        #print("Phone was added")
    
    @input_error
    def edit_phone(self, old_phone, new_phone):
        changes = False
        for index, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones.remove(phone)
                self.phones.insert(index, Phone(new_phone))
                changes = True
                break
        if not changes:
            print("No phone was found")
    
    @input_error
    def remove_phone(self, phone):
        self.phones.remove(Phone(phone))
        #print("Phone was deleted")
    
    def find_phone(self, phone):
        found_phone = "No phone was found"
        for phone_ in self.phones:
            if phone_.value == phone:
                found_phone = phone_
                break
        return found_phone



    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record:Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)
    
    @input_error #Key error posible
    def delete(self, name): 
        return f"Record {self.data.pop(name)} was deleted from adress book"

