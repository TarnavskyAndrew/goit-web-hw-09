from datetime import datetime
from utils.phone_utils import load_phone_codes


# 1. Базовий клас для всіх полів запису
class Fields: 
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    
# 2. Клас імені - обов'язкове поле
class Name(Fields): 
    pass


# 3. Клас телефону з валідацією номера 
class Phone:
    def __init__(self, phone, region="UA"):
        self.region = region.upper()
        self.value = self.format_phone(phone)

    def format_phone(self, phone):
        phone_codes = load_phone_codes()  # загрузка телефонных кодов из CSV
        user_digits = "".join(filter(str.isdigit, phone)) # видаляємо все, крім цифр

    # Якщо регіон - Україна (UA)          
        
        if self.region == "UA":
            return self.format_ukrainian(user_digits)
        else:
            return self.format_international(user_digits, phone_codes)        

    def format_ukrainian(self, user_digits):
        if len(user_digits) == 10 and user_digits.startswith("0"):
            user_digits = user_digits[1:]  # прибираємо 0
        elif len(user_digits) != 9:
            raise ValueError("Enter the number in the format 0671234567 or 671234567")

        code = "+380"
        operator = user_digits[:2]  # 67
        rest = user_digits[2:]      # 1234567
    
        return f"{code}({operator}){rest[:3]}-{rest[3:5]}-{rest[5:]}"    
        
    # Якщо регіон - інша країна
        
    def format_international(self, user_digits, phone_codes):
        code = phone_codes.get(self.region, "")
        if not code:
            raise ValueError(f"Телефонный код для региона {self.region} не найден.")
        
        # Стандарт ITU-T E.164: 10–15 цифр (включачи код країни)
        # Введений номер телефону без коду країни
        if len(user_digits) < 6 or len(user_digits) > 12:
            raise ValueError("Введите от 6 до 12 цифр без кода страны (он подставится автоматически).")        
        
        digits = code.replace("+", "") + user_digits # убираємо знак "+" з коду країни + номер телефону
        
        # Повний номер телефону, включаючи код країни
        if len(digits) < 10 or len(digits) > 15:
            raise ValueError("Полный номер должен содержать от 10 до 15 цифр.")

        # Розбиваємо: внутрішній код, номер
        internal = digits[len(code)-1:len(code)+2]  # наприклад "501" чи "30"
        rest = digits[len(code)+2:]  # остатня частина номера    
            
        # Форматування. Приблизний формат: +1 (501) 234-567
        if len(rest) == 6:
            return f"{code}({internal}){rest[:3]}-{rest[3:]}"
        if len(rest) >= 7:
            return f"{code}({internal}){rest[:3]}-{rest[3:6]}-{rest[6:]}"
        else:
            return f"{code}({internal}){rest}" 
        
        
    def normalized(self):   # повертає номер телефону без форматування
        return "".join(filter(str.isdigit, self.value))

    def __eq__(self, other):   # порівнюємо два номери
        if isinstance(other, Phone):
            return self.normalized() == other.normalized()
        elif isinstance(other, str):
            return self.normalized() == "".join(filter(str.isdigit, other))
        return False    
  
    def __str__(self):
        return self.value
            

# 4. Клас з датою народження, додає перевірку формату дати DD.MM.YYYY.
class Birthday(Fields):

    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")            