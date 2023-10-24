"""
 db_manager.py

 Database manager used to as a center to interface with the database

 Created by Anapat B., 27 Sep 2023
"""
import os
import sqlite3
from sqlite3 import Error

table_dict = {
    "main": ["recipe_id, name", "?, ?"],
    "ingredient_list": ["id, name", "?, ?"],
    "recipe_ingredients": ["recipe_id, name, amount, measurement", "?, ?, ?, ?"],
    "recipe_steps": ["recipe_id, step_number, step_instruction", "?, ?, ?"],
    "history_note": ["history_id", "recipe_id", "note_details", "timestamp", "?, ?, ?, ?"]
}

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
db_file = parent_dir + "/data/recipe_database.db3"
print(db_file)


def create_connection():
    """
    Establish connection with the database
    :return:
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def create_task(conn, task, table):
    """
    Create element to be added to the database
    :param conn: Connection to the database
    :param task: Elements to be added to the database
    :param table: Name of the table to add the data to
    :return:
    """

    cur = None
    try:
        sql = (" INSERT INTO " + table + "(" + table_dict[table][0] +
               ") VALUES(" + table_dict[table][1] + ") ")
        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit()
        print(f"{task}")
    except Error as e:
        print(e)
    return cur.lastrowid


# Query a search in the database
# "conn" is the connection to the database
# "table" is the name of the table to query the data from
# "header" is the header of the column to query from
# "element" is the element we want to find
def db_query(conn, table, header, element):
    """
    Query data from database
    :param conn: Connection to the database
    :param table: Name of the table to query the data from
    :param header: header of the column to query from
    :param element:
    :return:
    """

    rec = None
    try:
        cur = conn.cursor()
        sql_query = "SELECT * FROM " + table + " WHERE " + header + " = ?"
        cur.execute(sql_query, (element,))
        rec = cur.fetchall()

        if not rec:
            return None

        head = table_dict[table][0].split(",")
        for item in head:
            print(item, end="")
        print()
    except Error as e:
        print(e)
    return rec


# Query all elements from a table
# "conn" is the connection to the database
# "table" is the name of the table to query the data from
def db_searchbar_query(conn, table):
    """
    Query data from database
    :param conn:
    :param table:
    :return:
    """

    rec = None
    try:
        cur = conn.cursor()
        sql_query = "SELECT * FROM " + table
        cur.execute(sql_query)
        rec = cur.fetchall()

        print(rec)
    except Error as e:
        print(e)
    return rec
