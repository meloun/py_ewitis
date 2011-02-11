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
        
        
        #create MODEL and his structure
        myModel.myParameters.__init__(self, source)
                
        
        #table and db table name
        self.params['name'] = "runs"  
        
        #table keys
        self.params['keys'] = ["id", "date", "name", "description"]
        
        #db for acces
        self.params['db'] = source.db
        
        #guidata
        self.params['guidata'] = source.GuiData
                
        #=======================================================================
        # GUI
        #=======================================================================
        #VIEW
        self.params['view'] = source.ui.RunsProxyView
        
        #FILTER
        self.params['filter'] = source.ui.RunsFilterLineEdit
        self.params['filterclear'] = source.ui.RunsFilterClear
        
        #GROUPBOX
        self.params['add'] = source.ui.RunsAdd
        self.params['remove'] =  source.ui.RunsRemove
        self.params['export'] = source.ui.RunsExport
        self.params['import'] = None 
        self.params['delete'] = source.ui.RunsDelete
        
        #COUNTER
        self.params['counter'] = source.ui.runsCounter
                 
        

class RunsModel(myModel.myModel):
    def __init__(self, params):                        
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, params)
        
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
        user = self.params['db'].getParX("users", "id", run["name_id"]).fetchone()
        
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
        self.params['view'].setModel(self.proxy_model)
        self.params['view'].setRootIsDecorated(False)
        self.params['view'].setAlternatingRowColors(True)        
        self.params['view'].setSortingEnabled(True)
        self.params['view'].setColumnWidth(0,40)
        self.params['view'].setColumnWidth(1,120)
        self.params['view'].setColumnWidth(2,110)
        self.params['view'].setColumnWidth(3,80)
    
        
        #MODE EDIT/REFRESH        
        self.system = 0 
        
                                   
         
                               
