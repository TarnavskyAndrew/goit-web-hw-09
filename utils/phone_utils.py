import csv

def load_phone_codes(filepath="data/country_codes.csv"):
    codes = {}
    with open(filepath, encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            a2 = row["A2"].upper().strip()
            code = row["Phone Code"].strip()
            if a2 and code:
                codes[a2] = code
    return codes 