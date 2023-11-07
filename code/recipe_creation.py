"""
 recipe_creation.py

 Both the UI and logic for the recipe creation page

 Created by Inkaphol S., 11 Oct 2023
"""
import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QTextEdit, QListWidget, \
    QDoubleSpinBox, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, \
    QApplication
from PyQt5.QtCore import QRect, QLocale, Qt
from PyQt5.QtGui import QFont
import db_manager as db

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        self.ingredient_table_data = []
        self.valid_ingredients = []
        self.used_ingredients = []
        super().__init__()
        self.setupui()

    def setupui(self):
        """
        sets up the user interface
        :return:
        """
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
        error_font.setPointSize(8)

        self.recipe_name_prompt = QLabel(self.centralwidget)
        self.recipe_name_prompt.setObjectName("recipe_name_prompt")
        self.recipe_name_prompt.setGeometry(QRect(30, 30, 91, 41))
        self.recipe_name_prompt.setFont(prompt_font)
        self.recipe_name_prompt.setText("Name:")

        self.recipe_name_error = QLabel(self.centralwidget)
        self.recipe_name_error.setObjectName("recipe_name_error")
        self.recipe_name_error.setGeometry(QRect(725, 15, 175, 71))
        self.recipe_name_error.setFont(error_font)
        self.recipe_name_error.setStyleSheet("color: red;")
        self.recipe_name_error.hide()

        self.recipe_name_in = QTextEdit(self.centralwidget)
        self.recipe_name_in.setObjectName("recipe_name_in")
        self.recipe_name_in.setGeometry(QRect(180, 35, 371, 31))
        self.recipe_name_in.setPlaceholderText("Enter an Recipe Name")

        self.ingredient_prompt = QLabel(self.centralwidget)
        self.ingredient_prompt.setObjectName("ingredient_prompt")
        self.ingredient_prompt.setGeometry(QRect(30, 60, 141, 71))
        self.ingredient_prompt.setFont(prompt_font)
        self.ingredient_prompt.setText("Ingredient(s):")

        self.ingredient_error = QLabel(self.centralwidget)
        self.ingredient_error.setObjectName("ingredient_error")
        self.ingredient_error.setGeometry(QRect(725, 64, 175, 71))
        self.ingredient_error.setFont(error_font)
        self.ingredient_error.setStyleSheet("color: red;")
        self.ingredient_error.hide()


        self.ingredient_name_in = QTextEdit(self.centralwidget)
        self.ingredient_name_in.setObjectName("ingredient_name_in")
        self.ingredient_name_in.setGeometry(QRect(180, 81, 171, 31))
        self.ingredient_name_in.mousePressEvent = self.ingredient_name_in_click
        self.ingredient_name_in.setPlaceholderText("Enter an Ingredient Name")
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

        ___qtablewidgetitem = self.ingredient_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText("Name")
        ___qtablewidgetitem1 = self.ingredient_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText("Amount")
        ___qtablewidgetitem2 = self.ingredient_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText("Unit")

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
        self.add_ingredient.setText("Add Ingredient")
        self.add_ingredient.clicked.connect(self.add_to_ingredient_table)

        self.remove_ingredient = QPushButton(self.centralwidget)
        self.remove_ingredient.setObjectName("remove_ingredient")
        self.remove_ingredient.setGeometry(QRect(560, 130, 151, 41))
        self.remove_ingredient.setText("Remove Ingredient")
        self.remove_ingredient.clicked.connect(self.remove_from_ingredient_table)

        self.step_prompt = QLabel(self.centralwidget)
        self.step_prompt.setObjectName("step_prompt")
        self.step_prompt.setGeometry(QRect(30, 290, 111, 31))
        self.step_prompt.setFont(prompt_font)
        self.step_prompt.setText("Step(s):")

        self.step_error = QLabel(self.centralwidget)
        self.step_error.setObjectName("step_error")
        self.step_error.setGeometry(QRect(725, 275, 175, 71))
        self.step_error.setFont(error_font)
        self.step_error.setStyleSheet("color: red;")
        self.step_error.hide()

        self.step_in = QTextEdit(self.centralwidget)
        self.step_in.setObjectName("step_in")
        self.step_in.setGeometry(QRect(180, 290, 371, 81))
        self.step_in.setPlaceholderText("Enter Your Receipe Steps Here One by One")

        self.step_list = QListWidget(self.centralwidget)
        self.step_list.setObjectName("step_list")
        self.step_list.setGeometry(QRect(180, 380, 371, 211))

        self.add_step = QPushButton(self.centralwidget)
        self.add_step.setObjectName("add_step")
        self.add_step.setGeometry(QRect(570, 290, 151, 41))
        self.add_step.setText("Add Step")
        self.add_step.clicked.connect(self.add_to_step_list)

        self.remove_step = QPushButton(self.centralwidget)
        self.remove_step.setObjectName("remove_step")
        self.remove_step.setGeometry(QRect(570, 340, 151, 41))
        self.remove_step.setText("Remove Step")
        self.remove_step.clicked.connect(self.remove_from_step_list)

        self.confirm_btn = QPushButton(self.centralwidget)
        self.confirm_btn.setObjectName("confirm_btn")
        self.confirm_btn.setGeometry(QRect(570, 610, 151, 41))
        self.confirm_btn.setText("Confirm")
        self.name_status, self.ingredient_status, self.step_status = 0, 0, 0
        self.confirm_btn.clicked.connect(self.validate_and_add_new_recipe)


        self.cancel_btn = QPushButton(self.centralwidget)
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.setGeometry(QRect(400, 610, 151, 41))
        self.cancel_btn.setText("Cancel")

    def format_text(self, in_string, line_length):
        """
        Takes in an input string, the string is then segmented and cleared of any invalid symbols
        :param in_string: an input string
        :param line_length: denotes how many characters are wanted on one line of text
        :return:
        """
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

    def update_valid_ingredients(self):
        """
        Creating a list of valid ingredients by querying the database for all ingredients
        then taking out the used ingredients
        :return:
        """
        conn = db.create_connection()
        query_out = db.db_query_table(conn, "ingredient_list")

        self.valid_ingredients = []
        for item in query_out:
            if item[1] not in self.used_ingredients:
                self.valid_ingredients.append(item[1])

    def update_suggestions(self):
        """
        Updating the list that provides the user with ingredient suggestions
        :return:
        """

        in_string = self.ingredient_name_in.toPlainText()
        self.suggestion_list.clear()

        matching_suggestions = [suggestion for suggestion in self.valid_ingredients if in_string.lower() in suggestion.lower()]

        if matching_suggestions and self.ingredient_name_in.toPlainText() != "":
            for suggestion in matching_suggestions:
                self.suggestion_list.addItem(suggestion)
            self.suggestion_list.show()
        else:
            self.suggestion_list.hide()

    def select_suggestion(self):
        """
        Transferring the selected ingredient suggestion to the ingredient input field
        :return:
        """
        selected_suggestion = self.suggestion_list.currentItem()

        if selected_suggestion:
            self.ingredient_name_in.setText(selected_suggestion.text())

        self.suggestion_list.hide()

    def ingredient_name_in_click(self, event):
        """
        Connects the update_valid_ingredient function with the moment when the user
        clicks the ingredient_name_in
        :param event: the current user's input
        :return:
        """
        self.ingredient_name_in.clear()
        if event.button() == Qt.LeftButton:
            self.update_valid_ingredients()

    def update_ingredient_table(self):
        """
        Updating the ingredient_table using the 2D ingredient_table_data
        :return:
        """
        for row in range(len(self.ingredient_table_data)):
            for col in range(len(self.ingredient_table_data[row])):
                item = QTableWidgetItem(self.ingredient_table_data[row][col])
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.ingredient_table.setItem(row, col, item)

    def add_to_ingredient_table(self):
        """
        Adding the new ingredient to the ingredient_table, table_data, and the used_ingredients list
        :return:
        """
        new_ingredient = self.ingredient_name_in.toPlainText()
        new_amount = str(self.ingredient_amount_in.value())
        new_unit = self.ingredient_unit_in.currentText()

        if len(new_ingredient) < 1:
            return

        new_ingredient = new_ingredient.capitalize()
        if new_ingredient not in self.valid_ingredients:
            return

        self.ingredient_table.insertRow(self.ingredient_table.rowCount())
        self.ingredient_table_data.append([new_ingredient, new_amount, new_unit])
        self.used_ingredients.append(new_ingredient)
        self.update_ingredient_table()
        self.ingredient_name_in.clear()

    def remove_from_ingredient_table(self):
        """
        Removing the selected row from both the table, table_data, and the used_ingredients
        :return:
        """
        selected_row = self.ingredient_table.currentRow()

        print("Row: " + str(selected_row))
        if selected_row > -1:
            curr_name = self.ingredient_table.item(selected_row, 0).text()

            print("Active Ingredients: " + str(self.ingredient_table_data))
            print("To be Removed: " + curr_name)
            self.ingredient_table.removeRow(selected_row)
            self.ingredient_table_data.pop(selected_row)
            self.used_ingredients.remove(curr_name)

            self.update_ingredient_table()
            print("Active Ingredients: " + str(self.ingredient_table_data) + "\n\n\n")

    def add_to_step_list(self):
        """
        Adding the string from step_in to the step_list
        :return:
        """
        formatted_text = self.format_text(self.step_in.toPlainText(), 60)
        if formatted_text:
            self.step_list.addItem(formatted_text)
            self.step_in.clear()

    def remove_from_step_list(self):
        """
        Removing the selected step from step_list
        :return:
        """
        selected_items = self.step_list.selectedItems()
        for item in selected_items:
            self.step_list.takeItem(self.step_list.row(item))

    def validate_and_add_new_recipe(self):
        """
        Validating the name, ingredients, and steps field, then adding the information
        to the database if all three are valid
        :return:
        """
        error_status = {0: "", 1: "No Chars/Items", 2: "Too Many Chars/Items", 3: "Only Alphabets and Spaces", 4: "Duplicate Name Found"}
        self.name_status = self.validate_recipe_name()
        self.ingredient_status = self.validate_ingredients()
        self.step_status = self.validate_steps()

        self.recipe_name_error.setText(error_status[self.name_status])
        self.ingredient_error.setText(error_status[self.ingredient_status])
        self.step_error.setText(error_status[self.step_status])

        self.recipe_name_error.show()
        self.ingredient_error.show()
        self.step_error.show()

        self.all_status = 1
        if self.name_status == 0 and self.ingredient_status == 0 and self.step_status == 0:
            self.add2database()
            self.all_status = 0

    def validate_recipe_name(self):
        """
        Validation function for the recipe_name
        :return:
        0 - the name given is valid
        1 - no name is given
        2 - the name is too long
        3 - invalid symbols were detected
        4 - duplicate name detected
        """
        conn = db.create_connection()
        query = db.db_query_table(conn, "main")

        query = [item[1] for item in query]

        in_string = self.recipe_name_in.toPlainText().capitalize()
        if len(in_string) <= 0:
            return 1
        elif len(in_string) >= 64:
            return 2
        elif in_string in query:
            return 4

        for i in range(len(in_string)):
            if in_string[i].isalpha() or in_string[i].isspace():
                continue
            else:
                return 3

        return 0

    def validate_ingredients(self):
        """
        Validation function for ingredient_table
        :return:
        0 - the ingredient_table is populated
        1 - the ingredient_table is empty
        """
        if self.ingredient_table.item(0,0) == None:
            return 1
        return 0
    def validate_steps(self):
        """
        Validation function for step_list
        :return:
        0 - the step_list is populated
        1 - the step_list is empty
        """
        if self.step_list.item(0) == None:
            return 1
        return 0

    def add2database(self):
        """
        Adding the information given by the user to the application's database
        :return:
        """
        recipe_name = self.recipe_name_in.toPlainText().capitalize()
        ingredients = self.ingredient_table_data
        steps = []

        for i in range(self.step_list.count()):
            item = self.step_list.item(i)
            steps.append(item.text())

        print("Name: " + recipe_name)
        print("Recipe Ingredients: " + str(ingredients))
        print("Steps: " + str(steps))

        conn = db.create_connection()
        curr_id = db.query_max_id(conn, "main") + 1
        db.create_task(conn, [curr_id, recipe_name], "main")

        for ingredient in ingredients:
            db.create_task(conn, [curr_id, ingredient[0], ingredient[1], ingredient[2]], "recipe_ingredients")

        for i in range(len(steps)):
            db.create_task(conn, [curr_id, (i + 1), steps[i]], "recipe_steps")

    def clear_all(self):
        """
        clearing data from all the input and display fields, done every time the page is called from ui_control
        :return:
        """
        self.recipe_name_in.clear()
        self.ingredient_name_in.clear()
        self.ingredient_amount_in.setValue(0.5)
        self.ingredient_unit_in.setCurrentIndex(0)
        self.ingredient_table_data.clear()
        self.used_ingredients.clear()
        self.ingredient_table.setRowCount(0)
        self.step_in.clear()
        self.step_list.clear()

def main():
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()