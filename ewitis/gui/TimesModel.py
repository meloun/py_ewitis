#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import ewitis.gui.GuiData as GuiData


class TimesModel(myModel.myModel):
    def __init__(self, view, name, db, guidata, keys):                        
                
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, view, name, db, guidata, keys)
        
        self.showall = False
        
        
        #update with first run        
        first_run = self.db.getFirst("runs")
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
        
        #print time_db
        
        #get USER
        user_db = self.db.getParX("users", "id", time_db["user_id"]).fetchone()
        
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
        #prepare data
        #aux_id = self.model.item(a.row(), 0).text()            
        #aux_time = self.model.item(a.row(), 2).text()
        #aux_nr = self.model.item(a.row(), 1).text()
        
        #find user par nr (from user table)
        #try:            
        #    user = self.db.getParX("users", "nr", tabTime['nr']).fetchone()
        #    aux_dict = {"id" : aux_id, "user_id": aux_user["id"], "time_str" : aux_time}
        #except:
        #    aux_dict = {"id" : aux_id, "time_str" : aux_time}
        #    print "E: Times: unknown user"
            
        user = self.db.getParX("users", "nr", tabTime['nr']).fetchone()
        
        print "user: ",user
        print "tabTime: ",tabTime
        
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
    def  __init__(self, view, db, guidata):  
        
        #table and db table name
        name = "times"  
        
        #table keys
        keys = ["id", "nr", "time", "name", "kategory", "address"]
        
                                            
        
        #create MODEL
        self.model = TimesModel(view, name, db, guidata, keys)        
        
        #create PROXY MODEL
        self.proxy_model = TimesProxyModel() 
        
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
        self.view.setColumnWidth(1,40)
        self.view.setColumnWidth(2,100)
        self.view.setColumnWidth(3,100)
        self.view.setColumnWidth(4,60)
        self.view.setColumnWidth(5,100)
        
        #TIMERs
        self.timer1s = QtCore.QTimer(); 
        self.timer1s.start(1000);
        
        #MODE EDIT/REFRESH        
        self.system = 0 
               
        self.db = db
        
        #self.keys = keys
        
        #$self.updateModel()        
        #self.createSlots()
        
    def createSlots(self):
        print "I: Runs: vytvarim sloty.."
        
        # DOUBLE_CLICKED - nahazuje no_update aby se updatem nerusila moznost editace
        #QtCore.QObject.connect(self.view, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.slot_Entered)
        
        # ACTIVATED -vznika jen u NOT editable, shazuje no_update 
        #QtCore.QObject.connect(self.proxy_model, QtCore.SIGNAL("entered(QModelIndex)"), self.slot_Entered2)
        
        # DATA_CHANGED - zpetny zapis do DB, shozeni no_update
        #QtCore.QObject.connect(self.model, QtCore.SIGNAL("dataChanged(QModelIndex, QModelIndex )"), self.slot_ModelChanged)
               
    #=======================================================================
    # SLOTS
    #=======================================================================
        
              
        
    #MODEL CHANGED        
    def slot_ModelChanged_old(self,a,b):
        
        #user change, no auto update
        if((self.guidata.mode == GuiData.MODE_EDIT) and (self.guidata.user_actions == GuiData.ACTIONS_ENABLE)):                  
            #prepare data
            aux_id = self.model.item(a.row(), 0).text()            
            aux_time = self.model.item(a.row(), 2).text()
            aux_nr = self.model.item(a.row(), 1).text()
            
            #find user par nr (from user table)
            try:            
                aux_user = self.db.getParX("users", "nr", aux_nr).fetchone()
                aux_dict = {"id" : aux_id, "user_id": aux_user["id"], "time_str" : aux_time}
            except:
                aux_dict = {"id" : aux_id, "time_str" : aux_time}
                print "E: Times: unknown user" 
                                                            
            #replace                         
            self.db.update_from_dict("times", aux_dict)
            
            print "replacing.. ", self.run_id, aux_dict 
            time.sleep(0.1)  
            self.update(self.run_id)                    
        
    
    #UPDATE TABLE        
    def update(self, run_id = None):                     
        self.model.update(run_id)                                                                                    
    

            
            

        
        
    