#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import ewitis.gui.UsersModel as UsersModel
import ewitis.gui.GuiData as GuiData



class TimesParameters(myModel.myParameters):
    def __init__(self, source):
                
        #table and db table name
        self.name = "Times" 
        
        #TABLE USERS
        self.tabUser = source.U   
        
        #=======================================================================
        # KEYS
        #=======================================================================
        self.KEYS_DEF = [ \
                        {"name":"state",      "tabName": None,         "dbName": "state"},\
                        {"name":"id",         "tabName": "id",         "dbName": "id"},\
                        {"name":"nr",         "tabName": "nr",         "dbName": None},\
                        {"name":"run_id",     "tabName": None,         "dbName": "run_id"},\
                        {"name":"user_id",    "tabName": None,         "dbName": "user_id"},\
                        {"name":"cell",       "tabName": None,         "dbName": "cell"},\
                        {"name":"time_raw",   "tabName": None,         "dbName": "time_raw"},\
                        {"name":"time",       "tabName": "time",       "dbName": "time"},\
                        {"name":"name",       "tabName": "name",       "dbName": None},\
                        {"name":"category",   "tabName": "category",   "dbName": None},                                                                                                                           
                    ] 
        
        #create MODEL and his structure
        myModel.myParameters.__init__(self, source)        
                                     
        print "TIME KEYS2:", self.keys               
        print "TIME KEYS2_DB:", self.keys_db                
                
    
                                
        #=======================================================================
        # GUI
        #=======================================================================
        self.gui = {} 
        #VIEW
        self.gui['view'] = source.ui.TimesProxyView
        
        #FILTER
        self.gui['filter'] = source.ui.TimesFilterLineEdit
        self.gui['filterclear'] = source.ui.TimesFilterClear
        
        #GROUPBOX
        self.gui['add'] = source.ui.TimesAdd
        self.gui['remove'] =  source.ui.TimesRemove
        self.gui['export'] = source.ui.TimesExport
        self.gui['import'] = None 
        self.gui['delete'] = source.ui.TimesDelete
        
        #COUNTER
        self.gui['counter'] = source.ui.timesCounter
                 
        
        
    

class TimesModel(myModel.myModel):
    def __init__(self, params):                        
                
        
        #create MODEL and his structure

        myModel.myModel.__init__(self, params)
        
        self.showall = False
        self.showzero = True
        
        
        #update with first run        
        first_run = self.params.db.getFirst("runs")
        if(first_run != None):
            self.run_id = first_run['id']
        else:
            self.run_id = 0 #no times for run_id = 0 
                
        self.update()
                
    
    #setting flags for this model
    #first collumn is NOT editable
    def flags(self, index): 
        
        #id, name, category, addres NOT editable
        if ((index.column() == 3) or (index.column() == 4) or (index.column() == 5)):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

        return myModel.myModel.flags(self, index)
    
    def getDefaultTableRow(self): 
        row = myModel.myModel.getDefaultTableRow(self)
        row['nr'] = "0"
        row['time'] = "00:00:00,00"
        print "timeROOW", row
        return row 
    
    #["id", "nr", "time", "name", "category", "address"]
    def db2tableRow(self, dbTime):
        
        
        #hide all zero time?
        if(self.showzero == False):
            if (dbTime["time"]=="00:00:00,00"):  
                return {}                        
        
        #get USER
        user_db = self.params.db.getParX("users", "id", dbTime["user_id"]).fetchone()
        
        #exist user?
        if user_db == None:
            user = {'id':0, 'nr':0, 'name':'unknown', 'category':'', 'address':''}
        #exist => restrict username                
        else:
            if(user_db['name']==''):
                user_db['name'] = 'nobody'
            user = UsersModel.UsersModel.db2tableRow(self.params.tabUser.model, user_db) 
            #user = user_db
        
                        
        #1to1 keys just copy
        tabTime = myModel.myModel.db2tableRow(self, dbTime)
        #other keys            
        tabTime['nr'] = user['nr']        
        tabTime['name'] = user['name']
        tabTime['category'] = user['category']
        tabTime['address'] = user['address']        
                
        return tabTime
                                                                                   
    
    def table2dbRow(self, tabTime): 
                    
        #1to1 keys just copy
        dbTime = myModel.myModel.table2dbRow(self, tabTime)
        
        #get user
        user = self.params.db.getParX("users", "nr", tabTime['nr']).fetchone()
        
        #other keys
        dbTime['run_id'] = self.run_id
        
        #user not found
        if(user == None):
            self.params.showmessage(self.params.name+" Update error", "No user with number "+tabTime['nr']+"!")
            return None                        
        
        dbTime['user_id'] = user['id']         
                                                                                                                                         
        return dbTime
    
    #UPDATE TABLE        
    def update(self, run_id = None):
        
        if(run_id != None):                    
            self.run_id = run_id #update run_id
            
        #update times
        if(self.showall):
            #update all times             
            myModel.myModel.update(self)            
        else:            
            #update for selected run        
            myModel.myModel.update(self, "run_id", self.run_id)
                                                     

class TimesProxyModel(myModel.myProxyModel):
    def __init__(self):                        
        
        #create PROXYMODEL
        myModel.myProxyModel.__init__(self)  
    
   
# view <- proxymodel <- model 
class Times(myModel.myTable):
#    def  __init__(self, view, db, guidata):  
    def  __init__(self, params):
        
        self.params = params               
                                                    
        #create MODEL
        self.model = TimesModel(params)        
        
        #create PROXY MODEL
        self.proxy_model = TimesProxyModel() 
        
        myModel.myTable.__init__(self, params)
        
        
        #assign MODEL to PROXY MODEL
        #self.proxy_model.setSourceModel(self.model)
        
        #assign PROXY MODEL to VIEW        
        self.params.gui['view'].setModel(self.proxy_model)
        self.params.gui['view'].setRootIsDecorated(False)
        self.params.gui['view'].setAlternatingRowColors(True)        
        self.params.gui['view'].setSortingEnabled(True)
        self.params.gui['view'].setColumnWidth(0,40)
        self.params.gui['view'].setColumnWidth(1,40)
        self.params.gui['view'].setColumnWidth(2,80)
        self.params.gui['view'].setColumnWidth(3,100)
        self.params.gui['view'].setColumnWidth(4,80)
        self.params.gui['view'].setColumnWidth(5,100)
        
        #TIMERs
        self.timer1s = QtCore.QTimer(); 
        self.timer1s.start(1000);
        
        #MODE EDIT/REFRESH        
        self.system = 0
            
    def update(self, run_id = None):                      
        self.model.update(run_id = run_id)                
        self.update_counter()                                                     
        
                                    
                                                                                            
    

            
            

        
        
    