# -*- coding: utf-8 -*-
#!/usr/bin/env python
# 
#
#
#

import sys
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import ewitis.gui.GuiData as GuiData


class RunsParameters(myModel.myParameters):
    def __init__(self, source):                
                        
        #table and db table name
        self.name = "Runs" 
        
        #TABLE TIMES
        self.tabTimes = source.T 
        
        #=======================================================================
        # KEYS DEFINITION
        #=======================================================================        
        self.KEYS_DEF = [ \
                        {"name":"state",        "tabName": None,          "dbName": "state"},\
                        {"name":"id",           "tabName": "id",          "dbName": "id"},\
                        {"name":"starttime_id", "tabName": None,          "dbName": "starttime_id"},\
                        {"name":"date",         "tabName": "date",        "dbName": "date"},\
                        {"name":"name_id",      "tabName": None,          "dbName": "name_id"},\
                        {"name":"name",         "tabName": "name",        "dbName": None},\
                        {"name":"description",  "tabName": "description", "dbName": "description"},                                                                                                                          
                    ]  
        
        #create MODEL and his structure
        myModel.myParameters.__init__(self, source)
                                  
        #=======================================================================
        # GUI
        #=======================================================================
        self.gui = {} 
        #VIEW
        self.gui['view'] = source.ui.RunsProxyView
        
        #FILTER
        self.gui['filter'] = source.ui.RunsFilterLineEdit
        self.gui['filterclear'] = source.ui.RunsFilterClear
        
        #GROUPBOX
        self.gui['add'] = source.ui.RunsAdd
        self.gui['remove'] =  source.ui.RunsRemove
        self.gui['export'] = source.ui.RunsExport
        self.gui['import'] = None 
        self.gui['delete'] = source.ui.RunsDelete
        
        #COUNTER
        self.gui['counter'] = source.ui.runsCounter
                 
        

class RunsModel(myModel.myModel):
    def __init__(self, params):                        
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, params)
        
        self.update() 
                
    #setting flags for this model        
    #first collumn is NOT editable
    def flags(self, index):
        aux_flags = 0
        
        #id, name, category, addres NOT editable
        if (index.column() == 2):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
        return myModel.myModel.flags(self, index)
        
    def db2tableRow(self, run):                        
        
        #get USER
        user = self.params.db.getParX("users", "id", run["name_id"]).fetchone()
        
        #exist user?
        if user == None:
            run['name']='unknown'
        #exist => restrict username                
        else:
            if(user['name']==''):
                run['name'] = 'nobody'
            run['name'] = user['name']
                                
        return run
    
    def table2dbRow(self, run_table): 
        run_db = {"id" : run_table['id'], "date" : run_table['date'], "description" :  run_table['description']}                                                                       
        return run_db
    
    
        

class RunsProxyModel(myModel.myProxyModel):
    def __init__(self):                        
        
        #create PROXYMODEL
        myModel.myProxyModel.__init__(self)        
        
              
        
    
# view <- proxymodel <- model 
class Runs(myModel.myTable):
    def  __init__(self, params):                        
                
        #create MODEL
        self.model = RunsModel(params)        
        
        #create PROXY MODEL        
        self.proxy_model = RunsProxyModel()
        
        myModel.myTable.__init__(self, params)
        
        
        #assign MODEL to PROXY MODEL
        #self.proxy_model.setSourceModel(self.model)
        
        #assign PROXY MODEL to VIEW        
        #self.view = view 
        self.params.gui['view'].setModel(self.proxy_model)
        self.params.gui['view'].setRootIsDecorated(False)
        self.params.gui['view'].setAlternatingRowColors(True)        
        self.params.gui['view'].setSortingEnabled(True)
        self.params.gui['view'].setColumnWidth(0,40)
        self.params.gui['view'].setColumnWidth(1,120)
        self.params.gui['view'].setColumnWidth(2,110)
        self.params.gui['view'].setColumnWidth(3,80)
    
        
        #MODE EDIT/REFRESH        
        self.system = 0                       
                               
        #set selection to first row
        self.params.gui['view'].selectionModel().setCurrentIndex(self.model.index(0,0), QtGui.QItemSelectionModel.Rows | QtGui.QItemSelectionModel.SelectCurrent)
            
        #update table times (use selection to define run_id)        
        self.updateTimes()
        
    #=======================================================================
    # UPDATE TIMES
    #=======================================================================    
    # function for update table TIMES according to selection in RUNS
    def updateTimes(self):         
                         
        #get index of selected ID (from tableRuns) 
        rows = self.params.gui['view'].selectionModel().selectedRows() #default collumn = 0
                                      
        #update table times with run_id
        try:             
            #ziskani id z vybraneho radku                                         
            self.run_id = self.proxy_model.data(rows[0]).toString()                 
                                         
            #get TIMES from database & add them to the table
            self.params.guidata.user_actions = GuiData.ACTIONS_DISABLE
            self.params.tabTimes.update(run_id = self.run_id)             
            self.params.guidata.user_actions = GuiData.ACTIONS_ENABLE
        except:
            print "I: Times: nelze aktualizovat!"
        
    # REMOVE ROW               
    def sDelete(self):
        
        #delete run with additional message
        myModel.myTable.sDelete(self, "and ALL TIMES belonging to him")
        
        #delete times
        self.params.tabTimes.params.db.deleteParX("times", "run_id", self.run_id)               
        self.params.tabTimes.update()
        print "mazu"
        
         
        
                                   
         
                               
