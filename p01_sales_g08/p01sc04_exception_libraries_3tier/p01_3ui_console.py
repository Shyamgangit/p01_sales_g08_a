# Import all objects from the p01_2bl_salesmanager module
from p01_2bl_salesmanager import *


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


# Function to ask user for command and execute corresponding function
def execute_command(sales_list) -> None:
    while True:
        command = input("\n Please enter a command: ").strip().lower()

        if command == "view":
            # View all sales
            view_sales(sales_list)

        elif command == "add1":
            # Add sales with individual date components
            add_sales1(sales_list)

        elif command == "add2":
            # Add sales with full date
            add_sales2(sales_list)

        elif command == "import":
            # Import sales from a file
            import_sales(sales_list)

        elif command == "menu":
            # Display the menu again
            display_menu()

        elif command == "exit":
            # Exit the program
            break

        else:
            print("Invalid command. Please try again.")


def main():
    display_title()
    display_menu()

    # Get all original sales data from a CSV file
    sales_list = import_all_sales()

    # Execute user commands
    execute_command(sales_list)

    print("Bye!")


# If started as the main module, call the main function
if __name__ == "__main__":
    main()

