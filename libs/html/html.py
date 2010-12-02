# -*- coding: utf-8 -*-

'''
Created on 17.9.2009
@author: Lubos Melichar
'''
import htmltags
import libs.dicts.dicts as dicts

def head(title, styles='', scripts=''):
    aux_head = htmltags.HEAD(htmltags.META(content="text/html; charset=utf-8"))
    aux_head <= htmltags.HEAD(htmltags.TITLE(title))
    for style in styles:
        aux_head <= htmltags.LINK(rel="Stylesheet",href=style)
    #for script in scripts:
        #aux_head <= htmltags.LINK(rel="Stylesheet",href=style)
    return aux_head
    


def dicts_to_table(dicts, keys_to_show, css_class = ""):
    
    tabulka = htmltags.TABLE(cellpadding="6", cellspacing="0",Class=css_class)
    
    #ZAHLAVI, klice - nadpisy sloupcu      
    '''zahlavi = htmltags.TR()  # inicializace proměnné
    for key in keys_to_show:        
        zahlavi <= htmltags.TH(key)
        
    tabulka <= zahlavi
    '''

    #radky
    for dict in dicts:
        radekTabulky = htmltags.TR()  # inicializace proměnné                
        for key in keys_to_show:  # pres vsechny existujici slovniky v datech                        
            if key in dict:
                radekTabulky <= htmltags.TD(dict[key])
            else:
                radekTabulky <= htmltags.TD('-')  #tento klic ve slovniku neni => '-'
        tabulka <= radekTabulky        
                      
    return tabulka


def list_to_table(list):
    
    #cellpadding="6" cellspacing="0"
    tabulka = htmltags.TABLE(cellpadding="6", cellspacing="0")        
    
    for i in range(0,len(list)):
        radek = htmltags.TR(htmltags.TD(i))        
        radek <= htmltags.TD( str(list[i]))
        tabulka <= radek        
    return tabulka

class Html(object):
    ''' classdocs '''

    def __init__(selfparams):
        pass

if __name__ == "__main__":
    dicts = [{u'klíč1':u"čeština", u'klíč2':u"maďarština", u'klíč3':u"francouština"},
            {u'klíč1':u"čeština", u'klíč3':u"maďarština", u'klíč6':u"francouština"}
            ]
    list = ["a","b"]
    
    
    print head("ahoj", ["aaaa"])
    print dicts
    keys=[]
        
    print keys
    #print dicts_to_table(dictss)
    print dicts_to_table(dicts, ["klíč1", 'klíč2'])
    print list_to_table(list)
    
        