
# Provides the tools for creating and running tests.
import unittest

# Allows running external processes (like your console application) and interacting with their input/output.
import subprocess


from pathlib import Path
entry_point: Path = Path('../../p01sc4_exception_libraries_3tier/p01_3ui_console.py')
all_sales_csv: Path = Path('../../p01_files/all_sales.csv')
imported_files_txt: Path = Path('../../p01_files/imported_files.txt')
test_log: Path = Path('./test_log.txt')


class TestSalesDataImporter(unittest.TestCase):

    def setUp(self):
        """Set up the required content for testing"""
        with open(all_sales_csv, "w", newline='') as f:
            f.write("12493.0,2020-12-22,w\n"
                    "13761.0,2021-09-15,e\n"
                    "9710.0,2021-05-15,e\n"
                    "8934.0,2021-08-08,c\n"
                    "18340.0,2020-12-22,c\n"
                    "12345.0,2020-04-17,m\n"
                    "2929.0,2021-04-10,w\n"
                    )
        with open(imported_files_txt, "w") as f:
            f.write("")

    # def tearDown(self):
    #     """Tear down the environment for testing"""

    def run_app(self, input_data):
        """
        Simulates running the console application with user input.
        """
        # Start the process
        process = subprocess.Popen(
             ["python", entry_point],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True # ensures that input/output is handled as text (not bytes).
         )

        # Send input and get output
        # sends the simulated user input (via stdin) to the console app.
        stdout, stderr = process.communicate(input=input_data)

        return stdout, stderr


    def test_view_command(self):
        """
        Test the 'view' command to display sales data.
        """
        self.setUp()

        input_data = "view\nexit\n"  # Simulates input
        stdout, stderr = self.run_app(input_data)

        # Check that key parts of the expected output are present
        key_expected_output = (
            "     Date           Quarter        Region                  Amount\n"
            "-----------------------------------------------------------------\n"
            "1.   2020-12-22     4              West                $12,493.00\n"
            "2.   2021-09-15     3              East                $13,761.00\n"
            "3.   2021-05-15     2              East                 $9,710.00\n"
            "4.   2021-08-08     3              Central              $8,934.00\n"
            "5.   2020-12-22     4              Central             $18,340.00\n"
            "6.   2020-04-17     2              Mountain            $12,345.00\n"
            "7.   2021-04-10     2              West                 $2,929.00\n"
        )
        # Assert that the key expected output appears in the stdout
        self.assertIn(key_expected_output, stdout)  # self.assertEqual(stdout, key_expected_output)
        self.assertIn("-----------------------------------------------------------------\n", stdout)
        self.assertIn("TOTAL                                                  $78,512.00\n", stdout)


    def test_add1_command(self):
        """
        Test the 'add1' command for adding sales with detailed input validation.
        """
        self.setUp()

        input_data = ("add1\n"
                      "0\n"
                      "3245\n"
                      "0\n"
                      "3000\n"
                      "2021\n"
                      "0\n"
                      "20\n"
                      "2\n"
                      "0\n"
                      "40\n"
                      "14\n"
                      "x\n"
                      "c\n"
                      "exit\n"
                      )
        stdout, stderr = self.run_app(input_data)

        expected_steps = [ # "add1"
            "Amount:             ",  # "0\n"
            "Amount must be greater than zero.\nAmount:             ",  # "3245\n"
            "Year (2000-2999):   ",  # "0\n"
            "Year must be between 2000 and 2999.\nYear (2000-2999):   ",  # "3000\n"
            "Year must be between 2000 and 2999.\nYear (2000-2999):   ",  # "2021\n"
            "Month (1-12):       ",  # "0\n"
            "Month must be between 1 and 12.\nMonth (1-12):       ",  # "20\n"
            "Month must be between 1 and 12.\nMonth (1-12):       ",  # "2\n"
            "Day (1-28):         ",  # "0\n"
            "Day must be between 1 and 28.\nDay (1-28):         ",  # "40\n"
            "Day must be between 1 and 28.\nDay (1-28):         ",  # "14\n"
            "Region ('w', 'm', 'c', 'e'):",  # "x\n"
            "Region must be one of the following: ('w', 'm', 'c', 'e').\nRegion ('w', 'm', 'c', 'e'):",  # "c\n"
            "Sales for 2021-02-14 is added.\n",
            # "\n\nPlease enter a command: ", # "exit\n"
        ]

        for i, step in enumerate(expected_steps, start=1):
            if i == len(expected_steps):
                break # no need to check the last step
            else:
                self.assertIn(step, stdout)


    def test_add2_command(self):
        """
        Test the 'add2' command for adding sales with detailed input validation.
        """
        self.setUp()

        input_data = ("add2\n"
                      "4324\n"
                      "0021-08-14\n"
                      "202a\n"
                      "2021-8-14\n"
                      "e\n"
                      "exit\n"
                      )
        stdout, stderr = self.run_app(input_data)

        expected_steps = [ # "add2"
            "Amount:             ",  # "4324\n"
            "Date (yyyy-mm-dd):  ",  # "0021-08-14\n"
            "Year of the date must be between 2000 and 2999.\nDate (yyyy-mm-dd):  ",  # "202a\n"
            "202a is not in a valid date format.\nDate (yyyy-mm-dd):  ",  # "2021-8-14\n"
            "Region ('w', 'm', 'c', 'e'):",  # "e\n"
            "Sales for 2021-08-14 is added.\n",
            # "\n\nPlease enter a command: ", # "exit\n"
        ]

        for i, step in enumerate(expected_steps, start=1):
            if i == len(expected_steps):
                break # no need to check the last step
            else:
                self.assertIn(step, stdout)


    def test_import_command(self):
        """
        Test the 'import' command with valid and invalid filenames.
        """
        self.setUp()

        input_data = ("import\n"
            "region1\n"
            "import\n"
            "sales_q1_2021_x.csv\n"
            "import\n"
            "sales_q1_2021_w.csv\n"
            "import\n"
            "sales_q2_2021_w.csv\n"
            "import\n"
            "sales_q3_2021_w.csv\n"
            "import\n" 
            "sales_q4_2021_w.csv\n"
            "import\n"
            "sales_q4_2021_w.csv\n"
            "exit\n"
        )
        stdout, stderr = self.run_app(input_data)

        expected_steps = [ # "import\n"
            "Enter name of file to import: ",  # "region1\n"
            "Filename 'region1' doesn't follow the expected format of 'sales_qn_yyyy_r.csv'.\n"
            "\nPlease enter a command: ", # "import\n"
            "Enter name of file to import: ",  # "sales_q1_2021_x.csv\n"
            "Filename 'sales_q1_2021_x.csv' doesn't include one of the following region codes: ['w', 'm', 'c', 'e'].\n"
            "\nPlease enter a command: ",  # "import\n"
            "Enter name of file to import: ",  # "sales_q1_2021_w.csv\n"
            "<class 'FileNotFoundError'>. Fail to import sales from 'sales_q1_2021_w.csv'.\n"
            "\nPlease enter a command: ",  # "import\n"
            "Enter name of file to import: ",  # "sales_q2_2021_w.csv\n"
            "No sales to view.\n"
            "\nPlease enter a command: ",  # "import\n"
            "Enter name of file to import: ",  # "sales_q3_2021_w.csv\n"
            "     Date           Quarter        Region                  Amount\n"
            "-----------------------------------------------------------------\n"
            "1.   2021-07-15     3              West                $13,761.00\n"
            "2.*  ?              0              West                 $9,710.00\n"
            "3.*  2021-09-15     3              West                         ?\n"
            "-----------------------------------------------------------------\n"
            "TOTAL                                                  $23,471.00\n"
            "\nFile 'sales_q3_2021_w.csv' contains bad data.\n"
            "Please correct the data in the file and try again.\n"
            "\nPlease enter a command: ",  # "import\n"
            "Enter name of file to import: ",  # "sales_q4_2021_w.csv\n"
            "     Date           Quarter        Region                  Amount\n"
            "-----------------------------------------------------------------\n"
            "1.   2021-10-15     4              West                $13,761.00\n"
            "2.   2021-11-15     4              West                 $9,710.00\n"
            "3.   2021-12-15     4              West                 $8,934.00\n"
            "-----------------------------------------------------------------\n"
            "TOTAL                                                  $32,405.00\n"
            "\nImported sales added to list.\n"          
            "\nPlease enter a command: ",  # "import\n"
            "Enter name of file to import: ",  # "sales_q4_2021_w.csv\n"
            "File 'sales_q4_2021_w.csv' has already been imported.\n"
            "\nPlease enter a command: ",  # "exit\n"
        ]

        for i, step in enumerate(expected_steps, start=1):
            if i == len(expected_steps):
                break # no need to check the last step
            else:
                self.assertIn(step, stdout)


    def test_menu_command(self):
        """
        Test the 'menu' command to redisplay the menu.
        """
        input_data = "menu\nexit\n"
        stdout, stderr = self.run_app(input_data)

        # Check that key parts of the expected output are present
        key_expected_output = (
            "COMMAND MENU\n"
        )
        # Assert that the key expected output appears in the stdout
        self.assertIn(key_expected_output, stdout)
        self.assertIn("view   - View all sales\n", stdout)
        self.assertIn("add1   - Add sales by typing sales, year, month, day, and region\n", stdout)
        self.assertIn("add2   - Add sales by typing sales, date (YYYY-MM-DD), and region\n", stdout)
        self.assertIn("import - Import sales from file\n", stdout)
        self.assertIn("menu   - Show menu\n", stdout)
        self.assertIn("exit   - Exit program\n", stdout)


    def test_invalid_command(self):
        """
        Test an invalid command to redisplay the menu.
        """
        input_data = "anything\nexit\n"
        stdout, stderr = self.run_app(input_data)

        # Check that key parts of the expected output are present
        key_expected_output = (
            "Invalid command. Please try again.\n\nCOMMAND MENU\n"
        )
        # Assert that the key expected output appears in the stdout
        self.assertIn(key_expected_output, stdout)
        self.assertIn("view   - View all sales\n", stdout)
        self.assertIn("view   - View all sales\n", stdout)
        self.assertIn("add1   - Add sales by typing sales, year, month, day, and region\n", stdout)
        self.assertIn("add2   - Add sales by typing sales, date (YYYY-MM-DD), and region\n", stdout)
        self.assertIn("import - Import sales from file\n", stdout)
        self.assertIn("menu   - Show menu\n", stdout)
        self.assertIn("exit   - Exit program\n", stdout)


    def test_exit_command(self):
        """
        Test the 'exit' command to terminate the application.
        """
        input_data = "exit\n"
        stdout, stderr = self.run_app(input_data)

        self.assertIn("Saved sales records.", stdout)
        self.assertIn("Bye!", stdout)

def run_tests(group):
    # Open the log file for writing test results
    with open(test_log, "a") as f:
        header = "\n" + "~" * 10 + f" GROUP {group} REPORT " + "~" * 10 + "\n"
        f.write(header)
        # Create a test runner with the log file as the output stream
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        # Run all tests
        unittest.main(testRunner=runner, exit=False)


if __name__ == "__main__":
    import sys
    # Parse custom arguments
    custom_args = []
    remaining_args = []
    for arg in sys.argv:
        if arg.startswith("--"):
            custom_args.append(arg)
        else:
            remaining_args.append(arg)
    # Set the remaining arguments back to sys.argv
    sys.argv = remaining_args
    group = custom_args[0].replace('--', '')

    run_tests(group)

