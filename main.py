
import requests
import sqlite3

from dbcomms import Database

def junk():
    headers = {"User-Agent": "(https://www.wxbdm.github.io, bdmolyne@gmail.com)"}

    url1 = "https://api.weather.gov/products/types"

    response1 = requests.get(url1, headers=headers).json()
    r1 = response1['@graph']

    # connect to the database (will auto-create if it's not there).
    conn = sqlite3.connect("nwsinfo.db")
    cursor = conn.cursor()

    query = '''CREATE TABLE IF NOT EXISTS producttypes 
        (id INTEGER PRIMARY KEY,
         productCode TEXT NOT NULL,
         productNAME TEXT NOT NULL
        );
        '''
    cursor.execute(query)
    conn.commit()

    conn.close()

    headers = {"User-Agent": "(https://www.wxbdm.github.io, bdmolyne@gmail.com)"}
    url1 = "https://api.weather.gov/products/types"

    response1 = requests.get(url1, headers=headers).json()
    responses = response1['@graph']

    # connect to the database (will auto-create if it's not there).
    conn = sqlite3.connect("nwsinfo.db")
    cursor = conn.cursor()

    for n, product in enumerate(responses):
        query = f"INSERT INTO producttypes VALUES (?, ?, ?)"
        cursor.execute(query, (n, product['productCode'], product['productName']))
        conn.commit()

    conn.close()

def main():

    db = Database()
    db.table_name = 'producttypes'

    df = db.get_product_types()
    print(df)


if __name__ == "__main__":
    main()