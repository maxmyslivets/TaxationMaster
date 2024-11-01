
### Преобразование `resources.qrc` в `resource_rc.py`
```bash
pyside6-rcc resources/resources.qrc -o source/view/ui/resources_rc.py
```
Далее в файле `source/view/ui/ui_mainwindow.py`
заменить строку
```python
import resources_rc
```
на строку
```python
import source.view.ui.resources_rc
```
