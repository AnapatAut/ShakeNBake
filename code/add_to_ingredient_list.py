"""
 add_to_ingredient_list

 Connects to the recipe_database and creates a pre-set list of ingredients
 for the database using the data/ingredients_list.txt file as a base

 Created by Inkaphol S., 26 Sep 2023

 Modified to interface with the database
 through db_manager

 Modified by Anapat B., 28 Sep 2023

"""
import os.path
import db_manager as db


def main():
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)

    # create a database connection
    conn = db.create_connection()
    with conn:
        file_name = parent_dir + "/data/ingredient_list.txt"
        with open(file_name, "r") as in_file:
            for line in in_file:
                line = line.strip()
                id_num, name = line.split(";")
                task = (id_num, name)

                # create tasks
                db.create_task(conn, task, "ingredient_list")

if __name__ == '__main__':
    main()
