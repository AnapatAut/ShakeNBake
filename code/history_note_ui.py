#historynoteui.py

#Python code for UI of historynote

# Created by Shine on 19 Oct 2023

#Modified to have only add,delete and view in the UI as well as to be able to delete a specific row of note.

#Modified by Shine on 23 Oct 2023
import sys
import sqlite3
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QTextEdit, QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem

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
    conn = sqlite3.connect('cookbook.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT timestamp, note FROM history_notes WHERE recipe_name = ?
    ''', (recipe_name,))

    notes = cursor.fetchall()

    conn.close()

    return notes

def delete_history_notes(recipe_name, timestamp, note):
    conn = sqlite3.connect('cookbook.db')
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM history_notes WHERE recipe_name = ? AND timestamp = ? AND note = ?
    ''', (recipe_name, timestamp, note))

    conn.commit()
    conn.close()

# History note window
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Recipe History Notes'
        self.left = 100
        self.top = 100
        self.width = 920
        self.height = 680
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.recipe_label = QLabel('Recipe Name:')
        self.recipe_textbox = QLineEdit(self)

        self.write_history_label = QLabel('Write History Note:')
        self.write_history_textbox = QTextEdit(self)
        self.write_history_textbox.setReadOnly(False)  # Set the write_history_textbox to read-only initially

        self.history_label = QLabel('View History Note:')
        self.history_table = QTableWidget()
        self.history_table.setRowCount(0)
        self.history_table.setColumnCount(2)
        self.history_table.setHorizontalHeaderLabels(["Timestamp", "History Note"])
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make the table non-editable
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)  # Set row selection behavior

        self.addButton = QPushButton('Add', self)
        self.addButton.clicked.connect(self.addClicked)

        self.deleteButton = QPushButton('Delete', self)
        self.deleteButton.clicked.connect(self.deleteClicked)

        self.viewButton = QPushButton('View', self)
        self.viewButton.clicked.connect(self.viewClicked)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.recipe_label)
        self.layout.addWidget(self.recipe_textbox)
        self.layout.addWidget(self.write_history_label)
        self.layout.addWidget(self.write_history_textbox)
        self.layout.addWidget(self.history_label)
        self.layout.addWidget(self.history_table)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.addButton)
        button_layout.addWidget(self.deleteButton)
        button_layout.addWidget(self.viewButton)

        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)
        self.show()
        
    # Add button to add history note
    def addClicked(self):
        recipe_name = self.recipe_textbox.text()
        note = self.write_history_textbox.toPlainText()
        add_history_note(recipe_name, note)
        QMessageBox.about(self, "Success", "Note added successfully!")

    # Delete button to delete history note
    def deleteClicked(self):
        current_row = self.history_table.currentRow()
        if current_row >= 0:
            recipe_name = self.recipe_textbox.text()
            timestamp = self.history_table.item(current_row, 0).text()
            note = self.history_table.item(current_row, 1).text()
            delete_history_notes(recipe_name, timestamp, note)
            self.history_table.removeRow(current_row)
            QMessageBox.about(self, "Success", "Note deleted successfully!")

    # View button to view history note
    def viewClicked(self):
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
