
# [Import all objects from the p01_2bl_salesmanager module]


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


# [Write code to ask user to enter a command and call corresponding functions[ 
def execute_command(sales_list) -> None:
    pass


def main():
    display_title()
    display_menu()

    # get all original sales data from a csv file
    sales_list = import_all_sales()

    execute_command(sales_list)

    print("Bye!")


# if started as the main module, call the main function
if __name__ == "__main__":
    main()

  


  
