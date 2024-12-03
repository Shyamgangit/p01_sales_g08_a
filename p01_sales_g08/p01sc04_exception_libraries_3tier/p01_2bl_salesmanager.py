import p01_1da_sales as sd
import csv
from decimal import Decimal, InvalidOperation
import locale as lc
from datetime import datetime
from pathlib import Path

lc.setlocale(lc.LC_ALL, "en_US")

def import_all_sales() -> list:
    try:
        with open(sd.FILEPATH / sd.ALL_SALES, newline='') as csvfile:
            reader = csv.reader(csvfile)
            sales_list = []
            for line in reader:
                if len(line) > 0:
                    *amount_sales_date, region_code = line
                    sd.correct_data_types(amount_sales_date)
                    amount, sales_date = amount_sales_date[0], amount_sales_date[1]
                    data = {
                        "amount": amount,
                        "sales_date": sales_date,
                        "region": region_code,
                    }
                    sales_list.append(data)
            return sales_list
    except FileNotFoundError:
        print("Sales file not found")
        return []

def view_sales(sales_list: list) -> bool:
    bad_data_flag = False
    if len(sales_list) == 0:
        print("No sales to view.\n")
    else:
        col1_w, col2_w, col3_w, col4_w, col5_w = 5, 15, 15, 15, 15
        total_w = col1_w + col2_w + col3_w + col4_w + col5_w
        print(f"{' ':{col1_w}}"
              f"{'Date':{col2_w}}"
              f"{'Quarter':{col3_w}}"
              f"{'Region':{col4_w}}"
              f"{'Amount':>{col5_w}}")
        print(horizontal_line := f"{'-' * total_w}")
        total = Decimal('0.0')

        for idx, sales in enumerate(sales_list, start=1):
            if sd.has_bad_data(sales):
                bad_data_flag = True
                num = f"{idx}.*"
            else:
                num = f"{idx}."

            amount_str = sales["amount"]
            try:
                amount = Decimal(amount_str)
                if not sd.has_bad_amount(sales):
                    total += amount
            except InvalidOperation:
                amount = "Invalid Amount"
                bad_data_flag = True

            sales_date = sales["sales_date"]
            if sales_date == "?":
                sales_date_str = "Invalid Date"
                month = 0
            else:
                if isinstance(sales_date, str):
                    sales_date = datetime.strptime(sales_date, '%Y-%m-%d').date()
                sales_date_str = sales_date.strftime('%Y-%m-%d')
                month = int(sales_date_str.split("-")[1])

            region = sd.get_region_name(sales["region"])
            quarter = f"{sd.cal_quarter(month)}"
            print(f"{num:<{col1_w}}"
                  f"{sales_date_str:{col2_w}}"
                  f"{quarter:<{col3_w}}"
                  f"{region:{col4_w}}"
                  f"{lc.currency(amount, grouping=True) if isinstance(amount, Decimal) else amount:>{col5_w}}")

        print(horizontal_line)
        print(f"{'TOTAL':{col1_w}}"
              f"{' ':{col2_w + col3_w + col4_w}}"
              f"{lc.currency(total, grouping=True):>{col5_w}}\n")
    return bad_data_flag

def add_sales1(sales_list) -> None:
    data = sd.from_input1()
    sales_list.append(data)
    print(f"Sales for {data['sales_date']} is added.\n")

def add_sales2(sales_list) -> None:
    data = sd.from_input2()
    sales_list.append(data)
    print(f"Sales for {data['sales_date']} is added.\n")

def import_sales(sales_list) -> None:
    filename = input("Enter name of file to import: ")
    filepath_name = sd.FILEPATH / filename

    if not sd.is_valid_filename_format(filename):
        print(f"Filename '{filename}' doesn't follow the expected format of '{sd.NAMING_CONVENTION}'.")
    elif not sd.is_valid_region(sd.get_region_code(filename)):
        print(f"Filename '{filename}' doesn't include one of the following region codes: {list(sd.VALID_REGIONS.keys())}.")
    elif already_imported(filepath_name):
        filename = filename.replace("\n", "")
        print(f"File '{filename}' has already been imported.")
    else:
        try:
            imported_sales_list = sd.import_sales(filepath_name)
        except Exception as e:
            print(f"{type(e)}. Fail to import sales from '{filename}'.")
        else:
            bad_data_flag = view_sales(imported_sales_list)
            if bad_data_flag:
                print(f"File '{filename}' contains bad data.\nPlease correct the data in the file and try again.")
            elif len(imported_sales_list) > 0:
                sales_list.extend(imported_sales_list)
                print("Imported sales added to list.")
                add_imported_file(filepath_name)
            else:
                print("No valid sales data found in the file.")

def already_imported(filepath_name: Path) -> bool:
    try:
        with open(sd.FILEPATH / sd.IMPORTED_FILES) as file:
            files = [line.strip() for line in file.readlines()]
            # Ensure only filenames are in the list
            filenames_only = [Path(line).name for line in files]
            return filepath_name.name in filenames_only
    except FileNotFoundError:
        print(f"The file '{sd.IMPORTED_FILES}' does not exist.")
        return False

def add_imported_file(filepath_name: Path):
    try:
        with open(sd.FILEPATH / sd.IMPORTED_FILES, "a") as file:
            # Write only the filename to the file
            file.write(f"{filepath_name.name}\n")
    except Exception as e:
        print(f"{type(e)}. Failed to add the imported file to the record.")

def display_title():
    print("SALES DATA IMPORTER\n")

def display_menu():
    cmd_format = "6"  # ^ center, < is the default for str.
    print("COMMAND MENU",
          f"{'view':{cmd_format}} - View all sales",
          f"{'add1':{cmd_format}} - Add sales by typing sales, year, month, day, and region",
          f"{'add2':{cmd_format}} - Add sales by typing sales, date (YYYY-MM-DD), and region",
          f"{'import':{cmd_format}} - Import sales from file",
          f"{'menu':{cmd_format}} - Show menu",
          f"{'exit':{cmd_format}} - Exit program", sep='\n')

def execute_command(sales_list) -> None:
    while True:
        command = input("\nPlease enter a command: ").strip().lower()

        if command == "view":
            view_sales(sales_list)
        elif command == "add1":
            add_sales1(sales_list)
        elif command == "add2":
            add_sales2(sales_list)
        elif command == "import":
            import_sales(sales_list)
        elif command == "menu":
            display_menu()
        elif command == "exit":
            break
        else:
            print("Invalid command. Please try again.")

def main():
    display_title()
    display_menu()

    sales_list = import_all_sales()
    execute_command(sales_list)
    print("Bye!")

if __name__ == "__main__":
    main()

