# компиляция resources.qrc в resources_rc.py
rcc:
	pyside6-rcc resources/resources.qrc -o src/ui/resources_rc.py

# компиляция файлов *.ui в *.py
uic:
	pyside6-uic resources/main_window.ui -o src/ui/ui_mainwindow.py
	python make_tools/replace_import_resources_string.py

# сборка exe
exe:
	pyinstaller --noconfirm --onedir --console --icon "C:\Projects\TaxationTool\resources\taxation_tool.ico" --add-data "C:\Projects\TaxationTool\data;data/"  "C:\Projects\TaxationTool\TaxationTool.py"
	python make_tools/clear_directory_after_pyinstaller.py
