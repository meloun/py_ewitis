# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ewitis.ui'
#
# Created: Wed Dec 08 16:34:12 2010
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1099, 502)
        font = QtGui.QFont()
        MainWindow.setFont(font)
        MainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 1081, 421))
        self.tabWidget.setObjectName("tabWidget")
        self.tabRuns_Times = QtGui.QWidget()
        self.tabRuns_Times.setObjectName("tabRuns_Times")
        self.RunsFilterLineEdit = QtGui.QLineEdit(self.tabRuns_Times)
        self.RunsFilterLineEdit.setGeometry(QtCore.QRect(10, 10, 113, 20))
        self.RunsFilterLineEdit.setObjectName("RunsFilterLineEdit")
        self.RunsProxyView = QtGui.QTreeView(self.tabRuns_Times)
        self.RunsProxyView.setGeometry(QtCore.QRect(10, 30, 481, 321))
        self.RunsProxyView.setObjectName("RunsProxyView")
        self.TimesFilterLineEdit = QtGui.QLineEdit(self.tabRuns_Times)
        self.TimesFilterLineEdit.setGeometry(QtCore.QRect(510, 10, 113, 20))
        self.TimesFilterLineEdit.setObjectName("TimesFilterLineEdit")
        self.TimesProxyView = QtGui.QTreeView(self.tabRuns_Times)
        self.TimesProxyView.setGeometry(QtCore.QRect(510, 30, 551, 321))
        self.TimesProxyView.setObjectName("TimesProxyView")
        self.pushButton = QtGui.QPushButton(self.tabRuns_Times)
        self.pushButton.setGeometry(QtCore.QRect(10, 350, 31, 31))
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../_meloun/myPython/ewitis/src/ewitis/gui/img/list-add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(32, 32))
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_6 = QtGui.QPushButton(self.tabRuns_Times)
        self.pushButton_6.setGeometry(QtCore.QRect(40, 350, 31, 31))
        self.pushButton_6.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../../../../../_meloun/myPython/ewitis/src/ewitis/gui/img/list-remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon1)
        self.pushButton_6.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_6.setFlat(True)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_2 = QtGui.QPushButton(self.tabRuns_Times)
        self.pushButton_2.setGeometry(QtCore.QRect(510, 350, 31, 31))
        self.pushButton_2.setText("")
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_7 = QtGui.QPushButton(self.tabRuns_Times)
        self.pushButton_7.setGeometry(QtCore.QRect(540, 350, 31, 31))
        self.pushButton_7.setText("")
        self.pushButton_7.setIcon(icon1)
        self.pushButton_7.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_7.setFlat(True)
        self.pushButton_7.setObjectName("pushButton_7")
        self.tabWidget.addTab(self.tabRuns_Times, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.UsersProxyView = QtGui.QTreeView(self.tab_2)
        self.UsersProxyView.setGeometry(QtCore.QRect(10, 30, 841, 321))
        self.UsersProxyView.setObjectName("UsersProxyView")
        self.UsersFilterLineEdit = QtGui.QLineEdit(self.tab_2)
        self.UsersFilterLineEdit.setGeometry(QtCore.QRect(10, 10, 113, 20))
        self.UsersFilterLineEdit.setObjectName("UsersFilterLineEdit")
        self.pushButton_3 = QtGui.QPushButton(self.tab_2)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 350, 31, 31))
        self.pushButton_3.setText("")
        self.pushButton_3.setIcon(icon)
        self.pushButton_3.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_3.setFlat(True)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_8 = QtGui.QPushButton(self.tab_2)
        self.pushButton_8.setGeometry(QtCore.QRect(40, 350, 31, 31))
        self.pushButton_8.setText("")
        self.pushButton_8.setIcon(icon1)
        self.pushButton_8.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_8.setFlat(True)
        self.pushButton_8.setObjectName("pushButton_8")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1099, 20))
        self.menubar.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar_Port = QtGui.QToolBar(MainWindow)
        self.toolBar_Port.setEnabled(True)
        self.toolBar_Port.setObjectName("toolBar_Port")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar_Port)
        self.toolBar_Modes = QtGui.QToolBar(MainWindow)
        self.toolBar_Modes.setObjectName("toolBar_Modes")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar_Modes)
        self.aSetPort = QtGui.QAction(MainWindow)
        self.aSetPort.setEnabled(True)
        self.aSetPort.setObjectName("aSetPort")
        self.aConnectPort = QtGui.QAction(MainWindow)
        self.aConnectPort.setObjectName("aConnectPort")
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionHelo = QtGui.QAction(MainWindow)
        self.actionHelo.setObjectName("actionHelo")
        self.aRefresh = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("ewitis/gui/img/view-refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aRefresh.setIcon(icon2)
        self.aRefresh.setObjectName("aRefresh")
        self.aEditMode = QtGui.QAction(MainWindow)
        self.aEditMode.setCheckable(True)
        self.aEditMode.setChecked(True)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("ewitis/gui/img/pencil2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aEditMode.setIcon(icon3)
        self.aEditMode.setObjectName("aEditMode")
        self.aRefreshMode = QtGui.QAction(MainWindow)
        self.aRefreshMode.setCheckable(True)
        self.aRefreshMode.setChecked(False)
        self.aRefreshMode.setIcon(icon2)
        self.aRefreshMode.setIconVisibleInMenu(True)
        self.aRefreshMode.setObjectName("aRefreshMode")
        self.menuAbout.addAction(self.actionHelo)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.toolBar_Port.addAction(self.aSetPort)
        self.toolBar_Port.addSeparator()
        self.toolBar_Port.addAction(self.aConnectPort)
        self.toolBar_Modes.addAction(self.aEditMode)
        self.toolBar_Modes.addAction(self.aRefreshMode)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        MainWindow.setToolTip(QtGui.QApplication.translate("MainWindow", "Smazat vybran├Ż z├íznam", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setToolTip(QtGui.QApplication.translate("MainWindow", "Vlo┼żit z├íznam", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setToolTip(QtGui.QApplication.translate("MainWindow", "Vlo┼żit z├íznam", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabRuns_Times), QtGui.QApplication.translate("MainWindow", "Runs#Times", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setToolTip(QtGui.QApplication.translate("MainWindow", "Vlo┼żit z├íznam", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Users", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Menu1", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAbout.setTitle(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar_Port.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar_2", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar_Modes.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar_2", None, QtGui.QApplication.UnicodeUTF8))
        self.aSetPort.setText(QtGui.QApplication.translate("MainWindow", "PORT", None, QtGui.QApplication.UnicodeUTF8))
        self.aConnectPort.setText(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.aConnectPort.setToolTip(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelo.setText(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.aRefresh.setText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.aRefresh.setToolTip(QtGui.QApplication.translate("MainWindow", "Refresh (F5)", None, QtGui.QApplication.UnicodeUTF8))
        self.aRefresh.setShortcut(QtGui.QApplication.translate("MainWindow", "F5", None, QtGui.QApplication.UnicodeUTF8))
        self.aEditMode.setText(QtGui.QApplication.translate("MainWindow", "Editing mode", None, QtGui.QApplication.UnicodeUTF8))
        self.aEditMode.setToolTip(QtGui.QApplication.translate("MainWindow", "EDIT mode", None, QtGui.QApplication.UnicodeUTF8))
        self.aRefreshMode.setText(QtGui.QApplication.translate("MainWindow", "Refreshing mode", None, QtGui.QApplication.UnicodeUTF8))
        self.aRefreshMode.setToolTip(QtGui.QApplication.translate("MainWindow", "REFRESH mode", None, QtGui.QApplication.UnicodeUTF8))