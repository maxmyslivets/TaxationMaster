# компиляция resources.qrc в resources_rc.py
rcc:
	pyside6-rcc resources/resources.qrc -o source/view/ui/resources_rc.py

# компиляция файлов *.ui в *.py
uic:
	pyside6-uic resources/ui/mainwindow.ui -o source/view/ui/ui_mainwindow.py
	pyside6-uic resources/ui/settings.ui -o source/view/ui/ui_settings.py
	pyside6-uic resources/ui/configuration_import.ui -o source/view/ui/ui_configuration_import.py
	python make_tools/replace_import_resources_string.py

# сборка exe
exe:
	pyinstaller --noconfirm --onedir --console --icon "C:\Projects\TaxationTool\resources\ico\taxation_tool.ico" --name "TaxationTool"  "C:\Projects\TaxationTool\entrypoint.py"
	python make_tools/clear_directory_after_pyinstaller.py
