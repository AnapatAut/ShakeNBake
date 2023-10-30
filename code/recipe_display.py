"""This file gereates a window that displays the recipe of each menu item"""


import sqlite3
import datetime

import sys
import math
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont
import db_manager as db




class MainWindow(QMainWindow):
    """Generates the window"""
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Setups the UI like buttons and tables"""
        window_width = 920
        window_height = 680

        # Set the Window title (top left)
        self.setWindowTitle("Recipe")

        # Making the window
        self.setGeometry(0, 0, window_width, window_height)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        

        # The edit button
        self.edit_btn = QPushButton(self.centralwidget)
        self.edit_btn.setObjectName("EditBtn")
        self.edit_btn.setGeometry(QRect(720, 620, 80, 30))
        self.edit_btn.setText("Edit")


        # The remove button
        self.remove_btn = QPushButton(self.centralwidget)
        self.remove_btn.setObjectName("RemoveBtn")
        self.remove_btn.setGeometry(QRect(820, 620, 80, 30))
        self.remove_btn.setText("Remove")       

        # The add Note button
        self.add_note_btn = QPushButton(self.centralwidget)
        self.add_note_btn.setGeometry(QRect(700, 81 , 170, 60))
        self.add_note_btn.setObjectName("add_note_btn")
        # self.add_note_btn.setText("Add Note")
        self.add_note_btn.clicked.connect(self.get_recipe_name)


        # The notes table

        note_table_width =  170
        note_row_count = 5
        self.notes_widget = QTableWidget(self.centralwidget)
        self.notes_widget.setGeometry(QRect(700, 151, note_table_width, 261))
        self.notes_widget.setColumnCount(1)  # Set the number of columns
        self.notes_widget.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])
        self.notes_widget.setRowCount(note_row_count)  # Set the number of rows
        self.notes_widget.setColumnWidth(0, note_table_width)
        self.notes_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.notes_widget.verticalHeader().setVisible(False)
        self.notes_widget.horizontalHeader().setVisible(False)


            
        

        for row in range(5):
            notes = QTableWidgetItem(f"Ingredient {row + 1}")
            self.notes_widget.setItem(row, 0, notes)


 

        # The header text
        self.text_label = QLabel(self.centralwidget)
        self.text_label.setGeometry(QRect(35, 10, 662, 51))
        self.text_label.setText("Recipe")
        
        
        # set the colum width for the ingredient table
        table_width = 630
        ingredient_row_count = 6
        colum_wid = math.floor(table_width / 3) - 10
        self.ingredient_widget = QTableWidget(self.centralwidget)
        self.ingredient_widget.setGeometry(QRect(35, 80, table_width, 261))
        self.ingredient_widget.setColumnCount(3)  # Set the number of columns
        self.ingredient_widget.setRowCount(ingredient_row_count)  # Set the number of rows
        self.ingredient_widget.setColumnWidth(0, colum_wid)
        self.ingredient_widget.setColumnWidth(1, colum_wid)
        self.ingredient_widget.setColumnWidth(2, colum_wid)
        self.ingredient_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ingredient_widget.verticalHeader().setVisible(False)
        self.ingredient_widget.horizontalHeader().setVisible(False)

        for row in range(5):
            ingredient = QTableWidgetItem(f"Ingredient {row + 1}")
            self.ingredient_widget.setItem(row, 0, ingredient)
            ingredient = QTableWidgetItem(f"Name {row + 1}")
            self.ingredient_widget.setItem(row, 1, ingredient)
            ingredient = QTableWidgetItem(f"Amount {row + 1}")
            self.ingredient_widget.setItem(row, 2, ingredient)



        # set the colum width for the ingredient table
        step_row_count = 10
        colum_wid = table_width
        self.step_table = QTableWidget(self.centralwidget)
        self.step_table.setGeometry(QRect(35, 370, table_width, 261))
        self.step_table.setColumnCount(1)
        self.step_table.setHorizontalHeaderLabels(["Steps:", "Column 2", "Column 3"])
        self.step_table.setRowCount(step_row_count)
        self.step_table.setColumnWidth(0, colum_wid)
        self.step_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.step_table.verticalHeader().setVisible(False)


        for row in range(5):
            ingredient = QTableWidgetItem(f"Step {row + 1}")
            self.step_table.setItem(row, 0, ingredient)

        font = QFont()
        font.setPointSize(20)  # Set the font size to 14
        font.setBold(True)  # Make the text bold
        self.text_label.setFont(font)


    def window2(self):
        self.window = input_window()
        self.window.show()
        self.window.move(700, 200)

    def get_recipe_name(self):
        recipe_name = "recipe-name"
        conn = db.create_connection()
        
        curr_id = db.query_max_id(conn, "main") + 1

        db.create_task(conn, [curr_id, recipe_name], "main")
        
        print("added")


class input_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("input Window")


        inputWindow_width = 650
        inputWindow_height = 350

        self.setGeometry(0, 0, inputWindow_width, inputWindow_height)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)


def main():
    """Runs the main function"""

    
    app = QApplication(sys.argv)
    window = MainWindow()

    window.move(460, 170)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()