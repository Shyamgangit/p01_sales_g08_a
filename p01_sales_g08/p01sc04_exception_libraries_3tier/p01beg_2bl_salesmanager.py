# [import p01_1da_sales and use alias sd]

import csv
# [import class Decimal and constant ROUND_HALF_UP from decimal library]
import locale as lc

lc.setlocale(lc.LC_ALL, "en_US")


# [Add code to handle exception FileNotFoundError by displaying "Sales file not found"]
def import_all_sales() -> list:
    with (open(sd.FILEPATH / sd.ALL_SALES, newline='') as csvfile):
        reader = csv.reader(csvfile)
        sales_list = []
        for line in reader:
            if len(line) > 0:
                *amount_sales_date, region_code = line
                sd.correct_data_types(amount_sales_date)
                amount, sales_date = amount_sales_date[0], amount_sales_date[1]
                data = {"amount": amount,
                        "sales_date": sales_date,
                        "region": region_code,
                        }
                sales_list.append(data)
        return sales_list  # within with statement


# [Modify the code to use Decimal of decimal library and currency function of the locale library ]
def view_sales(sales_list: list) -> bool:
    bad_data_flag = False
    if len(sales_list) == 0:  # sales_list could be [] or None
        print("No sales to view.\n")
    else: # not empty
        col1_w, col2_w, col3_w, col4_w, col5_w = 5, 15, 15, 15, 15
        total_w = col1_w + col2_w + col3_w + col4_w + col5_w
        print(f"{' ':{col1_w}}"
              f"{'Date':{col2_w}}"
              f"{'Quarter':{col3_w}}"
              f"{'Region':{col4_w}}"
              f"{'Amount':>{col5_w}}")
        print(horizontal_line := f"{'-' * total_w}")
        total = 0.0

        for idx, sales in enumerate(sales_list, start=1):
            if sd.has_bad_data(sales):
                bad_data_flag = True
                num = f"{idx}.*"   # add period and asterisk
            else:
                num = f"{idx}."    # add period only

            amount = sales["amount"]
            if not sd.has_bad_amount(sales):
                total += amount

            sales_date = sales["sales_date"]
            if sd.has_bad_date(sales):
                bad_data_flag = True
                month = 0
            else:
                month = int(sales_date.split("-")[1])

            region = sd.get_region_name(sales["region"])
            quarter = f"{sd.cal_quarter(month)}"
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
    sales_list.append(data := sd.from_input1())
    print(f"Sales for {data["sales_date"]} is added.\n")


def add_sales2(sales_list) -> None:
    sales_list.append(data := sd.from_input2())
    print(f"Sales for {data["sales_date"]} is added.\n")


# [Modify the code accordingly to use objects from other module]
def import_sales(sales_list) -> None:
    # get filename from user
    filename = input("Enter name of file to import: ")
    filepath_name = FILEPATH / filename
    # check if filename is valid
    if not is_valid_filename_format(filename):
        print(f"Filename '{filename}' doesn't follow the expected",
              f"format of '{NAMING_CONVENTION}'.")
    # check if region code (the 5th character from end) is valid.
    elif not is_valid_region(get_region_code(filename)):
        print(f"Filename '{filename}' doesn't include one of",
              f"the following region codes: {list(VALID_REGIONS.keys())}.")
    # check if file has already been imported
    elif already_imported(filepath_name):
        filename = filename.replace("\n", "")  # remove new line character
        print(f"File '{filename}' has already been imported.")
    else:
        # import sales data from file
        try:
            imported_sales_list = import_sales(filepath_name)  # function in the imported module
        except Exception as e:  
            print(f"{type(e)}. Fail to import sales from '{filename}'.")
        else:
            # display imported sales
            bad_data_flag = view_sales(imported_sales_list)
            if bad_data_flag:
                print(f"File '{filename}' contains bad data.\n"
                     "Please correct the data in the file and try again.")
            elif len(imported_sales_list) > 0:  
                sales_list.extend(imported_sales_list)    
                print("Imported sales added to list.")
                add_imported_file(filepath_name)



# [Modify the code to raise and handle exception(s)]
def save_all_sales(sales_list: list, delimiter: str = ',') -> None:
    # convert the list of Sales to a list of lists of sales data (amount, sales_date, region.code), using comprehension
    sales_records = [[sales["amount"], f"{sales["sales_date"]:{sd.DATE_FORMAT}}", sales["region"]]
                     for sales in sales_list]
    try:
        with open(sd.FILEPATH / sd.ALL_SALES, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter)

            ''' The following additional code is only for practicing raising 
            exception for testing purpose, and will be commented out for 
            testing whether the function can save data successfully.
            You will write code to do the following:
            - Write a try clause in which raise an OSError.
            - Reraise the OSError in the except clause that handles the OSError exception.
            - Write code to make sure the csvfile is closed no matter an exception occurs or not.
            - Optionally, you may also add code to roll back the change to the imported_files]
            '''
            ...
          
            writer.writerows(sales_records)
            print("Saved sales records.")
    except Exception as e:
        print(type(e), "Sales data could not be saved.")



def main():
  '''
  Write code to test the functions in this module
  '''
  ...
  

if __name__ == "__main__":
    main()
