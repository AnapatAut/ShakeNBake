"""
 main_menu.py

 Python code for UI of main menu

 Created by Anapat B., 16 Oct 2023
"""

import sys
from PyQt5.QtCore import QRect, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QWidget, QListWidget, QPushButton, QLineEdit, QApplication
import db_manager as db
from collections import defaultdict


class ui_main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.full_recipe_list = []
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the UI page
        :return:
        """
        self.setWindowTitle("Main Menu")
        self.setGeometry(0, 0, 920, 680)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("central_widget")
        self.setCentralWidget(self.centralwidget)

        self.recipe_list_widget = QListWidget(self.centralwidget)
        self.recipe_list_widget.setObjectName("recipe_list_widget")
        self.recipe_list_widget.setGeometry(QRect(80, 80, 760, 500))

        self.add_recipe_widget = QPushButton(self.centralwidget)
        self.add_recipe_widget.setObjectName("add_recipe_widget")
        self.add_recipe_widget.setGeometry(QRect(760, 40, 80, 25))
        self.add_recipe_widget.setText(QCoreApplication.translate("Main Menu", "Add Recipe"))

        self.search_toggle_widget = QPushButton("Toggle", self.centralwidget)
        self.search_toggle_widget.setObjectName("search_toggle_widget")
        self.search_toggle_widget.setGeometry(QRect(80, 40, 100, 25))
        self.search_toggle_widget.setCheckable(True)
        self.search_toggle_widget.setText(QCoreApplication.translate("Main Menu", "Toggle Search"))

        self.search_bar_widget = QLineEdit(self.centralwidget)
        self.search_bar_widget.setObjectName("search_bar_widget")
        self.search_bar_widget.setGeometry(QRect(180, 40, 560, 25))
        self.setCentralWidget(self.centralwidget)

        self.toggle_search()
        self.search_toggle_widget.clicked.connect(self.toggle_search)

        self.recipe_list_widget.itemClicked.connect(self.view_recipe)

        self.add_recipe_widget.clicked.connect(self.add_recipe)

    def toggle_search(self):
        """
        Toggle search between search by recipe and ingredient
        :return:
        """
        self.get_recipe_list()
        self.search_bar_widget.clear()
        if self.search_toggle_widget.isChecked():
            print("Search Ingredient")
            self.search_bar_widget.setPlaceholderText(
                QCoreApplication.translate("Main Menu", "Search Ingredient"))
            self.get_ingredient_list()
            self.update_ingredient_list()
            self.search_bar_widget.textChanged.connect(self.update_ingredient_list)
        else:
            print("Search Recipe")
            self.search_bar_widget.setPlaceholderText(
                QCoreApplication.translate("Main Menu", "Search Recipe"))
            self.update_recipe_list()
            self.search_bar_widget.textChanged.connect(self.update_recipe_list)

    def get_recipe_list(self):
        """
        Fetch the recipe list from the database
        :return:
        """
        conn = db.create_connection()
        query = db.db_searchbar_query(conn, "main")
        try:
            self.full_recipe_list = []
            for recipes in query:
                self.full_recipe_list.append(recipes)
        except:
            print("Error")

    def update_recipe_list(self):
        """
        Update the recipes displayed according the user input
        :return:
        """
        str_input = self.search_bar_widget.text()
        self.recipe_list_widget.clear()
        print(str_input)
        matching_recipes = [recipe for recipe in self.full_recipe_list
                            if str_input.lower() in recipe[1].lower()]
        for recipe in matching_recipes:
            self.recipe_list_widget.addItem(recipe[1])

    def get_ingredient_list(self):
        """
        Fetch the recipe list from the database
        :return:
        """
        conn = db.create_connection()
        query = db.db_searchbar_query(conn, "recipe_ingredients")
        try:
            self.full_ingredient_list = defaultdict(list)
            for ingredient in query:
                self.full_ingredient_list[ingredient[0]].append(ingredient[1].lower())
            print(self.full_ingredient_list)

        except:
            print("Error")

    def update_ingredient_list(self):
        """

        :return:
        """
        conn = db.create_connection()
        self.recipe_list_widget.clear()
        str_input = self.search_bar_widget.text()
        if len(str_input) == 0:
            for recipe in self.full_recipe_list:
                self.recipe_list_widget.addItem(recipe[1])
            return
        str_input = str_input.split(';')
        print(str_input)

        matching_ingredients = []
        for ingredient in self.full_ingredient_list:
            found = 1
            for input in str_input:
                if input.lower() not in self.full_ingredient_list[ingredient]:
                    found = 0
                    break
            if found == 1:
                matching_ingredients.append(ingredient)
        for recipe in matching_ingredients:
            self.recipe_list_widget.addItem(db.db_query(conn, "main", "recipe_id", recipe)[0][1])

    def view_recipe(self, item):
        """
        Go to the View Recipe page
        :param item: Recipe the user selected
        :return:
        """
        print("Go to View Recipe Menu for: " + item.text())

    def add_recipe(self):
        """
        Go to the Add Recipe page
        :return:
        """
        print("Go to Add Recipe Menu")


def main():
    app = QApplication(sys.argv)
    window = ui_main_window()
    window.show()
    exit(app.exec_())


if __name__ == "__main__":
    main()
