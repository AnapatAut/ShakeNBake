"""
 main_menu.py

 Python code for UI of main menu

 Created by Anapat B., 16 Oct 2023
"""

import sys
from PyQt5.QtCore import QRect, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QWidget, QListWidget, QPushButton, QLineEdit, QApplication

import db_manager as db


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

        self.search_bar_widget = QLineEdit(self.centralwidget)
        self.search_bar_widget.setObjectName("search_bar_widget")
        self.search_bar_widget.setGeometry(QRect(80, 40, 640, 25))
        self.setCentralWidget(self.centralwidget)
        self.search_bar_widget.setPlaceholderText(
            QCoreApplication.translate("Main Menu", "Search Recipe/Ingredient"))

        self.recipe_list_widget.itemClicked.connect(self.view_recipe)

        self.add_recipe_widget.clicked.connect(self.add_recipe)

        self.get_recipe_list()
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
                self.full_recipe_list.append(recipes[1])
            print(self.full_recipe_list)
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
                            if str_input.lower() in recipe.lower()]
        for recipe in matching_recipes:
            self.recipe_list_widget.addItem(recipe)

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
