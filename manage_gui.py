# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Fri Jul 23 13:17:53 2010
#      by: PyQt4 UI code generator 4.7.4
#

import sys
import time
import manage_comm
from PyQt4 import QtCore, QtGui
import ewitis.gui.Ui_App as Ui_App
import ewitis.gui.myModel as myModel
import libs.myqt.myqtTable as myqtTable
import libs.myqt.myqtModel as myqtModel

import ewitis.gui.myModel as myModel

import ewitis.gui.GuiData as GuiData
import ewitis.gui.myModel as myModel
import ewitis.gui.RunsModel as RunsModel
import ewitis.gui.TimesModel as TimesModel
import ewitis.gui.UsersModel as UsersModel


import libs.sqlite.sqlite as sqlite
import ewitis.sql_queries.sql_queries as sql_queries

#COMM Shared Memory
DEFAULT_GUI_SHARED_MEMORY = { 
                             "statusbar_text": "ok",
                              "console_text":""
}



    
class wrapper_gui_ewitis(QtGui.QMainWindow):
    def __init__(self, parent=None, ShaMem_comm = manage_comm.DEFAULT_COMM_SHARED_MEMORY, ShaMem_gui = DEFAULT_GUI_SHARED_MEMORY):
        import libs.comm.serial_utils as serial_utils 
        
        #GUI
        QtGui.QWidget.__init__(self, parent)
        self.port_state = 0
        self.ui = Ui_App.Ui_MainWindow()
        self.ui.setupUi(self)                                                                 
        
        #GUI SHM
        self.ShaMem_gui = ShaMem_gui
        
        #GUI USER
        
        '''status bar'''
        self.ui.statusbar.showMessage(self.ShaMem_gui["statusbar_text"])
        
        '''aSetPort'''
        #nastaveni prvniho dostupneho portu
        self.ui.aSetPort.setText(serial_utils.enumerate_serial_ports().next())
                                                           
        #=======================================================================
        # DATABASE
        #=======================================================================
        try:           
            self.db = sqlite.sqlite_db("export/sqlite/test_db.sqlite")
        
            '''connect to db'''  
            self.db.connect()
        except:
            print "E: GUI: Database"                 
        
        
        #=======================================================================
        # TABLES
        #=======================================================================
        self.GuiData = GuiData.GuiData()
        self.R = RunsModel.Runs(self.ui.RunsProxyView, self.db, self.GuiData, ["id", "date", "name", "description"])
        self.R.updateModel()        
        self.T = TimesModel.Times(self.ui.TimesProxyView, self.db, self.GuiData, ["id", "nr", "time", "name", "kategory", "address"])
        self.updateTimes()
        self.U = UsersModel.Users(self.ui.UsersProxyView, self.db, self.GuiData, ["id", "nr", "name", "kategory", "address"])
        self.U.updateModel()
        
        #=======================================================================
        # SIGNALS
        #=======================================================================  
        QtCore.QObject.connect(self.ui.RunsProxyView.selectionModel(), QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"), self.sRunsProxyView_SelectionChanged)
        QtCore.QObject.connect(self.ui.aSetPort, QtCore.SIGNAL("activated()"), self.sPortSet)
        QtCore.QObject.connect(self.ui.aRefresh, QtCore.SIGNAL("activated()"), self.sRefresh)
        QtCore.QObject.connect(self.ui.aConnectPort, QtCore.SIGNAL("activated()"), self.sPortConnect)
        QtCore.QObject.connect(self.ui.actionAbout, QtCore.SIGNAL("activated()"), self.sAbout)  
        QtCore.QObject.connect(self.ui.aRefreshMode, QtCore.SIGNAL("activated()"), self.sRefreshMode)      
        QtCore.QObject.connect(self.ui.aEditMode, QtCore.SIGNAL("activated()"), self.sEditMode)
        
        self.ui.RunsFilterLineEdit.textChanged.connect(self.sRunsFilterRegExpChanged)
        self.ui.TimesFilterLineEdit.textChanged.connect(self.sTimesFilterRegExpChanged)
        self.ui.UsersFilterLineEdit.textChanged.connect(self.sUsersFilterRegExpChanged)
                      
                                                          
        #COMM
        self.ShaMem_comm = ShaMem_comm                
                       
        self.myManageComm = manage_comm.ManageComm(ShaMem_comm = self.ShaMem_comm) #COMM instance
        self.myManageComm.start() #start thread, 'run' flag should be 0, so this thread ends immediatelly                                                            

    # UPDATE TIMES
    # function for update table TIMES according to selection in RUNS
    def updateTimes(self):        
                         
        #ziskani oznaceneho radku z tableRuns 
        rows = self.ui.RunsProxyView.selectionModel().selectedRows()
            
        #ziskani id z vybraneho radku   
        try:                      
            run_id = self.R.proxy_model.data(self.R.proxy_model.index(rows[0].row(), 0)).toString()
                                             
            #get TIMES from database & add them to the table
            self.GuiData.user_actions = GuiData.ACTIONS_DISABLE
            self.T.update(run_id)             
            self.GuiData.user_actions = GuiData.ACTIONS_ENABLE
        except:
            print "I: Times: nelze aktualizovat!"        

         
    #=======================================================================
    # SLOTS
    #=======================================================================
    def sRunsProxyView_SelectionChanged(self, selected, deselected):               
        if(selected):
            #print "selection changed"  
            self.updateTimes()  #update TIMES table
            
    def sEditMode(self):
        print "I: switching to editing mode.."
        self.ui.aEditMode.setChecked(True) 
        self.ui.aRefreshMode.setChecked(False)
        self.GuiData.mode = GuiData.MODE_EDIT  
        #self.T.model.mode = myModel.MODE_EDIT           
        #self.R.model.mode = myModel.MODE_EDIT
        #self.U.model.mode = myModel.MODE_EDIT  
        
    def sRefreshMode(self):
        print "I: switching to refreshing mode.."
        self.ui.aRefreshMode.setChecked(True) 
        self.ui.aEditMode.setChecked(False)  
        self.GuiData.mode = GuiData.MODE_REFRESH     
        #self.T.model.mode = myModel.MODE_REFRESH          
        #self.R.model.mode = myModel.MODE_REFRESH
        #self.U.model.mode = myModel.MODE_REFRESH
              
                     
                                                                                           
    def sRefresh(self):
        print "I: refreshing.."
        self.R.update()
        
        self.R.update()              
    def sPortSet(self):
        import libs.comm.serial_utils as serial_utils 
        print "GUI: aPortSet activated()"
        
        #dostupne porty
        ports = []
        for p in serial_utils.enumerate_serial_ports():            
            ports.append(p)
        ports = sorted(ports)                    

        item, ok = QtGui.QInputDialog.getItem(self, "Serial Port",
                "Serial Port:", ports, 0, False)
        if ok and item:            
            self.ui.aSetPort.setText(item)
                       
    '''connect -> vytvari komunikacni vlakno'''        
    def sPortConnect(self):
        self.updateShM()
        if(self.ShaMem_comm["run"]): 
            print "GUI: aPortConnect activated()->disconnect", self.ui.aSetPort.text()  
            print "GUI: mazu COMM.."            
            self.ShaMem_comm["run"] = 0 #close current thread
            self.ui.aSetPort.setEnabled(True)   
            self.ui.aConnectPort.setText("Connect")                                
        else:
            print "GUI: aPortConnect activated()->connect", self.ui.aSetPort.text()
            print "GUI: zakladam COMM.."
            self.ShaMem_comm["run"] = 1
            self.myManageComm = manage_comm.ManageComm(ShaMem_comm = self.ShaMem_comm)           
            self.myManageComm.start()
            self.ui.aSetPort.setEnabled(False)
            self.ui.aConnectPort.setText("Disconnect")             
        print "GUI: ",self.ShaMem_comm["run"]

        
        
    def sAbout(self):
        print "GUI: aAbout activated()"                    
        QtGui.QMessageBox.information(self, "About", "Ewitis \n (c) 2010 \n\n Clever guysClever guysClever guysClever guysClever guysClever guys")


    
    def sRunsFilterRegExpChanged(self):
        regExp = QtCore.QRegExp(self.ui.RunsFilterLineEdit.text(),
                QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)
        self.R.proxy_model.setFilterRegExp(regExp)
    
    def sTimesFilterRegExpChanged(self):
        regExp = QtCore.QRegExp(self.ui.TimesFilterLineEdit.text(),
                QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)
        self.T.proxy_model.setFilterRegExp(regExp)
        
    def sUsersFilterRegExpChanged(self):
        regExp = QtCore.QRegExp(self.ui.UsersFilterLineEdit.text(),
                QtCore.Qt.CaseInsensitive, QtCore.QRegExp.FixedString)
        self.U.proxy_model.setFilterRegExp(regExp)
        
                               
                
    def __del__(self):
        print "GUI: mazu instanci.."  
         
    def start(self):
        self.app = QtGui.QApplication(sys.argv)
        self.myapp = wrapper_gui_ewitis()
        self.myapp.show()    
        sys.exit(self.app.exec_())
                
    def updateShM(self):
        self.ShaMem_comm["port"] = str(self.ui.aSetPort.text())       


class manage_gui():
    def __init__(self):
        #self.app = QtGui.QApplication(sys.argv)
        self.myapp = wrapper_gui_ewitis()
    def start(self):                    
        self.myapp.show()    
        sys.exit(self.app.exec_())            
    
if __name__ == "__main__":
    import sys
    import threading, time, sys
    #myManageGui = manage_gui()
    #myManageGui.start()
    
    def gui_start():
        app = QtGui.QApplication(sys.argv)
        myapp = wrapper_gui_ewitis()           
        myapp.show()
        sys.exit(app.exec_())
    
    gui_start()
        
    print "MANAGE GUI"
    #thread_gui = threading.Thread(target = gui_start)
    #thread_gui.start()
    
    