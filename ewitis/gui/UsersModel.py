#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import ewitis.gui.GuiData as GuiData
import libs.db_csv.db_csv as Db_csv




class UsersModel(myModel.myModel):
    def __init__(self, view, name, db, guidata, keys):                        
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, view, name, db, guidata, keys)

        self.update()                    

        
    #first collumn is NOT editable      
    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        
        if(self.guidata.mode == GuiData.MODE_REFRESH):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
        #id NOT editable
        if (index.column() == 0):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
    
    #"id", "nr", "name", "kategory", "address"
    def db2tableRow(self, dbUser):                                        
        
        
        tabUser = {}
        tabUser['id'] = dbUser['id']
        tabUser['nr'] = dbUser['nr']
        tabUser['name'] = dbUser['name']
        tabUser['kategory'] = dbUser['kategory']
        tabUser['address'] = dbUser['address']
                                
        return tabUser
    
    def table2dbRow(self, tabUser): 
        dbUser = {"id" : tabUser['id'], "nr" : tabUser['nr'], "name" :  tabUser['name'], "kategory" :  tabUser['kategory'], "address" : tabUser['address']}                                                                       
        return dbUser    
 
        
                

class UsersProxyModel(myModel.myProxyModel):
    def __init__(self):                        
        
        #create PROXYMODEL
        myModel.myProxyModel.__init__(self)  
        


# view <- proxymodel <- model 
class Users(myModel.myTable):
    def  __init__(self, name, view, db, guidata, keys):                
                
        #create MODEL
        self.model = UsersModel(view, name, db, guidata, keys)        
        
        #create PROXY MODEL
        self.proxy_model = UsersProxyModel() 
        
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
        self.view.setColumnWidth(1,50)
        self.view.setColumnWidth(2,150)
        self.view.setColumnWidth(3,150)
        self.view.setColumnWidth(4,150)        
        
        #TIMERs
        self.timer1s = QtCore.QTimer(); 
        self.timer1s.start(1000);
        
        #MODE EDIT/REFRESH        
        #self.mode = myModel.MODE_REFRESH
               
        #self.db = db
        
        #self.keys = keys
        
        #self.model.update()        
        #self.createSlots()
        
       
# view <- proxymodel <- model 
class Users_old(myModel.myTable):
    def  __init__(self, view, db, guidata, keys):                
        
        myModel.myTable.__init__(self, view, db, guidata, keys)
        
        #name
        self.name = "Users"
        
        #common Gui data
        #self.guidata = guidata
        
        #create MODEL
        self.model = UsersModel(db, guidata, keys)        
        
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
        self.mode = myModel.MODE_REFRESH
               
        self.db = db
        
        self.keys = keys
        
        self.model.update()        
        self.createSlots()
        
    def createSlots(self):
        print "I: Users: vytvarim sloty.."
        
        QtCore.QObject.connect(self.timer1s, QtCore.SIGNAL("timeout()"), self.slot_Timer1s);
        # DATA_CHANGED - zpetny zapis do DB, shozeni no_update
        #QtCore.QObject.connect(self.model, QtCore.SIGNAL("dataChanged(QModelIndex, QModelIndex )"), self.slot_ModelChanged)
               
    #=======================================================================
    # SLOTS
    #=======================================================================
        
    #UPDATE TIMER    
    def slot_Timer1s(self):        
        if (self.guidata.mode == GuiData.MODE_REFRESH): 
            self.update()    #update table              
        
    #MODEL CHANGED
    #zmenil se model -> save to DB        
    def slot_ModelChanged_old(self,a,b):
        
        #user change, no auto update
        if((self.guidata.mode == GuiData.MODE_EDIT) and (self.guidata.user_actions == GuiData.ACTIONS_ENABLE)):                                          
            
            #prepare data
            aux_id = self.model.item(a.row(), 0).text()
            aux_nr = self.model.item(a.row(), 1).text()            
            aux_name = self.model.item(a.row(), 2).text()
            aux_kategory = self.model.item(a.row(), 3).text()
            aux_address = self.model.item(a.row(), 4).text()
            
            aux_dict = {"id" : aux_id, "nr" : aux_nr, "name" : aux_name, "kategory" : aux_kategory, "address" : aux_address}                        
                                                            
            #replace
            try:                         
                self.db.update_from_dict("users", aux_dict)
            except:
                QtGui.QMessageBox.information(self.view, "Error", "User with this number already exist!")
            
            print "I: users: replacing.. ", aux_dict 
            time.sleep(0.1)  
            self.model.update()                     
        
    #IMPORT
    #CSV - id, kategorie, prijmeni, jmeno, adresa,.. 
    #DB - id, nr, name, kategory, address 
    def importCsv(self, filename):
        
        #create DB        
        aux_csv = Db_csv.Db_csv(filename)
        users =  aux_csv.load()
        
        #counters
        state = {'ko':0, 'ok':0}        
            
        for user in users:
                                           
            #prepare dict in SQL format
            user_db = { 'id': user[0], 'nr': user[0], 'name': user[2], 'kategory': user[1], 'address' : user[4]}
            
            #print user_db                                                 
            
            #ADD USER
            try:            
                self.db.insert_from_dict("users", user_db)
                state['ok'] += 1
            
            except:
                state['ko'] += 1 #increment errors for error message

        self.db.commit()                
        self.model.update()
        
        return state 
    
    def delete(self):
        self.db.delete("users")
        self.model.update()
        
    def deleteAll(self):
        self.db.deleteAll("users")
        self.model.update()
               
                
    
    #UPDATE TABLE        
    def update(self): 
        print "aa"
        self.model.update()  #update model          
    

        
        
            
            

        
        
    