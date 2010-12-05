#!/usr/bin/env python

import sys
from PyQt4 import Qt, QtCore, QtGui


MODE_EDIT, MODE_REFRESH = range(2)
SYSTEM_SLEEP, SYSTEM_WORKING = range(2)
    
class myModel(QtGui.QStandardItemModel):
    def __init__(self, keys):
        
        #model
        QtGui.QStandardItemModel.__init__(self, 0, len(keys))
        
        self.mode = MODE_EDIT
        
        #model structure
        for i in range(len(keys)):        
            self.setHeaderData(i, QtCore.Qt.Horizontal, keys[i]) 
            self.setHeaderData(i, QtCore.Qt.Horizontal, QtCore.QVariant(QtCore.Qt.AlignHCenter), QtCore.Qt.TextAlignmentRole)
        
        
    #setting flags for this model
    #first collumn is NOT editable
    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        
                                    
        if(self.mode ==  MODE_REFRESH):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
        #not editable items
        if (index.column() == 0):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def addRow(self, row):
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


              
