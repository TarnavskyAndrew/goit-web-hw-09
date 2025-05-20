from colorama import Fore


def input_error(func):
    def inner(*args, **kwargs):
        try:            
            return func(*args, **kwargs)  # викликаємо функцію і відразу повертаємо результат                           
        except (IndexError, ValueError, KeyError) as e:
            return f"{Fore.RED}[ERROR:]{Fore.RESET} {e}"
        
        # except ValueError:
        #     return f"{Fore.RED}[ERROR:]{Fore.RESET} Please write your name and phone number."
        # except KeyError:
        #     return f"{Fore.RED}[ERROR:]{Fore.RESET} Enter user name"
        # except IndexError:
        #     return f"{Fore.RED}[ERROR:]{Fore.RESET} Please provide enough information"
    return inner



