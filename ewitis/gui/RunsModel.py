# -*- coding: utf-8 -*-
#!/usr/bin/env python

# 
#
#
#

import sys
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel

class RunsModel(myModel.myModel):
    def __init__(self, keys):                        
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, keys)

class RunsProxyModel(myModel.myProxyModel):
    def __init__(self):                        
        
        #create PROXYMODEL
        myModel.myProxyModel.__init__(self)        
        
              
        
    
# view <- proxymodel <- model 
class Runs():
    def  __init__(self, view, db, keys):
        
        #create MODEL
        self.model = RunsModel(keys)
        #self.model.addRow(["aa","ab","vf"])
        
        #create PROXY MODEL        
        self.proxy_model = RunsProxyModel()
        
        
        #assign MODEL to PROXY MODEL
        self.proxy_model.setSourceModel(self.model)
        
        #assign PROXY MODEL to VIEW
        self.view = view 
        self.view.setModel(self.proxy_model)
        self.view.setRootIsDecorated(False)
        self.view.setAlternatingRowColors(True)        
        self.view.setSortingEnabled(True)
        self.view.setColumnWidth(0,50)
        self.view.setColumnWidth(1,130)
        self.view.setColumnWidth(2,150)
        self.view.setColumnWidth(3,100)
        
        #TIMERs
        self.timer1s = QtCore.QTimer() 
        self.timer1s.start(1000)
        
        self.mode = myModel.MODE_EDIT  
        self.noupdate = 0 
               
        self.db = db
        
        self.keys = keys
        
        self.updateModel()
        self.createSlots()
        
        
        
                                           
    def createSlots(self):
        print "I: Runs: vytvarim sloty.."
        QtCore.QObject.connect(self.view, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.slot_Entered)
        QtCore.QObject.connect(self.timer1s, QtCore.SIGNAL("timeout()"), self.slot_Timer1s);
        QtCore.QObject.connect(self.model, QtCore.SIGNAL("dataChanged(QModelIndex, QModelIndex )"), self.slot_ModelChanged)        

    
    #=======================================================================
    # SLOTS
    #=======================================================================
    
    # ENTER in table
    # by editing no update
    def slot_Entered(self):
        print "I: tableRuns: entered" 
        self.noupdate = 20
                
    #UPDATE TIMER    
    def slot_Timer1s(self):        
        if (self.model.mode == myModel.MODE_REFRESH): 
            self.update()    #update table            

    #MODEL CHANGED        
    def slot_ModelChanged(self,a,b):
        
        if(self.noupdate != 0): #user change, no auto update              
            mylist = []
            
            #take changed row
            for item in self.model.takeRow(a.row()):                
                mylist.append(item.text())
                
            #replace                         
            self.db.update_from_lists("runs",self.keys, mylist)
        self.noupdate = 0
        

    #UPDATE TABLE        
    def update(self):        
        if(self.noupdate == 0):                        
            self.updateModel()  #update model            
        else:
            print "I:noupdate: ",self.noupdate
            self.noupdate = self.noupdate - 1   #now I cant update, decremet update counter 
              

         
    #UPDATE MODEL
    def updateModel(self):
                
        #ziskani oznaceneho radku z tableRuns 
        try:
            rows = self.view.selectionModel().selectedRows()         
            model_index = rows[0] #selected row index #row = rows[0].row() if rows else 0
        except:
            pass              
            
        #get RUNS from database & add them to the table                    
        runs = self.db.getAll("runs")
        self.model.removeRows(0,self.model.rowCount())                
        for run in runs:
            aux_items = []
            
            #get USER
            user = self.db.getParX("users", "id", run["name_id"]).fetchone()             
            
            aux_array = [run["id"], run["date"], user["name"], run["description"]]
            
                            
            #for key in self.keys:                            
            #    if key in run.keys(): #content run this value?
            #        aux_items.append(run[key])                                                    
            self.model.addRow(aux_array)
            
        #selection back                           
        try: 
            self.view.selectionModel().setCurrentIndex(model_index, QtGui.QItemSelectionModel.Rows | QtGui.QItemSelectionModel.SelectCurrent) #self.tables_info['runs']['selection']            
        except:
            pass
            
                                
        #selection back
        #aux_index = self.model.index(row,0)                
        #self.view.selectionModel().setCurrentIndex(aux_index, QtGui.QItemSelectionModel.Rows | QtGui.QItemSelectionModel.SelectCurrent) #self.tables_info['runs']['selection']
