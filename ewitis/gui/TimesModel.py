#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import ewitis.gui.GuiData as GuiData


class TimesModel(myModel.myModel):
    def __init__(self, guidata, keys):                        
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, keys)
        self.GuiData = guidata
                
    
    #setting flags for this model
    #first collumn is NOT editable
    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        
        if(self.GuiData.mode == GuiData.MODE_REFRESH):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
        #id, name, kategory, addres NOT editable
        if ((index.column() == 0) or (index.column() == 3) or (index.column() == 4) or (index.column() == 5)):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

class TimesProxyModel(myModel.myProxyModel):
    def __init__(self):                        
        
        #create PROXYMODEL
        myModel.myProxyModel.__init__(self)  
        



   
# view <- proxymodel <- model 
class Times():
    def  __init__(self, view, db, guidata, keys):                
        
        #common Gui data
        self.guidata = guidata
        
        #create MODEL
        self.model = TimesModel(guidata, keys)        
        
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
        self.view.setColumnWidth(0,50)
        self.view.setColumnWidth(1,50)
        self.view.setColumnWidth(2,100)
        self.view.setColumnWidth(3,120)
        self.view.setColumnWidth(4,60)
        self.view.setColumnWidth(5,100)
        
        #TIMERs
        self.timer1s = QtCore.QTimer(); 
        self.timer1s.start(1000);
        
        #MODE EDIT/REFRESH        
        self.system = 0 
               
        self.db = db
        
        self.keys = keys
        
        #$self.updateModel()        
        self.createSlots()
        
    def createSlots(self):
        print "I: Runs: vytvarim sloty.."
        
        # DOUBLE_CLICKED - nahazuje no_update aby se updatem nerusila moznost editace
        #QtCore.QObject.connect(self.view, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.slot_Entered)
        
        # ACTIVATED -vznika jen u NOT editable, shazuje no_update 
        #QtCore.QObject.connect(self.proxy_model, QtCore.SIGNAL("entered(QModelIndex)"), self.slot_Entered2)
        
        # DATA_CHANGED - zpetny zapis do DB, shozeni no_update
        QtCore.QObject.connect(self.model, QtCore.SIGNAL("dataChanged(QModelIndex, QModelIndex )"), self.slot_ModelChanged)
               
    #=======================================================================
    # SLOTS
    #=======================================================================
        
              
        
    #MODEL CHANGED        
    def slot_ModelChanged(self,a,b):
        
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
    def update(self, run_id): 
        self.run_id = run_id                                               
        self.updateModel(run_id)  #update model                             
    
    #UPDATE TABLE        
    def updateModel(self, run_id):           
        
        #self.system = myModel.SYSTEM_WORKING
        self.guidata.user_actions = GuiData.ACTIONS_DISABLE
                               
        #get TIMES from database & add them to the table
        self.model.removeRows(0, self.model.rowCount())        
        try:                
            times = self.db.getParX("times","run_id", run_id)                        
            for time in times:
                
                #get USER
                user = self.db.getParX("users", "id", time["user_id"]).fetchone()
                                                             
                #add TABLE ROW                                                             
                aux_array = [time["id"], user['nr'], time["time_str"], user['name'], user['kategory'], user['address']]
                self.model.addRow(aux_array)                     
        except:
            print "I: DB: tableTimes is empty! "
            
        #self.system = myModel.SYSTEM_SLEEP
        self.guidata.user_actions = GuiData.ACTIONS_ENABLE
            
            

        
        
    