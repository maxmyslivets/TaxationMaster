# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
    QLabel, QLayout, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QSplitter, QStatusBar,
    QTabWidget, QTableWidget, QTableWidgetItem, QTextBrowser,
    QToolBar, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)
import source.view.ui.resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1371, 766)
        icon = QIcon()
        icon.addFile(u":/app/ico/taxation_tool.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.menu_database_species = QAction(MainWindow)
        self.menu_database_species.setObjectName(u"menu_database_species")
        icon1 = QIcon()
        icon1.addFile(u":/database/article.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_database_species.setIcon(icon1)
        self.menu_database_densitys = QAction(MainWindow)
        self.menu_database_densitys.setObjectName(u"menu_database_densitys")
        icon2 = QIcon()
        icon2.addFile(u":/database/file-text.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_database_densitys.setIcon(icon2)
        self.menu_project_new = QAction(MainWindow)
        self.menu_project_new.setObjectName(u"menu_project_new")
        icon3 = QIcon()
        icon3.addFile(u":/project/ico/file.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_project_new.setIcon(icon3)
        self.menu_database_volumes = QAction(MainWindow)
        self.menu_database_volumes.setObjectName(u"menu_database_volumes")
        icon4 = QIcon()
        icon4.addFile(u":/database/book.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_database_volumes.setIcon(icon4)
        self.menu_project_open = QAction(MainWindow)
        self.menu_project_open.setObjectName(u"menu_project_open")
        icon5 = QIcon()
        icon5.addFile(u":/project/ico/folder.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_project_open.setIcon(icon5)
        self.menu_project_import_taxation_plan = QAction(MainWindow)
        self.menu_project_import_taxation_plan.setObjectName(u"menu_project_import_taxation_plan")
        icon6 = QIcon()
        icon6.addFile(u":/project/file-receive.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_project_import_taxation_plan.setIcon(icon6)
        self.menu_processing_preprocessing = QAction(MainWindow)
        self.menu_processing_preprocessing.setObjectName(u"menu_processing_preprocessing")
        icon7 = QIcon()
        icon7.addFile(u":/processing/ico/off-grid.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_processing_preprocessing.setIcon(icon7)
        self.menu_processing_design_objects = QAction(MainWindow)
        self.menu_processing_design_objects.setObjectName(u"menu_processing_design_objects")
        icon8 = QIcon()
        icon8.addFile(u":/processing/inkpen.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_processing_design_objects.setIcon(icon8)
        self.menu_processing_sorted_numeration = QAction(MainWindow)
        self.menu_processing_sorted_numeration.setObjectName(u"menu_processing_sorted_numeration")
        icon9 = QIcon()
        icon9.addFile(u":/processing/stats-pipes.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_processing_sorted_numeration.setIcon(icon9)
        self.menu_processing_design_tables = QAction(MainWindow)
        self.menu_processing_design_tables.setObjectName(u"menu_processing_design_tables")
        icon10 = QIcon()
        icon10.addFile(u":/processing/paper-ruler.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_processing_design_tables.setIcon(icon10)
        self.menu_about = QAction(MainWindow)
        self.menu_about.setObjectName(u"menu_about")
        self.menu_manual = QAction(MainWindow)
        self.menu_manual.setObjectName(u"menu_manual")
        self.menu_project_save_as = QAction(MainWindow)
        self.menu_project_save_as.setObjectName(u"menu_project_save_as")
        icon11 = QIcon()
        icon11.addFile(u":/project/ico/file-save-as.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_project_save_as.setIcon(icon11)
        self.menu_project_save_as.setMenuRole(QAction.MenuRole.NoRole)
        self.menu_settings_settings = QAction(MainWindow)
        self.menu_settings_settings.setObjectName(u"menu_settings_settings")
        icon12 = QIcon()
        icon12.addFile(u":/setting/ico/settings-complex.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_settings_settings.setIcon(icon12)
        self.menu_project_save = QAction(MainWindow)
        self.menu_project_save.setObjectName(u"menu_project_save")
        icon13 = QIcon()
        icon13.addFile(u":/project/ico/file-save.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_project_save.setIcon(icon13)
        self.menu_project_save.setMenuRole(QAction.MenuRole.NoRole)
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
        self.tree_manager.setObjectName(u"tree_manager")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tree_manager.sizePolicy().hasHeightForWidth())
        self.tree_manager.setSizePolicy(sizePolicy1)
        self.tree_manager.setAcceptDrops(False)
        self.tree_manager.setAutoFillBackground(False)
        self.tree_manager.setUniformRowHeights(False)
        self.tree_manager.setItemsExpandable(True)
        self.tree_manager.setSortingEnabled(False)
        self.tree_manager.setHeaderHidden(False)
        self.tree_manager.setExpandsOnDoubleClick(True)
        self.splitter.addWidget(self.tree_manager)
        self.splitter_2 = QSplitter(self.splitter)
        self.splitter_2.setObjectName(u"splitter_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy2)
        self.splitter_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.splitter_2.setOrientation(Qt.Orientation.Vertical)
        self.splitter_2.setOpaqueResize(True)
        self.tabWidget = QTabWidget(self.splitter_2)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy3)
        self.tab_table = QWidget()
        self.tab_table.setObjectName(u"tab_table")
        self.gridLayout_2 = QGridLayout(self.tab_table)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.table = QTableWidget(self.tab_table)
        self.table.setObjectName(u"table")
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setProperty(u"showSortIndicator", False)
        self.table.verticalHeader().setStretchLastSection(False)

        self.gridLayout_2.addWidget(self.table, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_table, "")
        self.splitter_2.addWidget(self.tabWidget)
        self.layoutWidget = QWidget(self.splitter_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.vl3 = QVBoxLayout(self.layoutWidget)
        self.vl3.setObjectName(u"vl3")
        self.vl3.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.vl3.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy4)

        self.vl3.addWidget(self.label)

        self.console_log = QTextBrowser(self.layoutWidget)
        self.console_log.setObjectName(u"console_log")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(1)
        sizePolicy5.setHeightForWidth(self.console_log.sizePolicy().hasHeightForWidth())
        self.console_log.setSizePolicy(sizePolicy5)
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
        self.menu = QMenu(self.menu_project)
        self.menu.setObjectName(u"menu")
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
        self.menu_project.addAction(self.menu_project_save)
        self.menu_project.addAction(self.menu_project_save_as)
        self.menu_project.addSeparator()
        self.menu_project.addAction(self.menu.menuAction())
        self.menu.addAction(self.menu_project_import_taxation_plan)
        self.menu_database.addAction(self.menu_database_species)
        self.menu_database.addAction(self.menu_database_densitys)
        self.menu_database.addAction(self.menu_database_volumes)
        self.menu_settings.addAction(self.menu_settings_settings)
        self.menu_help.addAction(self.menu_about)
        self.menu_help.addAction(self.menu_manual)
        self.menu_processing_2.addAction(self.menu_processing_preprocessing)
        self.menu_processing_2.addAction(self.menu_processing_sorted_numeration)
        self.menu_processing_2.addAction(self.menu_processing_design_objects)
        self.menu_processing_2.addAction(self.menu_processing_design_tables)
        self.toolBar.addAction(self.menu_project_new)
        self.toolBar.addAction(self.menu_project_open)
        self.toolBar.addAction(self.menu_project_save)
        self.toolBar.addAction(self.menu_project_save_as)
        self.toolBar_2.addAction(self.menu_processing_preprocessing)
        self.toolBar_2.addAction(self.menu_processing_sorted_numeration)
        self.toolBar_2.addSeparator()
        self.toolBar_2.addAction(self.menu_processing_design_objects)
        self.toolBar_2.addAction(self.menu_processing_design_tables)
        self.toolBar_2.addSeparator()
        self.toolBar_3.addAction(self.menu_database_species)
        self.toolBar_3.addAction(self.menu_database_densitys)
        self.toolBar_3.addAction(self.menu_database_volumes)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Taxation Tool", None))
        self.menu_database_species.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0440\u043e\u0434\u044b", None))
        self.menu_database_densitys.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043b\u043e\u0442\u043d\u043e\u0441\u0442\u0438", None))
        self.menu_project_new.setText(QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439", None))
        self.menu_database_volumes.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0430\u0431\u043b\u0438\u0446\u0430 \u043e\u0431\u044a\u0435\u043c\u043e\u0432 \u0441\u0442\u0432\u043e\u043b\u043e\u0432", None))
        self.menu_project_open.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c", None))
        self.menu_project_import_taxation_plan.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u043f\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0447\u0435\u0440\u0442\u0435\u0436 \u0442\u0430\u043a\u0441\u0430\u0446\u0438\u0438", None))
#if QT_CONFIG(tooltip)
        self.menu_project_import_taxation_plan.setToolTip(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u043f\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0447\u0435\u0440\u0442\u0435\u0436 \u0442\u0430\u043a\u0441\u0430\u0446\u0438\u0438", None))
#endif // QT_CONFIG(tooltip)
        self.menu_processing_preprocessing.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0435\u0434\u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430", None))
#if QT_CONFIG(tooltip)
        self.menu_processing_preprocessing.setToolTip(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0435\u0434\u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430", None))
#endif // QT_CONFIG(tooltip)
        self.menu_processing_design_objects.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0444\u043e\u0440\u043c\u0438\u0442\u044c \u043e\u0431\u044a\u0435\u043a\u0442\u044b \u0432 \u0447\u0435\u0440\u0442\u0435\u0436", None))
        self.menu_processing_sorted_numeration.setText(QCoreApplication.translate("MainWindow", u"\u0423\u043f\u043e\u0440\u044f\u0434\u043e\u0447\u0438\u0442\u044c \u043d\u0443\u043c\u0435\u0440\u0430\u0446\u0438\u044e", None))
        self.menu_processing_design_tables.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0444\u043e\u0440\u043c\u0438\u0442\u044c \u0442\u0430\u0431\u043b\u0438\u0446\u044b \u0432 \u0447\u0435\u0440\u0442\u0435\u0436", None))
        self.menu_about.setText(QCoreApplication.translate("MainWindow", u"\u041e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0435", None))
        self.menu_manual.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0443\u043a\u043e\u0432\u043e\u0434\u0441\u0442\u0432\u043e", None))
        self.menu_project_save_as.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u043a\u0430\u043a", None))
        self.menu_settings_settings.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.menu_project_save.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
#if QT_CONFIG(tooltip)
        self.menu_project_save.setToolTip(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
#endif // QT_CONFIG(tooltip)
        ___qtreewidgetitem = self.tree_manager.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"\u041c\u0435\u043d\u0435\u0434\u0436\u0435\u0440 \u043f\u0440\u043e\u0435\u043a\u0442\u0430", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_table), QCoreApplication.translate("MainWindow", u"\u0427\u0435\u0440\u0442\u0435\u0436 \u0442\u0430\u043a\u0441\u0430\u0446\u0438\u0438", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0433\u0440\u0435\u0441\u0441", None))
        self.menu_project.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0435\u043a\u0442", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u043f\u043e\u0440\u0442", None))
        self.menu_database.setTitle(QCoreApplication.translate("MainWindow", u"\u0411\u0430\u0437\u044b \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.menu_settings.setTitle(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u043f\u0440\u0430\u0432\u043a\u0430", None))
        self.menu_processing_2.setTitle(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
        self.toolBar_2.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar_2", None))
        self.toolBar_3.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar_3", None))
    # retranslateUi

