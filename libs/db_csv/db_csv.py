# -*- coding: utf-8 -*-

'''
Created on 16.9.2009
@author: Lubos Melichar


'''
import csv




class Db_csv():    
    def __init__(self, filename):
        self.filename = filename
        
    #load csv from file to lists
    def load(self, encode = 'utf8'):
                        
        reader = csv.reader(open(self.filename, "r"), delimiter = ";", skipinitialspace=True)
        

        listofnames = []

        for name in reader:
            listofnames.append(name)
        
        #print listofnames
        return listofnames
    
    #save csv into file from lists
    def save(self, lists, keys = [], encode = 'utf8'):
        
        my_string = ""
        
        my_string += ";".join(str(x) for x in keys) + "\n"            
        
        for list in lists:        
            my_string += ";".join(str(x) for x in list) + "\n"
                    
        my_string = my_string.encode(encode)
        
        #print my_string    
        
        FILE = open(self.filename, 'w')
        FILE.write(my_string)
        FILE.close()                   
        
    
if __name__ == '__main__':
    
    db = Db_csv("Blizak_2010.csv")

    listofnames = db.load()  

    for i in listofnames:
        for h in i: 
            print h,";",
        print "\n-------------"
    
    print len(listofnames)    
        
           