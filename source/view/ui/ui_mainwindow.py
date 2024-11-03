# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowaClpNK.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHeaderView,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QSplitter, QStatusBar, QTabWidget,
    QTextBrowser, QToolBar, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)
import source.view.ui.resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1371, 766)
        icon = QIcon()
        icon.addFile(u":/icons/ico/taxation_tool.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.menu_database_species = QAction(MainWindow)
        self.menu_database_species.setObjectName(u"menu_database_species")
        self.menu_database_densitys = QAction(MainWindow)
        self.menu_database_densitys.setObjectName(u"menu_database_densitys")
        self.menu_project_new = QAction(MainWindow)
        self.menu_project_new.setObjectName(u"menu_project_new")
        self.menu_settings_paths = QAction(MainWindow)
        self.menu_settings_paths.setObjectName(u"menu_settings_paths")
        self.menu_database_volumes = QAction(MainWindow)
        self.menu_database_volumes.setObjectName(u"menu_database_volumes")
        self.menu_processing = QAction(MainWindow)
        self.menu_processing.setObjectName(u"menu_processing")
        self.menu_processing.setMenuRole(QAction.MenuRole.NoRole)
        self.menu_project_open = QAction(MainWindow)
        self.menu_project_open.setObjectName(u"menu_project_open")
        self.menu_project_import = QAction(MainWindow)
        self.menu_project_import.setObjectName(u"menu_project_import")
        self.menu_project_export = QAction(MainWindow)
        self.menu_project_export.setObjectName(u"menu_project_export")
        self.menu_processing_classification = QAction(MainWindow)
        self.menu_processing_classification.setObjectName(u"menu_processing_classification")
        self.menu_processing_design_objects = QAction(MainWindow)
        self.menu_processing_design_objects.setObjectName(u"menu_processing_design_objects")
        self.menu_processing_sorted_numeration = QAction(MainWindow)
        self.menu_processing_sorted_numeration.setObjectName(u"menu_processing_sorted_numeration")
        self.menu_processing_design_tables = QAction(MainWindow)
        self.menu_processing_design_tables.setObjectName(u"menu_processing_design_tables")
        self.menu_about = QAction(MainWindow)
        self.menu_about.setObjectName(u"menu_about")
        self.menu_manual = QAction(MainWindow)
        self.menu_manual.setObjectName(u"menu_manual")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.tree_manager = QTreeWidget(self.splitter)
        QTreeWidgetItem(self.tree_manager)
        QTreeWidgetItem(self.tree_manager)
        __qtreewidgetitem = QTreeWidgetItem(self.tree_manager)
        QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem)
        self.tree_manager.setObjectName(u"tree_manager")
        self.splitter.addWidget(self.tree_manager)
        self.splitter_2 = QSplitter(self.splitter)
        self.splitter_2.setObjectName(u"splitter_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy1)
        self.splitter_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.splitter_2.setOrientation(Qt.Orientation.Vertical)
        self.tabWidget = QTabWidget(self.splitter_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_model = QWidget()
        self.tab_model.setObjectName(u"tab_model")
        self.tabWidget.addTab(self.tab_model, "")
        self.tab_table = QWidget()
        self.tab_table.setObjectName(u"tab_table")
        self.tabWidget.addTab(self.tab_table, "")
        self.splitter_2.addWidget(self.tabWidget)
        self.layoutWidget = QWidget(self.splitter_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.vl3 = QVBoxLayout(self.layoutWidget)
        self.vl3.setObjectName(u"vl3")
        self.vl3.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.vl3.addWidget(self.label)

        self.console_log = QTextBrowser(self.layoutWidget)
        self.console_log.setObjectName(u"console_log")
        font = QFont()
        font.setPointSize(8)
        self.console_log.setFont(font)
        self.console_log.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.IBeamCursor))
        self.console_log.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.vl3.addWidget(self.console_log)

        self.splitter_2.addWidget(self.layoutWidget)
        self.splitter.addWidget(self.splitter_2)

        self.gridLayout.addWidget(self.splitter, 0, 2, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1371, 33))
        self.menu_project = QMenu(self.menubar)
        self.menu_project.setObjectName(u"menu_project")
        self.menu_database = QMenu(self.menubar)
        self.menu_database.setObjectName(u"menu_database")
        self.menu_settings = QMenu(self.menubar)
        self.menu_settings.setObjectName(u"menu_settings")
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName(u"menu_help")
        self.menu_processing_2 = QMenu(self.menubar)
        self.menu_processing_2.setObjectName(u"menu_processing_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.toolBar_2 = QToolBar(MainWindow)
        self.toolBar_2.setObjectName(u"toolBar_2")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar_2)
        self.toolBar_3 = QToolBar(MainWindow)
        self.toolBar_3.setObjectName(u"toolBar_3")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar_3)

        self.menubar.addAction(self.menu_project.menuAction())
        self.menubar.addAction(self.menu_processing_2.menuAction())
        self.menubar.addAction(self.menu_database.menuAction())
        self.menubar.addAction(self.menu_settings.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_project.addAction(self.menu_project_new)
        self.menu_project.addAction(self.menu_project_open)
        self.menu_project.addSeparator()
        self.menu_project.addAction(self.menu_project_import)
        self.menu_project.addAction(self.menu_project_export)
        self.menu_database.addAction(self.menu_database_species)
        self.menu_database.addAction(self.menu_database_densitys)
        self.menu_database.addAction(self.menu_database_volumes)
        self.menu_settings.addAction(self.menu_settings_paths)
        self.menu_help.addAction(self.menu_about)
        self.menu_help.addAction(self.menu_manual)
        self.menu_processing_2.addAction(self.menu_processing_classification)
        self.menu_processing_2.addAction(self.menu_processing_sorted_numeration)
        self.menu_processing_2.addAction(self.menu_processing_design_objects)
        self.menu_processing_2.addAction(self.menu_processing_design_tables)
        self.toolBar.addAction(self.menu_project_new)
        self.toolBar.addAction(self.menu_project_open)
        self.toolBar_2.addAction(self.menu_processing_classification)
        self.toolBar_2.addAction(self.menu_processing_sorted_numeration)
        self.toolBar_2.addAction(self.menu_processing_design_objects)
        self.toolBar_2.addAction(self.menu_processing_design_tables)
        self.toolBar_2.addSeparator()
        self.toolBar_3.addAction(self.menu_database_species)
        self.toolBar_3.addAction(self.menu_database_densitys)
        self.toolBar_3.addAction(self.menu_database_volumes)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Taxation Tool", None))
        self.menu_database_species.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0440\u043e\u0434\u044b", None))
        self.menu_database_densitys.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043b\u043e\u0442\u043d\u043e\u0441\u0442\u0438", None))
        self.menu_project_new.setText(QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439", None))
        self.menu_settings_paths.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0443\u0442\u0438", None))
        self.menu_database_volumes.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0430\u0431\u043b\u0438\u0446\u0430 \u043e\u0431\u044a\u0435\u043c\u043e\u0432 \u0441\u0442\u0432\u043e\u043b\u043e\u0432", None))
        self.menu_processing.setText(QCoreApplication.translate("MainWindow", u"\u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430", None))
        self.menu_project_open.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c", None))
        self.menu_project_import.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u043f\u043e\u0440\u0442...", None))
        self.menu_project_export.setText(QCoreApplication.translate("MainWindow", u"\u042d\u043a\u0441\u043f\u043e\u0440\u0442...", None))
        self.menu_processing_classification.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043b\u0430\u0441\u0441\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u043f\u043e \u0437\u043e\u043d\u0430\u043c", None))
        self.menu_processing_design_objects.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0444\u043e\u0440\u043c\u0438\u0442\u044c \u043e\u0431\u044a\u0435\u043a\u0442\u044b \u0432 \u0447\u0435\u0440\u0442\u0435\u0436", None))
        self.menu_processing_sorted_numeration.setText(QCoreApplication.translate("MainWindow", u"\u0423\u043f\u043e\u0440\u044f\u0434\u043e\u0447\u0438\u0442\u044c \u043d\u0443\u043c\u0435\u0440\u0430\u0446\u0438\u044e", None))
        self.menu_processing_design_tables.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0444\u043e\u0440\u043c\u0438\u0442\u044c \u0442\u0430\u0431\u043b\u0438\u0446\u044b \u0432 \u0447\u0435\u0440\u0442\u0435\u0436", None))
        self.menu_about.setText(QCoreApplication.translate("MainWindow", u"\u041e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0435", None))
        self.menu_manual.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0443\u043a\u043e\u0432\u043e\u0434\u0441\u0442\u0432\u043e", None))
        ___qtreewidgetitem = self.tree_manager.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"\u041c\u0435\u043d\u0435\u0434\u0436\u0435\u0440 \u043f\u0440\u043e\u0435\u043a\u0442\u0430", None));

        __sortingEnabled = self.tree_manager.isSortingEnabled()
        self.tree_manager.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.tree_manager.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"\u0427\u0435\u0440\u0442\u0435\u0436 \u0442\u0430\u043a\u0441\u0430\u0446\u0438\u0438 (dxf)", None));
        ___qtreewidgetitem2 = self.tree_manager.topLevelItem(1)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("MainWindow", u"\u0412\u0435\u0434\u043e\u043c\u043e\u0441\u0442\u044c \u0442\u0430\u043a\u0441\u0430\u0446\u0438\u0438 (xslx)", None));
        ___qtreewidgetitem3 = self.tree_manager.topLevelItem(2)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("MainWindow", u"\u0422\u0430\u0431\u043b\u0438\u0446\u044b \u043e\u0431\u044a\u0435\u043a\u0442\u043e\u0432 \u0442\u0430\u043a\u0441\u0430\u0446\u0438\u0438", None));
        ___qtreewidgetitem4 = ___qtreewidgetitem3.child(0)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("MainWindow", u"\u0417\u043e\u043d\u0430 \u0431\u043b\u0430\u0433\u043e\u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u0430", None));
        ___qtreewidgetitem5 = ___qtreewidgetitem3.child(1)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("MainWindow", u"\u0417\u043e\u043d\u0430 \u0443\u043b. \u041c\u043e\u043b\u043e\u0434\u0435\u0436\u043d\u0430\u044f", None));
        self.tree_manager.setSortingEnabled(__sortingEnabled)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_model), QCoreApplication.translate("MainWindow", u"\u041c\u043e\u0434\u0435\u043b\u044c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_table), QCoreApplication.translate("MainWindow", u"\u0422\u0430\u0431\u043b\u0438\u0446\u0430", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0433\u0440\u0435\u0441\u0441", None))
        self.menu_project.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0435\u043a\u0442", None))
        self.menu_database.setTitle(QCoreApplication.translate("MainWindow", u"\u0411\u0430\u0437\u044b \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.menu_settings.setTitle(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u043f\u0440\u0430\u0432\u043a\u0430", None))
        self.menu_processing_2.setTitle(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
        self.toolBar_2.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar_2", None))
        self.toolBar_3.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar_3", None))
    # retranslateUi

