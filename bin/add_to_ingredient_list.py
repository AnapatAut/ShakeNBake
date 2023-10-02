# Created by Inkaphol S., 26 Sep 2023
# Modified by Anapat B., 28 Sep 2023
import os.path
import db_manager as db


def main():
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)

    # create a database connection
    conn = db.create_connection()
    with conn:
        file_name = parent_dir + "/data/ingredient_list.txt"
        in_file = open(file_name, "r")
        for line in in_file:
            line = line.strip()
            id, name = line.split(";")
            task = (id, name)

            # create tasks
            db.create_task(conn, task, "ingredient_list")


if __name__ == '__main__':
    main()
