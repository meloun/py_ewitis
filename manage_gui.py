# -*- coding: utf-8 -*-

#
#
#

import sys
import time
import manage_comm
from PyQt4 import QtCore, QtGui
import ewitis.gui.Ui_App as Ui_App
import libs.db_csv.db_csv as Db_csv

import ewitis.gui.myModel as myModel
import ewitis.gui.GuiData as GuiData
import ewitis.gui.myModel as myModel
import ewitis.gui.RunsModel as RunsModel
import ewitis.gui.TimesModel as TimesModel
import ewitis.gui.UsersModel as UsersModel


import libs.sqlite.sqlite as sqlite
import ewitis.sql_queries.sql_queries as sql_queries


   
class wrapper_gui_ewitis(QtGui.QMainWindow):
    def __init__(self, parent=None, ShaMem_comm = manage_comm.DEFAULT_COMM_SHARED_MEMORY):    
        import libs.comm.serial_utils as serial_utils 
        
        #GUI
        QtGui.QWidget.__init__(self, parent)        
        self.ui = Ui_App.Ui_MainWindow()
        self.ui.setupUi(self)                
                                                                                      
        
        #GUI USER
        
        '''status bar'''
        self.ui.statusbar.showMessage("ok")
                
        #nastaveni prvniho dostupneho portu
        self.ui.aSetPort.setText(serial_utils.enumerate_serial_ports().next())
                                                           
        #=======================================================================
        # DATABASE
        #=======================================================================
        try:           
            self.db = sqlite.sqlite_db("db/test_db.sqlite")
        
            '''connect to db'''  
            self.db.connect()
        except:
            print "E: GUI: Database"                 
        
        
        #=======================================================================
        # TABLES
        #=======================================================================
        self.GuiData = GuiData.GuiData()
        self.R = RunsModel.Runs( RunsModel.RunsParameters(self).params )
        self.R.update()                
        self.T = TimesModel.Times( TimesModel.TimesParameters(self).params )
        #self.updateTimes()
        
        self.U = UsersModel.Users( UsersModel.UsersParameters(self).params)
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
        QtCore.QObject.connect(self.ui.aLockMode, QtCore.SIGNAL("activated()"), self.sLockMode)
        QtCore.QObject.connect(self.ui.aEditMode, QtCore.SIGNAL("activated()"), self.sEditMode)
        QtCore.QObject.connect(self.ui.tabWidget, QtCore.SIGNAL("currentChanged (int)"), self.sTabChanged)
        QtCore.QObject.connect(self.ui.TimesShowAll, QtCore.SIGNAL("stateChanged (int)"), self.sTimesShowAllChanged)
        QtCore.QObject.connect(self.ui.timesShowZero, QtCore.SIGNAL("stateChanged (int)"), self.sTimesShowZeroChanged)
                                                                         
        #COMM
        self.ShaMem_comm = ShaMem_comm                
                       
        self.myManageComm = manage_comm.ManageComm(ShaMem_comm = self.ShaMem_comm) #COMM instance
        
        
        
        self.myManageComm.start() #start thread, 'run' flag should be 0, so this thread ends immediatelly
          
    def __del__(self):
        print "GUI: mazu instanci.."                                                              

    #=======================================================================
    # UPDATE TIMES
    #=======================================================================    
    # function for update table TIMES according to selection in RUNS
    def updateTimes(self):         
                         
        #get index of selected ID (from tableRuns) 
        rows = self.ui.RunsProxyView.selectionModel().selectedRows() #default collumn = 0
                                      
        #update table times with run_id
        try: 
            
            #ziskani id z vybraneho radku                                         
            run_id = self.R.proxy_model.data(rows[0]).toString()                 
                                         
            #get TIMES from database & add them to the table
            self.GuiData.user_actions = GuiData.ACTIONS_DISABLE
            self.T.update(run_id = run_id)             
            self.GuiData.user_actions = GuiData.ACTIONS_ENABLE
        except:
            print "I: Times: nelze aktualizovat!"
    
    #=======================================================================
    # SHOW MESSAGE -     
    #=======================================================================
    # dialog, status bar
    # warning(OK), info(OK), warning_dialog(Yes, Cancel), input_integer(integer, OK)      
    def showMessage(self, title, message, type='warning', dialog=True, statusbar=True, value=0):
        
        #DIALOG
        if(dialog):                                
            if(type=='warning'):
                QtGui.QMessageBox.warning(self, title, message)            
            elif(type=='info'):
                QtGui.QMessageBox.information(self, title, message)
            elif(type=='warning_dialog'):
                ret = QtGui.QMessageBox.warning(self, title, message, QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Yes)                
                if (ret != QtGui.QMessageBox.Yes):
                    return False
                message = "succesfully"
            elif(type=='input_integer'):
                i, ok = QtGui.QInputDialog.getInteger(self, title, message, value=value)
                return i
            
        #STATUSBAR        
        if(statusbar):
            self.ui.statusbar.showMessage(title+" : " + message)
        
        return True
        
         
    def start(self):
        self.app = QtGui.QApplication(sys.argv)
        self.myapp = wrapper_gui_ewitis()
        self.myapp.show()    
        sys.exit(self.app.exec_())
                
    def updateShaMem_comm(self):
        self.ShaMem_comm["port"] = str(self.ui.aSetPort.text()) 
                

         
    #=======================================================================
    ### SLOTS ###
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
        
    def sTimesShowZeroChanged(self, state):        
        if(state == 0):
            self.T.model.showzero = False
        elif(state == 2):
            self.T.model.showzero = True
        self.T.update()
        
        
    def sRunsProxyView_SelectionChanged(self, selected, deselected):               
        if(selected):            
            self.updateTimes()  #update TIMES table                                                                               
                      
        
    #===========================================================================
    ### PORT TOOLBAR ### 
    #=========================================================================== 
    def sPortSet(self):
        import libs.comm.serial_utils as serial_utils         
        
        #dostupne porty
        ports = []
        for p in serial_utils.enumerate_serial_ports():            
            ports.append(p)
        ports = sorted(ports)                    

        item, ok = QtGui.QInputDialog.getItem(self, "Serial Port",
                "Serial Port:", ports, 0, False)
        
        title = "Port Set"
        if (ok and item):            
            self.ui.aSetPort.setText(item)
            self.showMessage(title, str(item), dialog = False)                
        
                           
    #=======================================================================
    # sPortConnect() -> create/kill communication thread 
    #=======================================================================        
    def sPortConnect(self):
        
        #refresh COMM data (gui -> shared memory; port, speed, etc..)
        self.updateShaMem_comm()
        
        title = "Port ("+self.ShaMem_comm["port"]+")"
        
        #comm runs?
        if(self.ShaMem_comm["enable"] == True):                            
            
            #=======================================================================
            # KILL COMMUNICATION - thread, etc..
            #=======================================================================
            #close current thread            
            self.ShaMem_comm["enable"] = False
            #gui 
            self.ui.aSetPort.setEnabled(True)   
            self.ui.aConnectPort.setText("Connect")
            self.showMessage(title, "disconnected", dialog = False)                                
        else:                                    
            
            #=======================================================================
            # CREATE COMMUNICATION - thread, etc..
            #=======================================================================
            # create thread
            self.ShaMem_comm["enable"] = True
            self.myManageComm = manage_comm.ManageComm(ShaMem_comm = self.ShaMem_comm)           
            self.myManageComm.start()
            #gui
            self.ui.aSetPort.setEnabled(False)
            self.ui.aConnectPort.setText("Disconnect")
            self.showMessage(title, "connected", dialog = False)                     
        
    #===========================================================================
    ### ACTION TOOLBAR ### 
    #=========================================================================== 
    def sRefresh(self):
        
        self.R.update()
        self.T.update()
        self.U.update()
        
        title = "Manual Refresh"
        self.showMessage(title, time.strftime("%H:%M:%S", time.localtime()), dialog = False)   
        
    #===========================================================================
    #### MODE TOOLBAR => EDIT, LOCK, REFRESH ### 
    #===========================================================================         
    def sEditMode(self):
        
        self.ui.aEditMode.setChecked(True) 
        self.ui.aLockMode.setChecked(False) 
        self.ui.aRefreshMode.setChecked(False)
        
        #self.GuiData.mode = GuiData.MODE_EDIT
          
        self.T.model.mode = myModel.MODE_EDIT           
        self.R.model.mode = myModel.MODE_EDIT
        self.U.model.mode = myModel.MODE_EDIT
        
        self.showMessage("Mode", "EDIT", dialog = False)
          
    def sRefreshMode(self):
        
        self.ui.aRefreshMode.setChecked(True)
        self.ui.aLockMode.setChecked(False) 
        self.ui.aEditMode.setChecked(False)  
        
        #self.GuiData.mode = GuiData.MODE_REFRESH     
                  
        self.R.model.mode = myModel.MODE_REFRESH
        self.T.model.mode = myModel.MODE_REFRESH
        self.U.model.mode = myModel.MODE_REFRESH  
        
        self.showMessage("Mode", "REFRESH", dialog = False)      
        
    def sLockMode(self):
        
        self.ui.aLockMode.setChecked(True)
        self.ui.aRefreshMode.setChecked(False) 
        self.ui.aEditMode.setChecked(False)
          
        #self.GuiData.mode = GuiData.MODE_LOCK     
                
        self.R.model.mode = myModel.MODE_LOCK
        self.T.model.mode = myModel.MODE_LOCK
        self.U.model.mode = myModel.MODE_LOCK
        
        self.showMessage("Mode", "LOCK", dialog = False)
                                                                                                                                                                                 
    def sAbout(self):                           
        QtGui.QMessageBox.information(self, "About", "Ewitis  - Electronic wireless timing \n\ninfo@ewitis.cz\nwww.ewitis.cz\n\n v0.1\n\n (c) 2011")                                                

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
    
    