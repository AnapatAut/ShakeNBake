"""historynoteui.py
"""
#Python code for UI of historynote

# Created by Shine on 19 Oct 2023

#Modified by Shine on 23 Oct 2023

#Modified to be able to delete specific rows

#Modified by Shine on 26 Oct 2023

#Modified for history note text box size
#Modified for limit text size input of note
#Modified to add back button to go to recipe page


#Modified by Shine on 2 Nov 2023

#Modified to directly view recipe without clicking view button
#Modified to directly alert to 'add note' when clicking add button without data
#Modified to improve size of history note table



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

# Backend code starts here
conn = sqlite3.connect('cookbook.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS history_notes (
        recipe_name TEXT,
        timestamp DATETIME,
        note TEXT
    )
''')

conn.commit()
conn.close()

def add_history_note(recipe_name, note):
    """Add history note"""
    conn = sqlite3.connect('cookbook.db')
    cursor = conn.cursor()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    cursor.execute('''
        INSERT INTO history_notes (recipe_name, timestamp, note)
        VALUES (?, ?, ?)
    ''', (recipe_name, timestamp, note))

    conn.commit()
    conn.close()

def view_history_notes(recipe_name):
    """View history note"""

    conn = sqlite3.connect('cookbook.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT timestamp, note FROM history_notes WHERE recipe_name = ?
    ''', (recipe_name,))

    notes = cursor.fetchall()

    conn.close()

    return notes

def delete_history_notes(recipe_name, timestamp, note):
    """Delete history note"""

    conn = sqlite3.connect('cookbook.db')
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM history_notes WHERE recipe_name = ? AND timestamp = ? AND note = ?
    ''', (recipe_name, timestamp, note))

    conn.commit()
    conn.close()

class App(QWidget):
    """History note window"""
    def __init__(self):
        super().__init__()
        self.title = 'Recipe History Notes'

        self.init_ui()

    def init_ui(self):
        """Set up the UI page"""
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 920, 680)

        self.recipe_label = QLabel('Recipe Name:')
        self.recipe_textbox = QLineEdit(self)
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
        recipe_name = self.recipe_textbox.text()
        note = self.write_history_textbox.toPlainText()
        if note.strip():  # Check if the note is not empty or contains only whitespace
            if len(note) <= 248:
                add_history_note(recipe_name, note)
                QMessageBox.about(self, "Success", "Note added successfully!")
                self.view_history()
            else:
                QMessageBox.about(self, "Error", "The number of characters is larger than the maximum limit 248. Please input again.")
        else:
            QMessageBox.about(self, "Error", "Note can't be blank. Please input some text.")
    def delete_clicked(self):
        """Delete button to delete history note"""
        current_row = self.history_table.currentRow()
        if current_row >= 0:
            recipe_name = self.recipe_textbox.text()
            timestamp = self.history_table.item(current_row, 0).text()
            note = self.history_table.item(current_row, 1).text()
            delete_history_notes(recipe_name, timestamp, note)
            self.history_table.removeRow(current_row)
            QMessageBox.about(self, "Success", "Note deleted successfully!")

    def back_clicked(self):
        print("Go back to recipe page")
        self.close()

    def view_history(self):
        """View history note"""
        recipe_name = self.recipe_textbox.text()
        notes = view_history_notes(recipe_name)
        self.history_table.setRowCount(0)  # Clear the table before populating new data

        if not notes:
            QMessageBox.about(self, "Info", "No history notes found for this recipe.")
        else:
            for row, (timestamp, note) in enumerate(notes):
                self.history_table.insertRow(row)
                self.history_table.setItem(row, 0, QTableWidgetItem(timestamp))
                self.history_table.setItem(row, 1, QTableWidgetItem(note))
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
