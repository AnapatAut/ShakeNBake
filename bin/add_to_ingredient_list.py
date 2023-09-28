##By: Inkaphol S.       Last Updated: 26/9/2023
import sqlite3
from sqlite3 import Error
import os


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO ingredients(ID,NAME)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    print(f"{task}")
    return cur.lastrowid


def main():
    BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test.db3')
    database = BASE_DIR

    # create a database connection
    conn = create_connection(database)
    with conn:
        file_name = "../data/ingredient_list.txt"
        in_file = open(file_name,"r")
        for line in in_file:
            line = line.strip()
            id, name = line.split(";")
            task = (id, name)

            # create tasks
            create_task(conn, task)

if __name__ == '__main__':
    main()

