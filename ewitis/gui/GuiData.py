# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
from PyQt4 import Qt, QtCore, QtGui

#MEASURE MODE
# MODE_TRAINING - simple version for customers 
# MODE_RACE - full version
MODE_TRAINING, MODE_RACE = range(2)
MEASURE_MODE_STRINGS = {MODE_TRAINING:"training", MODE_RACE:"race"}

#RACE & TRAINING SETTINGS
TRAINING_STANDART = {"name": u"standard",
                }

DEFAULT_RACE = {"name": u"ewitis race",
                "starts": [ {"nr_min":   0, "nr_max":  999, "nr_start": 1},                                                        
                          ]
                }

BC_KRALOVICE = {"name": u"Kralovický MTB Maraton",
                "starts": [ {"category" : "Kategorie A", "nr_min":   0, "nr_max":  49, "nr_start": 1},
                            {"category" : "Kategorie A", "nr_min":  50, "nr_max":  99, "nr_start": 2},
                            {"category" : "Kategorie A", "nr_min": 100, "nr_max": 149, "nr_start": 3},
                          ]
                }

#TABLE MODE
# EDIT - enable editing
# LOCK - disable editing
# REFRESH - automatic refreshing (disable editing)
MODE_EDIT, MODE_LOCK, MODE_REFRESH = range(3)

#USER ACTION
# ACTION_ENABLE - 
# ACTION_DISABLE - 
ACTIONS_ENABLE, ACTIONS_DISABLE = range(2)

#    
class GuiData():    
    def __init__(self):
        
        #MEASURE MODE
        #self.measure_mode = MODE_TRAINING    
        self.measure_mode = MODE_RACE
        
        #measure_setting  => RACE & TRAINING SELECT
        if(self.measure_mode == MODE_RACE):
            self.measure_setting = BC_KRALOVICE
        else:
            self.measure_setting = TRAINING_STANDART
        
        self.table_mode = MODE_EDIT
        self.user_actions = ACTIONS_ENABLE
        
    def getMesureModeString(self):
        return MEASURE_MODE_STRINGS[self.measure_mode]
    
    def getRaceName(self):          
        return self.measure_setting["name"]
    
    #get number of start according to user number
    def getStartNr(self, user_nr):
        for start in self.measure_setting['starts']:
            if (user_nr > start['nr_min']) and (user_nr < start['nr_max']):
                return start['nr_start']
        return None
        
        
        