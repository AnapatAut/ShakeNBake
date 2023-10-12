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
        super().__init__()
        self.setupui()

    # sets up the page format along with the creation of the page's widgets
    def setupui(self):
        self.setWindowTitle('Recipe Creation')
        self.setGeometry(100, 100, 920, 680)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        font = QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.recipe_name_prompt = QLabel(self.centralwidget)
        self.recipe_name_prompt.setObjectName("recipe_name_prompt")
        self.recipe_name_prompt.setGeometry(QRect(30, 30, 91, 41))
        self.recipe_name_prompt.setFont(font)
        self.recipe_name_prompt.setText("Name:")

        self.recipe_name_in = QTextEdit(self.centralwidget)
        self.recipe_name_in.setObjectName("recipe_name_in")
        self.recipe_name_in.setGeometry(QRect(180, 35, 371, 31))
        self.recipe_name_in.setPlaceholderText("Enter an Recipe Name")

        self.ingredient_prompt = QLabel(self.centralwidget)
        self.ingredient_prompt.setObjectName("ingredient_prompt")
        self.ingredient_prompt.setGeometry(QRect(30, 60, 141, 71))
        self.ingredient_prompt.setFont(font)

        self.ingredient_name_in = QTextEdit(self.centralwidget)
        self.ingredient_name_in.setObjectName("ingredient_name_in")
        self.ingredient_name_in.setGeometry(QRect(180, 81, 171, 31))
        if self.

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

        self.ingredient_measurement_in = QComboBox(self.centralwidget)
        self.ingredient_measurement_in.addItem("Grams")
        self.ingredient_measurement_in.addItem("Milligrams")
        self.ingredient_measurement_in.addItem("Kilogram")
        self.ingredient_measurement_in.addItem("Tablespoon(s)")
        self.ingredient_measurement_in.addItem("Teaspoon(s)")
        self.ingredient_measurement_in.addItem("none")
        self.ingredient_measurement_in.setObjectName("ingredient_measurement")
        self.ingredient_measurement_in.setGeometry(QRect(428, 81, 121, 31))
        self.ingredient_measurement_in.setAutoFillBackground(False)

        self.all_ingredient = QTableWidget(self.centralwidget)
        if (self.all_ingredient.columnCount() < 3):
            self.all_ingredient.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.all_ingredient.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.all_ingredient.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.all_ingredient.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.all_ingredient.setObjectName("all_ingredients")
        self.all_ingredient.setGeometry(QRect(180, 120, 371, 161))
        self.ingredient_table_header = self.all_ingredient.horizontalHeader()
        self.ingredient_table_header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.ingredient_table_header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ingredient_table_header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.add_ingredient = QPushButton(self.centralwidget)
        self.add_ingredient.setObjectName("add_ingredient")
        self.add_ingredient.setGeometry(QRect(560, 80, 151, 41))

        self.remove_ingredient = QPushButton(self.centralwidget)
        self.remove_ingredient.setObjectName("remove_ingredient")
        self.remove_ingredient.setGeometry(QRect(560, 130, 151, 41))

        self.step_prompt = QLabel(self.centralwidget)
        self.step_prompt.setObjectName("step_prompt")
        self.step_prompt.setGeometry(QRect(30, 290, 111, 31))
        self.step_prompt.setFont(font)

        self.step_in = QTextEdit(self.centralwidget)
        self.step_in.setObjectName("step_in")
        self.step_in.setGeometry(QRect(180, 290, 371, 81))

        self.all_steps = QListWidget(self.centralwidget)
        self.all_steps.setObjectName("all_steps")
        self.all_steps.setGeometry(QRect(180, 380, 371, 211))

        self.add_step = QPushButton(self.centralwidget)
        self.add_step.setObjectName("add_step")
        self.add_step.setGeometry(QRect(570, 290, 151, 41))
        self.add_step.clicked.connect(self.add_to_all_steps)

        self.remove_step = QPushButton(self.centralwidget)
        self.remove_step.setObjectName("remove_step")
        self.remove_step.setGeometry(QRect(570, 340, 151, 41))
        self.remove_step.clicked.connect(self.remove_from_all_steps)

        self.confirm_btn = QPushButton(self.centralwidget)
        self.confirm_btn.setObjectName("confirm_btn")
        self.confirm_btn.setGeometry(QRect(570, 590, 151, 41))
        self.confirm_btn.setText("Confirm")


        self.all_ingredient.raise_()
        self.recipe_name_in.raise_()
        self.confirm_btn.raise_()
        self.recipe_name_prompt.raise_()
        self.ingredient_prompt.raise_()
        self.add_ingredient.raise_()
        self.remove_ingredient.raise_()
        self.step_prompt.raise_()
        self.step_in.raise_()
        self.ingredient_amount_in.raise_()
        self.ingredient_measurement_in.raise_()
        self.ingredient_name_in.raise_()
        self.step_in.raise_()
        self.add_step.raise_()
        self.remove_step.raise_()
        self.suggestion_list.raise_()

        self.name_ui()

    # sets the display text for each of the widgets
    def name_ui(self):
        self.ingredient_prompt.setText("Ingredient(s):")
        self.ingredient_name_in.setPlaceholderText("Enter an Ingredient Name")
        self.add_ingredient.setText("Add Ingredient")
        self.remove_ingredient.setText("Remove Ingredient")
        self.step_prompt.setText("Step(s):")
        ___qtablewidgetitem = self.all_ingredient.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText("Name")
        ___qtablewidgetitem1 = self.all_ingredient.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText("Amount")
        ___qtablewidgetitem2 = self.all_ingredient.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText("Unit")

        self.step_in.setPlaceholderText("Enter Your Receipe Steps Here One by One")
        self.add_step.setText("Add Step")
        self.remove_step.setText("Remove Step")

    # adds the text within step_in into the all_steps
    def add_to_all_steps(self):
        step_text = self.step_in.toPlainText().replace('\n', '')

        if step_text:
            formatted_text = self.format_text(step_text, 60)
            self.all_steps.addItem(formatted_text)
            self.step_in.clear()

    # formats input text, used for steps
    def format_text(self, in_string, line_length):
        out_string = ""

        line_num = 1
        curr_line = ""
        for i in range(len(in_string)):
            if in_string[i - 1].isascii() and in_string[i].isspace():
                if int(i / line_length) >= line_num:
                    out_string += curr_line + "\n"

                    curr_line = ""
                    line_num += 1

            curr_line += in_string[i]

        if curr_line:
            out_string += curr_line

        return out_string

    # removes the selected item from the list table all_steps
    def remove_from_all_steps(self):
        selected_items = self.all_steps.selectedItems()
        for item in selected_items:
            self.all_steps.takeItem(self.all_steps.row(item))

    # pulls the list of valid ingredients from the database
    def update_ingredients_list(self):
        conn = db.create_connection()
        query_out = db.db_searchbar_query(conn, "ingredient_list")

        self.all_ingredients = []

        for item in query_out:
            self.all_ingredients.append(item[1])

    # updates the suggestion list according to the ingredient_name_in
    def update_suggestions(self):

        in_string = self.ingredient_name_in.toPlainText()

        self.suggestion_list.clear()

        matching_suggestions = [suggestion for suggestion in self.all_ingredients if in_string.lower() in suggestion.lower()]
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

def main():
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()