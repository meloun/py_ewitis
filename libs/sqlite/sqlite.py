'''
Created on 01.06.2010

@author: MELICHARL
'''
#-*- coding: utf-8 -*-  
from sqlite3 import dbapi2 as sqlite
import time

import libs.db_csv.db_csv as Db_csv

class CSV_FILE_Error(Exception): pass

#SQLITE DATABASE
# - getAll(), getParId(), getParX(), insert_from_lists
class sqlite_db(object):
    def __init__(self, db_name):        
        self.db_name = db_name 
        
    def lists_factory(self, cursor):                
        d = []
        
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d  
    
    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d       
        
    def connect(self):
        self.db = sqlite.connect(self.db_name)        
        self.db.row_factory = sqlite.Row
        
    def commit(self):        
        res = self.db.commit()                                          
        return res 
            
    def query(self, query):
        #print "query: ",query
        res = self.db.execute(query)                
        return res
        
    def getAll(self, tablename):
        query = "SELECT * from " + tablename        
        res = self.query(query)
        return res
    
    def getFirst(self, tablename):                
        res = self.getAll(tablename)  
        return res.fetchone()          
        
    def getParId(self, tablename, id):
        query = "select * from " + tablename + " where id = " + str(id)
        res = self.query(query)
        return res
    
    def getParX(self, tablename, parameter, value):
        query = "select * from " + tablename + " where " + parameter +" = " + str(value)        
        res = self.query(query)
        return res
    
    def getParXX(self, tablename, conditions, operation):
        
        #where_string = (" "+operation+" ").join(condition[0]+" = " + str(condition[1]) for condition in conditions)
        
        conditions_list = []
        
        #list of conditions in format ["id = 5","id = 8",..]
        for condition in conditions:
            conditions_list.append(condition[0]+" = " + str(condition[1]))
        
        #separate conditions with 'operator' - AND, OR, ..
        where_string =  (" "+operation+" ").join(conditions_list)
        
        query = "select * from " + tablename + " where " + where_string     
        
        res = self.query(query)
        return res

    ###########
    # INSERT
    ###########
    
    def insert_from_lists(self, tablename, keys, values, commit = True):
                
        
        '''vytvoreni stringu pro dotaz, nazvy sloupcu a hodnot '''        
        values_str = ','.join(["\""+str(x)+"\"" for x in values])
        keys_str = ','.join(keys)
            
        #print keys_str
        #print values_str
        
        '''sestaveni a provedeni dotazu'''
        query = "insert into %s(%s) values(%s)" % (tablename, keys_str, values_str)
        
        res = self.query(query)
        
        if(commit == True):
            self.commit()
        return res
    
    '''vlozeni jednoho zaznamu z dict'''
    def insert_from_dict(self, tablename, dict,  commit = True):        
        return self.insert_from_lists(tablename, dict.keys(), dict.values(), commit = commit )        
    
    ###########
    # REPLACE
    ###########
    
    '''nahrazeni jednoho zaznamu z lists'''
    def replace_from_lists(self, tablename, keys, values):
        
        '''vytvoreni stringu pro dotaz, nazvy sloupcu a hodnot '''        
        values_str = ','.join(["\""+str(x)+"\"" for x in values])
        keys_str = ','.join(keys)
            
        #print keys_str
        #print values_str
        
        '''sestaveni a provedeni dotazu'''
        query = "replace into %s(%s) values(%s)" % (tablename, keys_str, values_str)
        res = self.db.query(query)
        self.db.commit()
        return res
    
    
    ###########
    # UPDATE
    # - update users SET  kategory="Kat D", nr="4" WHERE id = "4"
    # - record has to exist
    ###########
    def update_from_lists(self, tablename, keys, values):
        
        #print keys
        #print values
        
        res = '' 
                       
        '''vytvoreni stringu pro dotaz, 
        column1=value, column2=value2,... '''                      
        mystring = ','.join([" "+str(k)+"=\""+str(v)+"\"" for k,v in zip(keys, values)])                            
        
        '''sestaveni a provedeni dotazu'''
        query = "update %s SET %s WHERE id = \"%s\"" % (tablename, mystring, values[0])        
        res = self.query(query)
        self.db.commit()
            
        return res
    
    def update_from_dict(self, tablename, dict):
        
        keys = dict.keys()
        values = dict.values()
                
        
        res = '' 
                       
        '''vytvoreni stringu pro dotaz, 
        column1=value, column2=value2,... '''                      
        mystring = ','.join([" "+str(k)+"=\""+str(v)+"\"" for k,v in zip(keys, values)])                            
        
        '''sestaveni a provedeni dotazu'''
        query = "update %s SET %s WHERE id = \"%s\"" % (tablename, mystring, dict['id'])                
              
        res = self.query(query)        
        self.db.commit()
            
        return res
        

    ###########
    # DELETE
    ###########                
    def delete(self, tablename, id):
        query = "delete from " + tablename
        
        res = self.query(query)
        self.db.commit()
        
    def deleteAll(self, tablename):
        query = "delete from " + tablename
        
        res = self.query(query)
        self.db.commit()
        
    #=============
    # IMPORT
    #=============
    # exception: CSV_FILE_Error (check the first line => header)
    #
    def importCsv(self, tablename, filename, keys):
                
        #create DB        
        aux_csv = Db_csv.Db_csv(filename)
        rows =  aux_csv.load()
        
        #counters
        state = {'ko':0, 'ok':0}                        
        
        #wrong file format?
        if (rows==[]) or (rows.pop(0) != keys):
            raise CSV_FILE_Error         
            
        for row in rows:                                                              
                                                      
            #ADD USER
            #try:            
            self.insert_from_dict(tablename, dict(zip(keys, row)), commit = False)
            state['ok'] += 1            
            #except:
            #    state['ko'] += 1 #increment errors for error message

        self.db.commit()                        
        
        return state         
        
if __name__ == "__main__":
    import json
  
    print "start"
    
    '''define db and tables'''
    db = sqlite_db("test_db.sqlite")   
    myTable = sqlite_table(db, "runs")
    
    '''connect to db'''  
    db.connect()    
    
    '''get 1 row par id'''  
    res = myTable.get(16)
    for rec in res:
        print rec['id']
    
    '''insert row from dict'''
    dict = {"state":1,"id":666} 
    myTable.insert_from_dict(dict)    
    
    '''insert row from lists'''
    keys = ["state","id"]
    values = [5, 888] 
    myTable.insert_from_lists(keys, values)          
    
    
    
    


    


    


            
    for i in res:       
        print i['id']
        #print i.keys()              
    print "end"     
   