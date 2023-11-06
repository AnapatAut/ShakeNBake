"""This file gereates a window that displays the recipe of each menu item"""

import sys
import math
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont
import db_manager as db




class MainWindow(QMainWindow):

    """Generates the window"""
    def __init__(self):
        super().__init__()
        self.recipe_id = 1
        self.main_data = []
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
        self.remove_btn = QPushButton(self.centralwidget)
        self.remove_btn.setObjectName("remove_tn")
        self.remove_btn.setGeometry(QRect(820, 620, 80, 30))
        self.remove_btn.setText("Remove")


        # The remove button
        self.back_btn = QPushButton(self.centralwidget)
        self.back_btn.setObjectName("back_btn")
        self.back_btn.setGeometry(QRect(720, 620, 80, 30))
        self.back_btn.setText("Back")


        # The add Note button
        self.add_note_btn = QPushButton(self.centralwidget)
        self.add_note_btn.setGeometry(QRect(700, 81 , 170, 60))
        self.add_note_btn.setObjectName("add_note_btn")
        self.add_note_btn.setText("Add/view notes")

        # The header text

        self.text_label = QLabel(self.centralwidget)
        self.text_label.setGeometry(QRect(35, 10, 662, 51))
        font = QFont()
        font.setPointSize(20)  # Set the font size to 14
        font.setBold(True)  # Make the text bold
        self.text_label.setFont(font)




    

        self.init_tables()




    def init_ingredient_table(self):
        # set the colum width for the ingredient table
        self.table_width = 630
        ingredient_row_count = 6
        colum_wid = math.floor(self.table_width / 4) + 8
        self.ingredient_table = QTableWidget(self.centralwidget)
        self.ingredient_table.setGeometry(QRect(35, 80, self.table_width, 261))
        self.ingredient_table.setColumnCount(4)
        self.ingredient_table.setColumnWidth(0, colum_wid)
        self.ingredient_table.setColumnWidth(1, colum_wid)
        self.ingredient_table.setColumnWidth(2, colum_wid)
        self.ingredient_table.verticalHeader().setVisible(False)
        self.ingredient_table.setHorizontalHeaderLabels(["ingredient number", "Ingredient", "Amount", "Unit"])
        self.ingredient_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def init_step_table(self):
        # set the colum width for the ingredient table
        step_row_count = 10
        colum_wid = 500
        self.step_table = QTableWidget(self.centralwidget)
        self.step_table.setGeometry(QRect(35, 370, self.table_width, 261))
        self.step_table.setColumnCount(2)
        self.step_table.setHorizontalHeaderLabels(["Steps:", "Column 2"])
        self.step_table.setColumnWidth(0,100)
        self.step_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.step_table.verticalHeader().setVisible(False)
        self.step_table.setColumnWidth(1, colum_wid)
        self.step_table.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def init_tables(self):
        """
        reads all the data and populate all the tables
        """
        self.init_ingredient_table()
        self.init_step_table()
        self.reading_main(self.recipe_id)
        self.reading_recipe_steps(self.recipe_id)
        self.reading_recipe_ingredient(self.recipe_id)
        if self.main_data is not None:
            self.text_label.setText(self.main_data[0][1])
        else:
            self.text_label.setText("The recipe has no name")
        self.populate_steps_table()
        self.populate_ingredient_table()
        

        


    def reading_main(self , recipe_id):
        """
        Reads all the data in recipe_steps and prints it out
        """
        conn = db.create_connection()
        self.main_data = db.db_query(conn, "main", "recipe_id", recipe_id)

    def reading_recipe_steps(self , recipe_id):
        """
        Reads all the data in recipe_steps and prints it out
        """
        conn = db.create_connection()
        self.steps_data = db.db_query(conn, "recipe_steps", "recipe_id", recipe_id)


    def populate_steps_table(self):
        """
        This read the db on recipe_steps and populate the corrisponding table with the data
        """
        if self.steps_data is not None:
            self.num_steps = len(self.steps_data)
        else:
            self.num_steps = 0
        self.step_table.setRowCount(self.num_steps)
        for row in range(self.num_steps):
            step_number = QTableWidgetItem(f"{self.steps_data[row][1]}")
            step_number.setTextAlignment(Qt.AlignCenter)
            self.step_table.setItem(row, 0, step_number)
            step_instrution = QTableWidgetItem(f"{self.steps_data[row][2]}")
            self.step_table.setItem(row, 1, step_instrution)
            

    def reading_recipe_ingredient(self , recipe_id):
        """
        Reads all the data in recipe_ingredient and prints it out
        """
        conn = db.create_connection()
        self.ingredient_data = db.db_query(conn, "recipe_ingredients", "recipe_id", recipe_id)

    def populate_ingredient_table(self):
        """
        This func populates the ingredient list tables
        """
        if self.ingredient_data is not None:
            self.ingredient_row = len(self.ingredient_data)
        else:
            self.ingredient_row = 0
        self.ingredient_table.setRowCount(self.ingredient_row)
        for row in range(self.ingredient_row):
            ingredient_number = QTableWidgetItem(f"{row + 1}")
            ingredient_number.setTextAlignment(Qt.AlignCenter)
            self.ingredient_table.setItem(row, 0, ingredient_number)
            ingredient_name = QTableWidgetItem(f"{self.ingredient_data[row][1]}")
            self.ingredient_table.setItem(row, 1, ingredient_name)
            ingredient_amount = QTableWidgetItem(f"{self.ingredient_data[row][2]}")
            self.ingredient_table.setItem(row, 2, ingredient_amount)
            ingredient_unit = QTableWidgetItem(f"{self.ingredient_data[row][3]}")
            self.ingredient_table.setItem(row, 3, ingredient_unit)

    def clear_all_data(self):
        """
        clears all the data in preperation for another set of data 
        """
        self.step_table.clear()
        self.ingredient_table.clear()
        self.text_label.clear()


class input_window(QMainWindow):
    """
    
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("input Window")


        input_window_width = 650
        input_window_height = 350

        self.setGeometry(0, 0, input_window_width, input_window_height)
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
