# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configuration_import.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication, QCheckBox,
    QDialog, QDialogButtonBox, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QSizePolicy,
    QSpacerItem, QSpinBox, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)
import source.view.ui.resources_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(654, 443)
        icon = QIcon()
        icon.addFile(u":/app/ico/taxation_tool.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_number = QLabel(self.groupBox)
        self.label_number.setObjectName(u"label_number")
        self.label_number.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_number, 0, 0, 1, 1)

        self.spinBox_number = QSpinBox(self.groupBox)
        self.spinBox_number.setObjectName(u"spinBox_number")
        self.spinBox_number.setMinimum(1)
        self.spinBox_number.setMaximum(6)

        self.gridLayout.addWidget(self.spinBox_number, 0, 1, 1, 1)

        self.label_name = QLabel(self.groupBox)
        self.label_name.setObjectName(u"label_name")
        self.label_name.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_name, 1, 0, 1, 1)

        self.spinBox_name = QSpinBox(self.groupBox)
        self.spinBox_name.setObjectName(u"spinBox_name")
        self.spinBox_name.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.spinBox_name.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToPreviousValue)
        self.spinBox_name.setMinimum(1)
        self.spinBox_name.setMaximum(6)
        self.spinBox_name.setStepType(QAbstractSpinBox.StepType.DefaultStepType)
        self.spinBox_name.setValue(2)

        self.gridLayout.addWidget(self.spinBox_name, 1, 1, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)

        self.horizontalSpacer = QSpacerItem(77, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_quantity = QLabel(self.groupBox)
        self.label_quantity.setObjectName(u"label_quantity")
        self.label_quantity.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_quantity, 0, 0, 1, 1)

        self.spinBox_quantity = QSpinBox(self.groupBox)
        self.spinBox_quantity.setObjectName(u"spinBox_quantity")
        self.spinBox_quantity.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.spinBox_quantity.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToPreviousValue)
        self.spinBox_quantity.setMinimum(1)
        self.spinBox_quantity.setMaximum(6)
        self.spinBox_quantity.setStepType(QAbstractSpinBox.StepType.DefaultStepType)
        self.spinBox_quantity.setValue(3)

        self.gridLayout_2.addWidget(self.spinBox_quantity, 0, 1, 1, 1)

        self.label_height = QLabel(self.groupBox)
        self.label_height.setObjectName(u"label_height")
        self.label_height.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_height, 1, 0, 1, 1)

        self.spinBox_height = QSpinBox(self.groupBox)
        self.spinBox_height.setObjectName(u"spinBox_height")
        self.spinBox_height.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.spinBox_height.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToPreviousValue)
        self.spinBox_height.setMinimum(1)
        self.spinBox_height.setMaximum(6)
        self.spinBox_height.setStepType(QAbstractSpinBox.StepType.DefaultStepType)
        self.spinBox_height.setValue(4)

        self.gridLayout_2.addWidget(self.spinBox_height, 1, 1, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout_2)

        self.horizontalSpacer_2 = QSpacerItem(77, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_diameter = QLabel(self.groupBox)
        self.label_diameter.setObjectName(u"label_diameter")
        self.label_diameter.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_diameter, 0, 0, 1, 1)

        self.spinBox_diameter = QSpinBox(self.groupBox)
        self.spinBox_diameter.setObjectName(u"spinBox_diameter")
        self.spinBox_diameter.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.spinBox_diameter.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToPreviousValue)
        self.spinBox_diameter.setMinimum(1)
        self.spinBox_diameter.setMaximum(6)
        self.spinBox_diameter.setStepType(QAbstractSpinBox.StepType.DefaultStepType)
        self.spinBox_diameter.setValue(5)

        self.gridLayout_3.addWidget(self.spinBox_diameter, 0, 1, 1, 1)

        self.label_quality = QLabel(self.groupBox)
        self.label_quality.setObjectName(u"label_quality")
        self.label_quality.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_quality, 1, 0, 1, 1)

        self.spinBox_quality = QSpinBox(self.groupBox)
        self.spinBox_quality.setObjectName(u"spinBox_quality")
        self.spinBox_quality.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.spinBox_quality.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToPreviousValue)
        self.spinBox_quality.setMinimum(1)
        self.spinBox_quality.setMaximum(6)
        self.spinBox_quality.setStepType(QAbstractSpinBox.StepType.DefaultStepType)
        self.spinBox_quality.setValue(6)

        self.gridLayout_3.addWidget(self.spinBox_quality, 1, 1, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout_3)


        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBox_import_first_row = QCheckBox(Dialog)
        self.checkBox_import_first_row.setObjectName(u"checkBox_import_first_row")
        self.checkBox_import_first_row.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.checkBox_import_first_row.setChecked(True)
        self.checkBox_import_first_row.setTristate(False)

        self.horizontalLayout_2.addWidget(self.checkBox_import_first_row)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_8 = QLabel(Dialog)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_3.addWidget(self.label_8)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.table_preshow = QTableWidget(Dialog)
        if (self.table_preshow.columnCount() < 6):
            self.table_preshow.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_preshow.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_preshow.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_preshow.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_preshow.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_preshow.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_preshow.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        if (self.table_preshow.rowCount() < 20):
            self.table_preshow.setRowCount(20)
        self.table_preshow.setObjectName(u"table_preshow")
        self.table_preshow.setRowCount(20)

        self.verticalLayout.addWidget(self.table_preshow)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u0418\u043c\u043f\u043e\u0440\u0442 \u0432\u0435\u0434\u043e\u043c\u043e\u0441\u0442\u0438 \u0442\u0430\u043a\u0441\u0430\u0446\u0438\u0438", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"\u0421\u0442\u043e\u043b\u0431\u0446\u044b", None))
        self.label_number.setText(QCoreApplication.translate("Dialog", u"\u041d\u043e\u043c\u0435\u0440 \u0442\u043e\u0447\u043a\u0438:", None))
        self.label_name.setText(QCoreApplication.translate("Dialog", u"\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435:", None))
        self.label_quantity.setText(QCoreApplication.translate("Dialog", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e:", None))
        self.label_height.setText(QCoreApplication.translate("Dialog", u"\u0412\u044b\u0441\u043e\u0442\u0430:", None))
        self.label_diameter.setText(QCoreApplication.translate("Dialog", u"\u0414\u0438\u0430\u043c\u0435\u0442\u0440:", None))
        self.label_quality.setText(QCoreApplication.translate("Dialog", u"\u0421\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435:", None))
        self.checkBox_import_first_row.setText(QCoreApplication.translate("Dialog", u"\u0418\u043c\u043f\u043e\u0440\u0442 \u043f\u0435\u0440\u0432\u043e\u0439 \u0441\u0442\u0440\u043e\u043a\u0438:", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"\u041f\u0440\u0435\u0434\u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440 \u043f\u0435\u0440\u0432\u044b\u0445 20 \u0441\u0442\u0440\u043e\u043a:", None))
        ___qtablewidgetitem = self.table_preshow.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"\u041d\u043e\u043c\u0435\u0440 \u0442\u043e\u0447\u043a\u0438", None));
        ___qtablewidgetitem1 = self.table_preshow.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435", None));
        ___qtablewidgetitem2 = self.table_preshow.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e", None));
        ___qtablewidgetitem3 = self.table_preshow.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"\u0412\u044b\u0441\u043e\u0442\u0430", None));
        ___qtablewidgetitem4 = self.table_preshow.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"\u0414\u0438\u0430\u043c\u0435\u0442\u0440", None));
        ___qtablewidgetitem5 = self.table_preshow.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"\u0421\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435", None));
    # retranslateUi

