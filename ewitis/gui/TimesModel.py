#!/usr/bin/env python

import sys
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel


class TimesModel(myModel.myModel):
    def __init__(self, keys):                        
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, keys)

class TimesProxyModel(myModel.myProxyModel):
    def __init__(self):                        
        
        #create PROXYMODEL
        myModel.myProxyModel.__init__(self)  
        

   
# view <- proxymodel <- model 
class Times():
    def  __init__(self, view, db_table, keys):
        
        #create MODEL
        self.model = TimesModel(keys)        
        
        #create PROXY MODEL
        self.proxy_model = TimesProxyModel() 
        
        
        #assign MODEL to PROXY MODEL
        self.proxy_model.setSourceModel(self.model)
        
        #assign PROXY MODEL to VIEW
        self.view = view 
        self.view.setModel(self.proxy_model)
        self.view.setRootIsDecorated(False)
        self.view.setAlternatingRowColors(True)        
        self.view.setSortingEnabled(True)
        
        #TIMERs
        self.timer1s = QtCore.QTimer(); 
        self.timer1s.start(1000);
        self.noupdate = 0 
               
        self.db_table = db_table
        
        self.keys = keys
        
        #self.updateModel()
        #self.updateModel2()
        #self.createSlots()
    
    #UPDATE TABLE        
    def update(self, run_id):           
                                 
        #get TIMES from database & add them to the table
        self.model.removeRows(0, self.model.rowCount())        
        try:                
            times = self.db_table.getParX("run_id", run_id)            
            for time in times:            
                aux_array = [time["id"],time["run_id"],time["user_id"],time["time_str"]]
                self.model.addRow(aux_array)                     
        except:
            print "I: DB: tableTimes is empty! "          
        
        
    