from p01beg_2bl_salesmanager import *

class ConsoleUI:
    def __init__(self):
        self._sales_manager = SalesManager()

    @staticmethod
    def display_title():
        print("SALES DATA IMPORTER\n")

    @staticmethod
    def display_menu():
        cmd_format = "6"  # ^ center, < is the default for str.
        print("COMMAND MENU",
              f"{'view':{cmd_format}} - View all sales",
              f"{'add1':{cmd_format}} - Add sales by typing sales, year, month, day, and region",
              f"{'add2':{cmd_format}} - Add sales by typing sales, date (YYYY-MM-DD), and region",
              f"{'import':{cmd_format}} - Import sales from file",
              f"{'menu':{cmd_format}} - Show menu",
              f"{'exit':{cmd_format}} - Exit program", sep='\n')


    def execute_command(self) -> None:
        while True:
            action = input("\nPlease enter a command: ").strip().lower()
            if action == "exit":
                self._sales_manager._datafileaccess.save_all_sales()
                break
            if action == 'view':
                self._sales_manager.view_sales(self._sales_manager._datafileaccess._all_sales_list)
            elif action == "import":
                self._sales_manager.import_sales()
            elif action == "add1":
                self._sales_manager.add_sales1()
            elif action == "add2":
                self._sales_manager.add_sales2()
            elif action == "menu":
                self.display_menu()
            else:
                print("Invalid command. Please try again.\n")
                self.display_menu()


def main():
    consoleui = ConsoleUI()
    consoleui.display_title()
    consoleui.display_menu()
    consoleui.execute_command()

    print("Bye!")


if __name__ == "__main__":
    main()
