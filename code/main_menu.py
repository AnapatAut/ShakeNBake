# main_menu.py
#
# Python code for UI of main menu
#
# Created by Anapat B., 16 Oct 2023


import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import db_manager as db


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Main Menu")
        self.setGeometry(0, 0, 920, 680)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"central_widget")
        self.setCentralWidget(self.centralwidget)

        self.recipe_list_widget = QListWidget(self.centralwidget)
        self.recipe_list_widget.setObjectName(u"recipe_list_widget")
        self.recipe_list_widget.setGeometry(QRect(80, 80, 760, 500))

        self.recipe_list_widget.itemClicked.connect(self.view_recipe)

        self.add_recipe_widget = QPushButton(self.centralwidget)
        self.add_recipe_widget.setObjectName(u"add_recipe_widget")
        self.add_recipe_widget.setGeometry(QRect(760, 40, 80, 25))

        self.add_recipe_widget.clicked.connect(self.add_recipe)

        self.search_bar_widget = QLineEdit(self.centralwidget)
        self.search_bar_widget.setObjectName(u"search_bar_widget")
        self.search_bar_widget.setGeometry(QRect(80, 40, 640, 25))
        self.setCentralWidget(self.centralwidget)

        self.get_recipe_list()
        self.update_recipe_list()
        self.search_bar_widget.textChanged.connect(self.update_recipe_list)

        self.retranslateUi(self)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.add_recipe_widget.setText(QCoreApplication.translate("MainWindow", u"Add Recipe", None))
        self.search_bar_widget.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"Search Recipe/Ingredient", None))

    # retranslateUi

    def get_recipe_list(self):
        conn = db.create_connection()
        query = db.db_searchbar_query(conn, "main")
        self.full_recipe_list = []
        for recipes in query:
            self.full_recipe_list.append(recipes[1])
        print(self.full_recipe_list)

    def update_recipe_list(self):

        str_input = self.search_bar_widget.text()
        self.recipe_list_widget.clear()
        print(str_input)
        matching_recipes = [recipe for recipe in self.full_recipe_list if str_input.lower() in recipe.lower()]
        for recipe in matching_recipes:
            self.recipe_list_widget.addItem(recipe)

    # Go to the View Recipe page
    def view_recipe(self, item):
        print("Go to View Recipe Menu for: " + item.text())

    # Go to Add Recipe page
    def add_recipe(self):
        print("Go to Add Recipe Menu")


def main():
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    exit(app.exec_())


if __name__ == "__main__":
    main()
