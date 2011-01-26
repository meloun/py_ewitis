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
        aux_flags = 0
        
        #id, name, kategory, addres NOT editable
        if (index.column() == 2):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
        return myModel.myModel.flags(self, index)
        
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
    def  __init__(self, view, db, guidata, ui):                        
        
        name = "runs"
        keys = ["id", "date", "name", "description"]
        
        self.ui = ui
        
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
        self.view.setColumnWidth(0,40)
        self.view.setColumnWidth(1,100)
        self.view.setColumnWidth(2,100)
        self.view.setColumnWidth(3,100)
    
        
        #MODE EDIT/REFRESH        
        self.system = 0 
        
                                            
        #QtCore.QObject.connect(self.view, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.slot_Entered)
        #QtCore.QObject.connect(self.timer1s, QtCore.SIGNAL("timeout()"), self.slot_Timer1s);
        #QtCore.QObject.connect(self.model, QtCore.SIGNAL("dataChanged(QModelIndex, QModelIndex )"), self.slot_ModelChanged)        
        
    #=======================================================================
    # SLOTS
    #=======================================================================                


    #UPDATE TABLE        
    #def update(self):                                        
    #    self.model.update()  #update model                                           
         
                               
