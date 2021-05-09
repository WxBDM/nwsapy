"""This file is intended to be the bridge between the database and the programmer.

There should not be any SQL queries run from any file. Create a method here and call it.
"""

import sqlite3
import pandas as pd

class Database:
    _conn = None
    _cursor = None

    def __init__(self, *args, **kwargs):
        self.database = "nwsinfo.db"
        self.table_name = None

    def _open_connection(self):
        """Opens a connection to the database."""

        if isinstance(self.table_name, type(None)):
            raise AttributeError("Table name must be set (Database.table_name = 'your table name')")

        self._conn = sqlite3.connect(self.database)
        self._cursor = self._conn.cursor()

    def _close_connection(self):
        """Closes the connection to the database."""

        self._conn.close()
        self._conn = None
        self._cursor = None

    def get_product_types(self):
        """Returns a pandas DataFrame of the product types.

        Returns
        =======
            df => pandas dataframe for producttypes table.
                Columns: productCode, productName
        """

        self._open_connection()

        df = pd.read_sql_query(f"SELECT * FROM {self.table_name}", self._conn)
        df = df.drop(columns = ['id'])

        self._close_connection()

        return df
