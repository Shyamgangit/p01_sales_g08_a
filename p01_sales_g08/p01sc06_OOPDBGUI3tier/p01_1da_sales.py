

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from pathlib import Path
import csv

@dataclass
class Region:
    code: str = ""
    name: str = ""


class Regions:

    def __init__(self):
        self._VALID_REGIONS = [Region("w", "West"), Region("m", "Mountain"),
                               Region("c", "Central"), Region("e", "East")]

    def __iter__(self):
        return iter(self._VALID_REGIONS)

    def get(self, code: str) -> Optional[Region]:
        for region_obj in self._VALID_REGIONS:
            if code == region_obj.code:
                return region_obj
        return None  # Explicitly return None if the region is not found

    def set_VALID_REGION(self, regions_list: list):
        self._VALID_REGIONS = regions_list

    def add_region(self, region: Region):
        self._VALID_REGIONS.append(region)

class Sales:
    DATE_FORMAT = "%Y-%m-%d"  # Class constants
    MIN_YEAR, MAX_YEAR = 2000, 2999

    def __init__(self, id: int, amount: float = 0.0, sales_date: date = None, region: Region = None):
        self._salesdata = {"ID": id, "amount": amount, "salesDate": sales_date, "region": region}

    def __str__(self):
        return (f"Sales(ID={self._salesdata['ID']}, amount={self._salesdata['amount']}, "
                f"date={self._salesdata['salesDate']}, region={self._salesdata['region']})")

    def __setitem__(self, key, value):
        self._salesdata[key] = value

    @property
    def id(self):
        return self._salesdata["ID"]

    @id.setter
    def id(self, value):
        self._salesdata["ID"] = value

    @property
    def amount(self):
        return self._salesdata["amount"]

    @amount.setter
    def amount(self, value):
        self._salesdata["amount"] = value  # Allow updating the amount

    @property
    def sales_date(self):
        return self._salesdata["salesDate"]

    @sales_date.setter
    def sales_date(self, value):
        self._salesdata["salesDate"] = value

    @property
    def region(self):
        return self._salesdata["region"]

    @region.setter
    def region(self, value):
        self._salesdata["region"] = value


    @property
    def has_bad_amount(self) -> bool:
        return self._salesdata["amount"] == "?" # or self.amount <= 0

    @property
    def has_bad_date(self) -> bool:
        return self._salesdata["salesDate"] == "?" # or not isinstance(self.sales_date, date)

    @property
    def has_bad_data(self) -> bool:
        return self.has_bad_amount or self.has_bad_date

    @staticmethod
    def correct_data_types(row):
        try:  # amount
            row[0] = float(row[0]) # convert to float
        except ValueError:
            row[0] = "?"    # Mark invalid amount as bad
        try:  # date
            sales_date = datetime.strptime(row[1], Sales.DATE_FORMAT)
            row[1] = sales_date.date()  # convert to date
        except ValueError:
            row[1] = "?"    # Mark invalid date as bad

    @staticmethod
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

    @staticmethod
    def is_leap_year(year: int) -> bool:
        if year % 400 == 0:  # divisible by 400 --> leap year
            return True
        elif year % 100 == 0:  # not divisible by 400, but by 100 --> not leap year
            return False
        elif year % 4 == 0:  # not divisible by 100, but by 4,  --> leap year
            return True
        else:
            return False

    @staticmethod
    def cal_max_day(year: int, month: int) -> int:
        if Sales.is_leap_year(year) and month == 2:  # short-circuit
            return 29
        elif month == 2:
            return 28
        elif month in (4, 6, 9, 11):
            return 30
        else:
            return 31


# ------------------------------------------------------

class SalesList:
    def __init__(self):
        self._sales_list = []  # Use a single underscore for protected attributes

    def __iter__(self):
        return iter(self._sales_list)

    @property
    def count(self):
        # Return the number of items in the sales list
        return len(self._sales_list)

    def __getitem__(self, index) -> Sales:     # to use []
        return self._sales_list[index]

    def add(self, sales_obj):
        # Add a sales object to the list
        self._sales_list.append(sales_obj)

    def concat(self, other_list):
        # Concatenate another SalesList into this one by iterating over it
        for sales in other_list:
            self.add(sales)


# -------------- Data Access (File) --------------------------

class DataFileAccess:
    FILEPATH = Path(__file__).parent.parent / 'p01_files'
    SALES_ID = {"Sales": 1}

    def __init__(self, filename: str=""):
        self._ALL_SALES = filename if filename else 'all_sales.csv'
        self._all_sale_filepath_name = DataFileAccess.FILEPATH / self._ALL_SALES
        self._all_sales_list = self.__import_all_sales()

    def __import_all_sales(self) -> SalesList:
        try:
            with open(self._all_sale_filepath_name, newline='') as csvfile:
                reader = csv.reader(csvfile)
                all_sales_list = SalesList()
                for line in reader:
                    if len(line) > 0:
                        *amount_sales_date, region_code = line
                        Sales.correct_data_types(amount_sales_date)
                        amount, sales_date = amount_sales_date[0], amount_sales_date[1]
                        kwarg = {"id": DataFileAccess.SALES_ID["Sales"],
                            "amount": amount,
                            "sales_date": sales_date,
                            "region": Regions().get(region_code),
                        }
                        sales = Sales(**kwarg)
                        all_sales_list.add(sales)
                        DataFileAccess.SALES_ID["Sales"] += 1
                return all_sales_list
        except FileNotFoundError:
            print("Sales file not found.")
            return SalesList()  # Return an empty list if file not found

    def add_sales(self, sales_obj):
        sales_obj["ID"] = DataFileAccess.SALES_ID["Sales"]
        self._all_sales_list.add(sales_obj)
        DataFileAccess.SALES_ID["Sales"] += 1

    def concat_saleslist(self, other_list):
        for sales in other_list:
            sales["ID"] = DataFileAccess.SALES_ID["Sales"]
            DataFileAccess.SALES_ID["Sales"] += 1
        self._all_sales_list.concat(other_list)


    def save_all_sales(self, delimiter: str = ',') -> None:
        sales_records = [[sales.amount, f"{sales.sales_date:{Sales.DATE_FORMAT}}", sales.region.code]
                         for sales in self._all_sales_list] # do not include sales.id in csv file.
        try:
            with open(self._all_sale_filepath_name, 'w', newline='') as csvfile:
                writer.writerows(sales_records)
                print("Saved sales records.")
        except Exception as e:
            print(type(e), "Sales data could not be saved.")


class SalesFile:
    NAMING_CONVENTION = "sales_qn_yyyy_r.csv"

    def __init__(self, filename: str=""):
        self._sales_filename: str = filename
        self._sales_filepath_name = DataFileAccess.FILEPATH / self._sales_filename

    @property
    def is_valid_filename_format(self) -> bool:
        if len(self._sales_filename) == len(SalesFile.NAMING_CONVENTION) and \
           self._sales_filename[:7] == SalesFile.NAMING_CONVENTION[:7] and \
           self._sales_filename[8] == SalesFile.NAMING_CONVENTION[8] and \
           self._sales_filename[13] == SalesFile.NAMING_CONVENTION[-6] and \
           self._sales_filename[-4:] == SalesFile.NAMING_CONVENTION[-4:]:
            return True
        return False

    def get_region_code(self) -> str:
        return self._sales_filename[self._sales_filename.rfind('.') - 1]

    def import_sales(self, delimiter: str=',') -> SalesList:   #Optional[SalesList]:
        with open(self._sales_filepath_name, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            region_code = self.get_region_code()
            imported_sales_list = SalesList()
            for amount_sales_date in reader:
                Sales.correct_data_types(amount_sales_date)
                amount, sales_date = amount_sales_date[0], amount_sales_date[1]
                kwarg = {"id": 0,   # temporary id, will be updated later
                        "amount": amount,
                        "sales_date": sales_date,
                        "region": Regions().get(region_code),
                        }
                sales = Sales(**kwarg)
                imported_sales_list.add(sales)
            return imported_sales_list  # within with statement


class ImportedFile:
    def __init__(self, filename: str=""):
        self._IMPORTED_FILES = filename if filename else 'imported_files.txt'
        self._imported_filepath_name = DataFileAccess.FILEPATH / self._IMPORTED_FILES

    def already_imported(self, filepath_name: Path) -> bool:
        try:
            with open(DataFileAccess.FILEPATH / self._IMPORTED_FILES) as file:
                files = [line.strip() for line in file.readlines()]  # Strip newlines
                return str(filepath_name) in files
        except FileNotFoundError:
            return False  # Returning False if file doesn't exist

    def add_imported_file(self, filepath_name: Path) -> None:
        try:
            with open(DataFileAccess.FILEPATH / self._IMPORTED_FILES, "a") as file:
                file.write(f"{filepath_name}\n")   # add newlines
        except Exception as e:
            print(f"{type(e)} - The imported file could not be documented.")


# ---------------- Data Access (Input) ---------------------------
class InputAccess:
    @staticmethod
    def from_input1() -> dict:
        amount = InputAccess.input_amount()
        year = InputAccess.input_year()
        month = InputAccess.input_month()
        day = InputAccess.input_day(year, month)
        sales_date = date(year, month, day)
        region = Regions().get(InputAccess.input_region_code())
        kwarg = {"id": 0,   # temporary id will be updated
                "amount": amount,
                "sales_date": sales_date,
                "region": region,}
        return kwarg


    @staticmethod
    def from_input2() -> dict:
        amount = InputAccess.input_amount()
        sales_date = InputAccess.input_date()
        region = Regions().get(InputAccess.input_region_code())
        kwarg = {"id": 0,   # temporary id will be updated
                "amount": amount,
                "sales_date": sales_date,
                "region": region,}
        return kwarg

    @staticmethod
    def input_amount() -> float:
        while True:
            try:
                entry = float(input(f"{'Amount:':20}"))
                if entry > 0:
                    return entry
                else:
                    print(f"Amount must be greater than zero.")
            except ValueError:
                print("Invalid amount value.")

    @staticmethod
    def input_int(entry_item: str, high: int, low: int = 1, fmt_width: int = 20) -> int:
        prompt = f"{entry_item.capitalize()} ({low}-{high}):"
        while True:
            try:
                entry = int(input(f"{prompt:{fmt_width}}"))
            except ValueError:
                print(f"Invalid {entry_item} value.")
                continue
            if low <= entry <= high:
                return entry
            else:
                print(f"{entry_item.capitalize()} must be between {low} and {high}.")

    @staticmethod
    def input_year() -> int:
       return InputAccess.input_int('year', Sales.MAX_YEAR, Sales.MIN_YEAR)

    @staticmethod
    def input_month() -> int:
        return InputAccess.input_int("month", 12, fmt_width=20)

    @staticmethod
    def input_day(year: int, month: int) -> int:
        max_day = Sales.cal_max_day(year, month)
        parameters = {"entry_item": "day", "high": max_day}
        return InputAccess.input_int(**parameters)

    @staticmethod
    def input_region_code() -> str:
        while True:
            fmt = 20
            valid_codes = tuple([region.code for region in Regions()])
            prompt = f"{f'Region {valid_codes}:':{fmt}}"
            code = input(prompt)
            if valid_codes.count(code) == 1:
                return code
            else:
                print(f"Region must be one of the following: {valid_codes}.")

    @staticmethod
    def input_date() -> Optional[date]:
        while True:
            entry = input(f"{'Date (yyyy-mm-dd):':20}")
            try:
                sales_date = datetime.strptime(entry, Sales.DATE_FORMAT)  # ValueError
            except ValueError:
                print(f"{entry} is not in a valid date format.")
            else:
                if Sales.MIN_YEAR <= sales_date.year <= Sales.MAX_YEAR:
                    return sales_date.date()
                else:
                    print(f"Year of the date must be between {Sales.MIN_YEAR} and {Sales.MAX_YEAR}.")




def main():
    all_sales_list = DataFileAccess()._all_sales_list
    print(f"{DataFileAccess.SALES_ID['Sales']=}")
    for sales in all_sales_list:    # SaleList.__iter__
        print(sales)                # Sales.__str__
    print()

    salesfile = SalesFile('region1')
    print(f"{salesfile._sales_filename=}, "
          f"{SalesFile.NAMING_CONVENTION=}, {salesfile.is_valid_filename_format=}")
    print(f"{DataFileAccess.SALES_ID['Sales']=}")
    print()

    salesfile = SalesFile('sales_q1_2021_x.csv')
    print(f"{salesfile._sales_filename=}, "
          f"{salesfile.is_valid_filename_format=}, {salesfile.get_region_code()=}")
    saleslist = salesfile.import_sales()
    print(f"{(saleslist is None)=}, {saleslist._sales_list=}")
    print(f"{DataFileAccess.SALES_ID['Sales']=}")
    print()

    salesfile = SalesFile('sales_q2_2021_w.csv')
    print(f"{salesfile._sales_filename=}, "
          f"{salesfile.is_valid_filename_format=}, {salesfile.get_region_code()=}")
    saleslist = salesfile.import_sales()
    print(f"{(saleslist is None)=}, {saleslist._sales_list=}")
    print(f"{DataFileAccess.SALES_ID['Sales']=}")
    print()

    salesfile = SalesFile('sales_q3_2021_w.csv')
    print(f"{salesfile._sales_filename=}, "
          f"{salesfile.is_valid_filename_format=}, {salesfile.get_region_code()=}")
    saleslist = salesfile.import_sales()
    print(f"{(saleslist is None)=}, {saleslist._sales_list=}")
    for sales in saleslist._sales_list:
        print(f"{str(sales)=}")
    print(f"{DataFileAccess.SALES_ID['Sales']=}")
    print()

    salesfile = SalesFile('sales_q4_2021_w.csv')
    print(f"{salesfile._sales_filename=}, "
          f"{salesfile.is_valid_filename_format=}, {salesfile.get_region_code()=}")
    saleslist = salesfile.import_sales()
    print(f"{(saleslist is None)=}, {saleslist._sales_list=}")
    for sales in saleslist._sales_list:
        print(f"{str(sales)=}")
    print(f"{DataFileAccess.SALES_ID['Sales']=}")
    all_sales_list.concat(saleslist)
    for sales in saleslist._sales_list:
        print(f"{str(sales)=}")
    for sales in all_sales_list:
        print(f"{str(sales)=}")
    print(f"{DataFileAccess.SALES_ID['Sales']=}")
    print()

    importedfile = ImportedFile()
    print(f"{importedfile.already_imported(salesfile._sales_filepath_name)=}")
    importedfile.add_imported_file(salesfile._sales_filepath_name)
    print(f"{DataFileAccess.SALES_ID['Sales']=}")
    print(f"{importedfile.already_imported(salesfile._sales_filepath_name)=}")


if __name__ == '__main__':
    main()