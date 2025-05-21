# bot_assistant
from colorama import Fore
from models.AddressBook import AddressBook
from views.console_view import ConsoleView
from utils.region import get_valid_region
from handlers.commands import (
    add_contact,
    change_contact,
    show_phone,
    show_all_contacts,
    add_birthday,
    show_birthday,
    birthdays,
    delete_contact
)

def parse_input(user_input):           
    parts = user_input.strip().split()
    if not parts:
        return "", []                           # якщо користувач введе пусте значення
    cmd, *args = parts
    return cmd.lower(), args                    # повертаємо команду та аргументи як список


def main():
    view = ConsoleView()

    # 1. Привітання бота
    view.display_message(f"{Fore.GREEN}Welcome to the assistant bot!{Fore.RESET}") 

    # 2. Введення регіону
    region = get_valid_region(view)  # отримуємо регіон від користувача 

    # 3. Завантажуємо адресну книгу з файлу та продовжуємо роботу
    book = AddressBook.load_data()  
    
    # 5. Виводимо список доступних команд      
    while True:
        user_input = input(f"{Fore.YELLOW}>{Fore.RESET} Enter a command: ")   
        command, args = parse_input(user_input)

        if not command:
            view.display_message(f"{Fore.YELLOW} Empty input. Type a command like 'hello' or 'add'.{Fore.RESET}")   
            continue                            # користувач нічого не ввів - пропускаємо

        if command in ["close", "exit"]:        # exit або close – завершити роботу бота.
            AddressBook.save_data(book)         # зберігає будь-який екземпляр AddressBook
            view.display_message(f"{Fore.GREEN}Goodbye, have a nice day!{Fore.RESET}")            
            break
        
        
        elif command == "hello":                # hello – вітання від бота.
            view.display_message("How can I help you?")            
            
        elif command == "add":                  # add [ім'я] [номер] — додати новий контакт або номер до наявного.
            view.display_message(add_contact(args, book, region))  
            
        elif command == "change":               # change [ім'я] [старий_номер] [новий_номер] — щоб змінити номер телефону для вказаного контакту.
            view.display_message(change_contact(args, book, region))                   

        elif command == "phone":                # phone [ім'я] — щоб показати всі номери телефону для вказаного контакту.
            view.display_message(show_phone(args, book))

        elif command == "all":                  # all — показати всі контакти з номерами та датами привітання (якщо є).
            view.display_contact(show_all_contacts(book))
    
        elif command == "add-birthday":         # add-birthday [ім'я] [DD.MM.YYYY] – додати дату народження до контакту.
            view.display_message(add_birthday(args, book))

        elif command == "show-birthday":        # show-birthday [ім'я] – показати дату народження вказаного контакту.
            view.display_message(show_birthday(args, book))

        elif command == "birthdays":            # birthdays - показати список контактів, яких потрібно привітати по днях на наступному тижні.
            view.display_message(birthdays(args, book))   
            
        elif command == "delete":               # delete [ім'я] – видалити контакт з адресної книги.
            view.display_message(delete_contact(args, book))            

                    
        else:
            view.display_message("Invalid command.")

if __name__ == "__main__":
    main()