# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ewitis.ui'
#
# Created: Sat Jan 08 10:27:16 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1105, 504)
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
        self.RunsFilterClear = QtGui.QPushButton(self.tabRuns_Times)
        self.RunsFilterClear.setGeometry(QtCore.QRect(123, 10, 21, 21))
        self.RunsFilterClear.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../_meloun/myPython/ewitis/src/ewitis/gui/img/mail-delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RunsFilterClear.setIcon(icon)
        self.RunsFilterClear.setIconSize(QtCore.QSize(16, 16))
        self.RunsFilterClear.setFlat(True)
        self.RunsFilterClear.setObjectName("RunsFilterClear")
        self.RunsIcons = QtGui.QGroupBox(self.tabRuns_Times)
        self.RunsIcons.setGeometry(QtCore.QRect(300, 0, 191, 29))
        self.RunsIcons.setTitle("")
        self.RunsIcons.setObjectName("RunsIcons")
        self.RunsExport = QtGui.QPushButton(self.RunsIcons)
        self.RunsExport.setGeometry(QtCore.QRect(80, 0, 31, 31))
        self.RunsExport.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../../../../../_meloun/myPython/ewitis/src/ewitis/gui/img/export.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RunsExport.setIcon(icon1)
        self.RunsExport.setIconSize(QtCore.QSize(24, 24))
        self.RunsExport.setFlat(True)
        self.RunsExport.setObjectName("RunsExport")
        self.RunsImport = QtGui.QPushButton(self.RunsIcons)
        self.RunsImport.setGeometry(QtCore.QRect(120, 0, 31, 31))
        self.RunsImport.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../../../../../_meloun/myPython/ewitis/src/ewitis/gui/img/import.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RunsImport.setIcon(icon2)
        self.RunsImport.setIconSize(QtCore.QSize(24, 24))
        self.RunsImport.setFlat(True)
        self.RunsImport.setObjectName("RunsImport")
        self.RunsAdd = QtGui.QPushButton(self.RunsIcons)
        self.RunsAdd.setGeometry(QtCore.QRect(0, 0, 31, 31))
        self.RunsAdd.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../../../../../_meloun/myPython/ewitis/src/ewitis/gui/img/list-add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RunsAdd.setIcon(icon3)
        self.RunsAdd.setIconSize(QtCore.QSize(32, 32))
        self.RunsAdd.setFlat(True)
        self.RunsAdd.setObjectName("RunsAdd")
        self.RunsRemove = QtGui.QPushButton(self.RunsIcons)
        self.RunsRemove.setGeometry(QtCore.QRect(40, 0, 31, 31))
        self.RunsRemove.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../../../../../_meloun/myPython/ewitis/src/ewitis/gui/img/list-remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RunsRemove.setIcon(icon4)
        self.RunsRemove.setIconSize(QtCore.QSize(32, 32))
        self.RunsRemove.setFlat(True)
        self.RunsRemove.setObjectName("RunsRemove")
        self.RunsDelete = QtGui.QPushButton(self.RunsIcons)
        self.RunsDelete.setGeometry(QtCore.QRect(160, 0, 31, 31))
        self.RunsDelete.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../../../../../_meloun/myPython/ewitis/src/ewitis/gui/img/emptytrash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RunsDelete.setIcon(icon5)
        self.RunsDelete.setIconSize(QtCore.QSize(24, 24))
        self.RunsDelete.setFlat(True)
        self.RunsDelete.setObjectName("RunsDelete")
        self.TimesFilterClear = QtGui.QPushButton(self.tabRuns_Times)
        self.TimesFilterClear.setGeometry(QtCore.QRect(623, 10, 21, 21))
        self.TimesFilterClear.setText("")
        self.TimesFilterClear.setIcon(icon)
        self.TimesFilterClear.setIconSize(QtCore.QSize(16, 16))
        self.TimesFilterClear.setFlat(True)
        self.TimesFilterClear.setObjectName("TimesFilterClear")
        self.TimesIcons = QtGui.QGroupBox(self.tabRuns_Times)
        self.TimesIcons.setGeometry(QtCore.QRect(870, 0, 191, 29))
        self.TimesIcons.setTitle("")
        self.TimesIcons.setObjectName("TimesIcons")
        self.TimesExport = QtGui.QPushButton(self.TimesIcons)
        self.TimesExport.setGeometry(QtCore.QRect(80, 0, 31, 31))
        self.TimesExport.setText("")
        self.TimesExport.setIcon(icon1)
        self.TimesExport.setIconSize(QtCore.QSize(24, 24))
        self.TimesExport.setFlat(True)
        self.TimesExport.setObjectName("TimesExport")
        self.TimesImport = QtGui.QPushButton(self.TimesIcons)
        self.TimesImport.setGeometry(QtCore.QRect(120, 0, 31, 31))
        self.TimesImport.setText("")
        self.TimesImport.setIcon(icon2)
        self.TimesImport.setIconSize(QtCore.QSize(24, 24))
        self.TimesImport.setFlat(True)
        self.TimesImport.setObjectName("TimesImport")
        self.TimesAdd = QtGui.QPushButton(self.TimesIcons)
        self.TimesAdd.setGeometry(QtCore.QRect(0, 0, 31, 31))
        self.TimesAdd.setText("")
        self.TimesAdd.setIcon(icon3)
        self.TimesAdd.setIconSize(QtCore.QSize(32, 32))
        self.TimesAdd.setFlat(True)
        self.TimesAdd.setObjectName("TimesAdd")
        self.TimesRemove = QtGui.QPushButton(self.TimesIcons)
        self.TimesRemove.setGeometry(QtCore.QRect(40, 0, 31, 31))
        self.TimesRemove.setText("")
        self.TimesRemove.setIcon(icon4)
        self.TimesRemove.setIconSize(QtCore.QSize(32, 32))
        self.TimesRemove.setFlat(True)
        self.TimesRemove.setObjectName("TimesRemove")
        self.TimesDelete = QtGui.QPushButton(self.TimesIcons)
        self.TimesDelete.setGeometry(QtCore.QRect(160, 0, 31, 31))
        self.TimesDelete.setText("")
        self.TimesDelete.setIcon(icon5)
        self.TimesDelete.setIconSize(QtCore.QSize(24, 24))
        self.TimesDelete.setFlat(True)
        self.TimesDelete.setObjectName("TimesDelete")
        self.tabWidget.addTab(self.tabRuns_Times, "")
        self.tabUsers = QtGui.QWidget()
        self.tabUsers.setObjectName("tabUsers")
        self.UsersProxyView = QtGui.QTreeView(self.tabUsers)
        self.UsersProxyView.setGeometry(QtCore.QRect(10, 30, 841, 321))
        self.UsersProxyView.setObjectName("UsersProxyView")
        self.UsersFilterLineEdit = QtGui.QLineEdit(self.tabUsers)
        self.UsersFilterLineEdit.setGeometry(QtCore.QRect(10, 10, 113, 20))
        self.UsersFilterLineEdit.setObjectName("UsersFilterLineEdit")
        self.UsersFilterClear = QtGui.QPushButton(self.tabUsers)
        self.UsersFilterClear.setGeometry(QtCore.QRect(123, 10, 21, 21))
        self.UsersFilterClear.setText("")
        self.UsersFilterClear.setIcon(icon)
        self.UsersFilterClear.setIconSize(QtCore.QSize(16, 16))
        self.UsersFilterClear.setFlat(True)
        self.UsersFilterClear.setObjectName("UsersFilterClear")
        self.UsersIcons = QtGui.QGroupBox(self.tabUsers)
        self.UsersIcons.setGeometry(QtCore.QRect(660, 0, 191, 29))
        self.UsersIcons.setTitle("")
        self.UsersIcons.setObjectName("UsersIcons")
        self.UsersExport = QtGui.QPushButton(self.UsersIcons)
        self.UsersExport.setGeometry(QtCore.QRect(80, 0, 31, 31))
        self.UsersExport.setText("")
        self.UsersExport.setIcon(icon1)
        self.UsersExport.setIconSize(QtCore.QSize(24, 24))
        self.UsersExport.setFlat(True)
        self.UsersExport.setObjectName("UsersExport")
        self.UsersImport = QtGui.QPushButton(self.UsersIcons)
        self.UsersImport.setGeometry(QtCore.QRect(120, 0, 31, 31))
        self.UsersImport.setText("")
        self.UsersImport.setIcon(icon2)
        self.UsersImport.setIconSize(QtCore.QSize(24, 24))
        self.UsersImport.setFlat(True)
        self.UsersImport.setObjectName("UsersImport")
        self.UsersAdd = QtGui.QPushButton(self.UsersIcons)
        self.UsersAdd.setGeometry(QtCore.QRect(0, 0, 31, 31))
        self.UsersAdd.setText("")
        self.UsersAdd.setIcon(icon3)
        self.UsersAdd.setIconSize(QtCore.QSize(32, 32))
        self.UsersAdd.setFlat(True)
        self.UsersAdd.setObjectName("UsersAdd")
        self.UsersRemove = QtGui.QPushButton(self.UsersIcons)
        self.UsersRemove.setGeometry(QtCore.QRect(40, 0, 31, 31))
        self.UsersRemove.setText("")
        self.UsersRemove.setIcon(icon4)
        self.UsersRemove.setIconSize(QtCore.QSize(32, 32))
        self.UsersRemove.setFlat(True)
        self.UsersRemove.setObjectName("UsersRemove")
        self.UsersDelete = QtGui.QPushButton(self.UsersIcons)
        self.UsersDelete.setGeometry(QtCore.QRect(160, 0, 31, 31))
        self.UsersDelete.setText("")
        self.UsersDelete.setIcon(icon5)
        self.UsersDelete.setIconSize(QtCore.QSize(24, 24))
        self.UsersDelete.setFlat(True)
        self.UsersDelete.setObjectName("UsersDelete")
        self.tabWidget.addTab(self.tabUsers, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1105, 20))
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
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("ewitis/gui/img/view-refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aRefresh.setIcon(icon6)
        self.aRefresh.setObjectName("aRefresh")
        self.aEditMode = QtGui.QAction(MainWindow)
        self.aEditMode.setCheckable(True)
        self.aEditMode.setChecked(True)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("ewitis/gui/img/pencil2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aEditMode.setIcon(icon7)
        self.aEditMode.setObjectName("aEditMode")
        self.aRefreshMode = QtGui.QAction(MainWindow)
        self.aRefreshMode.setCheckable(True)
        self.aRefreshMode.setChecked(False)
        self.aRefreshMode.setIcon(icon6)
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
        self.RunsFilterClear.setToolTip(QtGui.QApplication.translate("MainWindow", "Cancel filter", None, QtGui.QApplication.UnicodeUTF8))
        self.RunsExport.setToolTip(QtGui.QApplication.translate("MainWindow", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.RunsImport.setToolTip(QtGui.QApplication.translate("MainWindow", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.RunsAdd.setToolTip(QtGui.QApplication.translate("MainWindow", "Add run", None, QtGui.QApplication.UnicodeUTF8))
        self.RunsRemove.setToolTip(QtGui.QApplication.translate("MainWindow", "Remove run(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.RunsDelete.setToolTip(QtGui.QApplication.translate("MainWindow", "Clear table", None, QtGui.QApplication.UnicodeUTF8))
        self.TimesFilterClear.setToolTip(QtGui.QApplication.translate("MainWindow", "Cancel filter", None, QtGui.QApplication.UnicodeUTF8))
        self.TimesExport.setToolTip(QtGui.QApplication.translate("MainWindow", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.TimesImport.setToolTip(QtGui.QApplication.translate("MainWindow", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.TimesAdd.setToolTip(QtGui.QApplication.translate("MainWindow", "Add time", None, QtGui.QApplication.UnicodeUTF8))
        self.TimesRemove.setToolTip(QtGui.QApplication.translate("MainWindow", "Remove time(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.TimesDelete.setToolTip(QtGui.QApplication.translate("MainWindow", "Clear table", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabRuns_Times), QtGui.QApplication.translate("MainWindow", "Runs#Times", None, QtGui.QApplication.UnicodeUTF8))
        self.UsersFilterClear.setToolTip(QtGui.QApplication.translate("MainWindow", "Cancel filter", None, QtGui.QApplication.UnicodeUTF8))
        self.UsersExport.setToolTip(QtGui.QApplication.translate("MainWindow", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.UsersImport.setToolTip(QtGui.QApplication.translate("MainWindow", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.UsersAdd.setToolTip(QtGui.QApplication.translate("MainWindow", "Add user", None, QtGui.QApplication.UnicodeUTF8))
        self.UsersRemove.setToolTip(QtGui.QApplication.translate("MainWindow", "Remove user(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.UsersDelete.setToolTip(QtGui.QApplication.translate("MainWindow", "Clear table", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabUsers), QtGui.QApplication.translate("MainWindow", "Users", None, QtGui.QApplication.UnicodeUTF8))
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