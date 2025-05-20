from abc import ABC, abstractmethod

class UserView(ABC):
    @abstractmethod
    def display_contact(self, contact):
        pass

    @abstractmethod
    def display_help(self):
        pass

    @abstractmethod
    def display_message(self, message):
        pass