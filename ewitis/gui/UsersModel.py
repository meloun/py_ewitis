#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import ewitis.gui.GuiData as GuiData


class UsersModel(myModel.myModel):
    def __init__(self, guidata, keys):                        
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, keys)
        self.GuiData = guidata
        
    #first collumn is NOT editable      
    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        
        if(self.GuiData.mode == GuiData.MODE_REFRESH):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
        #id NOT editable
        if (index.column() == 0):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
                

class UsersProxyModel(myModel.myProxyModel):
    def __init__(self):                        
        
        #create PROXYMODEL
        myModel.myProxyModel.__init__(self)  
        



   
# view <- proxymodel <- model 
class Users():
    def  __init__(self, view, db, guidata, keys):                
        
        #common Gui data
        self.guidata = guidata
        
        #create MODEL
        self.model = UsersModel(guidata, keys)        
        
        #create PROXY MODEL
        self.proxy_model = UsersProxyModel() 
        
        
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
        self.view.setColumnWidth(2,150)
        self.view.setColumnWidth(3,150)
        self.view.setColumnWidth(4,150)        
        
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
        print "I: Users: vytvarim sloty.."
        
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
            aux_nr = self.model.item(a.row(), 1).text()            
            aux_name = self.model.item(a.row(), 2).text()
            aux_kategory = self.model.item(a.row(), 3).text()
            aux_address = self.model.item(a.row(), 4).text()
            
            aux_dict = {"id" : aux_id, "nr" : aux_nr, "name" : aux_name, "kategory" : aux_kategory, "address" : aux_address}
            print "E: Times: unknown user" 
                                                            
            #replace                         
            self.db.update_from_dict("users", aux_dict)
            
            print "I: users: replacing.. ", aux_dict 
            time.sleep(0.1)  
            self.updateModel()                     
        
    
    #UPDATE TABLE        
    def update(self): 
        pass         
    
    #UPDATE TABLE        
    def updateModel(self):           
        
        self.guidata.user_actions = GuiData.ACTIONS_DISABLE
        
        #get TIMES from database & add them to the table
        self.model.removeRows(0, self.model.rowCount())
        
        try:                
            users = self.db.getAll("users")                        
            for user in users:                            
                                                             
                #add TABLE ROW                                                             
                aux_array = [user["id"], user['nr'], user["name"], user['kategory'], user['address']]
                self.model.addRow(aux_array)                     
        except:
            print "I: DB: tableTimes is empty! "
            
        self.guidata.user_actions = GuiData.ACTIONS_ENABLE
        
        
            
            

        
        
    