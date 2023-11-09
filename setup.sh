#! /bin/bash

rm -r build
rm -r dist
rm -r ui_control.spec
pyinstaller --collect-all code/ui_control.py --add-data "data/recipe_database.db3:data/recipe_database.db3" code/ui_control.py  code/recipe_creation.py  code/recipe_display.py code/main_menu.py code/history_note.py code/db_manager.py 
cd dist
mv ui_control/_internal/data/ ui_control/
cd ui_control/data/
mv recipe_database.db3/ ..
cd ..
mv recipe_database.db3/recipe_database.db3 data/
rmdir recipe_database.db3
