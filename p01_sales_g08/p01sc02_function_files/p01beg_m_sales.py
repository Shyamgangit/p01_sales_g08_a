from functools import singledispatch
from pathlib import Path  # pathlib is preferred to os.path.join
import csv

# Regions
VALID_REGIONS = {"w": "West", "m": "Mountain", "c": "Central", "e": "East"}
# Sales date
DATE_FORMAT = "%Y-%m-%d"
MIN_YEAR, MAX_YEAR = 2000, 2_999
# files
FILEPATH = Path(__file__).parent.parent / 'p01_files'
IMPORTED_FILES = 'imported_files.txt'
ALL_SALES = 'all_sales.csv'
NAMING_CONVENTION = "sales_qn_yyyy_r.csv"


# --------------- Sales Input and Files (Data Access) ------------------------
def input_amount() -> float:
    """
    Gets a sales amount greater than zero from the user,
    converts it to a float value, and returns the float
    value.
    If the user enter an invalid number, display
    a warning message to the user on the console,
    and let the user enter a new number.
    """
    while True:
        entry = float(input(f"{'Amount:':20}"))
        if entry > 0:
            return entry
        else:
            print(f"Amount must be greater than zero.")


def input_int(entry_item: str, high: int, low: int = 1, fmt_width: int = 20) -> int:
    """
    Get a valid int number from the user and return it.
    If the user enter an invalid number, display
    a warning message to the user on the console,
    and let the user enter a new number.
    """
    prompt = f"{entry_item.capitalize()} ({low}-{high}):"
    while True:
        entry = int(input(f"{prompt:{fmt_width}}"))
        if low <= entry <= high:
            return entry
        else:
            print(f"{entry_item.capitalize()} must be between {low} and {high}.")


def input_year() -> int:
    """
    Gets a year between 2000 and 2999 from the user,
    converts it to an int value, and returns the int value.
    """
    # use input_int() with positional arguments and default argument values if possible
    ...


def input_month() -> int:
    """
    Gets a month between 1 and 12 from the user, converts
    it to an int value, and returns the int value.
    """
    # call input_int() with positional entry_item and high, default value of low,
    # and passing 20 for argument fmt_width
    ...


def is_leap_year(year: int) -> bool:
    if year % 400 == 0:  # divisible by 400 --> leap year
        return True
    elif year % 100 == 0:  # not divisible by 400, but by 100 --> not leap year
        return False
    elif year % 4 == 0:  # not divisible by 100, but by 4,  --> leap year
        return True
    else:
        return False


def cal_max_day(year: int, month: int) -> int:
    if is_leap_year(year) and month == 2:  # short-circuit
        return 29
    elif month == 2:
        return 28
    elif month in (4, 6, 9, 11):
        return 30
    else:
        return 31


def input_day(year: int, month: int) -> int:
    """
    Gets a day from the user, converts it to an int
    value, and returns the int value.
    Based on month parameter, day must be between 1 and 28, 30, or 31.
    month 1, 3, 5, 7, 8, 10, 12: 1-31
    month 2: 1-28 (not leap year), 1-29 (leap year)
    month 4, 5, 9, 11: 1-30
    """
    max_day = cal_max_day(year, month)
    parameters = {"entry_item": "day", "high": max_day}
    # call input_int() using dictionary as keyword arguments
    ...


def is_valid_region(region_code: str) -> bool:
    """
    Return True if the region_code is one of the keys of the VALID_REGIONS.
    Otherwise False
    """
    # Complete the task in one return statement
    ...


def get_region_name(region_code: str) -> str:
    """
    Return the corresponding region name for a given region_code
    """
    # Complete the task in one return statement
    ...


def input_region_code() -> str:
    """
    Gets and returns a valid region code from the user.
    If the user enter an invalid region code, display
    a warning message to the user on the console,
    and let the user enter a new region code.
    """
    while True:
        fmt = 20
        valid_codes = tuple(VALID_REGIONS.keys())
        prompt = f"{f'Region {valid_codes}:':{fmt}}"
        code = input(prompt)
        if valid_codes.count(code) == 1:
            return code
        else:
            print(f"Region must be one of the following: {valid_codes}.")


def input_date() -> str:
    """
    Gets a date in yyyy-mm-dd format with a year between 2000 and 2999
    from the user and returns a date.
    If the user enter an invalid date, display
    a warning message to the user on the console,
    and let the user enter a new date.
    """
    while True:
        entry = input(f"{'Date (yyyy-mm-dd):':20}").strip()
        if len(entry) == 10 and entry[4] == '-' and entry[7] == '-' \
                and entry[:4].isdigit() and entry[5:7].isdigit() \
                and entry[8:].isdigit():
            yyyy, mm, dd = int(entry[:4]), int(entry[5:7]), int(entry[8:])
            if (1 <= mm <= 12) and (1 <= dd <= cal_max_day(yyyy, mm)):
                if MIN_YEAR <= yyyy <= MAX_YEAR:
                    return entry
                else:
                    print(f"Year of the date must be between {MIN_YEAR} and {MAX_YEAR}.")
            else:
                print(f"{entry} is not in a valid date format.")
        else:
            print(f"{entry} is not in a valid date format.")


def cal_quarter(month: int) -> int:
    if month in (1, 2, 3):
        quarter = 1
    elif month in (4, 5, 6):
        quarter = 2
    elif month in (7, 8, 9):
        quarter = 3
    elif month in (10, 11, 12):
        quarter = 4
    else:
        quarter = 0
    return quarter


def correct_data_types(row):
    """
    Try to convert valid amount to float type
    and mark invalid amount or sales date as '?'
    """
    try:  # amount
        row[0] = float(row[0])  # convert to float
    except ValueError:
        row[0] = "?"  # Mark invalid amount as bad
    # date
    if len(row[1]) == 10 and row[1][4] == '-' and row[1][7] == '-' \
            and row[1][:4].isdigit() and row[1][5:7].isdigit() and row[1][8:10].isdigit():
        yyyy, mm, dd = int(row[1][:4]), int(row[1][5:7]), int(row[1][8:10])
        if not (1 <= mm <= 12) or not (1 <= dd <= cal_max_day(yyyy, mm)):
            row[1] = "?"  # Mark invalid date as bad
    else:
        row[1] = "?"  # Mark invalid date as bad


def has_bad_amount(data: dict) -> bool:
    return data["amount"] == "?"  # or data["amount"] < 0


def has_bad_date(data: dict) -> bool:
    return data["sales_date"] == "?"  # or not isinstance(self.sales_date, date)


def has_bad_data(data: dict) -> bool:
    return has_bad_amount(data) or has_bad_date(data)


def from_input1():
    amount = input_amount()
    year = input_year()
    month = input_month()
    day = input_day(year, month)
    sales_date = f"{year}-{str(month).zfill(2)}-{day:02}"
    region_code = input_region_code()
    return {"amount": amount,
            "sales_date": sales_date,
            "region": region_code,
            }


def from_input2():
    amount = input_amount()
    sales_date = input_date()
    region_code = input_region_code()
    return {"amount": amount,
            "sales_date": sales_date,
            "region": region_code,
            }


def is_valid_filename_format(filename):
    """
    Return True if the filename is in the valid filename format.
    Otherwise, False.
    """
    ...


def get_region_code(sales_filename: str) -> str:
    """
    Get the region code from a given filename.
    If the filename following the name convention, the region code
    is the character rigth before the extension name.
    """
    # write one return statement to complete the task.
    ...


def already_imported(filepath_name: Path) -> bool:
    """
    Return True if the filename is in the IMPORTED_FILES.
    Otherwise, False.
    """
    ...


def add_imported_file(filepath_name: Path):
    """Add the filepath_name into IMPORTED_FILES"""
    ...


'''
In Python, you cannot directly define two functions with the same name, 
as the second function definition will overwrite the first one. 
Python provides a way to perform function overloading based on argument types 
using functools.singledispatch. 
This allows you to define multiple versions of a function, 
each handling different types of arguments.
from functools import singledispatch
@singledispatch  # for whichever defined first in the file
def import_sales(filename: str) -> list:
    pass
@import_sales.register  # for whichever defined later
def _(sales_list: list) -> None:
    pass
'''
@singledispatch
def import_sales(filepath_name: Path, delimiter: str = ',') -> list:
    with open(filepath_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        filename = filepath_name.name
        region_code = filename[filename.rfind('.') - 1]
        imported_sales_list = []
        for amount_sales_date in reader:
            correct_data_types(amount_sales_date)
            amount, sales_date = amount_sales_date[0], amount_sales_date[1]
            data = {"amount": amount,
                    "sales_date": sales_date,
                    "region": region_code,
                    }
            imported_sales_list.append(data)
        return imported_sales_list  # within with statement


# --------------- Sales Manager (Business Logic)---------------------

def import_all_sales() -> list:
    """
    Read each row of sales data from the file ALL_SALES into a dictionary
    data = {"amount": amount,
            "sales_date": sales_date,
            "region": region_code}
    Return a list of dictionaries.
    """
    ...


def view_sales(sales_list: list) -> bool:
    """
    Display "No sles to view" if there is no sales data in the sales_list.
    Otherwise, calculate the total amount and display sales data and the
    total amount on the console.
    """
    col1_w, col2_w, col3_w, col4_w, col5_w = 5, 15, 15, 15, 15  # column width
    bad_data_flag = False
    if len(sales_list) == 0:  # sales_list could be [] or None
        print("No sales to view.\n")
    else: # not empty
        total_w = col1_w + col2_w + col3_w + col4_w + col5_w
        print(f"{' ':{col1_w}}"
              f"{'Date':{col2_w}}"
              f"{'Quarter':{col3_w}}"
              f"{'Region':{col4_w}}"
              f"{'Amount':>{col5_w}}")
        print(horizontal_line := f"{'-' * total_w}")
        total = 0.0

        for idx, sales in enumerate(sales_list, start=1):
            if has_bad_data(sales):
                bad_data_flag = True
                num = f"{idx}.*"   # add period and asterisk
            else:
                num = f"{idx}."    # add period only

            amount = sales["amount"]
            if not has_bad_amount(sales):
                total += amount

            sales_date = sales["sales_date"]
            if has_bad_date(sales):
                bad_data_flag = True
                month = 0
            else:
                month = int(sales_date.split("-")[1])

            region = get_region_name(sales["region"])
            quarter = f"{cal_quarter(month)}"
            print(f"{num:<{col1_w}}"
                  f"{sales_date:{col2_w}}"
                  f"{quarter:<{col3_w}}"
                  f"{region:{col4_w}}"
                  f"{amount:>{col5_w}}")

        print(horizontal_line)
        print(f"{'TOTAL':{col1_w}}"
              f"{' ':{col2_w + col3_w + col4_w}}"
              f"{total:>{col5_w}}\n")
    return bad_data_flag


def add_sales1(sales_list) -> None:
    """
     Get the sales data from_input1() which
     asks user to enter sales amount and date by calling following functions
       - input_amount(), input_year(), input_month(), input_day()
     Add sales data to the sales_list
     Notify the user by displaying a message on the console_
    """
    ...


def add_sales2(sales_list) -> None:
    """
     Get the sales data from_input2() which
     asks user to enter sales amount and date by calling following functions
       - input_amount(), input_date()
     Add sales data to the sales_list
     Notify the user by displaying a message on the console_
    """
    ...


@import_sales.register
def _(sales_list: list)-> None: # def import_sales(sales_list: list) -> None:
    # get filename from user
    filename = input("Enter name of file to import: ")
    filepath_name = FILEPATH / filename
    # check if filename is valid
    if not is_valid_filename_format(filename):
        print(f"Filename '{filename}' doesn't follow the expected",
              f"format of '{NAMING_CONVENTION}.")
    # check if region code (the 5th character from end) is valid.
    elif not is_valid_region(get_region_code(filename)):
        print(f"Filename '{filename}' doesn't include one of",
              f"the following region codes: {list(VALID_REGIONS.keys())}.")
    # check if file has already been imported
    elif already_imported(filepath_name):
        filename = filename.replace("\n", "") # remove new line character
        print(f"File '{filename}' has already been imported.")
    else:
        # import sales data from file to a list
        imported_sales_list = import_sales(filepath_name)
        # check if import succeeded (including []). imported_sales_list could be None or []
        if imported_sales_list is None:  # only handle imported_sales_list is None here.
            print(f"Fail to import sales from '{filename}'.")
        else:
            # display imported sales, and also return if there is bad data.
            bad_data_flag = view_sales(imported_sales_list)
            if bad_data_flag:
                print(f"File '{filename}' contains bad data.\n"
                      "Please correct the data in the file and try again.")
            elif len(imported_sales_list) > 0:  # handle imported_sales_list is not [] here.
                    sales_list.extend(imported_sales_list)
                    print("Imported sales added to list.\n")
                    add_imported_file(filepath_name)


def save_all_sales(sales_list, delimiter: str=',') -> None:
    """
    Convert each sales data dictionary in the sales_list into a list
    Save the converted sales list which now is a list of lists into the file ALL_SALES.
    """
    # convert the list of dictionaries to a list of lists, using comprehension

    # Save the converted sales list which now is a list of lists into the file ALL_SALES.
    ...




# ----------------TESTING--------------------------------------------
def main():
    sales_list = import_all_sales()
    view_sales(sales_list)

    add_sales1(sales_list)
    add_sales2(sales_list)
    view_sales(sales_list)

    print("\nPlease enter file name 'region1'")
    import_sales(sales_list)  # region1
    print("\nPlease enter file name 'sales_q1_2021_x.csv'")
    import_sales(sales_list)  # sales_q1_2021_x.csv
    print("\nPlease enter file name 'sales_q2_2021_w.csv'")
    import_sales(sales_list)  # sales_q2_2021_w.csv
    print("\nPlease enter file name 'sales_q3_2021_w.csv'")
    import_sales(sales_list)  # sales_q3_2021_w.csv
    view_sales(sales_list)

    print("\nPlease enter file name 'sales_q4_2021_w.csv'")
    import_sales(sales_list)  # sales_q4_2021_w.csv, including add_imported_file()
    print("\nPlease enter file name 'sales_q4_2021_w.csv' again")
    import_sales(sales_list)
    save_all_sales(sales_list)

    print("\nPlease enter file name 'sales_q1_2021_w.csv'")
    import_sales(sales_list)  # sales_q1_2021_w.csv, FileNotFound


if __name__ == '__main__':
    main()
