"""
 ui_control.py

 Python code for control UI pages

 Created by Anapat B., 2 Nov 2023
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QApplication
import main_menu
import recipe_creation
import recipe_display
import history_note


class ui_control(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Multi-Page App")
        self.setGeometry(0, 0, 920, 680)

        self.stacked_widget = QStackedWidget(self)

        # Create instances of Page1 and Page2 and add them to the stacked widget
        self.main_menu_page = main_menu.ui_main_window()
        self.recipe_creation_page = recipe_creation.Ui_MainWindow()
        self.recipe_display_page = recipe_display.MainWindow()
        self.history_note_page = history_note.App()
        self.stacked_widget.addWidget(self.main_menu_page)
        self.stacked_widget.addWidget(self.recipe_creation_page)
        self.stacked_widget.addWidget(self.recipe_display_page)
        self.stacked_widget.addWidget(self.history_note_page)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.stacked_widget.setCurrentIndex(0)

        self.main_menu_page.add_recipe_widget.clicked.connect(self.to_recipe_creation)
        self.main_menu_page.recipe_list_widget.itemClicked.connect(self.to_recipe_display)
        self.recipe_creation_page.confirm_btn.clicked.connect(self.recipe_creation_confirm)
        self.recipe_creation_page.cancel_btn.clicked.connect(self.to_main_menu)
        self.recipe_display_page.add_note_btn.clicked.connect(self.to_history_notes)
        self.history_note_page.back_button.clicked.connect(self.to_recipe_display)
        self.recipe_display_page.back_btn.clicked.connect(self.to_main_menu)
        self.recipe_display_page.add_note_btn.clicked.connect(self.to_history_notes)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def recipe_creation_confirm(self):
        if self.recipe_creation_page.all_status == 0:
            self.to_main_menu()

    def to_main_menu(self):
        self.stacked_widget.setCurrentIndex(0)
        self.main_menu_page.search_bar_widget.clear()
        self.main_menu_page.get_recipe_list()
        self.main_menu_page.display_all_recipes()

    def to_recipe_creation(self):
        self.recipe_creation_page.clear_all()
        self.stacked_widget.setCurrentIndex(1)


    def to_recipe_display(self):
        self.recipe_display_page.recipe_id = self.main_menu_page.recipe_id
        self.recipe_display_page.clear_all_data()
        self.recipe_display_page.init_tables()
        self.stacked_widget.setCurrentIndex(2)

    def to_history_notes(self):
        self.history_note_page.recipe_id = self.main_menu_page.recipe_id
        self.history_note_page.view_history()
        self.stacked_widget.setCurrentIndex(3)


def main():
    app = QApplication(sys.argv)
    window = ui_control()
    window.show()
    exit(app.exec_())


if __name__ == "__main__":
    main()
