#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import ewitis.gui.UsersModel as UsersModel
import ewitis.gui.GuiData as GuiData
import ewitis.gui.TimesUtils as Utils
import libs.utils.utils as utils








class TimesParameters(myModel.myParameters):
    def __init__(self, source):
                
        #table and db table name
        self.name = "Times" 
        
        #TABLED
        self.tabUser = source.U 
        
        #guidata
        self.guidata = source.GuiData          
        
        #=======================================================================
        # KEYS
        #=======================================================================
        if(self.guidata.measure_mode == GuiData.MODE_TRAINING):
            self.KEYS_DEF = [ \
                            {"name":"state",      "tabName": None,         "dbName": "state"},\
                            {"name":"id",         "tabName": "id",         "dbName": "id"},\
                            {"name":"nr",         "tabName": "nr",         "dbName": None},\
                            {"name":"run_id",     "tabName": None,         "dbName": "run_id"},\
                            {"name":"user_id",    "tabName": None,         "dbName": "user_id"},\
                            {"name":"cell",       "tabName": "cell",       "dbName": "cell"},\
                            {"name":"time_raw",   "tabName": None,         "dbName": "time_raw"},\
                            {"name":"time",       "tabName": "time",       "dbName": "time"},\
                            {"name":"name",       "tabName": "name",       "dbName": None},\
                            {"name":"category",   "tabName": "category",   "dbName": None},                                                                                                                           
                        ]
        elif(self.guidata.measure_mode == GuiData.MODE_RACE):
            self.KEYS_DEF = [ \
                            {"name":"state",      "tabName": None,              "dbName": "state"}, \
                            {"name":"id",         "tabName": "id",              "dbName": "id"},\
                            {"name":"nr",         "tabName": "nr",              "dbName": None},\
                            {"name":"run_id",     "tabName": None,              "dbName": "run_id"},\
                            {"name":"user_id",    "tabName": None,              "dbName": "user_id"},\
                            {"name":"cell",       "tabName": "cell",            "dbName": "cell"},\
                            {"name":"time_raw",   "tabName": None,              "dbName": "time_raw"},\
                            {"name":"time",       "tabName": "time",            "dbName": "time"},\
                            {"name":"name",       "tabName": "name",            "dbName": None},\
                            {"name":"category",   "tabName": "category",        "dbName": None},\
                            {"name":"order",      "tabName": "order",           "dbName": None},\
                            {"name":"order_kat",  "tabName": "order in cat.",   "dbName": None},\
                            {"name":"start_nr",   "tabName": "start_nr",        "dbName": None},                                                                                                                         
            ]
             
        
        #create MODEL and his structure
        myModel.myParameters.__init__(self, source)        
                                
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
        self.gui['export_www'] = source.ui.TimesWwwExport
        self.gui['import'] = None 
        self.gui['delete'] = source.ui.TimesDelete
        
        #COUNTER
        self.gui['counter'] = source.ui.timesCounter
        
        
                 
        
        
    

class TimesModel(myModel.myModel):
    def __init__(self, params):                        
                
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, params)
        
        #add utils function
        self.utils = Utils.TimesUtils(self)
        
                
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
        if ((index.column() == 4) or (index.column() == 5) or (index.column() == 6)):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

        return myModel.myModel.flags(self, index)
    
    def getDefaultTableRow(self): 
        row = myModel.myModel.getDefaultTableRow(self)
        row['cell'] = "N"                  
        row['nr'] = "0"        
        row['time'] = "00:00:00,00"                    
        return row                 

    
    #["id", "nr", "cell", "time", "name", "category", "address"]
    def db2tableRow(self, dbTime):
        
        
        #hide all zero time?
        if(self.showzero == False):
            if (dbTime["time"]=="00:00:00,00"):  
                return {}                        
        
        ''' USER '''         
        user =  self.params.tabUser.get_tab_user(dbTime["user_id"]) 
                        
        ''' 1to1 KEYS '''
        tabTime = myModel.myModel.db2tableRow(self, dbTime)        
                                    
        #time                         
        tabTime['start_nr'] = self.params.guidata.getStartNr(user['nr']) #get starttime number                          
        tabTime['time'] = self.utils.dbtime2tabtime( dbTime, tabTime['start_nr']) #dbtime -> tabtime
        
        #other keys             
        tabTime['nr'] = user['nr']        
        tabTime['name'] = user['name']
        tabTime['category'] = user['category']
        tabTime['address'] = user['address']
        tabTime['cell'] = dbTime['cell']                  
        
        
        #RACE MODE?
        if(self.params.guidata.measure_mode == GuiData.MODE_RACE):
            
            dbTime["category"] = tabTime['category']
            
            #GET ORDER
            try:
                order = self.utils.getOrder(dbTime)
                if(order["start"] >= order["end"]):                    
                    tabTime['order'] = '%03d' % order["start"]
                    #tabTime['order'] = str(order["start"])
                else:
                    tabTime['order'] = '%03d - %03d ' % (order["start"], order["end"])
                    #tabTime['order'] = str(order["start"])+" - "+str(order["end"])                
            except self.utils.ZeroRawTime_Error, self.utils.NoneRawTime_Error:
                tabTime['order'] = None
                    
            #GET ORDER IN CATEGEORY
            try:
                order_incategory = self.utils.getOrder(dbTime, incategory=True)                                                           
                if(order_incategory["start"] >= order_incategory["end"]):  
                    #tabTime['order in cat.'] = order_incategory["start"]                  
                    tabTime['order in cat.'] = '%03d' % order_incategory["start"]
                    #tabTime['order in cat.'] = str(order_incategory["start"])           
                else:
                    #tabTime['order in cat.'] = order_incategory["start"]
                    tabTime['order in cat.'] = '%03d - %03d ' % (order_incategory["start"], order_incategory["end"])
                    #tabTime['order in cat.'] = str(order_incategory["start"])+" - "+str(order_incategory["end"])
            except:
                tabTime['order in cat.'] = None
            
            
            #tabTime['order'] = aux_order       
            #tabTime['order in cat.'] = aux_order2              
                
        return tabTime
                                                                                   
    
    def table2dbRow(self, tabTime): 
                            
        #1to1 keys, just copy
        dbTime = myModel.myModel.table2dbRow(self, tabTime)        
        
        #user nr => user id
        if(tabTime['nr'] == "0"):
            dbTime['user_id'] = 0
        else:
            user = self.params.db.getParX("users", "nr", tabTime['nr']).fetchone() 
                             
            #user not found => nothing to save
            if(user == None):
                self.params.showmessage(self.params.name+" Update error", "No user with number "+str(tabTime['nr'])+"!")
                return None
            
            #add user_id                     
            dbTime['user_id'] = user['id']    
        
        #get TIME in absolut format                 
        try:        
            #get raw time 
            dbTime['time_raw'] = self.utils.time2timeraw(tabTime['time'])
            
            #incement start time        
            if(tabTime['start_nr']):
                dbTime['time_raw'] = dbTime['time_raw'] + self.start_times[int(tabTime['start_nr'])-1]['time_raw']        
        except:
            self.params.showmessage(self.params.name+" Update error", "Wrong time format.!")
            return None                                
            
        dbTime['run_id'] = self.run_id 
            
                                                                                                                                         
        return dbTime
    

    
    
     
        
    
    #UPDATE TABLE        
    def update(self, run_id = None):
        
        if(run_id != None):                    
            self.run_id = run_id #update run_id
            
        #update start times
        self.start_times = self.utils.getStartTimes(self.run_id)
        
        #update times
        if(self.showall):
            
            #get run ids
            conditions = []
            ids = self.params.tabRuns.proxy_model.ids()                     
            for id in ids:
                conditions.append(['run_id', id])                            
                                         
            #update all times             
            myModel.myModel.update(self, conditions = conditions, operation = 'OR')            
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
        self.params.gui['view'].setColumnWidth(2,30)
        self.params.gui['view'].setColumnWidth(3,80)
        self.params.gui['view'].setColumnWidth(4,80)
        self.params.gui['view'].setColumnWidth(5,100)
        self.params.gui['view'].setColumnWidth(6,100)
        
        #TIMERs
        self.timer1s = QtCore.QTimer(); 
        self.timer1s.start(1000);
        
        #MODE EDIT/REFRESH        
        self.system = 0
            
    def update(self, run_id = None):                      
        self.model.update(run_id = run_id)                
        self.update_counter()                                                             
        
                                    
                                                                                            
    

            
            

        
        
    