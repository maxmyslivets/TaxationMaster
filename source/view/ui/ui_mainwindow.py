# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowJmwfVF.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QProgressBar, QSizePolicy, QSpacerItem, QStatusBar,
    QTextBrowser, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)
import source.view.ui.resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1219, 820)
        icon = QIcon()
        icon.addFile(u":/icons/ico/taxation_tool.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.menu_database_species = QAction(MainWindow)
        self.menu_database_species.setObjectName(u"menu_database_species")
        self.menu_database_densitys = QAction(MainWindow)
        self.menu_database_densitys.setObjectName(u"menu_database_densitys")
        self.action_3 = QAction(MainWindow)
        self.action_3.setObjectName(u"action_3")
        self.menu_settings_paths = QAction(MainWindow)
        self.menu_settings_paths.setObjectName(u"menu_settings_paths")
        self.menu_database_volumes = QAction(MainWindow)
        self.menu_database_volumes.setObjectName(u"menu_database_volumes")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 0, 1201, 761))
        self.hl1 = QHBoxLayout(self.widget)
        self.hl1.setObjectName(u"hl1")
        self.hl1.setContentsMargins(0, 0, 0, 0)
        self.vl1 = QVBoxLayout()
        self.vl1.setObjectName(u"vl1")
        self.tree_file_manager = QTreeWidget(self.widget)
        QTreeWidgetItem(self.tree_file_manager)
        __qtreewidgetitem = QTreeWidgetItem(self.tree_file_manager)
        __qtreewidgetitem1 = QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(self.tree_file_manager)
        __qtreewidgetitem2 = QTreeWidgetItem(self.tree_file_manager)
        QTreeWidgetItem(__qtreewidgetitem2)
        __qtreewidgetitem3 = QTreeWidgetItem(self.tree_file_manager)
        QTreeWidgetItem(__qtreewidgetitem3)
        QTreeWidgetItem(__qtreewidgetitem3)
        QTreeWidgetItem(self.tree_file_manager)
        QTreeWidgetItem(self.tree_file_manager)
        self.tree_file_manager.setObjectName(u"tree_file_manager")

        self.vl1.addWidget(self.tree_file_manager)

        self.tree_file_manager_temp = QTreeWidget(self.widget)
        QTreeWidgetItem(self.tree_file_manager_temp)
        QTreeWidgetItem(self.tree_file_manager_temp)
        __qtreewidgetitem4 = QTreeWidgetItem(self.tree_file_manager_temp)
        QTreeWidgetItem(__qtreewidgetitem4)
        QTreeWidgetItem(__qtreewidgetitem4)
        QTreeWidgetItem(self.tree_file_manager_temp)
        __qtreewidgetitem5 = QTreeWidgetItem(self.tree_file_manager_temp)
        QTreeWidgetItem(__qtreewidgetitem5)
        QTreeWidgetItem(self.tree_file_manager_temp)
        self.tree_file_manager_temp.setObjectName(u"tree_file_manager_temp")
        self.tree_file_manager_temp.setColumnCount(1)

        self.vl1.addWidget(self.tree_file_manager_temp)


        self.hl1.addLayout(self.vl1)

        self.line_v = QFrame(self.widget)
        self.line_v.setObjectName(u"line_v")
        self.line_v.setWindowModality(Qt.WindowModality.NonModal)
        self.line_v.setCursor(QCursor(Qt.CursorShape.SizeHorCursor))
        self.line_v.setMouseTracking(False)
        self.line_v.setAcceptDrops(False)
        self.line_v.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_v.setFrameShape(QFrame.Shape.VLine)

        self.hl1.addWidget(self.line_v)

        self.vl2 = QVBoxLayout()
        self.vl2.setObjectName(u"vl2")
        self.frame_work = QFrame(self.widget)
        self.frame_work.setObjectName(u"frame_work")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_work.sizePolicy().hasHeightForWidth())
        self.frame_work.setSizePolicy(sizePolicy)
        self.frame_work.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_work.setFrameShadow(QFrame.Shadow.Raised)
        self.label_3 = QLabel(self.frame_work)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(250, 170, 81, 16))

        self.vl2.addWidget(self.frame_work)

        self.vl3 = QVBoxLayout()
        self.vl3.setObjectName(u"vl3")
        self.hl2 = QHBoxLayout()
        self.hl2.setObjectName(u"hl2")
        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.hl2.addWidget(self.label_5)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.hl2.addItem(self.horizontalSpacer_2)

        self.progressBar_3 = QProgressBar(self.widget)
        self.progressBar_3.setObjectName(u"progressBar_3")
        self.progressBar_3.setValue(0)
        self.progressBar_3.setTextVisible(False)
        self.progressBar_3.setInvertedAppearance(False)

        self.hl2.addWidget(self.progressBar_3)


        self.vl3.addLayout(self.hl2)

        self.console_log = QTextBrowser(self.widget)
        self.console_log.setObjectName(u"console_log")
        font = QFont()
        font.setPointSize(8)
        self.console_log.setFont(font)
        self.console_log.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.IBeamCursor))
        self.console_log.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.vl3.addWidget(self.console_log)


        self.vl2.addLayout(self.vl3)


        self.hl1.addLayout(self.vl2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1219, 33))
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_database = QMenu(self.menubar)
        self.menu_database.setObjectName(u"menu_database")
        self.menu_settings = QMenu(self.menubar)
        self.menu_settings.setObjectName(u"menu_settings")
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName(u"menu_help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_database.menuAction())
        self.menubar.addAction(self.menu_settings.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.action_3)
        self.menu_database.addAction(self.menu_database_species)
        self.menu_database.addAction(self.menu_database_densitys)
        self.menu_database.addSeparator()
        self.menu_database.addAction(self.menu_database_volumes)
        self.menu_settings.addAction(self.menu_settings_paths)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Taxation Tool", None))
        self.menu_database_species.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0440\u043e\u0434\u044b", None))
        self.menu_database_densitys.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043b\u043e\u0442\u043d\u043e\u0441\u0442\u0438", None))
        self.action_3.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0444\u0430\u0439\u043b\u044b", None))
        self.menu_settings_paths.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0443\u0442\u0438", None))
        self.menu_database_volumes.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0430\u0431\u043b\u0438\u0446\u0430 \u043e\u0431\u044a\u0435\u043c\u043e\u0432 \u0441\u0442\u0432\u043e\u043b\u043e\u0432", None))
        ___qtreewidgetitem = self.tree_file_manager.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"\u041c\u0435\u043d\u0435\u0434\u0436\u0435\u0440 \u0444\u0430\u0439\u043b\u043e\u0432", None));

        __sortingEnabled = self.tree_file_manager.isSortingEnabled()
        self.tree_file_manager.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.tree_file_manager.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        ___qtreewidgetitem2 = self.tree_file_manager.topLevelItem(1)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        ___qtreewidgetitem3 = ___qtreewidgetitem2.child(0)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u0434\u043e\u0447\u0435\u0440\u043d\u0438\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        ___qtreewidgetitem4 = ___qtreewidgetitem3.child(0)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u0434\u043e\u0447\u0435\u0440\u043d\u0438\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        ___qtreewidgetitem5 = self.tree_file_manager.topLevelItem(2)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        ___qtreewidgetitem6 = self.tree_file_manager.topLevelItem(3)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        ___qtreewidgetitem7 = ___qtreewidgetitem6.child(0)
        ___qtreewidgetitem7.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u0434\u043e\u0447\u0435\u0440\u043d\u0438\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        ___qtreewidgetitem8 = self.tree_file_manager.topLevelItem(4)
        ___qtreewidgetitem8.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        ___qtreewidgetitem9 = ___qtreewidgetitem8.child(0)
        ___qtreewidgetitem9.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u0434\u043e\u0447\u0435\u0440\u043d\u0438\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        ___qtreewidgetitem10 = ___qtreewidgetitem8.child(1)
        ___qtreewidgetitem10.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u0434\u043e\u0447\u0435\u0440\u043d\u0438\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        ___qtreewidgetitem11 = self.tree_file_manager.topLevelItem(5)
        ___qtreewidgetitem11.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        ___qtreewidgetitem12 = self.tree_file_manager.topLevelItem(6)
        ___qtreewidgetitem12.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        self.tree_file_manager.setSortingEnabled(__sortingEnabled)

        ___qtreewidgetitem13 = self.tree_file_manager_temp.headerItem()
        ___qtreewidgetitem13.setText(0, QCoreApplication.translate("MainWindow", u"\u0412\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0435 \u0444\u0430\u0439\u043b\u044b", None));

        __sortingEnabled1 = self.tree_file_manager_temp.isSortingEnabled()
        self.tree_file_manager_temp.setSortingEnabled(False)
        ___qtreewidgetitem14 = self.tree_file_manager_temp.topLevelItem(0)
        ___qtreewidgetitem14.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        ___qtreewidgetitem15 = self.tree_file_manager_temp.topLevelItem(1)
        ___qtreewidgetitem15.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        ___qtreewidgetitem16 = self.tree_file_manager_temp.topLevelItem(2)
        ___qtreewidgetitem16.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        ___qtreewidgetitem17 = ___qtreewidgetitem16.child(0)
        ___qtreewidgetitem17.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u0434\u043e\u0447\u0435\u0440\u043d\u0438\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        ___qtreewidgetitem18 = ___qtreewidgetitem16.child(1)
        ___qtreewidgetitem18.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u0434\u043e\u0447\u0435\u0440\u043d\u0438\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        ___qtreewidgetitem19 = self.tree_file_manager_temp.topLevelItem(3)
        ___qtreewidgetitem19.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        ___qtreewidgetitem20 = self.tree_file_manager_temp.topLevelItem(4)
        ___qtreewidgetitem20.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        ___qtreewidgetitem21 = ___qtreewidgetitem20.child(0)
        ___qtreewidgetitem21.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u0434\u043e\u0447\u0435\u0440\u043d\u0438\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        ___qtreewidgetitem22 = self.tree_file_manager_temp.topLevelItem(5)
        ___qtreewidgetitem22.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        self.tree_file_manager_temp.setSortingEnabled(__sortingEnabled1)

        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0430\u0431\u043e\u0447\u0430\u044f \u0437\u043e\u043d\u0430", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0446\u0435\u0441\u0441 \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f", None))
        self.progressBar_3.setFormat(QCoreApplication.translate("MainWindow", u"%p%", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
        self.menu_database.setTitle(QCoreApplication.translate("MainWindow", u"\u0411\u0430\u0437\u044b \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.menu_settings.setTitle(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u043f\u0440\u0430\u0432\u043a\u0430", None))
    # retranslateUi

