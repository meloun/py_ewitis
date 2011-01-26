#!/usr/bin/env python

#SIGNALs & SLOTs
#class for adding and manage signals and slots

import sys
from PyQt4 import Qt, QtCore, QtGui
import libs.db_csv.db_csv as Db_csv
import libs.sqlite.sqlite as sqlite


class AddSignal():
    def __init__(self, gui):
        self.gui = gui

   
    def table(self, table, filter, btn_clearfilter, btn_add, btn_remove, btn_export, btn_import, btn_delete):
        
        # CLEAR FILTER BUTTON -> CLEAR FILTER
        QtCore.QObject.connect(btn_clearfilter, QtCore.SIGNAL("clicked()"), lambda : self.sFilterClear(filter))
        
        # FILTER CHANGE -> CHANGE TABLE
        QtCore.QObject.connect(filter, QtCore.SIGNAL("textChanged (const QString & )"), lambda : self.sFilterRegExp(filter, table))
        
        # EXPORT BUTTON -> EXPORT CSV
        QtCore.QObject.connect(btn_export, QtCore.SIGNAL("clicked()"), lambda : self.sExport(table))
        
        # IMPORT BUTTON -> CHANGE TABLE
        if (btn_import != None):
            QtCore.QObject.connect(btn_import, QtCore.SIGNAL("clicked()"), lambda : self.sImport(table))        
        
        # DELETE BUTTON -> EMPTY TABLE
        QtCore.QObject.connect(btn_delete, QtCore.SIGNAL("clicked()"), lambda : self.sDeleteAll(table))
        
        
    # CLEAR FILTER BUTTON -> CLEAR FILTER        
    def sFilterClear(self,filter):    
        filter.setText("")
                        
    # FILTER CHANGE -> CHANGE TABLE
    def sFilterRegExp(self, filter, table):    
        regExp = QtCore.QRegExp(filter.text(), QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)
        table.proxy_model.setFilterRegExp(regExp)      
    
     
    
    # IMPORT
    # CSV FILE => DB               
    def sImport(self, table): 
                           
        filename = QtGui.QFileDialog.getOpenFileName(self.gui,"Import CSV to table "+table.name,"table_"+table.name+".csv","Csv Files (*.csv)")        
        
        #cancel or close window
        if(filename == ""):                 
            return        
                  
        try:              
            #state = table.importCsv2(filename)
            state = table.db.importCsv(table.name, filename, table.keys)
            table.model.update()
            self.sImportDialog(table, state)
        except sqlite.CSV_FILE_Error:
            self.gui.showMessage(table.name+" CSV Import", "NOT Succesfully imported\n wrong file format")
        #except:
        #    self.gui.showMessage(table.name+" CSV Import", "nothing imported", type="info", dialog=False)
            
            
        
    def sImportDialog(self, table, state):               
        #error message
        title = table.name+" CSV Import"
        if(state['ko'] != 0) :                                               
            self.gui.showMessage(title, "NOT Succesfully"+"\n\n" +str(state['ok'])+" record(s) imported.\n"+str(state['ko'])+" record(s) NOT imported.\n\n Probably already exist.") 
        else:                        
            self.gui.showMessage(title,"Succesfully"+"\n\n" +str(state['ok'])+" record(s) imported.", type='info')                                
        
    # EXPORT
    # WEB (or DB) => CSV FILE
    # what you see, is exported    
    def sExport(self, table, source='table'):                        
        
        #get filename, gui dialog 
        filename = QtGui.QFileDialog.getSaveFileName(self.gui,"Export table "+table.name+" to CSV","table_"+table.name+".csv","Csv Files (*.csv)")                
        if(filename == ""):
            return
              
        #title
        title = table.name + " CSV Export"
         
        #export to csv file
        try:                        
            table.export_csv(filename, source)                                
            self.gui.showMessage(title, "Succesfully", dialog=False)            
        except:            
            self.gui.showMessage(title, "NOT succesfully \n\nCannot write into the file")
                     
                        
    # DELETE BUTTON          
    def sDeleteAll(self, table):
        table.deleteAll()                                
    