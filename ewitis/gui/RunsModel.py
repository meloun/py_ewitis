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

class RunsModel(myModel.myModel):
    def __init__(self, view, name, db, guidata, keys):                        
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, view, name, db, guidata, keys)
        
        self.update() 
                
    #setting flags for this model        
    #first collumn is NOT editable
    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        
        if(self.guidata.mode == GuiData.MODE_REFRESH):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
        #id, name, kategory, addres NOT editable
        if ((index.column() == 0) or (index.column() == 2)):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        
    def db2tableRow(self, run):                        
        
        #get USER
        user = self.db.getParX("users", "id", run["name_id"]).fetchone()
        
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
    def  __init__(self, name, view, db, guidata, keys):                        
        
        #create MODEL
        self.model = RunsModel(view, name, db, guidata, keys)        
        
        #create PROXY MODEL        
        self.proxy_model = RunsProxyModel()
        
        myModel.myTable.__init__(self, name, view, db, guidata, keys)
        
        
        #assign MODEL to PROXY MODEL
        #self.proxy_model.setSourceModel(self.model)
        
        #assign PROXY MODEL to VIEW        
        self.view = view 
        self.view.setModel(self.proxy_model)
        self.view.setRootIsDecorated(False)
        self.view.setAlternatingRowColors(True)        
        self.view.setSortingEnabled(True)
        self.view.setColumnWidth(0,50)
        self.view.setColumnWidth(1,130)
        self.view.setColumnWidth(2,150)
        self.view.setColumnWidth(3,100)
        
        #TIMERs
        self.timer1s = QtCore.QTimer() 
        self.timer1s.start(1000)
        
        #MODE EDIT/REFRESH        
        self.system = 0 
        
        #self.mode = myModel.MODE_EDIT           
               
        #self.db = db                
        
        #self.keys = keys
        
        #self.updateModel()
        #self.createSlots()
                                            
        #QtCore.QObject.connect(self.view, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.slot_Entered)
        #QtCore.QObject.connect(self.timer1s, QtCore.SIGNAL("timeout()"), self.slot_Timer1s);
        #QtCore.QObject.connect(self.model, QtCore.SIGNAL("dataChanged(QModelIndex, QModelIndex )"), self.slot_ModelChanged)        
        
    #=======================================================================
    # SLOTS
    #=======================================================================    
                
    #UPDATE TIMER    
    def slot_Timer1s(self):        
        if (self.guidata.mode == GuiData.MODE_REFRESH): 
            self.update()    #update table            

    #MODEL CHANGED        
    def slot_ModelChanged_old(self,a,b):
        
        #user change, no auto update
        if((self.guidata.mode == GuiData.MODE_EDIT) and (self.guidata.user_actions == GuiData.ACTIONS_ENABLE)):
            
            #prepare data
            aux_id = self.model.item(a.row(), 0).text()            
            aux_date = self.model.item(a.row(), 1).text()    
            aux_description = self.model.item(a.row(), 3).text()
            
            aux_dict = {"id" : aux_id, "date" : aux_date, "description" :  aux_description}
            
            #replace                         
            self.db.update_from_dict("runs", aux_dict)

    #UPDATE TABLE        
    def update(self):                                        
        self.model.update()  #update model                                   
         
    #UPDATE MODEL
    #automaticky update, nahazuje se SYSTEM_WORKING aby nereagoval ModelChanged
    def updateModel_old(self):
        return
        
        self.guidata.user_actions = GuiData.ACTIONS_DISABLE
        
        #ziskani oznaceneho radku z tableRuns 
        try:
            rows = self.view.selectionModel().selectedRows()         
            model_index = rows[0] #selected row index #row = rows[0].row() if rows else 0
        except:
            pass              
            
        #get RUNS from database & add them to the table                    
        runs = self.db.getAll("runs")
        self.model.removeRows(0,self.model.rowCount())                
        for run in runs:
            aux_items = []
            
            #get USER
            user = self.db.getParX("users", "id", run["name_id"]).fetchone()
            
            #exist user?
            if user==None:
                username='unknown'
            #NOT exist => restrict username                
            else:
                if(user['name']==''):
                    username = 'nobody'
                username = user['name']
                
            
            
            try:
                aux_array = [run["id"], run["date"], username, run["description"]]
                #for key in self.keys:                            
                #    if key in run.keys(): #content run this value?
                #        aux_items.append(run[key])                                                    
                self.model.addRow(aux_array)
            except:
                print "E: Runs: Beh nelze pridat", run["id"] #, user["name"] 
            
                            

            
        #selection back                           
        try: 
            self.view.selectionModel().setCurrentIndex(model_index, QtGui.QItemSelectionModel.Rows | QtGui.QItemSelectionModel.SelectCurrent) #self.tables_info['runs']['selection']            
        except:
            pass
        
        self.guidata.user_actions = GuiData.ACTIONS_ENABLE                                        
