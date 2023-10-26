"""
 main_menu.py

 Python code for UI of main menu

 Created by Anapat B., 16 Oct 2023
"""

import sys
from PyQt5.QtCore import QRect, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QWidget, QListWidget, QPushButton, QLineEdit, QLabel, QApplication
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

        self.recipe_header = QLabel(self.centralwidget)
        self.recipe_header.setObjectName("recipe_header")
        self.recipe_header.setGeometry(100, 98, 100, 25)
        self.recipe_header.setStyleSheet("font-weight: bold")
        self.recipe_header.setText("Recipe Name")

        self.ingredient_header = QLabel(self.centralwidget)
        self.ingredient_header.setObjectName("ingredient_header")
        self.ingredient_header.setGeometry(380, 98, 140, 25)
        self.ingredient_header.setStyleSheet("font-weight: bold")
        self.ingredient_header.setText("Recipe Ingredients")

        self.ingredient_search_indicator = QLabel(self.centralwidget)
        self.ingredient_search_indicator.setObjectName("ingredient_search_indicator")
        self.ingredient_search_indicator.setGeometry(190, 60, 650, 25)

        self.recipe_list_widget = QListWidget(self.centralwidget)
        self.recipe_list_widget.setObjectName("recipe_list_widget")
        self.recipe_list_widget.setGeometry(QRect(80, 120, 280, 500))

        self.ingredient_list_widget = QListWidget(self.centralwidget)
        self.ingredient_list_widget.setObjectName("ingredient_list_widget")
        self.ingredient_list_widget.setGeometry(QRect(360, 120, 480, 500))

        self.add_recipe_widget = QPushButton(self.centralwidget)
        self.add_recipe_widget.setObjectName("add_recipe_widget")
        self.add_recipe_widget.setGeometry(QRect(760, 40, 80, 25))
        self.add_recipe_widget.setText(QCoreApplication.translate("Main Menu", "Add Recipe"))

        self.search_toggle_widget = QPushButton("Toggle", self.centralwidget)
        self.search_toggle_widget.setObjectName("search_toggle_widget")
        self.search_toggle_widget.setGeometry(QRect(80, 40, 100, 25))
        self.search_toggle_widget.setCheckable(True)
        self.search_toggle_widget.setText(QCoreApplication.translate("Main Menu", "Toggle Search"))

        self.search_confirm_widget = QPushButton(self.centralwidget)
        self.search_confirm_widget.setObjectName("add_recipe_widget")
        self.search_confirm_widget.setGeometry(QRect(660, 40, 80, 25))
        self.search_confirm_widget.setText(QCoreApplication.translate("Main Menu", "Search"))

        self.search_bar_widget = QLineEdit(self.centralwidget)
        self.search_bar_widget.setObjectName("search_bar_widget")
        self.search_bar_widget.setGeometry(QRect(190, 40, 470, 25))
        self.search_bar_widget.setMaxLength(56)
        self.setCentralWidget(self.centralwidget)

        self.toggle_search()
        self.search_toggle_widget.clicked.connect(self.toggle_search)

        self.recipe_list_widget.itemClicked.connect(self.view_recipe)

        self.add_recipe_widget.clicked.connect(self.add_recipe)

        self.update_recipe_list()

    def toggle_search(self):
        """
        Toggle search between search by recipe and ingredient
        :return:
        """
        self.get_recipe_list()
        self.search_bar_widget.clear()
        self.ingredient_search_indicator.clear()
        if self.search_toggle_widget.isChecked():
            print("Search Ingredient")
            self.search_bar_widget.setPlaceholderText(
                QCoreApplication.translate("Main Menu", "Search Ingredient (Use ';' as separator)"))
            self.search_confirm_widget.show()
            self.get_ingredient_list()
            # self.update_ingredient_list()
            # self.search_bar_widget.textChanged()
            self.search_confirm_widget.clicked.connect(self.update_ingredient_list)
        else:
            print("Search Recipe")
            self.search_bar_widget.setPlaceholderText(
                QCoreApplication.translate("Main Menu", "Search Recipe"))
            self.search_confirm_widget.hide()

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
        if self.search_toggle_widget.isChecked():
            return
        self.recipe_list_widget.clear()
        self.ingredient_list_widget.clear()
        str_input = self.search_bar_widget.text()
        print(str_input, end=" [i] main_menu.py->def update_recipe_list->str_input\n")
        matching_recipes = [recipe for recipe in self.full_recipe_list
                            if str_input.lower() in recipe[1].lower()]
        for recipe in matching_recipes:
            self.add_display_list(recipe[0])

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
            print(self.full_ingredient_list, end=" [i] main_menu.py->def get_ingredient_list->self.full_ingredient_list\n")

        except:
            print("Error")

    def update_ingredient_list(self):
        """

        :return:
        """
        self.recipe_list_widget.clear()
        self.ingredient_list_widget.clear()
        str_input = self.search_bar_widget.text()
        str_input = str_input.split(';')
        str_input = [input.lower() for input in str_input]
        for input in str_input:
            if input is str_input[0]:
                search = input
            else:
                search = search + ", " + input
        self.ingredient_search_indicator.setText("Searching for ingredients: " + search)
        print(str_input, end=" [i] main_menu.py->def update_ingredient_list->str_input\n")

        for recipe_id in self.full_ingredient_list:
            found = 0
            for input in str_input:
                if input in self.full_ingredient_list[recipe_id]:
                    found += 1
            if found == len(str_input):
                ingredients = self.full_ingredient_list[recipe_id][0]
                self.add_display_list(recipe_id)

    def add_display_list(self, recipe_id):
        ingredient_list = []
        count = 0
        conn = db.create_connection()
        self.recipe_list_widget.addItem(db.db_query(conn, "main", "recipe_id", recipe_id)[0][1])
        query = db.db_query(conn, "recipe_ingredients", "recipe_id", recipe_id)
        for ingredient in query:
            if ingredient is query[0]:
                ingredients = ingredient[1]
            else:
                ingredients = ingredients + ", " + ingredient[1]
        self.ingredient_list_widget.addItem(ingredients)

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
