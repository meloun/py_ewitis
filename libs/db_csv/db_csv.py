# -*- coding: utf-8 -*-

'''
Created on 16.9.2009
@author: Lubos Melichar


'''
import csv




class Db_csv():    
    def __init__(self, filename):
        self.filename = filename
        
    def load_from_file(self):                        
        reader = csv.reader(open(self.filename, "rb"), delimiter = ";", skipinitialspace=True)

        listofnames = []

        for name in reader:
            listofnames.append(name)
        
        return listofnames
    
if __name__ == '__main__':
    
    db = Db_json("Blizak_2010.csv")

    listofnames = db.load_from_file()  

    for i in listofnames:
        for h in i: 
            print h,";",
        print "\n-------------"
    
    print len(listofnames)    
        
           