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
            break
        else:
            print(f"Amount must be greater than zero.")
    amount = entry