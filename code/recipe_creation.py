# recipe_creation.py
#
# Both the UI and top level logic for the recipe creation page
#
# Created by Inkaphol S., 11 Oct 2023
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect, QLocale, Qt
from PyQt5.QtGui import QFont
import db_manager as db

# the recipe_creation_window
class Ui_MainWindow(QMainWindow):
    def __init__(self):
        self.ingredient_table_data = []
        self.valid_ingredients = []
        self.used_ingredients = []
        super().__init__()
        self.setupui()

    # sets up the page format along with the creation of the page's widgets
    def setupui(self):
        self.setWindowTitle('Recipe Creation')
        self.setGeometry(100, 100, 920, 680)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        prompt_font = QFont()
        prompt_font.setFamily("Verdana")
        prompt_font.setPointSize(12)

        error_font = QFont()
        error_font.setFamily("Verdana")
        error_font.setPointSize(10)

        self.recipe_name_prompt = QLabel(self.centralwidget)
        self.recipe_name_prompt.setObjectName("recipe_name_prompt")
        self.recipe_name_prompt.setGeometry(QRect(30, 30, 91, 41))
        self.recipe_name_prompt.setFont(prompt_font)
        self.recipe_name_prompt.setText("Name:")

        self.recipe_name_error = QLabel(self.centralwidget)
        self.recipe_name_error.setObjectName("recipe_name_error")
        self.recipe_name_error.setGeometry(QRect(720, 15, 141, 71))
        self.recipe_name_error.setFont(prompt_font)
        self.recipe_name_error.setStyleSheet("color: red;")

        self.recipe_name_in = QTextEdit(self.centralwidget)
        self.recipe_name_in.setObjectName("recipe_name_in")
        self.recipe_name_in.setGeometry(QRect(180, 35, 371, 31))
        self.recipe_name_in.setPlaceholderText("Enter an Recipe Name")

        self.ingredient_prompt = QLabel(self.centralwidget)
        self.ingredient_prompt.setObjectName("ingredient_prompt")
        self.ingredient_prompt.setGeometry(QRect(30, 60, 141, 71))
        self.ingredient_prompt.setFont(prompt_font)

        self.ingredient_error = QLabel(self.centralwidget)
        self.ingredient_error.setObjectName("ingredient_error")
        self.ingredient_error.setGeometry(QRect(720, 64, 141, 71))
        self.ingredient_error.setFont(prompt_font)
        self.ingredient_error.setStyleSheet("color: red;")

        self.ingredient_name_in = QTextEdit(self.centralwidget)
        self.ingredient_name_in.setObjectName("ingredient_name_in")
        self.ingredient_name_in.setGeometry(QRect(180, 81, 171, 31))
        self.ingredient_name_in.mousePressEvent = self.ingredient_name_in_click
        self.ingredient_name_in.textChanged.connect(self.update_suggestions)

        self.suggestion_list = QListWidget(self.centralwidget)
        self.suggestion_list.setGeometry(QRect(180, 111, 171, 160))
        self.suggestion_list.itemClicked.connect(self.select_suggestion)
        self.suggestion_list.hide()

        self.ingredient_amount_in = QDoubleSpinBox(self.centralwidget)
        self.ingredient_amount_in.setObjectName("ingredient_amount_in")
        self.ingredient_amount_in.setGeometry(QRect(350, 81, 81, 31))
        self.ingredient_amount_in.setDecimals(1)
        self.ingredient_amount_in.setMaximum(9999.0)
        self.ingredient_amount_in.setMinimum(0.5)
        self.ingredient_amount_in.setSingleStep(0.50)
        self.ingredient_amount_in.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        self.ingredient_unit_in = QComboBox(self.centralwidget)
        self.ingredient_unit_in.addItem("Grams")
        self.ingredient_unit_in.addItem("Milligrams")
        self.ingredient_unit_in.addItem("Kilogram")
        self.ingredient_unit_in.addItem("Tablespoon(s)")
        self.ingredient_unit_in.addItem("Teaspoon(s)")
        self.ingredient_unit_in.addItem("none")
        self.ingredient_unit_in.setObjectName("ingredient_measurement")
        self.ingredient_unit_in.setGeometry(QRect(428, 81, 121, 31))
        self.ingredient_unit_in.setAutoFillBackground(False)

        self.ingredient_table = QTableWidget(self.centralwidget)
        if (self.ingredient_table.columnCount() < 3):
            self.ingredient_table.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.ingredient_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.ingredient_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.ingredient_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)

        self.ingredient_table.setObjectName("ingredient_table")
        self.ingredient_table.setGeometry(QRect(180, 120, 371, 161))
        self.ingredient_table_header = self.ingredient_table.horizontalHeader()
        self.ingredient_table_header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.ingredient_table_header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ingredient_table_header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.ingredient_table.setSelectionMode(QTableWidget.SingleSelection)
        self.ingredient_table.setSelectionBehavior(QTableWidget.SelectRows)

        self.add_ingredient = QPushButton(self.centralwidget)
        self.add_ingredient.setObjectName("add_ingredient")
        self.add_ingredient.setGeometry(QRect(560, 80, 151, 41))
        self.add_ingredient.clicked.connect(self.add_to_ingredient_table)

        self.remove_ingredient = QPushButton(self.centralwidget)
        self.remove_ingredient.setObjectName("remove_ingredient")
        self.remove_ingredient.setGeometry(QRect(560, 130, 151, 41))
        self.remove_ingredient.clicked.connect(self.remove_from_ingredient_table)

        self.step_prompt = QLabel(self.centralwidget)
        self.step_prompt.setObjectName("step_prompt")
        self.step_prompt.setGeometry(QRect(30, 290, 111, 31))
        self.step_prompt.setFont(prompt_font)

        self.step_error = QLabel(self.centralwidget)
        self.step_error.setObjectName("step_error")
        self.step_error.setGeometry(QRect(720, 350, 141, 71))
        self.step_error.setFont(prompt_font)
        self.step_error.setStyleSheet("color: red;")

        self.step_in = QTextEdit(self.centralwidget)
        self.step_in.setObjectName("step_in")
        self.step_in.setGeometry(QRect(180, 290, 371, 81))

        self.step_list = QListWidget(self.centralwidget)
        self.step_list.setObjectName("step_list")
        self.step_list.setGeometry(QRect(180, 380, 371, 211))

        self.add_step = QPushButton(self.centralwidget)
        self.add_step.setObjectName("add_step")
        self.add_step.setGeometry(QRect(570, 290, 151, 41))
        self.add_step.clicked.connect(self.add_to_step_list)

        self.remove_step = QPushButton(self.centralwidget)
        self.remove_step.setObjectName("remove_step")
        self.remove_step.setGeometry(QRect(570, 340, 151, 41))
        self.remove_step.clicked.connect(self.remove_from_step_list)

        self.confirm_btn = QPushButton(self.centralwidget)
        self.confirm_btn.setObjectName("confirm_btn")
        self.confirm_btn.setGeometry(QRect(570, 590, 151, 41))
        self.confirm_btn.setText("Confirm")

        self.ingredient_table.raise_()
        self.recipe_name_in.raise_()
        self.confirm_btn.raise_()
        self.recipe_name_prompt.raise_()
        self.ingredient_prompt.raise_()
        self.add_ingredient.raise_()
        self.remove_ingredient.raise_()
        self.step_prompt.raise_()
        self.step_in.raise_()
        self.ingredient_amount_in.raise_()
        self.ingredient_unit_in.raise_()
        self.ingredient_name_in.raise_()
        self.step_in.raise_()
        self.add_step.raise_()
        self.remove_step.raise_()
        self.suggestion_list.raise_()
        self.ingredient_error.raise_()
        self.step_error.raise_()
        self.recipe_name_error.raise_()
        self.name_ui()

    # sets the display text for each of the widgets
    def name_ui(self):
        self.recipe_name_error.setText("NO ERROR")
        self.ingredient_prompt.setText("Ingredient(s):")
        self.ingredient_error.setText("NO ERROR")
        self.step_error.setText("NO ERROR")
        self.ingredient_name_in.setPlaceholderText("Enter an Ingredient Name")
        self.add_ingredient.setText("Add Ingredient")
        self.remove_ingredient.setText("Remove Ingredient")
        self.step_prompt.setText("Step(s):")
        ___qtablewidgetitem = self.ingredient_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText("Name")
        ___qtablewidgetitem1 = self.ingredient_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText("Amount")
        ___qtablewidgetitem2 = self.ingredient_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText("Unit")

        self.step_in.setPlaceholderText("Enter Your Receipe Steps Here One by One")
        self.add_step.setText("Add Step")
        self.remove_step.setText("Remove Step")

    # formats input text, used for steps
    def format_text(self, in_string, line_length):
        common_symbols = ['.', ',', '?', '!', ';', ':', '-', "'", '"', '(', ')', '[', ']',
                          '{', '}', '&', '@', '#', '$', '%', '^', '*', '+', '-', '=', '>', '<']
        out_string = ""
        curr_line = ""
        line_num = 1

        for i in range(len(in_string)):
            if (in_string[i - 1].isalnum() or in_string[i - 1] in common_symbols) and in_string[i] == ' ':

                if int(len(curr_line) / line_length) >= line_num:
                    out_string += curr_line + "\n"
                    curr_line = ""
                    line_num += 1
                    continue

            if (in_string[i].isalnum()) or (in_string[i] in common_symbols) or (in_string[i] == ' '):
                curr_line += in_string[i]

        if curr_line:
            out_string += curr_line

        return out_string

    # adds the text within step_in into the all_steps
    def add_to_step_list(self):
        formatted_text = self.format_text(self.step_in.toPlainText(), 60)
        if formatted_text:
            self.step_list.addItem(formatted_text)
            self.step_in.clear()

    # removes the selected item from the list table all_steps
    def remove_from_step_list(self):
        selected_items = self.step_list.selectedItems()
        for item in selected_items:
            self.step_list.takeItem(self.step_list.row(item))

    # pulls the list of valid ingredients from the database
    def update_valid_ingredients(self):
        conn = db.create_connection()
        query_out = db.db_searchbar_query(conn, "ingredient_list")

        self.valid_ingredients = []
        for item in query_out:
            if item[1] not in self.used_ingredients:
                self.valid_ingredients.append(item[1])

    # updates the suggestion list according to the ingredient_name_in
    def update_suggestions(self):

        in_string = self.ingredient_name_in.toPlainText()
        self.suggestion_list.clear()

        matching_suggestions = [suggestion for suggestion in self.valid_ingredients if in_string.lower() in suggestion.lower()]

        if matching_suggestions and self.ingredient_name_in.toPlainText() != "":
            for suggestion in matching_suggestions:
                self.suggestion_list.addItem(suggestion)
            self.suggestion_list.show()
        else:
            self.suggestion_list.hide()

    # transfer the selected suggestion to the ingredient_name_in field
    def select_suggestion(self):
        selected_suggestion = self.suggestion_list.currentItem()

        if selected_suggestion:
            self.ingredient_name_in.setText(selected_suggestion.text())

        self.suggestion_list.hide()

    def ingredient_name_in_click(self, event):
        self.ingredient_name_in.clear()
        if event.button() == Qt.LeftButton:
            self.update_valid_ingredients()

    def update_ingredient_table(self):
        self.ingredient_table.insertRow(self.ingredient_table.rowCount())
        for row in range(len(self.ingredient_table_data)):
            for col in range(len(self.ingredient_table_data[row])):
                item = QTableWidgetItem(self.ingredient_table_data[row][col])
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.ingredient_table.setItem(row, col, item)

    def add_to_ingredient_table(self):

        new_ingredient = self.ingredient_name_in.toPlainText().replace('\n', '')
        new_amount = str(self.ingredient_amount_in.value())
        new_unit = self.ingredient_unit_in.currentText()

        if len(new_ingredient) < 1:
            return

        new_ingredient = new_ingredient.capitalize()
        if new_ingredient not in self.valid_ingredients:
            return

        self.ingredient_table_data.append([new_ingredient, new_amount, new_unit])
        self.used_ingredients.append(new_ingredient)
        self.update_ingredient_table()
        self.ingredient_name_in.clear()

    def remove_from_ingredient_table(self):
        selected_row = -1
        selected_row = self.ingredient_table.currentRow()
        print(selected_row)
        if selected_row != -1:
            self.ingredient_table.removeRow(selected_row)



def main():
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()