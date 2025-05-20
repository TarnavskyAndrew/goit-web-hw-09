from colorama import Fore
import csv

def get_supported_regions_from_file(filepath):
    with open(filepath, encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row["A2"].upper() for row in reader if row["A2"].strip()]


def get_valid_region(view, filepath="data/country_codes.csv"):
    country_codes = get_supported_regions_from_file(filepath)
    
    while True:     
        region_input = input(
            "\nEnter the region code (eg UA, US, DE).\n"
            "Press Enter to use the default region: UA\n"
            ">>> "
        ).strip().upper()     
        
        if region_input in ["EXIT", "CLOSE"]:  # якщо користувач ввів close або exit
            view.display_message(f"{Fore.GREEN}Goodbye, have a nice day!{Fore.RESET}") 
            exit()                         

        if not region_input:
            return "UA"

        if region_input not in country_codes:
            view.display_message(
                f"Region '{region_input}' is not supported.\n" 
                f"Valid regions are: {', '.join(sorted(country_codes))}"
            )
        else:
            return region_input 