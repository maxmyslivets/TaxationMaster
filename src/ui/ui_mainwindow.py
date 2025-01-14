# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QMainWindow, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QStatusBar,
    QTabWidget, QTableView, QTextEdit, QToolBar,
    QToolBox, QVBoxLayout, QWidget)
import src.ui.resources_rc

class Ui_TaxationTool(object):
    def setupUi(self, TaxationTool):
        if not TaxationTool.objectName():
            TaxationTool.setObjectName(u"TaxationTool")
        TaxationTool.resize(786, 587)
        icon = QIcon()
        icon.addFile(u":/window/taxation_tool.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        TaxationTool.setWindowIcon(icon)
        self.action_import_taxation_list = QAction(TaxationTool)
        self.action_import_taxation_list.setObjectName(u"action_import_taxation_list")
        self.action_import_taxation_list.setMenuRole(QAction.MenuRole.NoRole)
        self.action_import_topographic_plan = QAction(TaxationTool)
        self.action_import_topographic_plan.setObjectName(u"action_import_topographic_plan")
        self.action_import_topographic_plan.setMenuRole(QAction.MenuRole.NoRole)
        self.action_get_count_tree = QAction(TaxationTool)
        self.action_get_count_tree.setObjectName(u"action_get_count_tree")
        self.action_get_count_tree.setMenuRole(QAction.MenuRole.NoRole)
        self.action_species_and_types = QAction(TaxationTool)
        self.action_species_and_types.setObjectName(u"action_species_and_types")
        self.action_identification_shrub = QAction(TaxationTool)
        self.action_identification_shrub.setObjectName(u"action_identification_shrub")
        self.action_identification_shrub.setMenuRole(QAction.MenuRole.NoRole)
        self.action_replace_comma_to_dot = QAction(TaxationTool)
        self.action_replace_comma_to_dot.setObjectName(u"action_replace_comma_to_dot")
        self.action_replace_comma_to_dot.setMenuRole(QAction.MenuRole.NoRole)
        self.action_replace_dot_comma_to_comma = QAction(TaxationTool)
        self.action_replace_dot_comma_to_comma.setObjectName(u"action_replace_dot_comma_to_comma")
        self.action_replace_dot_comma_to_comma.setMenuRole(QAction.MenuRole.NoRole)
        self.action_validation = QAction(TaxationTool)
        self.action_validation.setObjectName(u"action_validation")
        self.action_validation.setMenuRole(QAction.MenuRole.NoRole)
        self.action_compare_numbers = QAction(TaxationTool)
        self.action_compare_numbers.setObjectName(u"action_compare_numbers")
        self.action_compare_numbers.setMenuRole(QAction.MenuRole.NoRole)
        self.action_insert_zones = QAction(TaxationTool)
        self.action_insert_zones.setObjectName(u"action_insert_zones")
        self.action_insert_zones.setMenuRole(QAction.MenuRole.NoRole)
        self.action_insert_taxation_list_orm = QAction(TaxationTool)
        self.action_insert_taxation_list_orm.setObjectName(u"action_insert_taxation_list_orm")
        self.action_insert_taxation_list_orm.setMenuRole(QAction.MenuRole.NoRole)
        self.action_insert_protected_zones = QAction(TaxationTool)
        self.action_insert_protected_zones.setObjectName(u"action_insert_protected_zones")
        self.action_insert_protected_zones.setMenuRole(QAction.MenuRole.NoRole)
        self.action_insert_zone_objects = QAction(TaxationTool)
        self.action_insert_zone_objects.setObjectName(u"action_insert_zone_objects")
        self.action_insert_zone_objects.setMenuRole(QAction.MenuRole.NoRole)
        self.action_open_excel_template = QAction(TaxationTool)
        self.action_open_excel_template.setObjectName(u"action_open_excel_template")
        self.action_open_excel_template.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(TaxationTool)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setFrameShape(QFrame.Shape.NoFrame)
        self.splitter.setFrameShadow(QFrame.Shadow.Plain)
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.setHandleWidth(0)
        self.splitter.setChildrenCollapsible(True)
        self.toolBox = QToolBox(self.splitter)
        self.toolBox.setObjectName(u"toolBox")
        self.toolBox.setFrameShape(QFrame.Shape.Box)
        self.toolBox.setFrameShadow(QFrame.Shadow.Raised)
        self.toolBox.setLineWidth(1)
        self.toolBox.setMidLineWidth(0)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.page.setGeometry(QRect(0, 0, 780, 200))
        self.toolBox.addItem(self.page, u"\u0412\u0432\u043e\u0434 \u0434\u0430\u043d\u043d\u044b\u0445")
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setGeometry(QRect(0, 0, 780, 200))
        self.gridLayout_2 = QGridLayout(self.page_2)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabWidget = QTabWidget(self.page_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.tabWidget.setTabShape(QTabWidget.TabShape.Triangular)
        self.tabWidget.setElideMode(Qt.TextElideMode.ElideLeft)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_3 = QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tableView_density = QTableView(self.tab_2)
        self.tableView_density.setObjectName(u"tableView_density")
        self.tableView_density.setFrameShape(QFrame.Shape.Box)
        self.tableView_density.setFrameShadow(QFrame.Shadow.Raised)
        self.tableView_density.setShowGrid(True)
        self.tableView_density.setGridStyle(Qt.PenStyle.NoPen)
        self.tableView_density.setSortingEnabled(True)

        self.gridLayout_3.addWidget(self.tableView_density, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_4 = QGridLayout(self.tab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.tableView_species = QTableView(self.tab)
        self.tableView_species.setObjectName(u"tableView_species")
        self.tableView_species.setFrameShape(QFrame.Shape.Box)
        self.tableView_species.setFrameShadow(QFrame.Shadow.Raised)
        self.tableView_species.setShowGrid(True)
        self.tableView_species.setGridStyle(Qt.PenStyle.NoPen)
        self.tableView_species.setSortingEnabled(True)

        self.gridLayout_4.addWidget(self.tableView_species, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")

        self.verticalLayout_2.addWidget(self.tabWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(9, 9, 9, 9)
        self.horizontalSpacer_2 = QSpacerItem(178, 18, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.btn_edit_db_2 = QPushButton(self.page_2)
        self.btn_edit_db_2.setObjectName(u"btn_edit_db_2")

        self.horizontalLayout_2.addWidget(self.btn_edit_db_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.toolBox.addItem(self.page_2, u"\u0411\u0430\u0437\u044b \u0434\u0430\u043d\u043d\u044b\u0445")
        self.splitter.addWidget(self.toolBox)
        self.textEdit = QTextEdit(self.splitter)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"Consolas"])
        self.textEdit.setFont(font)
        self.textEdit.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.IBeamCursor))
        self.textEdit.setFrameShape(QFrame.Shape.Box)
        self.textEdit.setFrameShadow(QFrame.Shadow.Raised)
        self.textEdit.setLineWidth(1)
        self.textEdit.setMidLineWidth(0)
        self.textEdit.setReadOnly(True)
        self.splitter.addWidget(self.textEdit)

        self.verticalLayout.addWidget(self.splitter)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setOrientation(Qt.Orientation.Horizontal)

        self.verticalLayout.addWidget(self.progressBar)

        self.progressBar2 = QProgressBar(self.centralwidget)
        self.progressBar2.setObjectName(u"progressBar2")
        self.progressBar2.setValue(0)
        self.progressBar2.setTextVisible(False)

        self.verticalLayout.addWidget(self.progressBar2)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        TaxationTool.setCentralWidget(self.centralwidget)
        self.toolBar_import = QToolBar(TaxationTool)
        self.toolBar_import.setObjectName(u"toolBar_import")
        TaxationTool.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar_import)
        self.toolBar_validation = QToolBar(TaxationTool)
        self.toolBar_validation.setObjectName(u"toolBar_validation")
        TaxationTool.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar_validation)
        TaxationTool.insertToolBarBreak(self.toolBar_validation)
        self.toolBar_replace_comma = QToolBar(TaxationTool)
        self.toolBar_replace_comma.setObjectName(u"toolBar_replace_comma")
        TaxationTool.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar_replace_comma)
        TaxationTool.insertToolBarBreak(self.toolBar_replace_comma)
        self.toolBar_insert_orm = QToolBar(TaxationTool)
        self.toolBar_insert_orm.setObjectName(u"toolBar_insert_orm")
        TaxationTool.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar_insert_orm)
        TaxationTool.insertToolBarBreak(self.toolBar_insert_orm)
        self.statusBar = QStatusBar(TaxationTool)
        self.statusBar.setObjectName(u"statusBar")
        TaxationTool.setStatusBar(self.statusBar)

        self.toolBar_import.addAction(self.action_open_excel_template)
        self.toolBar_import.addAction(self.action_import_taxation_list)
        self.toolBar_import.addAction(self.action_import_topographic_plan)
        self.toolBar_import.addAction(self.action_insert_zones)
        self.toolBar_import.addAction(self.action_insert_protected_zones)
        self.toolBar_validation.addAction(self.action_get_count_tree)
        self.toolBar_validation.addAction(self.action_compare_numbers)
        self.toolBar_validation.addAction(self.action_identification_shrub)
        self.toolBar_validation.addAction(self.action_validation)
        self.toolBar_replace_comma.addAction(self.action_replace_comma_to_dot)
        self.toolBar_replace_comma.addAction(self.action_replace_dot_comma_to_comma)
        self.toolBar_insert_orm.addAction(self.action_insert_taxation_list_orm)
        self.toolBar_insert_orm.addAction(self.action_insert_zone_objects)

        self.retranslateUi(TaxationTool)

        self.toolBox.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(TaxationTool)
    # setupUi

    def retranslateUi(self, TaxationTool):
        TaxationTool.setWindowTitle(QCoreApplication.translate("TaxationTool", u"TaxationTool", None))
        self.action_import_taxation_list.setText(QCoreApplication.translate("TaxationTool", u"\u0418\u043c\u043f\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0432\u0435\u0434\u043e\u043c\u043e\u0441\u0442\u044c", None))
        self.action_import_topographic_plan.setText(QCoreApplication.translate("TaxationTool", u"\u0412\u0441\u0442\u0430\u0432\u0438\u0442\u044c \u0434\u0430\u043d\u043d\u044b\u0435 \u0441 \u043f\u043b\u0430\u043d\u0430", None))
#if QT_CONFIG(tooltip)
        self.action_import_topographic_plan.setToolTip(QCoreApplication.translate("TaxationTool", u"\u0418\u043c\u043f\u043e\u0440\u0442 \u0442\u043e\u043f\u043e\u0433\u0440\u0430\u0444\u0438\u0447\u0435\u0441\u043a\u043e\u0433\u043e \u043f\u043b\u0430\u043d\u0430", None))
#endif // QT_CONFIG(tooltip)
        self.action_get_count_tree.setText(QCoreApplication.translate("TaxationTool", u"\u041f\u043e\u0434\u0441\u0447\u0438\u0442\u0430\u0442\u044c \u0434\u0435\u0440\u0435\u0432\u044c\u044f", None))
#if QT_CONFIG(tooltip)
        self.action_get_count_tree.setToolTip(QCoreApplication.translate("TaxationTool", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">\u041f\u043e\u0434\u0441\u0447\u0438\u0442\u0430\u0442\u044c \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0434\u0435\u0440\u0435\u0432\u044c\u0435\u0432 \u0432 \u0432\u044b\u0434\u0435\u043b\u0435\u043d\u043d\u043e\u0439 \u043a\u043e\u043b\u043e\u043d\u043a\u0435</span></p><p><br/></p><p>\u0412\u044b\u0434\u0435\u043b\u0438\u0442\u0435 \u0432 Excel \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f \u0438\u0437 \u043a\u043e\u043b\u043e\u043d\u043a\u0438 <span style=\" font-style:italic;\">\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e</span> \u043d\u0430 \u043b\u0438\u0441\u0442\u0435 <span style=\" font-style:italic;\">\u0412\u0435\u0434\u043e\u043c\u043e\u0441\u0442\u044c</span>. \u041f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0430 \u043f\u0440\u043e\u0438\u0437\u0432\u0435\u0434\u0435\u0442 \u0440\u0430\u0441\u0447\u0435\u0442 \u0438 \u0432\u044b\u0432\u0435\u0434\u0435\u0442 \u043e\u043a\u043d\u043e \u0441"
                        " \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u043e\u043c \u043f\u043e\u0434\u0441\u0447\u0435\u0442\u0430.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.action_species_and_types.setText(QCoreApplication.translate("TaxationTool", u"\u041f\u043e\u0440\u043e\u0434\u044b \u0438 \u0442\u0438\u043f\u044b \u041e\u0420\u041c", None))
        self.action_identification_shrub.setText(QCoreApplication.translate("TaxationTool", u"\u041e\u043f\u0440\u0435\u0434\u0435\u043b\u0438\u0442\u044c \u043a\u0443\u0441\u0442\u0430\u0440\u043d\u0438\u043a", None))
#if QT_CONFIG(tooltip)
        self.action_identification_shrub.setToolTip(QCoreApplication.translate("TaxationTool", u"\u041e\u043f\u0440\u0435\u0434\u0435\u043b\u0438\u0442\u044c \u043a\u0443\u0441\u0442\u0430\u0440\u043d\u0438\u043a", None))
#endif // QT_CONFIG(tooltip)
        self.action_replace_comma_to_dot.setText(QCoreApplication.translate("TaxationTool", u"\u0417\u0430\u043c\u0435\u043d\u0438\u0442\u044c \u0417\u0430\u043f\u044f\u0442\u0443\u044e \u043d\u0430 \u0422\u043e\u0447\u043a\u0443", None))
#if QT_CONFIG(tooltip)
        self.action_replace_comma_to_dot.setToolTip(QCoreApplication.translate("TaxationTool", u"\u0417\u0430\u043c\u0435\u043d\u0438\u0442\u044c \u0417\u0430\u043f\u044f\u0442\u0443\u044e \u043d\u0430 \u0422\u043e\u0447\u043a\u0443", None))
#endif // QT_CONFIG(tooltip)
        self.action_replace_dot_comma_to_comma.setText(QCoreApplication.translate("TaxationTool", u"\u0417\u0430\u043c\u0435\u043d\u0438\u0442\u044c \u0422\u043e\u0447\u043a\u0443 \u0441 \u0437\u0430\u043f\u044f\u0442\u043e\u0439 \u043d\u0430 \u0417\u0430\u043f\u044f\u0442\u0443\u044e", None))
#if QT_CONFIG(tooltip)
        self.action_replace_dot_comma_to_comma.setToolTip(QCoreApplication.translate("TaxationTool", u"\u0417\u0430\u043c\u0435\u043d\u0438\u0442\u044c \u0422\u043e\u0447\u043a\u0443 \u0441 \u0437\u0430\u043f\u044f\u0442\u043e\u0439 \u043d\u0430 \u0417\u0430\u043f\u044f\u0442\u0443\u044e", None))
#endif // QT_CONFIG(tooltip)
        self.action_validation.setText(QCoreApplication.translate("TaxationTool", u"\u041f\u0440\u043e\u0432\u0435\u0440\u0438\u0442\u044c \u0441\u0442\u0440\u043e\u043a\u0443", None))
#if QT_CONFIG(tooltip)
        self.action_validation.setToolTip(QCoreApplication.translate("TaxationTool", u"\u0412\u0430\u043b\u0438\u0434\u0430\u0446\u0438\u044f \u0441\u0442\u0440\u043e\u043a\u0438", None))
#endif // QT_CONFIG(tooltip)
        self.action_compare_numbers.setText(QCoreApplication.translate("TaxationTool", u"\u0421\u0440\u0430\u0432\u043d\u0438\u0442\u044c \u043d\u043e\u043c\u0435\u0440\u0430", None))
#if QT_CONFIG(tooltip)
        self.action_compare_numbers.setToolTip(QCoreApplication.translate("TaxationTool", u"\u0421\u0440\u0430\u0432\u043d\u0438\u0442\u044c \u043d\u0430\u043b\u0438\u0447\u0438\u0435 \u043d\u043e\u043c\u0435\u0440\u043e\u0432 \u0432 Excel \u0438 Autocad", None))
#endif // QT_CONFIG(tooltip)
        self.action_insert_zones.setText(QCoreApplication.translate("TaxationTool", u"\u0412\u0441\u0442\u0430\u0432\u0438\u0442\u044c \u0437\u043e\u043d\u044b", None))
#if QT_CONFIG(tooltip)
        self.action_insert_zones.setToolTip(QCoreApplication.translate("TaxationTool", u"\u0412\u0441\u0442\u0430\u0432\u0438\u0442\u044c \u0437\u043e\u043d\u044b \u0438\u0437 \u0442\u043e\u043f\u043e\u0433\u0440\u0430\u0444\u0438\u0447\u0435\u0441\u043a\u043e\u0433\u043e \u043f\u043b\u0430\u043d\u0430 \u0432 \u0442\u0430\u0431\u043b\u0438\u0446\u0443", None))
#endif // QT_CONFIG(tooltip)
        self.action_insert_taxation_list_orm.setText(QCoreApplication.translate("TaxationTool", u"\u0421\u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0432\u0435\u0434\u043e\u043c\u043e\u0441\u0442\u044c \u041e\u0420\u041c", None))
#if QT_CONFIG(tooltip)
        self.action_insert_taxation_list_orm.setToolTip(QCoreApplication.translate("TaxationTool", u"\u0412\u0441\u0442\u0430\u0432\u043a\u0430 \u0432\u0435\u0434\u043e\u043c\u043e\u0441\u0442\u0438 \u041e\u0420\u041c", None))
#endif // QT_CONFIG(tooltip)
        self.action_insert_protected_zones.setText(QCoreApplication.translate("TaxationTool", u"\u0412\u0441\u0442\u0430\u0432\u0438\u0442\u044c \u043e\u0445\u0440\u0430\u043d\u043d\u044b\u0435 \u0437\u043e\u043d\u044b", None))
#if QT_CONFIG(tooltip)
        self.action_insert_protected_zones.setToolTip(QCoreApplication.translate("TaxationTool", u"\u0412\u0441\u0442\u0430\u0432\u0438\u0442\u044c \u0437\u043e\u043d\u044b \u0438\u0437 \u0442\u043e\u043f\u043e\u0433\u0440\u0430\u0444\u0438\u0447\u0435\u0441\u043a\u043e\u0433\u043e \u043f\u043b\u0430\u043d\u0430 \u0432 \u0442\u0430\u0431\u043b\u0438\u0446\u0443", None))
#endif // QT_CONFIG(tooltip)
        self.action_insert_zone_objects.setText(QCoreApplication.translate("TaxationTool", u"\u0412\u0441\u0442\u0430\u0432\u0438\u0442\u044c \u043e\u0431\u044a\u0435\u043a\u0442\u044b \u0434\u043b\u044f \u0437\u043e\u043d\u044b", None))
#if QT_CONFIG(tooltip)
        self.action_insert_zone_objects.setToolTip(QCoreApplication.translate("TaxationTool", u"\u0412\u0441\u0442\u0430\u0432\u0438\u0442\u044c \u043e\u0431\u044a\u0435\u043a\u0442\u044b \u0434\u043b\u044f \u0437\u043e\u043d\u044b", None))
#endif // QT_CONFIG(tooltip)
        self.action_open_excel_template.setText(QCoreApplication.translate("TaxationTool", u"\u041d\u043e\u0432\u044b\u0439 Excel", None))
#if QT_CONFIG(tooltip)
        self.action_open_excel_template.setToolTip(QCoreApplication.translate("TaxationTool", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0448\u0430\u0431\u043b\u043e\u043d Excel \u0444\u0430\u0439\u043b\u0430", None))
#endif // QT_CONFIG(tooltip)
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), QCoreApplication.translate("TaxationTool", u"\u0412\u0432\u043e\u0434 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("TaxationTool", u"\u0422\u0438\u043f\u044b, \u043f\u043e\u0440\u043e\u0434\u044b", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("TaxationTool", u"\u041f\u043b\u043e\u0442\u043d\u043e\u0441\u0442\u044c \u0434\u0440\u0435\u0432\u0438\u0441\u0438\u043d\u044b", None))
        self.btn_edit_db_2.setText(QCoreApplication.translate("TaxationTool", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QCoreApplication.translate("TaxationTool", u"\u0411\u0430\u0437\u044b \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.textEdit.setHtml(QCoreApplication.translate("TaxationTool", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Consolas'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.toolBar_import.setWindowTitle(QCoreApplication.translate("TaxationTool", u"toolBar", None))
        self.toolBar_validation.setWindowTitle(QCoreApplication.translate("TaxationTool", u"toolBar_2", None))
        self.toolBar_replace_comma.setWindowTitle(QCoreApplication.translate("TaxationTool", u"toolBar", None))
        self.toolBar_insert_orm.setWindowTitle(QCoreApplication.translate("TaxationTool", u"toolBar", None))
    # retranslateUi

