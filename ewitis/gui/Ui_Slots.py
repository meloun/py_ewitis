#!/usr/bin/env python

#SIGNALs & SLOTs
#class for adding and manage signals and slots

import sys
from PyQt4 import Qt, QtCore, QtGui


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
        QtCore.QObject.connect(btn_import, QtCore.SIGNAL("clicked()"), lambda : self.sImport(table))        
        
        # DELETE BUTTON -> EMPTY TABLE
        QtCore.QObject.connect(btn_delete, QtCore.SIGNAL("clicked()"), lambda : self.sDelete(table))
        
        
    # CLEAR FILTER BUTTON -> CLEAR FILTER        
    def sFilterClear(self,filter):    
        filter.setText("")
                        
    # FILTER CHANGE -> CHANGE TABLE
    def sFilterRegExp(self, filter, table):    
        regExp = QtCore.QRegExp(filter.text(), QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)
        table.proxy_model.setFilterRegExp(regExp)      
    
            
    # IMPORT BUTTON -> CHANGE TABLE     
    #WEB - id, kategorie, prijmeni, jmeno, adresa,.. 
    #DB - id, nr, name, kategory, address 
    def sImport(self, table):                        
        fileName = QtGui.QFileDialog.getOpenFileName(self.gui,"a","aa","Csv Files (*.csv)") 
        print "aa",fileName        
        state = table.importCsv("Blizak_2010.csv")
        self.sImportDialog(table, state)
        
    def sImportDialog(self, table, state):               
        #error message
        title = "Import"
        if(state['ko'] != 0) :                                               
            message = str(state['ko'])+" record(s) NOT succesfully imported.\n\n Probably already exist."
            QtGui.QMessageBox.warning(self.gui, title, message)
        else:
            message = str(state['ok'])+" record(s) succesfully imported."
            QtGui.QMessageBox.information(self.gui, title, message)            
        #self.ui.statusbar.showMessage(title+" : " + message)
        
    # EXPORT BUTTON -> EXPORT CSV     
    #WEB - id, kategorie, prijmeni, jmeno, adresa,.. 
    #DB - id, nr, name, kategory, address 
    def sExport(self, table):                        
        print "exportuji.."
                        
    # DELETE BUTTON -> EXPORT CSV         
    #WEB - id, kategorie, prijmeni, jmeno, adresa,.. 
    #DB - id, nr, name, kategory, address 
    def sDelete(self, table):                        
        print "delete.."
    