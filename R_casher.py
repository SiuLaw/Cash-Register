#!/usr/bin/env python3
# Copyright 2009-2017 BHG http://bw.org/
import os
import csv
import gc
from tkinter import *
dir_path = os.path.dirname(__file__)
os.chdir(dir_path)

stockItemAttr = ["seller","fandom","maintype","bundle","price","details","stock"]

############################################################################################################################
#FUNCTION

# Part of input
def listToCSVtxt( input_list ):
    output_text = ""
    length = len( input_list )
    for i in range( length ):
        output_text += input_list[i]
        if i < length - 1:
            output_text += ","
        else:
            output_text += "\n"
    return output_text 

# Input -> list -> stored into csv file
def Input(csvfile,objectClass,ItemAttr): 
    newAttr = []
    i = 0
    newObject = objectClass()
    objectAttrLength = newObject.lenAttr()
    
    #turning input into list
    while i < objectAttrLength:
        newAttr.append(boxes[i].get() )
        i +=1
    
    #turning storing list via listToCSVtxt
    if( os.path.isfile(csvfile) == False ):
            file = open(csvfile,"a+")
            text = listToCSVtxt( ItemAttr ) 
            file.write(text) 
            file.close
            
    file = open(csvfile,"a+")
    text = listToCSVtxt( newAttr )
    file.write( text )
    file.close

# Storing stock
def stockInput():
    Input('stock.csv',stockItem,stockItemAttr)
    stockList = importObject('stock.csv',stockItem)
    display_stock(root,stockList)

# Read csvfile -> import as objects
def importObject( csvfile ,objectClass):
    # initialize the objectList for output
    objectList = []
    
    # Stop the import if the csvfile does not exist
    if ( os.path.isfile( csvfile ) == False ):
        print( "There are no existing csv file named: " + csvfile )
        return objectList
    
    file = open( csvfile ,'r')
    spamreader = csv.reader( file ,delimiter = ",")
    table = []
    for line in spamreader:
        table.append(line)
    
    col_title_passed = False
    for i in range( len(table) ):
        line = table[i]
        if( col_title_passed == False ):
            col_title_passed = True
            continue

        # newObject = objectClass(line[0],line[1],line[2],line[3],line[4],line[5],line[6])
        newObject = objectClass( line )
        objectList.append( newObject )
    file.close
    
    return objectList

def printObjectList( objectList ):
    for obj in objectList:
        print( obj.__dict__ )

# Converting empty input into default value
def inputOrDefault( inp_val, def_val ):
    if inp_val == "":
        return def_val
    else:
        return inp_val

# Making a list consisted of objects
def objectintoList (x,objectClass):
    olist = []
    for things in x:
        if isinstance(things,objectClass):
            olist.append(things)
    return olist

############################################################################################################################
#GUI FUNCTION
def display_label(root):
    #For Labels
    i = 0
    while i < stockItemAttrLength:
        title = str(stockItemAttr[i]).capitalize() 
        Label(root,text = title).grid(row = 1,column = i)
        Label(root,text = title).grid(row = 3,column = i)
        i += 1
    print( "label display updated" )

def display_stock(root,stockList):
    #For displaying stock
    i = 0
    lists = []
    n = stockItemAttrLength
    
    #while loop to create enough boxes for all stockItemAttr
    while i < n: 
        list_stock = Listbox(root) 
        list_stock.grid(row = 2,column = i) 
        lists.append(list_stock)
        q = 0
    
        #inserting attribute of each imputed objects into listbox
        while q < len(stockList): #
            for things in stockList:
                attribute = stockList[q]
                list_stock.insert(END, attribute.switcher(i))
                q += 1
        i += 1
    print( "stock display updated" )

############################################################################################################################
#MAIN CLASS
class Item:
    
    def __init__(self, *args): #*args = for any number of arguments
        # DEFAULT VALUES
        self.seller   = "Unknown seller"
        self.fandom   = "Unknown fandom"
        self.maintype = "Unknown type"
        self.bundle   = "Unknown bundle"
        self.price    = 0
        self.details  = "-"
        
        if len(args) >= 6:
            # When the args are input as individually ( i.e. Item( seller, fandom, maintype, bundle, price, details ) )
            self.initializeFromArgs(*args)
        elif len(args) == 1:
            # When there is only one input, then check that it is a list
            if( isinstance( args[0], list) ):
                self.initializeFromList(args[0])
            else:
                print("Only one input and not list")
        else:
            pass
            
    # Set the attr values with the 6 arguments
    def initializeFromArgs(self,*args):

        self.seller   = inputOrDefault( args[0],"Unknown seller" )
        self.fandom   = inputOrDefault( args[1],"Unknown fandom" )
        self.maintype = inputOrDefault( args[2],"Unknown type" )
        self.bundle   = inputOrDefault( args[3],"Unknown bundle" )
        self.price    = inputOrDefault( args[4],0 ) 
        self.details  = inputOrDefault( args[5],"-" )
        
    # Set the attr values with the single "list" arguments
    def initializeFromList(self,argList):
        self.seller   = inputOrDefault( argList[0],"Unknown seller" )
        self.fandom   = inputOrDefault( argList[1],"Unknown fandom" )
        self.maintype = inputOrDefault( argList[2],"Unknown type" )
        self.bundle   = inputOrDefault( argList[3],"Unknown bundle" )
        self.price    = inputOrDefault( argList[4],0 ) 
        self.details  = inputOrDefault( argList[5],"-" )
    
    # Amount of attribute, for number of loops needed
    def lenAttr(self):
        attrLength = len(list(self.__dict__.keys()))
        return attrLength
    
#SUB CLASS
class stockItem(Item):
    
    def __init__(self,*args):
        self.stock = "0"
        super().__init__(*args) #inherit all arguments from class Item
        
        # Dealing with the extra input of "stock", unique to the stockItem class
        if( len(args) == 7 ):
            self.stock = inputOrDefault( args[6], 0 )
        elif len(args) == 1:
            if isinstance( args[0], list):
                self.stock = inputOrDefault( args[0][6], 0 )
    
    #calling attributes with number
    def switcher(self,number):
        switcher = {
            0: self.seller,
            1: self.fandom,
            2: self.maintype,
            3: self.bundle,
            4: self.price,
            5: self.details,
            6: self.stock
        }
        return switcher.get(number, 0)
    
    def sales(self):
        self.stock = int(self.stock) - 1
        
class salesItem(Item):
    
    def __init__(self,seller = "Unknown seller", fandom="Unknown fandom",maintype = "Unknown type",bundle = "Unknown bundle",price = 0,details = "-", discount = False, alternativePrice = 0):
        super().__init__(seller,fandom,maintype,bundle,price,details)
        self.discount = discount
        self.alternativePrice = alternativePrice

#For grabbing stuff from 
def readFile(x):
    file = open(x,"r")
  
############################################################################################################################
#DEFAULT ITEMS

#Deafult StockItem
defaultStockItem = stockItem()
stockItemAttrLength = defaultStockItem.lenAttr()

############################################################################################################################
#OBJECT INPUT
#Object into list
objectList = importObject('stock.csv',stockItem)
allObject = gc.get_objects()
stockList = objectintoList (allObject,stockItem)

############################################################################################################################
#TKinter
root = Tk()
Label(root, text='Stock list').grid(row = 0,column = 3)
Button(root,text = "Input", command=stockInput).grid(row = 5)


#For Labels
display_label(root)
        
#For displaying stock
display_stock(root,stockList)

#For Entries
i = 0
boxes = []
while i < stockItemAttrLength:
    entry = Entry(root)
    entry.grid(row = 4, column = i)
    istr = str(i)
    boxes.append(entry)
    i += 1

mainloop()
############################################################################################################################