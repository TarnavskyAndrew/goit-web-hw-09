from models.record import Record
from utils.decorators import input_error

@input_error
# Функція додає новий контакт або оновлює існуючий.
# Якщо контакт з таким ім'ям вже існує — до нього додається номер телефону.
def add_contact(args, book, region="UA"):
    name, phone = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone, region)
    return "Contact added/updated."

@input_error
# Функція замінює старий номер телефону на новий для вказаного контакту.
# Якщо контакт не знайдено — повертає повідомлення про помилку.
def change_contact(args, book, region="UA"):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone, region)
        return "Phone updated."
    return "Contact not found."

@input_error
# Функція повертає всі номери телефону для вказаного імені.
# Якщо запис не знайдено — повідомляє про це.
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        phones = ", ".join([phone.value for phone in record.phones])
        return f"{name}: {phones}"
    return "Contact not found."

@input_error
# Функція виводить всі збережені контакти з номерами телефону та, за наявності, з днем народження.
def show_all_contacts(book):
    return book.show_all_contacts() or "No contacts found."

@input_error
# Функція додає дату народження до існуючого контакту. Формат дати має бути DD.MM.YYYY.
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    return "Contact not found."

@input_error
# Функція показує дату народження вказаного контакту, якщо вона збережена.
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is {record.birthday.value}"
    return "Birthday not found."

@input_error
# Функція повертає список контактів, у яких день народження наступає протягом найближчих 7 днів.
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if upcoming:
        return "\n".join([f"{name} — Greetings: {date.strftime('%d.%m.%Y')}" for name, date in upcoming])
    return "No upcoming birthdays."
