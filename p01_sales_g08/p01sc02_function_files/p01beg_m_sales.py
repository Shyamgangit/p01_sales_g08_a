from functools import singledispatch
from pathlib import Path
import csv
import os

# Regions
VALID_REGIONS = {"w": "West", "m": "Mountain", "c": "Central", "e": "East"}
# Sales date
DATE_FORMAT = "%Y-%m-%d"
MIN_YEAR, MAX_YEAR = 2000, 2999
# files
FILEPATH = Path(__file__).parent.parent / 'p01_files'
IMPORTED_FILES = 'imported_files.txt'
ALL_SALES = 'all_sales.csv'
NAMING_CONVENTION = "sales_qn_yyyy_r.csv"


# --------------- Sales Input and Files (Data Access) ------------------------
def input_amount() -> float:
    while True:
        entry = float(input(f"{'Amount:':20}"))
        if entry > 0:
            return entry
        else:
            print(f"Amount must be greater than zero.")


def input_int(entry_item: str, high: int, low: int = 1, fmt_width: int = 20) -> int:
    prompt = f"{entry_item.capitalize()} ({low}-{high}):"
    while True:
        entry = int(input(f"{prompt:{fmt_width}}"))
        if low <= entry <= high:
            return entry
        else:
            print(f"{entry_item.capitalize()} must be between {low} and {high}.")


def input_year() -> int:
    return input_int("year", MAX_YEAR, MIN_YEAR)


def input_month() -> int:
    return input_int("month", 12, 1, 20)


def is_leap_year(year: int) -> bool:
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True
    else:
        return False


def cal_max_day(year: int, month: int) -> int:
    if is_leap_year(year) and month == 2:
        return 29
    elif month == 2:
        return 28
    elif month in (4, 6, 9, 11):
        return 30
    else:
        return 31


def input_day(year: int, month: int) -> int:
    max_day = cal_max_day(year, month)
    parameters = {"entry_item": "day", "high": max_day}
    return input_int(**parameters)


def is_valid_region(region_code: str) -> bool:
    return region_code.lower() in VALID_REGIONS


def get_region_name(region_code: str) -> str:
    return VALID_REGIONS.get(region_code.lower(), "INVALID")


def input_region_code() -> str:
    valid_codes = tuple(VALID_REGIONS.keys())
    while True:
        prompt = f"{f'Region {valid_codes}:':{20}}"
        code = input(prompt).lower()
        if code in valid_codes:
            return code
        else:
            print(f"Region must be one of the following: {valid_codes}.")


def input_date() -> str:
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
    try:
        row[0] = float(row[0])
    except ValueError:
        row[0] = "?"
    if len(row[1]) == 10 and row[1][4] == '-' and row[1][7] == '-' \
            and row[1][:4].isdigit() and row[1][5:7].isdigit() and row[1][8:10].isdigit():
        yyyy, mm, dd = int(row[1][:4]), int(row[1][5:7]), int(row[1][8:10])
        if not (1 <= mm <= 12) or not (1 <= dd <= cal_max_day(yyyy, mm)):
            row[1] = "?"
    else:
        row[1] = "?"


def has_bad_amount(data: dict) -> bool:
    return data["amount"] == "?"


def has_bad_date(data: dict) -> bool:
    return data["sales_date"] == "?"


def has_bad_data(data: dict) -> bool:
    return has_bad_amount(data) or has_bad_date(data)


@singledispatch
def import_sales(filepath_name: Path, delimiter: str = ',') -> list:
    with open(filepath_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        filename = filepath_name.name
        region_code = get_region_code(filename)

        imported_sales_list = []
        for amount_sales_date in reader:
            correct_data_types(amount_sales_date)
            amount, sales_date = amount_sales_date[0], amount_sales_date[1]
            data = {
                "amount": amount,
                "sales_date": sales_date,
                "region": get_region_name(region_code)
            }
            imported_sales_list.append(data)
        return imported_sales_list


@import_sales.register
def _(sales_list: list) -> None:
    filename = input("Enter name of file to import: ")
    filepath_name = FILEPATH / filename
    if not is_valid_filename_format(filename):
        print(f"Filename '{filename}' doesn't follow the expected format of '{NAMING_CONVENTION}.")
    elif not is_valid_region(get_region_code(filename)):
        print(f"Filename '{filename}' doesn't include one of the following region codes: {list(VALID_REGIONS.keys())}.")
    elif already_imported(filepath_name):
        filename = filename.replace("\n", "")
        print(f"File '{filename}' has already been imported.")
    else:
        imported_sales_list = import_sales(filepath_name)
        if imported_sales_list is None:
            print(f"Fail to import sales from '{filename}'.")
        else:
            bad_data_flag = view_sales(imported_sales_list)
            if bad_data_flag:
                print(f"File '{filename}' contains bad data.\nPlease correct the data in the file and try again.")
            elif len(imported_sales_list) > 0:
                sales_list.extend(imported_sales_list)
                print("Imported sales added to list.\n")
                add_imported_file(filepath_name)


def import_all_sales() -> list:
    sales_data = []
    with open(FILEPATH / ALL_SALES, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if len(row) < 3:
                print(f"Skipping incomplete row: {row}")
                continue

            amount, sales_date, region_code = row
            data = {
                "amount": float(amount.strip()),
                "sales_date": sales_date.strip(),
                "region": get_region_name(region_code.strip())
            }
            sales_data.append(data)
    return sales_data


def view_sales(sales_list: list) -> bool:
    col1_w, col2_w, col3_w, col4_w, col5_w = 5, 15, 15, 15, 15
    bad_data_flag = False
    if len(sales_list) == 0:
        print("No sales to view.\n")
        return bad_data_flag

    total_w = col1_w + col2_w + col3_w + col4_w + col5_w
    print(f"{'':{col1_w}}{'Date':{col2_w}}{'Quarter':{col3_w}}{'Region':{col4_w}}{'Amount':>{col5_w}}")
    print(horizontal_line := f"{'-' * total_w}")
    total = 0.0

    for idx, sales in enumerate(sales_list, start=1):
        if has_bad_data(sales):
            bad_data_flag = True
            num = f"{idx}.*"
        else:
            num = f"{idx}."

        if isinstance(sales['amount'], float):
            amount = sales['amount']
            total += amount
        else:
            amount = sales['amount']

        sales_date = sales['sales_date']
        if has_bad_date(sales):
            bad_data_flag = True
            month = 0
        else:
            month = int(sales_date.split('-')[1])

        region = sales['region']
        quarter = f"{cal_quarter(month)}"
        print(f"{num:<{col1_w}}{sales_date:{col2_w}}{quarter:<{col3_w}}{region:{col4_w}}{amount:>{col5_w}}")

    print(horizontal_line)
    print(f"{'TOTAL':{col1_w}}{' ':{col2_w + col3_w + col4_w}}{total:>{col5_w}}\n")
    return bad_data_flag


def add_sales1(sales_list) -> None:
    amount = input_amount()
    year = input_year()
    month = input_month()
    day = input_day(year, month)
    region_code = input_region_code()

    sales_data = {
        "amount": amount,
        "sales_date": f"{year}-{month:02d}-{day:02d}",
        "region": VALID_REGIONS[region_code],
    }
    sales_list.append(sales_data)
    print(f"Sales for {sales_data['sales_date']} is added.")


def add_sales2(sales_list) -> None:
    amount = input_amount()
    sales_date = input_date()
    region_code = input_region_code()

    sales_data = {
        "amount": amount,
        "sales_date": sales_date,
        "region": VALID_REGIONS[region_code],
    }
    sales_list.append(sales_data)
    print(f"Sales for {sales_data['sales_date']} is added.")


def is_valid_filename_format(filename: str) -> bool:
    return (len(filename) == len(NAMING_CONVENTION) and
            filename[:7] == NAMING_CONVENTION[:7] and
            filename[8] == NAMING_CONVENTION[8] and
            filename[13] == NAMING_CONVENTION[-6] and
            filename[-4:] == NAMING_CONVENTION[-4:])


def get_region_code(sales_filename: str) -> str:
    if is_valid_filename_format(sales_filename):
        return sales_filename[-5].lower()
    return "INVALID"


def already_imported(filepath_name: Path) -> bool:
    try:
        with open(IMPORTED_FILES, 'r') as file:
            imported_files = file.read().splitlines()
        return filepath_name.name in imported_files
    except FileNotFoundError:
        return False


def add_imported_file(filepath_name: Path):
    with open(IMPORTED_FILES, 'a') as file:
        file.write(f"{filepath_name.name}\n")


def save_all_sales(sales_list, delimiter: str = ',') -> None:
    converted_sales_list = [[sale["amount"], sale["sales_date"], sale["region"]] for sale in sales_list]

    with open(ALL_SALES, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter)
        writer.writerows(converted_sales_list)

    print(f"All sales data has been saved to '{ALL_SALES}'.")


def main():
    sales_list = import_all_sales()
    view_sales(sales_list)

    add_sales1(sales_list)
    add_sales2(sales_list)
    view_sales(sales_list)

    print("\nPlease enter file name 'region1'")
    import_sales(sales_list)
    print("\nPlease enter file name 'sales_q1_2021_x.csv'")
    import_sales(sales_list)
    print("\nPlease enter file name 'sales_q2_2021_w.csv'")
    import_sales(sales_list)
    print("\nPlease enter file name 'sales_q3_2021_w.csv'")
    import_sales(sales_list)
    view_sales(sales_list)

    print("\nPlease enter file name 'sales_q4_2021_w.csv'")
    import_sales(sales_list)
    print("\nPlease enter file name 'sales_q4_2021_w.csv' again")
    import_sales(sales_list)
    save_all_sales(sales_list)

    print("\nPlease enter file name 'sales_q1_2021_w.csv'")
    import_sales(sales_list)


if __name__ == '__main__':
    main()
