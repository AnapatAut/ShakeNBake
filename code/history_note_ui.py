#historynoteui.py

#Python code for UI of historynote

# Created by Shine, 19 Oct 2023


import sys
import sqlite3
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QTextEdit, QHBoxLayout, QMessageBox

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

def edit_history_notes(recipe_name, new_notes):
    conn = sqlite3.connect('cookbook.db')
    cursor = conn.cursor()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    cursor.execute('''
        UPDATE history_notes SET note = ? WHERE recipe_name = ?
    ''', (new_notes, recipe_name))

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

        self.history_label = QLabel('History Note:')
        self.history_textbox = QTextEdit(self)
        self.history_textbox.setReadOnly(True)  # Set the history_textbox to read-only initially

        self.addButton = QPushButton('Add', self)
        self.addButton.clicked.connect(self.addClicked)

        self.editButton = QPushButton('Edit', self)
        self.editButton.clicked.connect(self.editClicked)

        self.viewButton = QPushButton('View', self)
        self.viewButton.clicked.connect(self.viewClicked)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.recipe_label)
        self.layout.addWidget(self.recipe_textbox)
        self.layout.addWidget(self.history_label)
        self.layout.addWidget(self.history_textbox)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.addButton)
        button_layout.addWidget(self.editButton)
        button_layout.addWidget(self.viewButton)

        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)
        self.show()
        
    #Add button to Edit history note
    def addClicked(self):
        recipe_name = self.recipe_textbox.text()
        note = self.history_textbox.toPlainText()
        add_history_note(recipe_name, note)
        QMessageBox.about(self, "Success", "Note added successfully!")

    #Edit button to Edit history note
    def editClicked(self):
        recipe_name = self.recipe_textbox.text()
        if not recipe_name:
            QMessageBox.about(self, "Error", "Please enter a recipe name!")
            return

        notes = view_history_notes(recipe_name)

        if not notes:
            self.history_textbox.setReadOnly(False)  # Enable editing if no history note is found
            self.history_textbox.setText("")  # Clear the text box
            QMessageBox.about(self, "Info", "No history notes found for this recipe. You can now edit and add new notes.")
        else:
            self.history_textbox.setReadOnly(False)  # Enable editing
            text = ""
            for timestamp, note in notes:
                text += f"{timestamp} - {note}\n"
            self.history_textbox.setText(text)
    #View button to view history note
    def viewClicked(self):
        recipe_name = self.recipe_textbox.text()
        notes = view_history_notes(recipe_name)
        if not notes:
            self.history_textbox.setText("No history notes found for this recipe.")
        else:
            text = ""
            for timestamp, note in notes:
                text += f"{timestamp} - {note}\n"
            self.history_textbox.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
