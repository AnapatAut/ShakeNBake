# Created by Anapat B., 27 Sep 2023
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
