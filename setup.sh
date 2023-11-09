#! /bin/bash

pip install pyqt5
rm -r ui_control/
pyinstaller --collect-all code/ui_control.py --add-data "data/recipe_database.db3:data/recipe_database.db3" code/ui_control.py  code/recipe_creation.py  code/recipe_display.py code/main_menu.py code/history_note.py code/db_manager.py 
rm -r build
rm -r ui_control.spec
mv dist/ui_control ui_control/
rm -r dist
mv ui_control/_internal/data/ ui_control/
cd ui_control/data/
mv recipe_database.db3/ ..
cd ..
mv recipe_database.db3/recipe_database.db3 data/
rmdir recipe_database.db3
