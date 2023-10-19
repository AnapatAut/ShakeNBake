import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont
import math

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        tableWidth = 920
        tableHeight = 920
        self.setGeometry(0, 0, tableWidth, tableHeight)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")
        self.setCentralWidget(self.centralwidget)

        self.EditBtn = QPushButton(self.centralwidget)
        self.EditBtn.setObjectName(u"EditBtn")
        self.EditBtn.setGeometry(QRect(720, 620, 80, 30))

        self.RemoveBtn = QPushButton(self.centralwidget)
        self.RemoveBtn.setObjectName(u"RemoveBtn")
        self.RemoveBtn.setGeometry(QRect(820, 620, 80, 30))

        self.textLabel = QLabel(self.centralwidget)
        self.textLabel.setGeometry(QRect(35, 10, 662, 51))
        self.textLabel.setText("Recipe")

        # Create a table widget

        colum_len = math.floor(tableWidth / 3)
        self.IngredientWidget = QTableWidget(self.centralwidget)
        self.IngredientWidget.setGeometry(QRect(35, 80, 662, 261))
        self.IngredientWidget.setColumnCount(3)  # Set the number of columns
        self.IngredientWidget.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])  # Set column headers
        self.IngredientWidget.setRowCount(20)  # Set the number of rows
        self.IngredientWidget.setColumnWidth(0, colum_len)

        for row in range(5):
            ingredient = QTableWidgetItem(f"Ingredient {row + 1}")
            self.IngredientWidget.setItem(row, 0, ingredient)
            ingredient = QTableWidgetItem(f"Name {row + 1}")
            self.IngredientWidget.setItem(row, 1, ingredient)
            ingredient = QTableWidgetItem(f"Amount {row + 1}")
            self.IngredientWidget.setItem(row, 2, ingredient)
        
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QRect(35, 370, 662, 261))
        self.tableWidget.setColumnCount(3)  # Set the number of columns
        self.tableWidget.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])  # Set column headers
        self.tableWidget.setRowCount(20)  # Set the number of rows
        self.tableWidget.setColumnWidth(0, colum_len)

        for row in range(5):
            ingredient = QTableWidgetItem(f"Step {row + 1}")
            self.IngredientWidget.setItem(row, 0, ingredient)
            ingredient = QTableWidgetItem(f"Name {row + 1}")
            self.IngredientWidget.setItem(row, 1, ingredient)
            ingredient = QTableWidgetItem(f"Amount {row + 1}")
            self.IngredientWidget.setItem(row, 2, ingredient)

        
        font = QFont()
        font.setPointSize(20)  # Set the font size to 14
        font.setBold(True)  # Make the text bold
        self.textLabel.setFont(font)


        for row in range(5):
            ingredient = QTableWidgetItem(f"Ingredient {row + 1}")
            self.IngredientWidget.setItem(row, 0, ingredient)
            ingredient = QTableWidgetItem(f"Name {row + 1}")
            self.IngredientWidget.setItem(row, 1, ingredient)
            ingredient = QTableWidgetItem(f"Amount {row + 1}")
            self.IngredientWidget.setItem(row, 2, ingredient)

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle("Recipe")
        self.EditBtn.setText("Edit")
        self.RemoveBtn.setText("Remove")

def main():
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
