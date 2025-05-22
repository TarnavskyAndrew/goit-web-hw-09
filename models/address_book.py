from collections import UserDict
from datetime import datetime, timedelta
import pickle
# from colorama import Fore

#  5. Адресна книга: зберігає всі записи
class AddressBook(UserDict): 
           
    def add_record(self, record): # додає телефон 
        self.data[record.name.value] = record
        
    def find(self, name): # повертає на ім'я 
        return self.data.get(name) 
    
    def delete(self, name): # видаляє на ім'я         
        if name in self.data:
            del self.data[name]
        else:                
            # print(f"Contact '{name}' not found.")
            return None  
        
    def show_all_contacts(self):
        if not self.data:
            return "No contacts yet."  # якщо адресна книга пуста, повертаємо повідомлення        
        return "\n".join(str(record) for record in self.data.values())   # Повертаємо всі контакти у вигляді рядка 
    
    
    # Функція перенесення поздоровлень з вихідних 
    def adjust_for_weekend(self, date):
        if date.weekday() == 5:  # Суббота
            return date + timedelta(days=2)
        elif date.weekday() == 6:  # Воскресенье
            return date + timedelta(days=1)
        return date
    
    # Метод для отримання майбутніх привітань    
    def get_upcoming_birthdays(self, days=7):
        today = datetime.today().date()
        upcoming_birthdays = []
        
        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                birthday_this_year = birthday_date.replace(year=today.year)
                
                # Якщо день народження вже пройшов цього року, то переносимо на наступний
                
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                    
                # Переносимо вітання з вихідних
                
                congrat_date = self.adjust_for_weekend(birthday_this_year)
                day_diff = (congrat_date - today).days
                if 0 <= day_diff <= days:
                    upcoming_birthdays.append((record.name.value, congrat_date))
        return upcoming_birthdays
    
    
    # Метод зберігає переданий об'єкт адресної книги у файл у форматі pickle.
    @staticmethod 
    def save_data(book, filename="data/addressbook.pkl"):
        with open(filename, "wb") as file:
            pickle.dump(book, file)
            
            
    # Метод завантажує об'єкт адресної книги з файлу у форматі pickle.
    @staticmethod 
    def load_data(filename="data/addressbook.pkl"):        
        try:
            with open(filename, "rb") as file:                
                return pickle.load(file)
        except FileNotFoundError:
            return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

 
    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
    
    
    
  