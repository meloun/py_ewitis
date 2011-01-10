'''
Created on 01.06.2010

@author: MELICHARL
'''
#-*- coding: utf-8 -*-  
from sqlite3 import dbapi2 as sqlite
import time

#SQLITE DATABASE
# - getAll(), getParId(), getParX(), insert_from_lists
class sqlite_db(object):
    def __init__(self, db_name):        
        self.db_name = db_name        
        
    def connect(self):
        self.db = sqlite.connect(self.db_name)
        self.db.row_factory = sqlite.Row
        
    def commit(self):        
        res = self.db.commit()                                          
        return res 
            
    def query(self, query):
        #print query
        res = self.db.execute(query)                
        return res
        
    def getAll(self, tablename):
        query = "SELECT * from " + tablename        
        res = self.query(query)
        return res           
        
    def getParId(self, tablename, id):
        query = "select * from " + tablename + " where id = " + str(id)
        res = self.query(query)
        return res
    
    def getParX(self, tablename, parameter, value):
        query = "select * from " + tablename + " where " + parameter +" = " + str(value)        
        res = self.query(query)
        return res

    ###########
    # INSERT
    ###########
    
    def insert_from_lists(self, tablename, keys, values):
        
        '''vytvoreni stringu pro dotaz, nazvy sloupcu a hodnot '''        
        values_str = ','.join(["\""+str(x)+"\"" for x in values])
        keys_str = ','.join(keys)
            
        #print keys_str
        #print values_str
        
        '''sestaveni a provedeni dotazu'''
        query = "insert into %s(%s) values(%s)" % (tablename, keys_str, values_str)
        res = self.query(query)
        self.commit()
        return res
    
    '''vlozeni jednoho zaznamu z dict'''
    def insert_from_dict(self, tablename, dict):
        return self.insert_from_lists(tablename, dict.keys(), dict.values())        
    
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
        
        print keys
        print values
        
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
        print query        
        res = self.query(query)
        self.db.commit()
            
        return res
        

    ###########
    # DELETE
    ###########                
    def delete(self, tablename, id):
        query = "select " + tablename
        print query
        
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
   