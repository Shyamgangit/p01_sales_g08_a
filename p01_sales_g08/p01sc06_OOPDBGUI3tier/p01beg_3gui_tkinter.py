import p01beg_1da_sales_db as db
from p01beg_1da_sales import Sales, Regions

from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox  # To override the basic Tk widgets, the import should follow the Tk import

class SalesFrame(ttk.Frame):
    sqlite_dbaccess: db.SQLiteDBAccess   # type hint

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.parent = parent
        self.salesDate_entry = None
        self.region_entry = None
        self.amount_entry = None
        self.id_entry = None
        self.getAmount_button = None
        self.clearField_button = None
        self.saveChanges_button = None
        
        # Define string variable for text entry fields
        self.salesDate = tk.StringVar()
        self.region = tk.StringVar()
        self.amount = tk.StringVar()
        self.id = tk.StringVar()

        self.init_components()
        
        # for database access
        self.sales = None
        self.sqlite_dbaccess = db.SQLiteDBAccess()


    def init_components(self):
        # Display the grid of labels and text entry fields
        self.pack()
        ttk.Label(self, text="Enter date and region to get sales amount",
                  ).grid(row=0, column=0, columnspan=4)

        ttk.Label(self, text="Date:").grid(row=1, column=0, sticky=tk.E)
        self.salesDate_entry = ttk.Entry(self, width=25, textvariable=self.salesDate)
        self.salesDate_entry.grid(row=1, column=1, columnspan=2)

        ttk.Label(self, text="Region:").grid(row=2, column=0, sticky=tk.E)
        self.region_entry = ttk.Entry(self, width=25, textvariable=self.region)
        self.region_entry.grid(row=2, column=1, columnspan=2)

        ttk.Label(self, text="Amount:").grid(row=3, column=0, sticky=tk.E)
        self.amount_entry = ttk.Entry(self, width=25, textvariable=self.amount, state=tk.DISABLED)
        self.amount_entry.grid(row=3, column=1, columnspan=2)

        ttk.Label(self, text="ID:").grid(row=4, column=0, sticky=tk.E)
        self.id_entry = ttk.Entry(self, width=25, textvariable=self.id, state="readonly")
        self.id_entry.grid(row=4, column=1, columnspan=2)

        # Create a frame to store the buttons
        button_frame = ttk.Frame(self)
        # Add the button frame to the bottom row of the main grid
        button_frame.grid(row=5, column=0, columnspan=4, sticky=tk.E)
        # Add buttons to the button frame
        self.getAmount_button = ttk.Button(button_frame, text="Get Amount", command=self.get_amount)
        self.getAmount_button.grid(row=0, column=0, padx=5)
        self.clearField_button = ttk.Button(button_frame, text="Clear Field", command=self.clear_field)
        self.clearField_button.grid(row=0, column=1)
        self.saveChanges_button = ttk.Button(button_frame, text="Save Changes", command=self.save_changes, state=tk.DISABLED)
        self.saveChanges_button.grid(row=0, column=2)
        ttk.Button(button_frame, text="Exit", command=self.parent.destroy).grid(row=0, column=3, padx=5)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)


    def get_amount(self):
        sales_date = self.salesDate.get()
        region_code = self.region.get()
        if sales_date == "" or region_code == "":
            messagebox.showerror("Error", "Please enter date and region to get sales amount")
        else:
            # check if sales date is in the right format
            try:
                sales_date = datetime.strptime(sales_date, Sales.DATE_FORMAT).date()  # ValueError
            except ValueError:
                messagebox.showerror("Error", f"{sales_date} is not in a valid date format \n"
                                              "'yyyy-mm-dd'")
            else:
                # check if region is one of the right option
                regions = self.sqlite_dbaccess.retrieve_regions()
                region_codes = [region.code for region in regions]
                if region_code not in region_codes:
                    messagebox.showerror("Error", f"{region_code} is not one of the following \n"
                                                  f"region code: {region_codes}")
                else: # check if there is sales by the date and region
                    self.sales = self.sqlite_dbaccess.retrieve_sales_by_date_region(sales_date, region_code)
                    if self.sales is None:
                        # clear id and amount field
                        self.amount.set("")
                        self.id.set("")
                        # notify user for no sales and expected values
                        messagebox.showerror("Error", "No sales found.")
                    else:
                        self.amount.set(self.sales.amount)
                        self.id.set(self.sales.id)
                        self.salesDate_entry.config(state=tk.DISABLED)
                        self.region_entry.config(state=tk.DISABLED)
                        self.amount_entry.config(state=tk.ACTIVE)
                        self.saveChanges_button.config(state=tk.NORMAL)

    
    def clear_field(self):
        self.id.set("")
        self.amount.set("")
        self.salesDate.set("")
        self.region.set("")
        self.salesDate_entry.config(state=tk.NORMAL)
        self.region_entry.config(state=tk.NORMAL)
        self.amount_entry.config(state=tk.DISABLED)
        self.getAmount_button.config(state=tk.NORMAL)
        self.clearField_button.config(state=tk.NORMAL)
        self.saveChanges_button.config(state=tk.DISABLED)

    
    def save_changes(self):
        sales_date = self.salesDate.get()
        region_code = self.region.get()
        amount = self.amount.get()
        id = self.id.get()
        if id == '':
            messagebox.showerror("Error", "No sales to save.")
        elif amount == "":
            messagebox.showerror("Error", "Please enter amount to save sales amount")
        else: # update amount for a sale record by id
            id = int(id)
            amount = float(amount)
            sales_date = datetime.strptime(sales_date, Sales.DATE_FORMAT).date()
            region = Regions().get(region_code)
            self.sales = Sales(id, amount, sales_date, region)
            self.sqlite_dbaccess.update_sales(self.sales)
            messagebox.showinfo("Success", f"{str(self.sales)} is updated.")
            self.clear_field()


def main():
    root = tk.Tk()
    root.title("Edit Sales Amount")
    SalesFrame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
