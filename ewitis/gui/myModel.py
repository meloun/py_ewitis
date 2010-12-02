#!/usr/bin/env python

import sys
from PyQt4 import QtCore, QtGui


    
    
class myModel(QtGui.QStandardItemModel):
    def __init__(self, keys):
        
        #model
        QtGui.QStandardItemModel.__init__(self, 0, len(keys))
        
        #model structure
        for i in range(len(keys)):        
            self.setHeaderData(i, QtCore.Qt.Horizontal, keys[i]) 
        
    #setting flags for this model
    #first collumn is NOT editable
    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        
        if (index.column() == 0):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def addRow(self, row):
        self.insertRow(0)
        
        nr_column = 0
        for item in row:
            #print "pridavam", item, nr_column            
            self.setData(self.index(0,nr_column), item)       
            nr_column = nr_column+1
            

class myProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self):
        #model
        QtGui.QSortFilterProxyModel.__init__(self)
        self.setDynamicSortFilter(True)        
        self.setFilterKeyColumn(-1)


              
