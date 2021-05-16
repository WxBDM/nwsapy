"""This file is intended to be the bridge between the database and the programmer.

There should not be any SQL queries run from any file. Create a method here and call it.
"""

import sqlite3


def set_user_agent(user_agent_str):
    conn = sqlite3.connect("headers.db")
    cursor = conn.cursor()

    # create the table
    query = "CREATE TABLE IF NOT EXISTS headers (id INTEGER PRIMARY KEY, keys text, value_pair text);"
    cursor.execute(query)

    # add user agent to db
    # check to see if it's already in the db
    query = "SELECT EXISTS(SELECT 1 FROM headers);"
    result = cursor.execute(query).fetchall()
    if result[0][0] == 0:
        query = "INSERT INTO headers (id, keys, value_pair) VALUES (?, ?, ?);"
        cursor.execute(query, (1, 'User-Agent', user_agent_str))
        conn.commit()

    # If it's already set, then update it.
    else:
        query = "UPDATE headers SET keys = ?, value_pair = ? WHERE keys = 'User-Agent';"
        cursor.execute(query, ('User-Agent', user_agent_str))
        conn.commit()

    conn.close()


def get_user_agent_dict():
    conn = sqlite3.connect("headers.db")
    cursor = conn.cursor()

    # check to see if it's in the database. If so, get it.
    query = "SELECT EXISTS(SELECT keys FROM headers WHERE keys = 'User-Agent');"
    result = cursor.execute(query).fetchall()
    if result[0][0] == 1:
        query = "SELECT keys, value_pair FROM headers WHERE keys = 'User-Agent';"
        info = cursor.execute(query)
        info = info.fetchall()
        return dict({info[0][0] : info[0][1]})

    # If it's already set, then update it.
    else:
        print("User-Agent hasn't been set. Be sure to set it using `nwsapy.set_user_agent()")
        return {"NWSAPy" : "nulluser@email.com"}

    conn.close()