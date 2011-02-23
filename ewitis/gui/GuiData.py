#!/usr/bin/env python

import sys
from PyQt4 import Qt, QtCore, QtGui


MODE_EDIT, MODE_LOCK, MODE_REFRESH = range(3)
ACTIONS_ENABLE, ACTIONS_DISABLE = range(2)
    
class GuiData():    
    def __init__(self):
        self.mode = MODE_EDIT
        self.user_actions = ACTIONS_ENABLE
        