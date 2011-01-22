#!/usr/bin/env python

import sys
import time
from PyQt4 import Qt, QtCore, QtGui
import ewitis.gui.GuiData as GuiData
import libs.db_csv.db_csv as Db_csv

TABLE_RUNS, TABLE_TIMES, TABLE_USERS = range(3)
MODE_EDIT, MODE_REFRESH = range(2)
SYSTEM_SLEEP, SYSTEM_WORKING = range(2)
    
class myModel(QtGui.QStandardItemModel):
    def __init__(self, view, name, db, guidata, keys):
        
        #model
        QtGui.QStandardItemModel.__init__(self, 0, len(keys))                
        
        self.view = view
        self.name  = name
        self.db  = db
        self.guidata = guidata
        self.keys = keys
        self.mode = MODE_EDIT
        
        #model structure
        for i in range(len(keys)):        
            self.setHeaderData(i, QtCore.Qt.Horizontal, keys[i]) 
            self.setHeaderData(i, QtCore.Qt.Horizontal, QtCore.QVariant(QtCore.Qt.AlignHCenter), QtCore.Qt.TextAlignmentRole)
                    
        print self.name," : vytvarim sloty"
        QtCore.QObject.connect(self, QtCore.SIGNAL("itemChanged(QStandardItem *)"), self.slot_ModelChanged)
                
    #MODEL CHANGED - define editable rows
    #first collumn is NOT editable
    def flags(self, index):
        
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled        

        #refresh mode => NOT editable                                    
        if(self.mode ==  MODE_REFRESH):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
        #NOT editable items
        if (index.column() == 0):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable                    
        
    #MODEL CHANGED
    #model changed -> save to DB        
    def slot_ModelChanged(self, item):
                
        #user change, no auto update
        if((self.guidata.mode == GuiData.MODE_EDIT) and (self.guidata.user_actions == GuiData.ACTIONS_ENABLE)):                                          
            
            #virtual function
            #get dictionary with row-data, ready for DB
            tabRow = self.getRow(item.row())                        
                        
            dbRow = self.table2dbRow(tabRow)
                                                            
            #replace
            try:
                print "trying update"                                       
                self.db.update_from_dict(self.name, dbRow)
            except:
                QtGui.QMessageBox.warning(self.view, "Error", "User with this number already exist!")
            
            print "I: users: replacing.. ", dbRow            
            self.update()

    
    # get row values in dict
    def getRow(self, row):
        column = 0
        dict = {}
        
        for key in self.keys:            
            dict[key] = self.item(row, column).text()
            column += 1
        
        return dict    
                
    # go through all keys in dict,  if exist => value added 
    def addRow(self, row):
        nr_column = 0                        

        self.insertRow(0)                
                        
        #through defined keys
        for key in self.keys:                                        
                                                     
            #exist in row?                                               
            if (key in row.keys()):                                                                      
                
                #set data                                   
                self.setData(self.index(0,nr_column), row[key])
                
                #next column
                nr_column += 1
            else:
                print "NOT adding row ", key
                            
    
    
    # update model from DB
    # call table-specific function <= upgrade dictionary
    def update(self, parameter=None, value=None):
                
        self.guidata.user_actions = GuiData.ACTIONS_DISABLE
        
      
        
        #remove all rows
        self.removeRows(0, self.rowCount())  
        
        #get rows from DB
        if (parameter == None):                
            rows = self.db.getAll(self.name)
        else:
            rows = self.db.getParX(self.name, parameter, value)
        
        
                                    
        #add rows in table
        for row in rows:            
            
            #convert "db-row" to dict (in dict can be added record)
            row_dict = self.db.dict_factory(rows, row)
            
            #call table-specific function, return "table-row"                               
            row_table = self.db2tableRow(row_dict)                                                                                                
            
            #add row to the table            
            self.addRow(row_table)
                                 
        #except:
        #    print "I: DB ",self.name,": is empty! "
            
        self.guidata.user_actions = GuiData.ACTIONS_ENABLE
        
                                                        
    def addRow_old(self, row):
        self.insertRow(0)
        
        nr_column = 0
        for item in row:
            
            #set data           
            self.setData(self.index(0,nr_column), item)
            
            #set data alignment
            if (nr_column<2):
                self.setData(self.index(0,nr_column), QtCore.QVariant(QtCore.Qt.AlignHCenter), QtCore.Qt.TextAlignmentRole)
                       
            nr_column = nr_column+1
            

class myProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self):
        #model
        QtGui.QSortFilterProxyModel.__init__(self)
        self.setDynamicSortFilter(True)        
        self.setFilterKeyColumn(-1)
        
    #get ids
    def ids(self):
        ids = []
        for i in range(self.rowCount()):
            row = []
            index = self.index(i,0)                              
            ids.append(str(self.data(index).toString()))
        return ids
        
    #get headerData
    def header(self):
        header = []
        for i in range(self.columnCount()):
            header.append(str(self.headerData(i, 0x01).toString()))
        return header
    
    #get current state in lists
    def lists(self):
        rows = []
        for i in range(self.rowCount()):
            row = []
            for j in range(self.columnCount()):
                index = self.index(i,j)  
                row.append(str(self.data(index).toString()))            
            rows.append(row)
        return rows


class myTable():
    def  __init__(self, name, view, db, guidata, keys):                
                
        
        #name
        self.name = name
        
        #common Gui data
        self.guidata = guidata
        
        #create MODEL
        #self.model = UsersModel(db, guidata, keys)        
        
        #create PROXY MODEL
        #self.proxy_model = UsersProxyModel() 
        
        
        #assign MODEL to PROXY MODEL
        self.proxy_model.setSourceModel(self.model)
        
        #assign PROXY MODEL to VIEW
        '''self.view = view 
        self.view.setModel(self.proxy_model)
        self.view.setRootIsDecorated(False)
        self.view.setAlternatingRowColors(True)        
        self.view.setSortingEnabled(True)
        self.view.setColumnWidth(0,50)
        self.view.setColumnWidth(1,50)
        self.view.setColumnWidth(2,150)
        self.view.setColumnWidth(3,150)
        self.view.setColumnWidth(4,150)'''        
        
        #TIMERs
        self.timer1s = QtCore.QTimer(); 
        self.timer1s.start(1000);
        
        #MODE EDIT/REFRESH        
        self.mode = MODE_EDIT
               
        self.db = db
        
        self.keys = keys
        
                
        self.createSlots()
        
    def createSlots(self):
        print "I: XX:",self.name," vytvarim sloty.."
        
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
        
    def export_csv(self, filename, source='table'):
        aux_csv = Db_csv.Db_csv(filename) #create csv class
        
        #FROM TABLE 
        if(source == 'table'):
            #get table as lists; save into file in csv format                
            aux_csv.save(self.proxy_model.lists(), keys = self.keys) 
        
        #FROM DB
        elif(source == 'db'):
            ids = self.proxy_model.ids()
    
            conditions = []
            for id in ids:
                conditions.append(['id', id])
                            
            #get db as tuples; save into file in csv format
            rows = self.db.getParXX(self.name, conditions, 'OR')
            aux_csv.save(rows)
            
    def update(self):
                    
        #get row-selection
        try:
            rows = self.view.selectionModel().selectedRows()         
            model_index = rows[0] #selected row index #row = rows[0].row() if rows else 0        
        except:
            pass 
        
        self.model.update()
        
            
        #row-selection back                           
        try: 
            self.view.selectionModel().setCurrentIndex(model_index, QtGui.QItemSelectionModel.Rows | QtGui.QItemSelectionModel.SelectCurrent) #self.tables_info['runs']['selection']            
        except:
            pass
        
         
        
    def delete(self):
        self.db.delete(self.name)
        self.model.update()
        
    def deleteAll(self):
        self.db.deleteAll(self.name)
        self.model.update()
        
                                        
            
    #IMPORT
    #CSV - id, kategorie, prijmeni, jmeno, adresa,.. 
    #DB - id, nr, name, kategory, address 
    def importCsv2_old(self, filename):
        
        print "importCsv2"
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
        
        
        
                        
                
        
        
        
        


              
