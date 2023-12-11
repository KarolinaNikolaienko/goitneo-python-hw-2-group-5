import re

class PhoneNumError(Exception):
    pass

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Invalid data was given"
        except KeyError:
            if func.__name__ == "show_phone":
                return f"Contact {args[0].capitalize()} does not exist"
            else:
                return "Contact does not exist"
        except IndexError: # have never been caught
            return "Invalid command"
        except PhoneNumError:
            return "Phone must consist of 10 digits"
    return inner

@input_error
def parse_input(user_input):
    """Parses entered by user command.
    The command splits on 'cmd' - action that user wants the program to do,
    and 'args' - data on which the action is performed.
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    name, phone = args
    name = name.capitalize()
    if phone:
        num = re.findall(r"^\d{10}$", phone)  # ^(?:(?:\d{10})|(?:\+\d{12}))$ for numbers 10 digits and '+' 12 digits
        if not num:
            raise PhoneNumError
    if contacts and contacts.get(name, False): # if contacts are not empty and the contact being added already exists
        print(f"Contact {name} already exists. Do you want to rewrite it?")
        command = input("Yes / No:  ").strip().lower()
        while command not in ["yes", "no"]:
            command = input("Invalid command\nYes / No:  ").strip().lower()
        if command == "no":
            return "Contact remained unchanged"
        elif command == "yes":
            contacts[name] = phone
            return "Contact was rewritten"
    contacts[name] = phone
    return "Contact added"

@input_error
def change_contact(args, contacts):
    name, phone = args
    name = name.capitalize()
    if phone:
        num = re.findall(r"^(?:(?:\d{10})|(?:\+\d{12}))$", phone)
        if not num:
            raise PhoneNumError
    if contacts and contacts.get(name, False): 
        contacts[name] = phone
        return "Contact updated"
    else:
        print(f"Contact {name} does not exist. Do you want to add it?")
        command = input("Yes / No:  ").strip().lower()
        while command not in ["yes", "no"]:
            command = input("Invalid command\nYes / No:  ").strip().lower()
        if command == "no":
            return "Contact was not added"
        elif command == "yes":
            contacts[name] = phone
            return "Contact added"

@input_error
def show_phone(name, contacts):
    name = name.capitalize()
    return contacts[name]


def all_contacts(contacts):
    if not contacts:
        return "Contact list is empty"
    str = ""
    for name, number in contacts.items():
        str += f"{name} {number}\n"
    return str.strip()

@input_error # IndexError is possible, but was never caught
def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        command = parse_input(input("Enter a command: ").strip().lower())

        if command[0] in ["close", "exit"]:
            print("Good bye!")
            break

        elif command[0] in ["hello", "hi"]:
            print("How can I help you?")
        
        elif command[0] == "add":
            print(add_contact(command[1:], contacts))
        elif command[0] == "change":
            print(change_contact(command[1:], contacts))
        elif command[0] == "phone":
            print(show_phone(command[1], contacts))
        elif command[0] == "all":
            print(all_contacts(contacts))
        
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()