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
import libs.db_csv.db_csv as Db_csv

import ewitis.gui.myModel as myModel

import ewitis.gui.GuiData as GuiData
import ewitis.gui.Ui_Slots as Ui_Slots
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
        self.R = RunsModel.Runs(self.ui.RunsProxyView, self.db, self.GuiData, self.ui)
        self.R.update()        
        self.T = TimesModel.Times(self.ui.TimesProxyView, self.db, self.GuiData)
        self.updateTimes()
        self.U = UsersModel.Users("users", self.ui.UsersProxyView, self.db, self.GuiData, ["id", "nr", "name", "kategory", "address"])
        self.U.model.update()
        
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
        QtCore.QObject.connect(self.ui.tabWidget, QtCore.SIGNAL("currentChanged (int)"), self.sTabChanged)
        QtCore.QObject.connect(self.ui.TimesShowAll, QtCore.SIGNAL("stateChanged (int)"), self.sTimesShowAllChanged)
        
        #SIGNALs & SLOTs
        #class for adding and manage signals and slots
        AddSignal =  Ui_Slots.AddSignal(self)       
        
        AddSignal.table(self.R, 
                self.ui.RunsFilterLineEdit, self.ui.RunsFilterClear,
                self.ui.RunsExport, self.ui.RunsExport,
                self.ui.RunsExport, None, 
                self.ui.RunsDelete)
        
        AddSignal.table(self.T, 
                        self.ui.TimesFilterLineEdit, self.ui.TimesFilterClear,
                        self.ui.TimesExport, self.ui.TimesExport,
                        self.ui.TimesExport, None, 
                        self.ui.TimesDelete)
        
        AddSignal.table(self.U, 
                self.ui.UsersFilterLineEdit, self.ui.UsersFilterClear,
                self.ui.UsersImport, self.ui.UsersImport,
                self.ui.UsersExport, self.ui.UsersImport, 
                self.ui.UsersDelete)                                                                  
        #COMM
        self.ShaMem_comm = ShaMem_comm                
                       
        self.myManageComm = manage_comm.ManageComm(ShaMem_comm = self.ShaMem_comm) #COMM instance
        self.myManageComm.start() #start thread, 'run' flag should be 0, so this thread ends immediatelly
        
    def ehm(self):
        print "mandolin"    
    def __del__(self):
        print "GUI: mazu instanci.."                                                              

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
    
    def showMessage(self, title, message, type='warning', dialog=True, statusbar=True):
        
        #DIALOG
        if(dialog):                                
            if(type=='warning'):
                QtGui.QMessageBox.warning(self, title, message)            
            elif(type=='info'):
                QtGui.QMessageBox.information(self, title, message)
        #STATUSBAR        
        if(statusbar):
            self.ui.statusbar.showMessage(title+" : " + message)    
         
    def start(self):
        self.app = QtGui.QApplication(sys.argv)
        self.myapp = wrapper_gui_ewitis()
        self.myapp.show()    
        sys.exit(self.app.exec_())
                
    def updateShM(self):
        self.ShaMem_comm["port"] = str(self.ui.aSetPort.text()) 
                

         
    #=======================================================================
    # SLOTS
    #=======================================================================
    def sTabChanged(self, nr):
        if(nr==0):
            self.R.update()
            self.updateTimes()  #update TIMES table
            #self.T.update()
        elif(nr==1):
            self.U.update()
            
    def sTimesShowAllChanged(self, state):        
        if(state == 0):
            self.T.model.showall = False
        elif(state == 2):
            self.T.model.showall = True
        self.T.update()
        
        
    def sRunsProxyView_SelectionChanged(self, selected, deselected):               
        if(selected):
            #print "selection changed"  
            self.updateTimes()  #update TIMES table
            
    def sEditMode(self):
        print "I: switching to editing mode.."
        self.ui.aEditMode.setChecked(True) 
        self.ui.aRefreshMode.setChecked(False)
        self.GuiData.mode = GuiData.MODE_EDIT  
        self.T.model.mode = myModel.MODE_EDIT           
        self.R.model.mode = myModel.MODE_EDIT
        self.U.model.mode = myModel.MODE_EDIT  
        
    
    def sImportRuns(self):
        pass         
    def sImportTimes(self):
        pass
     
    #tlacitko pro import uzivatelu
    #WEB - id, kategorie, prijmeni, jmeno, adresa,.. 
    #DB - id, nr, name, kategory, address 
    def sImportUsers(self):        
                
        #import       
        state = self.U.importCsv("Blizak_2010.csv")
        self.sImportDialog(state)
    
                       
    def sImportDialog(self, state):               
        #error message
        title = "Import"
        if(state['ko'] != 0) :                                               
            message = str(state['ko'])+" record(s) NOT succesfully imported.\n\n Probably already exist."
            QtGui.QMessageBox.warning(self, title, message)
        else:
            message = str(state['ok'])+" record(s) succesfully imported."
            QtGui.QMessageBox.information(self, title, message)            
        self.ui.statusbar.showMessage(title+" : " + message)        
                      
        
        
    def sRefreshMode(self):
        print "I: switching to refreshing mode.. main"
        self.ui.aRefreshMode.setChecked(True) 
        self.ui.aEditMode.setChecked(False)  
        self.GuiData.mode = GuiData.MODE_REFRESH     
        self.T.model.mode = myModel.MODE_REFRESH          
        self.R.model.mode = myModel.MODE_REFRESH
        #self.U.model.mode = myModel.MODE_REFRESH
              
                     
                                                                                           
    def sRefresh(self):
        print "I: refreshing.."
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
    
    