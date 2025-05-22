from models.address_book import AddressBook
from models.fields import Phone
from utils.phone_utils import load_phone_codes


book = AddressBook.load_data() # завантажуємо існуючу адресну книгу з файлу
phone_codes = load_phone_codes()  # A2 -> завантажуємо словник телефонних кодів: {"UA": "+380", "US": "+1", ...}

# Шнветуємо словник телефонних кодів, щоб отримати регіон за префіксом телефону: : "380" → "UA", "+1" → "US",..
prefix_to_region = {
    phone_code.replace("+", ""): region_code
    for region_code, phone_code in phone_codes.items()
}
# Створюємо список префіксів, відсортований за довжиною від більшого до меншого, щоб знайти найдовший можливий збіг (наприклад, "380" перед "38").
prefixes_sorted = sorted(prefix_to_region.keys(), key=len, reverse=True)

for record in book.data.values():
    new_phones = [] #Створюємо новий список для збереження переформатованих телефонів цього контакту. 

    for old_phone in record.phones:
        digits_only = "".join(filter(str.isdigit, old_phone.value)) # видаляємо все, крім цифр 
        region_code = None
        user_part = None

        # визначаємо регіон за префіксом
        if digits_only.startswith("380"):
            region_code = "UA"
            user_part = digits_only[3:]  # відрізаємо "380"
            if user_part.startswith("0"):  # якщо залишився "0", видаляємо його
                user_part = user_part[1:]

        else:
            for prefix in prefixes_sorted: # перебираємо префікси
                if digits_only.startswith(prefix): # перевіряємо, чи починається номер з префікса
                    region_code = prefix_to_region[prefix]   # отримуємо регіон за префіксом
                    user_part = digits_only[len(prefix):]   # видаляємо префікс з номера
                    break

        if region_code and user_part: # якщо регіон і частина номера знайдені
            try:
                new_phone = Phone(user_part, region_code) # створюємо новий номер телефону
                new_phones.append(new_phone) # додаємо новий номер до списку
            except Exception as e:
                print(f"Error recreating number {old_phone.value}: {e}") 
        else:
            print(f"Failed to determine country for number: {old_phone.value}")

    record.phones = new_phones  # оновлюємо список телефонів контакту на нові (переформатовані)

AddressBook.save_data(book) # зберігаємо оновлену адресну книгу з новими телефонами у файл.
print("All numbers resaved with correct region.")