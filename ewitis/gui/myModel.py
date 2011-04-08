#!/usr/bin/env python

import sys
import time
from PyQt4 import Qt, QtCore, QtGui
import ewitis.gui.GuiData as GuiData
import libs.db_csv.db_csv as Db_csv
import libs.sqlite.sqlite as sqlite

TABLE_RUNS, TABLE_TIMES, TABLE_USERS = range(3)
MODE_EDIT, MODE_LOCK, MODE_REFRESH = range(3)
SYSTEM_SLEEP, SYSTEM_WORKING = range(2)

#COMMON PARAMETERS for all tables
    #source.showMessage - callback METHOD,  for showing dialogs, messages
    #source.db - database
    #source.GuiData - 
    #self.KEYS_DEF - table definition
class myParameters():
    def __init__(self, source):
        
        #=======================================================================
        # KEYS
        #=======================================================================
        
        #table keys
        self.keys = []
        
        #db keys, needed for model.importCsv()
        self.keys_db = []
                
        #copy keys to lists (from table definition)
        for key in self.KEYS_DEF:
            if (key['tabName']):           
                self.keys.append(key['tabName'])
            if (key['dbName']):
                self.keys_db.append(key['dbName'])        
        
        #callback METHOD,  for showing dialogs, messages
        self.showmessage = source.showMessage
    
        #db for acces
        self.db = source.db
        
        #guidata
        self.guidata = source.GuiData
        
    @staticmethod    
    def getKey(keys, name):
        for key in keys:
            if name == key['name']:
                return key                                

                
class myModel(QtGui.QStandardItemModel):
    def __init__(self, params):
        
        
        self.params = params
        
        #model
        QtGui.QStandardItemModel.__init__(self, 0, len(self.params.keys))                
        

        self.mode = MODE_EDIT
        
        #model structure
        for i in range(len(self.params.keys)):        
            self.setHeaderData(i, QtCore.Qt.Horizontal, self.params.keys[i]) 
            self.setHeaderData(i, QtCore.Qt.Horizontal, QtCore.QVariant(QtCore.Qt.AlignHCenter), QtCore.Qt.TextAlignmentRole)
                    
        print self.params.name," : vytvarim sloty"
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
    

    #db2tableRow - convert DATABASE row to TABLE row
    #basic method, copy 1to1 keys
    def db2tableRow(self, dbRow):
        
        tabRow = {}
        
        #1to1 keys just copy
        for key in self.params.KEYS_DEF:            
                        
            #is for this key alias in DB also in TABLE?
            if((key['tabName']!=None) and (key['dbName']!=None)):
                tabRow[ key['tabName']] = dbRow[key['dbName']]
        
        return tabRow 
    
    #table2dbRow - convert TABLE row to DATABASE row       
    #basic method, copy 1to1 keys
    def table2dbRow(self, tabRow):
        
        dbRow = {}
        
        #1to1 keys just copy
        for key in self.params.KEYS_DEF:            
            
            #is for this key alias in DB also in TABLE?            
            if((key['tabName']!=None) and (key['dbName']!=None)):
                dbRow[ key['dbName']] = tabRow[key['tabName']]
                #convert to normal string
                
        #convert QString to str
        for key in dbRow.keys():
            if type(dbRow[key]) is Qt.QString:
                dbRow[key] = str(dbRow[key].toUtf8())
                
        return dbRow
            
    
    #MODEL CHANGED
    #model changed -> save to DB        
    def slot_ModelChanged(self, item):                        
        
        #user change, no auto update
        if((self.params.guidata.mode == GuiData.MODE_EDIT) and (self.params.guidata.user_actions == GuiData.ACTIONS_ENABLE)):                                                                  
                        
            #get dictionary with row-data, ready for DB
            tabRow = self.getRow(item.row())                                                      
            
            #dbRow <- tableRow
            dbRow = self.table2dbRow(tabRow)
                                        
            #exist row? 
            if (dbRow != None):                                                                            
                #update DB
                #try:
                    #print self.params.name, dbRow                                        
                self.params.db.update_from_dict(self.params.name, dbRow)
                #except:                
                #    self.params.showmessage(self.params.name+" Update", "Error!")
                #    return
                
            #update model                                                               
            self.update()            

    
    def getDefaultTableRow(self):        
        row = {}     
           
        for key in self.params.keys:            
            row[key] = ""
            
        
        if row.has_key('id'):
            try:
                row['id'] = self.params.db.getMax(self.params.name, 'id') + 1
            except:
                row['id'] = 0
                
        
        return row
    
    # get row values in dict
    def getRow(self, row):
        column = 0
        dict = {}
        
        for key in self.params.keys:            
            dict[key] = self.item(row, column).text()
            column += 1
        
        return dict    
                
    # go through all keys in dict,  if exist => value added 
    def addRow(self, row):
        nr_column = 0                        

        if (row == {}):            
            return
            
        self.insertRow(0)                
                        
        #through defined keys
        for key in self.params.keys:                                      
                                                     
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
                
        self.params.guidata.user_actions = GuiData.ACTIONS_DISABLE        
                      
        #remove all rows
        self.removeRows(0, self.rowCount())  
        
        #get rows from DB
        if (parameter == None):                
            rows = self.params.db.getAll(self.params.name)
        else:
            rows = self.params.db.getParX(self.params.name, parameter, value)
                                                    
        #add rows in table
        for row in rows:            
            
            #convert "db-row" to dict (in dict can be added record)
            row_dict = self.params.db.dict_factory(rows, row)
            
            #call table-specific function, return "table-row"                               
            row_table = self.db2tableRow(row_dict)                                                                                                
            
            #add row to the table            
            self.addRow(row_table)                                 
            
        self.params.guidata.user_actions = GuiData.ACTIONS_ENABLE                
                                                            
            

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
                mystr1 = self.data(index).toString()                   
                mystr2 = mystr1.toUtf8()                
                row.append(mystr2)            
            rows.append(row)
        return rows


class myTable():
    def  __init__(self, params):                
                        
        #name
        self.params = params        
        
        #assign MODEL to PROXY MODEL
        self.proxy_model.setSourceModel(self.model)               
        
        #TIMERs
        self.timer1s = QtCore.QTimer(); 
        self.timer1s.start(1000);
        
        #MODE EDIT/REFRESH        
        self.mode = MODE_EDIT                     
                
        self.createSlots()
        
        #update "Counter"
        self.sFilterRegExp()
        
    def createSlots(self):
        print "I: ",self.params.name," vytvarim sloty.."
        
        #TIMEOUT
        QtCore.QObject.connect(self.timer1s, QtCore.SIGNAL("timeout()"), self.slot_Timer1s)
        
        # CLEAR FILTER BUTTON -> CLEAR FILTER
        QtCore.QObject.connect(self.params.gui['filterclear'], QtCore.SIGNAL("clicked()"), self.sFilterClear)
        
        # FILTER CHANGE -> CHANGE TABLE
        QtCore.QObject.connect(self.params.gui['filter'], QtCore.SIGNAL("textChanged (const QString & )"), self.sFilterRegExp)
        
        # ADD ROW BUTTON
        QtCore.QObject.connect(self.params.gui['add'], QtCore.SIGNAL("clicked()"), self.sAdd)
        
        # REMOVE ROW BUTTON
        QtCore.QObject.connect(self.params.gui['remove'], QtCore.SIGNAL("clicked()"), self.sDelete)
        
        # IMPORT BUTTON -> CHANGE TABLE
        if (self.params.gui['import'] != None):
            QtCore.QObject.connect(self.params.gui['import'], QtCore.SIGNAL("clicked()"), self.sImport)   
            
        # EXPORT BUTTON
        QtCore.QObject.connect(self.params.gui['export'], QtCore.SIGNAL("clicked()"), self.sExport)
        
        # DELETE BUTTON -> EMPTY TABLE
        QtCore.QObject.connect(self.params.gui['delete'], QtCore.SIGNAL("clicked()"), self.sDeleteAll)
        
        #self.sFilterRegExp(filter, table, label_counter)
                             
    #=======================================================================
    # SLOTS
    #=======================================================================
        
    #UPDATE TIMER    
    def slot_Timer1s(self):                 
        if (self.params.guidata.mode == GuiData.MODE_REFRESH): 
            self.update()    #update table            
    
        # CLEAR FILTER BUTTON -> CLEAR FILTER        
    def sFilterClear(self):    
        self.params.gui['filter'].setText("")
                        
    # FILTER CHANGE -> CHANGE TABLE
    def sFilterRegExp(self):    
        regExp = QtCore.QRegExp(self.params.gui['filter'].text(), QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)
        self.proxy_model.setFilterRegExp(regExp)
        self.update_counter()
        #self.params['counter'].setText(str(self.proxy_model.rowCount())+"/"+str(self.model.rowCount()))
              
                 
    # ADD ROW               
    def sAdd(self):
        title = "Table "+self.params.name+" Add"                
        
        row = self.model.getDefaultTableRow()
                
        my_id = self.params.showmessage(title,"ID: ", type="input_integer", value = row['id'])
        
        if my_id == None:
            return
                
        res = self.params.db.getParId(self.params.name, my_id).fetchone()
        
        #this ID exist?
        if(res):
            self.params.showmessage(title,"Record with this ID already exist!")
            return
     
        #get dict for adding
        #row = {}
        #for key in self.params['keys']:
        #    row[key] = ''
        row['id'] = my_id
                
        self.model.params.guidata.user_actions = GuiData.ACTIONS_DISABLE        
        #self.model.addRow(row)
        #print "NOW", row
        dbRow = self.model.table2dbRow(row)
        if(dbRow != None):        
            self.params.db.insert_from_dict(self.params.name, dbRow)            
            self.params.showmessage(title,"succesfully (id="+str(my_id)+")", dialog = False)

        self.update()            
        self.model.params.guidata.user_actions = GuiData.ACTIONS_ENABLE
        
    # REMOVE ROW               
    def sDelete(self, label=""):                
        
        #title
        title = "Table '"+self.params.name + "' Delete"
                        
        #get selected id
        try:                     
            rows = self.params.gui['view'].selectionModel().selectedRows()                        
            id = self.proxy_model.data(rows[0]).toString()
        except:
            self.params.showmessage(title, "Nelze smazat")
            
        #confirm dialog and delete
        if (label!=""):
            label="\n\n("+label+")"        
        if (self.params.showmessage(title, "Are you sure you want to delete 1 record from table '"+self.params.name+"' ? \n (id="+str(id)+")"+label, type='warning_dialog')):                        
            self.delete(id)                          
                                                      
        
    # IMPORT
    # CSV FILE => DB               
    def sImport(self): 
                           
                                   
        #gui dialog -> get filename
        filename = QtGui.QFileDialog.getOpenFileName(self.params.gui['view'],"Import CSV to table "+self.params.name,"table_"+self.params.name+".csv","Csv Files (*.csv)")                
        
        #cancel or close window
        if(filename == ""):                 
            return        
                  
        #import
        try:              
            #state = table.importCsv2(filename)
            state = self.params.db.importCsv(self.params.name, filename, self.params.keys_db)
            self.model.update()
            self.sImportDialog(state)
        except sqlite.CSV_FILE_Error:
            self.params.showmessage(self.params.name+" CSV Import", "NOT Succesfully imported\n wrong file format")
                                
    def sImportDialog(self, state):                            
        #title
        title = "Table '"+self.params.name + "' CSV Import"
        
        if(state['ko'] != 0) :
            self.params.showmessage(title, "NOT Succesfully"+"\n\n" +str(state['ok'])+" record(s) imported.\n"+str(state['ko'])+" record(s) NOT imported.\n\n Probably already exist.")                                                            
        else:
            self.params.showmessage(title,"Succesfully"+"\n\n" +str(state['ok'])+" record(s) imported.", type='info')                                               
        
    # EXPORT
    # WEB (or DB) => CSV FILE
    # what you see, is exported    
    def sExport(self, source='table'):                        
        
        #get filename, gui dialog 
        filename = QtGui.QFileDialog.getSaveFileName(self.params.gui['view'],"Export table "+self.params.name+" to CSV","table_"+self.params.name+".csv","Csv Files (*.csv)")                
        if(filename == ""):
            return              
        
        #title
        title = "Table '"+self.params.name + "' CSV Export"
         
        #export to csv file
        #try:                        
        self.export_csv(filename, source)                                
        self.params.showmessage(title, "Succesfully", dialog=False)            
        #except:            
        #    self.params['showmessage'](title, "NOT succesfully \n\nCannot write into the file")
                     
                        
    # DELETE BUTTON          
    def sDeleteAll(self):
        
        #title
        title = "Table '"+self.params.name + "' Delete"
        
        #confirm dialog and delete
        if (self.params.showmessage(title, "Are you sure you want to delete table '"+self.params.name+"' ?", type='warning_dialog')):
            self.deleteAll()                                            
    
                  
        
    def export_csv(self, filename, source='table'):
        aux_csv = Db_csv.Db_csv(filename) #create csv class
        
        #FROM TABLE 
        if(source == 'table'):
            #get table as lists; save into file in csv format                
            aux_csv.save(self.proxy_model.lists(), keys = self.params.keys) 
        
        #FROM DB
        elif(source == 'db'):
            ids = self.proxy_model.ids()
    
            conditions = []
            for id in ids:
                conditions.append(['id', id])
                            
            #get db as tuples; save into file in csv format
            rows = self.params.db.getParXX(self.params.name, conditions, 'OR')
            aux_csv.save(rows)
            
    def update(self, parameter=None, value=None, selectionback=True):
        
        print "basic update"
                    
        #get row-selection
        if(selectionback==True):
            try:
                rows = self.params.gui['view'].selectionModel().selectedRows()         
                model_index = rows[0] #selected row index #row = rows[0].row() if rows else 0         
            except:
                pass 
        
        self.model.update(parameter, value)
        
            
        #row-selection back
        if(selectionback==True):                           
            try:                
                self.params.gui['view'].selectionModel().setCurrentIndex(model_index, QtGui.QItemSelectionModel.Rows | QtGui.QItemSelectionModel.SelectCurrent)            
            except:
                pass
        
        self.update_counter()
        
    def update_counter(self):        
        self.params.gui['counter'].setText(str(self.proxy_model.rowCount())+"/"+str(self.model.rowCount()))
                         
    def delete(self, id):

        self.params.db.delete(self.params.name, id)                          
        self.model.update()
        
    def deleteAll(self):
        self.params.db.deleteAll(self.params.name)
        self.model.update()
        
                                        
        
        
        
                        
                
        
        
        
        


              
