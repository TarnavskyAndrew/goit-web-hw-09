from views.abstract_view import UserView

class ConsoleView(UserView):
    def display_contact(self, contact):
        print("\nAll contacts:")
        print(contact)

    def display_help(self):
        print("\n List of commands:")
        print("  hello       — greeting")
        print("  add         — add contact")
        print("  change      — change contact")
        print("  phone       — show phone")
        print("  show all    — all contacts")
        print("  help        — help")
        print("  exit        — exit")

    def display_message(self, message):
        print(f": {message}")
        