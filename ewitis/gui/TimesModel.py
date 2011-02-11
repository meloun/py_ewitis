#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import ewitis.gui.GuiData as GuiData


class TimesParameters(myModel.myParameters):
    def __init__(self, source):
        
        #create MODEL and his structure
        myModel.myParameters.__init__(self, source)
        
        self.params['ui']  = source.ui
        
        #table and db table name
        self.params['name'] = "times"  
        
        #table keys
        self.params['keys'] = ["id", "nr", "time", "name", "kategory", "address"]
        
        #db for acces
        self.params['db'] = source.db
        
        #guidata
        self.params['guidata'] = source.GuiData
                                
        #=======================================================================
        # GUI
        #=======================================================================
        #VIEW
        self.params['view'] = source.ui.TimesProxyView
        
        #FILTER
        self.params['filter'] = source.ui.TimesFilterLineEdit
        self.params['filterclear'] = source.ui.TimesFilterClear
        
        #GROUPBOX
        self.params['add'] = source.ui.TimesAdd
        self.params['remove'] =  source.ui.TimesRemove
        self.params['export'] = source.ui.TimesExport
        self.params['import'] = None 
        self.params['delete'] = source.ui.TimesDelete
        
        #COUNTER
        self.params['counter'] = source.ui.timesCounter
                 
        
        
    

class TimesModel(myModel.myModel):
    def __init__(self, params):                        
                
        
        #create MODEL and his structure

        myModel.myModel.__init__(self, params)
        
        self.showall = False
        self.showzero = True
        
        
        #update with first run        
        first_run = self.params['db'].getFirst("runs")
        if(first_run != None):
            self.run_id = first_run['id']
        else:
            self.run_id = 0 #no times for run_id = 0 
                
        self.update()
                
    
    #setting flags for this model
    #first collumn is NOT editable
    def flags(self, index): 
        
        #id, name, kategory, addres NOT editable
        if ((index.column() == 3) or (index.column() == 4) or (index.column() == 5)):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

        return myModel.myModel.flags(self, index)
    
    #["id", "nr", "time", "name", "kategory", "address"]
    def db2tableRow(self, time_db):
        
        
        #hide all zero time?
        if(self.showzero == False):
            if (time_db["time_str"]=="00:00:00,00"):  
                return {}
        
        
        #print time_db
        
        #get USER
        user_db = self.params['db'].getParX("users", "id", time_db["user_id"]).fetchone()
        
        #exist user?
        if user_db == None:
            user = {'id':0, 'nr':0, 'name':'unknown', 'kategory':'', 'address':''}
        #exist => restrict username                
        else:
            if(user_db['name']==''):
                user_db['name'] = 'nobody'
            user = user_db            
        
        time_table = {}
        time_table['id'] = time_db["id"]
        time_table['nr'] = user['nr']
        time_table['time'] = time_db["time_str"]
        time_table['name'] = user['name']
        time_table['kategory'] = user['kategory']
        time_table['address'] = user['address']
        time_table['description'] = user['address']
                
        return time_table
    
    def table2dbRow(self, tabTime): 
            
        user = self.params['db'].getParX("users", "nr", tabTime['nr']).fetchone()
        
        
        if(user == None):
            dbTime = {'id': tabTime['id'], 'time_str' : tabTime['time']}
        else:
            dbTime = {'id': tabTime['id'], 'user_id':user['id'], 'time_str' : tabTime['time']} 
                                                                                                                                         
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
        self.params['view'].setModel(self.proxy_model)
        self.params['view'].setRootIsDecorated(False)
        self.params['view'].setAlternatingRowColors(True)        
        self.params['view'].setSortingEnabled(True)
        self.params['view'].setColumnWidth(0,40)
        self.params['view'].setColumnWidth(1,40)
        self.params['view'].setColumnWidth(2,80)
        self.params['view'].setColumnWidth(3,100)
        self.params['view'].setColumnWidth(4,80)
        self.params['view'].setColumnWidth(5,100)
        
        #TIMERs
        self.timer1s = QtCore.QTimer(); 
        self.timer1s.start(1000);
        
        #MODE EDIT/REFRESH        
        self.system = 0
            
    def update(self, run_id = None):                
        self.model.update(run_id = run_id)                
        self.update_counter()                                                    
        

               
    #=======================================================================
    # SLOTS
    #=======================================================================
        
              
        
    #MODEL CHANGED        
    def slot_ModelChanged_old(self,a,b):
        
        #user change, no auto update
        if((self.params['guidata'].mode == GuiData.MODE_EDIT) and (self.params['guidata'].user_actions == GuiData.ACTIONS_ENABLE)):                  
            #prepare data
            aux_id = self.model.item(a.row(), 0).text()            
            aux_time = self.model.item(a.row(), 2).text()
            aux_nr = self.model.item(a.row(), 1).text()
            
            #find user par nr (from user table)
            try:            
                aux_user = self.params['db'].getParX("users", "nr", aux_nr).fetchone()
                aux_dict = {"id" : aux_id, "user_id": aux_user["id"], "time_str" : aux_time}
            except:
                aux_dict = {"id" : aux_id, "time_str" : aux_time}
                print "E: Times: unknown user" 
                                                            
            #replace                         
            self.params['db'].update_from_dict("times", aux_dict)
            
            print "replacing.. ", self.run_id, aux_dict 
            time.sleep(0.1)  
            self.update(self.run_id)                    
                                                                                            
    

            
            

        
        
    