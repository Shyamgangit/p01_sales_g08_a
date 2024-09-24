
# Regions
VALID_REGIONS = {"w": "West", "m": "Mountain", "c": "Central", "e": "East"}
# Sales date
MIN_YEAR, MAX_YEAR = 2000, 2_999
# file
NAMING_CONVENTION = "sales_qn_yyyy_r.csv"


# --------------- Sales Input and Files (Data Access) ------------------------

sales_list = []  # for storing sales data user entered.

# input amount
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
        break
    else:
        print(f"Amount must be greater than zero.")
amount = entry


# input year
"""
Get a valid int number from the user.
If the user enter an invalid number, display
a warning message to the user on the console,
and let the user enter a new number.
"""
entry_item, high, low, fmt_width = 'year', MAX_YEAR, MIN_YEAR, 20
prompt = f"{entry_item.capitalize()} ({low}-{high}):"
while True:
    entry = int(input(f"{prompt:{fmt_width}}"))
    if low <= entry <= high:
        break
    else:
        print(f"{entry_item.capitalize()} must be between {low} and {high}.")
year = entry


# input month
"""
Get a valid int number from the user.
If the user enter an invalid number, display
a warning message to the user on the console,
and let the user enter a new number.
"""
entry_item, high, low, fmt_width = 'month', 12, 1, 20
prompt = f"{entry_item.capitalize()} ({low}-{high}):"
while True:
    entry = int(input(f"{prompt:{fmt_width}}"))
    if low <= entry <= high:
        break
    else:
        print(f"{entry_item.capitalize()} must be between {low} and {high}.")
month = entry

# check if the year is a leap year
is_leap_year = False
if year % 400 == 0:  # divisible by 400 --> leap year
    is_leap_year = True
elif year % 100 == 0:  # not divisible by 400, but by 100 --> not leap year
    is_leap_year = False
elif year % 4 == 0:  # not divisible by 100, but by 4,  --> leap year
    is_leap_year = True
else:
    is_leap_year = False

# calculate the max day of a month
cal_max_day = 0
if is_leap_year and month == 2:
    cal_max_day = 29
elif month == 2:
    cal_max_day = 28
elif month in (4, 6, 9, 11):
    cal_max_day = 30
else:
    cal_max_day = 31


# input day
"""
Get a valid int number from the user.
If the user enter an invalid number, display
a warning message to the user on the console,
and let the user enter a new number.
"""
entry_item, high, low, fmt_width = 'day', cal_max_day, 1, 20
prompt = f"{entry_item.capitalize()} ({low}-{high}):"
while True:
    entry = int(input(f"{prompt:{fmt_width}}"))
    if low <= entry <= high:
        break
    else:
        print(f"{entry_item.capitalize()} must be between {low} and {high}.")
day = entry


# Form the sales date in 'yyyy-mm-dd' format based on given year, month, and day
sales_date = f"{year}-{month:02}-{day:02}"


# input region code
"""
Gets a valid region code from the user.
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
        break
    else:
        print(f"Region must be one of the following: {valid_codes}.")
region_code = code


# from input 1
"""
Create a dictionary using the amount, sales date and region code.
Append the dictionary into the sales list
"""
from_input1 = {"amount": amount,
               "sales_date": sales_date,
               "region": region_code,
               }
sales_list.append(from_input1)


# input date
"""
Gets a date in yyyy-mm-dd format with a year between 2000 and 2999
from the user.
If the user enter an invalid date, display
a warning message to the user on the console,
and let the user enter a new date.
"""
sales_date = ''
while True:
    entry = input(f"{'Date (yyyy-mm-dd):':20}").strip()
    if len(entry) == 10 and entry[4] == '-' and entry[7] == '-' \
            and entry[:4].isdigit() and entry[5:7].isdigit() \
            and entry[8:].isdigit():
        yyyy, mm, dd = int(entry[:4]), int(entry[5:7]), int(entry[8:])
        is_leap_year = False
        if yyyy % 400 == 0:  # divisible by 400 --> leap year
            is_leap_year = True
        elif yyyy % 100 == 0:  # not divisible by 400, but by 100 --> not leap year
            is_leap_year = False
        elif yyyy % 4 == 0:  # not divisible by 100, but by 4,  --> leap year
            is_leap_year = True
        else:
            is_leap_year = False
        cal_max_day = 0
        if is_leap_year and mm == 2:
            cal_max_day = 29
        elif mm == 2:
            cal_max_day = 28
        elif mm in (4, 6, 9, 11):
            cal_max_day = 30
        else:
            cal_max_day = 31
        if (1 <= mm <= 12) and (1 <= dd <= cal_max_day):
            if MIN_YEAR <= yyyy <= MAX_YEAR:
                sales_date = f"{yyyy}-{str(mm).zfill(2)}-{dd:02}"
                break
            else:
                print(f"Year of the date must be between {MIN_YEAR} and {MAX_YEAR}.")
        else:
            print(f"{entry} is not in a valid date format.")
    else:
        print(f"{entry} is not in a valid date format.")


# from input 2
"""
Create a dictionary using the amount, sales date and region code.
Append the dictionary into the sales list
"""
from_input2 = {"amount": amount,
               "sales_date": sales_date,
               "region": region_code,
               }
sales_list.append(from_input2)


# input file name
"""
Gets a file name from the user.
If the user enter a file name in an invalid format or 
the file name does not contain a valid region code, display
a warning message to the user on the console,
and let the user enter a new date.
"""
while True:
    # get filename from user
    filename = input("Enter name of file to import: ")

    is_valid_filename_format = False
    is_valid_region = False

    # check if filename is valid
    if len(filename) == len(NAMING_CONVENTION) and \
            filename[:7] == NAMING_CONVENTION[:7] and \
            filename[8] == NAMING_CONVENTION[8] and \
            filename[13] == NAMING_CONVENTION[-6] and \
            filename[-4:] == NAMING_CONVENTION[-4:]:
        is_valid_filename_format = True
        # check if region code (the 5th character from end) is valid.
        region_code = filename[filename.rfind('.') - 1]
        is_valid_region = tuple(VALID_REGIONS.keys()).count(region_code) == 1
    else:
        print(f"Filename '{filename}' doesn't follow the expected",
              f"format of '{NAMING_CONVENTION}.")
        continue

    if not is_valid_region:
        print(f"Filename '{filename}' doesn't include one of",
              f"the following region codes: {list(VALID_REGIONS.keys())}.")
    else:
        break


# from file
from_file = {"filename": filename,
             "region": region_code,
             }


# Display collected information in the sales_list
col1_w, col2_w, col3_w, col4_w, col5_w = 5, 15, 15, 15, 15  # column width
total_w = col1_w + col2_w + col3_w + col4_w + col5_w
print(f"{' ':{col1_w}}"
      f"{'Date':{col2_w}}"
      f"{'Quarter':{col3_w}}"
      f"{'Region':{col4_w}}"
      f"{'Amount':>{col5_w}}")
print(horizontal_line := f"{'-' * total_w}")

total = 0.0
for idx, sales in enumerate(sales_list, start=1):
    num = f"{idx}."

    amount = sales["amount"]
    total += amount

    sales_date = sales["sales_date"]
    month = int(sales_date.split("-")[1])

    region_code = sales["region"]
    region = VALID_REGIONS[region_code]

    # calculate quarter
    cal_quarter = 0
    if month in (1, 2, 3):
        cal_quarter = 1
    elif month in (4, 5, 6):
        cal_quarter = 2
    elif month in (7, 8, 9):
        cal_quarter = 3
    elif month in (10, 11, 12):
        cal_quarter = 4
    else:
        cal_quarter = 0
    quarter = f"{cal_quarter}"

    print(f"{num:<{col1_w}}"
          f"{sales_date:{col2_w}}"
          f"{quarter:<{col3_w}}"
          f"{region:{col4_w}}"
          f"{amount:>{col5_w}}")

print(horizontal_line)
print(f"{'TOTAL':{col1_w}}"
      f"{' ':{col2_w + col3_w + col4_w}}"
      f"{total:>{col5_w}}\n")

print(from_file)

