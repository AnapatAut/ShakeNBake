"""This file gereates a window that displays the recipe of each menu item"""

import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont


class MainWindow(QMainWindow):
    """Generates the window"""
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Setups the UI like buttons and tables"""
        table_width = 920
        table_height = 680
        self.setGeometry(0, 0, table_width, table_height)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        self.edit_btn = QPushButton(self.centralwidget)
        self.edit_btn.setObjectName("EditBtn")
        self.edit_btn.setGeometry(QRect(720, 620, 80, 30))

        self.remove_btn = QPushButton(self.centralwidget)
        self.remove_btn.setObjectName("RemoveBtn")
        self.remove_btn.setGeometry(QRect(820, 620, 80, 30))

        self.text_label = QLabel(self.centralwidget)
        self.text_label.setGeometry(QRect(35, 10, 662, 51))
        self.text_label.setText("Recipe")

        colum_len = math.floor(table_width / 3)
        self.ingredient_widget = QTableWidget(self.centralwidget)
        self.ingredient_widget.setGeometry(QRect(35, 80, 662, 261))
        self.ingredient_widget.setColumnCount(3)  # Set the number of columns
        self.ingredient_widget.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])
        self.ingredient_widget.setRowCount(20)  # Set the number of rows
        self.ingredient_widget.setColumnWidth(0, colum_len)

        for row in range(5):
            ingredient = QTableWidgetItem(f"Ingredient {row + 1}")
            self.ingredient_widget.setItem(row, 0, ingredient)
            ingredient = QTableWidgetItem(f"Name {row + 1}")
            self.ingredient_widget.setItem(row, 1, ingredient)
            ingredient = QTableWidgetItem(f"Amount {row + 1}")
            self.ingredient_widget.setItem(row, 2, ingredient)


        self.table_widget = QTableWidget(self.centralwidget)
        self.table_widget.setGeometry(QRect(35, 370, 662, 261))
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Steps:", "Column 2", "Column 3"])
        self.table_widget.setRowCount(20)
        self.table_widget.setColumnWidth(0, colum_len)

        for row in range(5):
            ingredient = QTableWidgetItem(f"Step {row + 1}")
            self.table_widget.setItem(row, 0, ingredient)
            ingredient = QTableWidgetItem(f"Name {row + 1}")
            self.table_widget.setItem(row, 1, ingredient)
            ingredient = QTableWidgetItem(f"Amount {row + 1}")
            self.table_widget.setItem(row, 2, ingredient)

        font = QFont()
        font.setPointSize(20)  # Set the font size to 14
        font.setBold(True)  # Make the text bold
        self.text_label.setFont(font)


        self.retranslate_ui()





    def retranslate_ui(self):
        """Set the names of title and buttons"""
        self.setWindowTitle("Recipe")
        self.edit_btn.setText("Edit")
        self.remove_btn.setText("Remove")

def main():
    """Runs the main function"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
