#historynotes.py

#Add history notes to a recipe, for example “2023-09-13 18:00 Cooked for my boyfriend”. 
#The date and time should be automatically set basedon the PC internal clock.

#Created by Shine on, 3rd Oct, 2023

import sqlite3
import datetime

# Initialize the database
def initialize_database():
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

# Function to add a history note to the database
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

# Function to view all historical notes for a recipe
def view_history_notes(recipe_name):
    conn = sqlite3.connect('cookbook.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT timestamp, note FROM history_notes WHERE recipe_name = ?
    ''', (recipe_name,))

    notes = cursor.fetchall()

    conn.close()

    return notes

# Function to edit history notes for a specific recipe
def edit_history_notes(recipe_name, new_notes):
    conn = sqlite3.connect('cookbook.db')
    cursor = conn.cursor()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    cursor.execute('''
        INSERT INTO history_notes (recipe_name, timestamp, note)
        VALUES (?, ?, ?)
    ''', (recipe_name, timestamp, new_notes))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_database()

    while True:
        action = input("Enter 'a' to add a note, 'e' to edit notes, 'v' to view notes, or 'q' to quit: ").lower()

        if action == 'q':
            break

        if action == 'a':
            recipe_name = input("Enter recipe name: ")
            note = input("Enter history note: ")
            add_history_note(recipe_name, note)
        elif action == 'e':
            recipe_name = input("Enter the recipe name to edit notes: ")
            new_notes = input("Enter the new history notes: ")
            edit_history_notes(recipe_name, new_notes)
        elif action == 'v':
            recipe_name = input("Enter recipe name to view notes: ")
            notes = view_history_notes(recipe_name)
            print(f"\nHistorical notes for {recipe_name}:\n")
            for timestamp, note in notes:
                print(f"{timestamp} - {note}")


