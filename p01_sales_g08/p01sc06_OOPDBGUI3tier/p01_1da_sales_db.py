import sqlite3
from pathlib import Path
from datetime import date
from typing import Optional
from p01_1da_sales import Sales, Regions, Region

class SQLiteDBAccess:
    SQLITEDBPATH = Path(__file__).parent.parent / 'p01_db'

    def __init__(self):
        self._sqlite_sales_db = 'sales_db.sqlite'
        self._dbpath_sqlite_sales_db = SQLiteDBAccess.SQLITEDBPATH / self._sqlite_sales_db

    def connect(self) -> sqlite3.Connection:
        """Connect to the SQLite database and return the connection object."""
        return sqlite3.connect(self._dbpath_sqlite_sales_db)

    def retrieve_sales_by_date_region(self, sales_date: date, region_code: str) -> Optional[Sales]:
        """Retrieve ID, amount, salesDate, and region field from Sales table for the given salesDate and region values."""
        conn = self.connect()
        cursor = conn.cursor()
        query = "SELECT ID, amount, salesDate, region FROM Sales WHERE salesDate=? AND region=?"
        cursor.execute(query, (sales_date, region_code))
        result = cursor.fetchone()
        conn.close()
        if result:
            return Sales(result[0], result[1], result[2], Regions().get(result[3]))
        return None

    def update_sales(self, sales: Sales) -> None:
        """Update amount, salesDate, and region fields of Sales table for the record with the given ID value."""
        conn = self.connect()
        cursor = conn.cursor()
        query = "UPDATE Sales SET amount=?, salesDate=?, region=? WHERE ID=?"
        cursor.execute(query, (sales.amount, sales.sales_date, sales.region.code, sales.id))
        conn.commit()
        conn.close()

    def retrieve_regions(self) -> Regions:
        """Retrieve region code and name from the Region table."""
        conn = self.connect()
        cursor = conn.cursor()
        query = "SELECT code, name FROM Region"
        cursor.execute(query)
        regions = Regions()
        for code, name in cursor.fetchall():
            regions.add_region(Region(code, name))
        conn.close()
        return regions
