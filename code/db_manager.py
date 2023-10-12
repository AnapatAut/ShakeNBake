# db_manager.py
#
# Database manager used to as a center to interface with the database
#
# Created by Anapat B., 27 Sep 2023
#
# Modified to allow query all elements from a database table
#
# Modified by Anapat B., 12 Oct 2023

import os
import sqlite3
from sqlite3 import Error

table_dict = {
    "main": ["recipe_id, name, ingredients, steps", "?, ?, ?, ?"],
    "ingredient_list": ["id, name", "?, ?"],
    "recipe_ingredients": ["recipe_id, name, amount, measurement", "?, ?, ?, ?"],
    "recipe_steps": ["id, step_number, step_instruction", "?, ?, ?"]
}

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
db_file = parent_dir + "/data/recipe_database.db3"
print(db_file)


# Establish connection with the database
def create_connection():
    """
    Connect with database
    :return:
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


# Create element to be added to the database
# "conn" is the connection to the database
# "task" is elements to be added to the database
# "table" is the name of the table to add the data to
def create_task(conn, task, table):
    """
    Create a new task
    :param conn:
    :param task:
    :param table:
    :return:
    """

    try:
        sql = " INSERT INTO " + table + "(" + table_dict[table][0] + ") VALUES(" + table_dict[table][1] + ") "
        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit()
        print(f"{task}")
        return cur.lastrowid
    except Error as e:
        print(e)


# Query a search in the database
# "conn" is the connection to the database
# "table" is the name of the table to query the data from
# "header" is the header of the column to query from
# "element" is the element we want to find
def db_query(conn, table, header, element):
    """
    Query data from database
    :param conn:
    :param table:
    :param header:
    :param element:
    :return:
    """

    try:
        cur = conn.cursor()
        sql_query = "SELECT * FROM " + table + " WHERE " + header + " = ?"
        cur.execute(sql_query, (element,))
        rec = cur.fetchall()

        if not rec:
            return None

        head = table_dict[table][0].split(",")
        for element in head:
            print(element, end="")
        print()

        return rec
    except Error as e:
        print(e)


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

    try:
        cur = conn.cursor()
        sql_query = "SELECT * FROM " + table
        cur.execute(sql_query)
        rec = cur.fetchall()

        if not rec:
            return None

        print(rec)

        return rec
    except Error as e:
        print(e)
