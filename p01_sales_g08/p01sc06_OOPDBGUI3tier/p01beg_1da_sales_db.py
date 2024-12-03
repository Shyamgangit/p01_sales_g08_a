# [import any other necessary module(s)]
import sqlite3
from typing import Optional, List, Any
from pathlib import Path
from datetime import date

from p01_sales.p01sc06_OOPDBGUI3tier.p01beg_1da_sales import Regions
from p01beg_1da_sales import Sales, Regions

# -------------- Data Access (SQLite) --------------------------
class SQLiteDBAccess:
    SQLITEDBPATH = Path(__file__).parent.parent / 'p01_db'

    def __init__(self):
        self._sqlite_sales_db = 'sales_db.sqlite'
        self._dbpath_sqlite_sales_db = SQLiteDBAccess.SQLITEDBPATH / self._sqlite_sales_db


    def connect(self) -> sqlite3.Connection:
        '''Connect to the SQLite database and return the connection object.'''
        try:
            connection = sqlite3.connect(self._dbpath_sqlite_sales_db)
            return connection
        except sqlite3.Error as e:
            print(f"SQLite connection error: {e}")
            raise

    def retrieve_sales_by_date_region(self, sales_date: date, region_code: str) -> Optional[Sales]:
        '''retrieve ID, amount, salesDate, adn region field from Sales table for the records that have the given salesDate and region values.'''
        query = '''
            SELECT id, amount, salesDate, region
            FROM Sales
            WHERE salesDate = ? AND region = ?;
        '''
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (sales_date.isoformat(), region_code))
                row = cursor.fetchone()
                if row:
                    return Sales(*row)
                return None
        except sqlite3.Error as e:
            print(f"Error retrieving sales by date and region: {e}")
            raise

    def update_sales(self, sales: Sales) -> None:
        '''update amount, salesDate, and region fields of Sales table for the record with the given ID value. '''

        query = '''
            UPDATE Sales
            SET amount = ?, salesDate = ?, region = ?
            WHERE id = ?;
        '''
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (sales.amount, sales.sales_date.isoformat(), sales.region, sales.id))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating sales record: {e}")
            raise

    def retrieve_regions(self) -> list[Regions]:
        '''retreive region code and name from Region table'''

        query = '''
            SELECT regionCode, regionName
            FROM Region;
        '''
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                rows: list[Any] = cursor.fetchall()
                return [Regions() for row in rows]
        except sqlite3.Error as e:
            print(f"Error retrieving regions: {e}")
            raise