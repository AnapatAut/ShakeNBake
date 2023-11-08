"""historynoteui.py
"""
# Python code for UI of historynote

# Created by Shine on 19 Oct 2023

# Modified by Shine on 23 Oct 2023

# Modified to be able to delete specific rows

# Modified by Shine on 26 Oct 2023

# Modified for history note text box size
# Modified for limit text size input of note
# Modified to add back button to go to recipe page


# Modified by Shine on 2 Nov 2023

# Modified to directly view recipe without clicking view button
# Modified to directly alert to 'add note' when clicking add button without data
# Modified to improve size of history note table

# Modified by Shine on 7 Nov 2023
# Modified to do the connection with db_manager


import sys
import sqlite3
import datetime

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRect, Qt
import db_manager as db


class App(QWidget):
    """History note window"""

    def __init__(self):
        super().__init__()
        self.title = 'Recipe History Notes'
        self.recipe_id = 1
        # self.recipe_list = [(1,'Sushi'),(2,'Fine')]
        self.init_ui()

    def init_ui(self):
        """Set up the UI page"""

        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 920, 680)

        name = [[0, "No Recipe Found"]]
        self.recipe_label = QLabel(
            f'<html><head/><body><p><span style=" font-size:20pt; font-weight:600;">Recipe Name:  {name[0][1]}</span></p></body></html>'
        )
        self.recipe_textbox = QLabel(self)

        # # self.recipe_textbox.setText("Sushi")
        # self.recipe_textbox.setText([recipe[1] for recipe in self.recipe_list if recipe[0] == self.recipe_id][0])
        # self.recipe_textbox.setReadOnly(True)
        self.write_history_label = QLabel('Write History Note:')
        self.write_history_textbox = QTextEdit(self)
        self.write_history_textbox.setReadOnly(False)
        self.write_history_textbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.write_history_textbox.setMaximumHeight(50)  # Set the maximum height as needed
        self.history_label = QLabel('View History Note:')
        self.history_table = QTableWidget()
        self.history_table.setRowCount(0)
        self.history_table.setColumnCount(2)
        self.history_table.setHorizontalHeaderLabels(["Timestamp", "History Note"])
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)

        self.add_button = QPushButton('Add', self)
        self.add_button.clicked.connect(self.add_clicked)

        self.delete_button = QPushButton('Delete', self)
        self.delete_button.clicked.connect(self.delete_clicked)

        # self.view_button = QPushButton('View', self)
        # self.view_button.clicked.connect(self.view_clicked)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.recipe_label)
        self.layout.addWidget(self.recipe_textbox)
        self.layout.addWidget(self.write_history_label)
        self.layout.addWidget(self.write_history_textbox)
        self.layout.addWidget(self.history_label)
        self.layout.addWidget(self.history_table)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        # button_layout.addWidget(self.view_button)

        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(self.back_clicked)
        button_layout.addWidget(self.back_button)

        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

        self.show()

    def add_clicked(self):
        """Add button to add history note"""
        # recipe_name = self.recipe_textbox.text()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        note_details = self.write_history_textbox.toPlainText()

        if note_details.strip():  # Check if the note is not empty or contains only whitespace
            if len(note_details) <= 248:
                conn = db.create_connection()
                table = "history_note"
                curr_id = db.query_max_id(conn, table) + 1
                data_to_insert = [curr_id, self.recipe_id, note_details, timestamp]
                db.create_task(conn, data_to_insert, table)
                self.write_history_textbox.clear()
                self.view_history()
            else:
                QMessageBox.about(
                    self,
                    "Error",
                    "The number of characters is larger than the maximum limit 248. Please input again.",
                )
        else:
            QMessageBox.about(self, "Error", "Note can't be blank. Please input some text.")

    def delete_clicked(self):
        """Delete button to delete history note"""
        current_row = self.history_table.currentRow()
        conn = db.create_connection()
        all_notes = db.db_query(conn, "history_note", "recipe_id", self.recipe_id)

        if current_row >= 0:
            conn = db.create_connection()
            db.db_remove_history_notes(conn, all_notes[current_row][0], self.recipe_id)
            self.history_table.removeRow(current_row)

    def clear_history_table(self):
        """Clear the history table"""
        self.history_table.setRowCount(0)
        print(self.recipe_id)

    def back_clicked(self):
        """Go back to the previous page"""
        print("Go back to recipe page")
        self.clear_history_table()
        self.close()

    def view_history(self):
        conn = db.create_connection()
        name = db.db_query(conn, "main", "recipe_id", self.recipe_id)
        print(name, end="--------\n")
        notes = db.db_query(conn, "history_note", "recipe_id", self.recipe_id)

        self.history_table.setRowCount(0)  # Clear the table before populating new data
        self.recipe_label.setText(
            f'<html><head/><body><p><span style=" font-size:20pt; font-weight:600;">Recipe Name:  {name[0][1]}</span></p></body></html>')

        if notes:
            for row, (history_id, _, timestamp, note) in enumerate(notes):
                self.history_table.insertRow(row)
                self.history_table.setItem(row, 0, QTableWidgetItem(str(note)))
                self.history_table.setItem(row, 1, QTableWidgetItem(timestamp))
                # self.history_table.setItem(row, 2, QTableWidgetItem(note))
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
