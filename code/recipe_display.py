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
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont
import db_manager as db




class MainWindow(QMainWindow):
    """Generates the window"""
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """
        Setups the UI like buttons and tables
        """
        window_width = 920
        window_height = 680

        # Set the Window title (top left)
        self.setWindowTitle("Recipe Display")

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
        location = "recipe_display"
        self.remove_btn = QPushButton(self.centralwidget)
        self.remove_btn.setObjectName("push")
        self.remove_btn.setGeometry(QRect(820, 620, 80, 30))
        self.remove_btn.setText("Remove")       
        # self.remove_btn.clicked.connect(self.remove_from_step_list)

        # The add Note button
        self.add_note_btn = QPushButton(self.centralwidget)
        self.add_note_btn.setGeometry(QRect(700, 81 , 170, 60))
        self.add_note_btn.setObjectName("add_note_btn")
        self.add_note_btn.setText("Add notes")
        self.add_note_btn.clicked.connect(self.reading_recipe_steps)


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
        colum_wid = math.floor(table_width / 4) + 8
        self.ingredient_widget = QTableWidget(self.centralwidget)
        self.ingredient_widget.setGeometry(QRect(35, 80, table_width, 261))
        self.ingredient_widget.setColumnCount(4)  # Set the number of columns
        self.ingredient_widget.setRowCount(ingredient_row_count)  # Set the number of rows
        self.ingredient_widget.setHorizontalHeaderLabels(["Ingredient Number", "Ingredient", "amount", "Unit"])
        self.ingredient_widget.setColumnWidth(0, colum_wid)
        self.ingredient_widget.setColumnWidth(1, colum_wid)
        self.ingredient_widget.setColumnWidth(2, colum_wid)
        self.ingredient_widget.verticalHeader().setVisible(False)
        self.reading_recipe_ingredient()
        self.populate_ingredient_table()




        # set the colum width for the ingredient table
        step_row_count = 10
        colum_wid = 500
        self.step_table = QTableWidget(self.centralwidget)
        self.step_table.setGeometry(QRect(35, 370, table_width, 261))
        self.step_table.setColumnCount(2)
        self.step_table.setHorizontalHeaderLabels(["Steps:", "Column 2"])
        self.step_table.setRowCount(step_row_count)
        self.step_table.setColumnWidth(0,100)
        self.step_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.step_table.verticalHeader().setVisible(False)
        self.step_table.setColumnWidth(1, colum_wid)
        self.reading_recipe_steps()
        self.populate_steps_table()
    

        font = QFont()
        font.setPointSize(20)  # Set the font size to 14
        font.setBold(True)  # Make the text bold
        self.text_label.setFont(font)

    def pushing_recipe_steps(self):
        """
        Adds an entry to the recipe_steps database
        """
        conn = db.create_connection()
        
        curr_id = db.query_max_id(conn, "recipe_steps") + 1

        task = (curr_id ,curr_id , "task")

        db.create_task(conn, task, "recipe_steps")
        
        print("added")


    def populate_steps_table(self):
        """
        This read the db on recipe_steps and populate the corrisponding table with the data
        """
        num_steps = len(self.steps_data)
        for row in range(num_steps):
            step_number = QTableWidgetItem(f"{self.steps_data[row][1]}")
            step_number.setTextAlignment(Qt.AlignCenter)
            self.step_table.setItem(row, 0, step_number)
            step_instrution = QTableWidgetItem(f"{self.steps_data[row][2]}")
            self.step_table.setItem(row, 1, step_instrution)


    def reading_recipe_steps(self):
        """
        Reads all the data in recipe_steps and prints it out
        """
        conn = db.create_connection()
        self.steps_data = db.db_query_table(conn, "recipe_steps")
        
    def reading_recipe_ingredient(self):
        """
        Reads all the data in recipe_ingredient and prints it out
        """
        conn = db.create_connection()
        self.ingredient_data = db.db_query_table(conn, "recipe_ingredients")

    def populate_ingredient_table(self):
        """
        This func populates the ingredient list tables
        """
        ingredient_row = len(self.ingredient_data)
        for row in range(ingredient_row):
            ingredient_number = QTableWidgetItem(f"{row + 1}")
            ingredient_number.setTextAlignment(Qt.AlignCenter)
            self.ingredient_widget.setItem(row, 0, ingredient_number)
            
            ingredient_name = QTableWidgetItem(f"{self.ingredient_data[row][1]}")
            self.ingredient_widget.setItem(row, 1, ingredient_name)
            
            ingredient_amount = QTableWidgetItem(f"{self.ingredient_data[row][2]}")
            self.ingredient_widget.setItem(row, 2, ingredient_amount)
            
            ingredient_unit = QTableWidgetItem(f"{self.ingredient_data[row][3]}")
            self.ingredient_widget.setItem(row, 3, ingredient_unit)

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