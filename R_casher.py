#!/usr/bin/env python3
# Copyright 2009-2017 BHG http://bw.org/
import os
import csv
from tkinter import *
dir_path = os.path.dirname(__file__)
os.chdir(dir_path)

stockItemAttr = ["seller","fandom","maintype","bundle","price","details","stock"]

############################################################################################################################
#FUNCTION

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

def Input(csvfile,objectClass,ItemAttr): #for input->list->object
    newAttr = []
    i = 0
    newObject = objectClass()
    objectAttrLength = newObject.lenAttr()
    while i < objectAttrLength:
        newAttr.append(boxes[i].get() )
        i +=1
    if( os.path.isfile(csvfile) == False ):
            file = open(csvfile,"a+")
            text = listToCSVtxt( ItemAttr ) 
            file.write(text) 
            file.close
            
    file = open(csvfile,"a+")
    text = listToCSVtxt( newAttr )
    file.write( text )
    file.close
    
def storeInput():
    Input('stock.csv',stockItem,stockItemAttr)

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

def inputOrDefault( inp_val, def_val ):
    if inp_val == "":
        return def_val
    else:
        return inp_val

############################################################################################################################
#MAIN CLASS
class Item:
    
    def __init__(self, *args):
        # DEFAULT VALUES
        self.seller   = "Unknown seller"
        self.fandom   = "Unknown fandom"
        self.maintype = "Unknown type"
        self.bundle   = "Unknown bundle"
        self.price    = 0
        self.details  = "-"
        
        if len(args) > 1:
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
            # print("Empty object created")
            
    def initializeFromArgs(self,*args):
        # set the attr values with the 6 arguments
        self.seller   = inputOrDefault( args[0],"Unknown seller" )
        self.fandom   = inputOrDefault( args[1],"Unknown fandom" )
        self.maintype = inputOrDefault( args[2],"Unknown type" )
        self.bundle   = inputOrDefault( args[3],"Unknown bundle" )
        self.price    = inputOrDefault( args[4],0 ) 
        self.details  = inputOrDefault( args[5],"-" )
        
    def initializeFromList(self,argList):
        # set the attr values with the single "list" arguments
        self.seller   = inputOrDefault( argList[0],"Unknown seller" )
        self.fandom   = inputOrDefault( argList[1],"Unknown fandom" )
        self.maintype = inputOrDefault( argList[2],"Unknown type" )
        self.bundle   = inputOrDefault( argList[3],"Unknown bundle" )
        self.price    = inputOrDefault( argList[4],0 ) 
        self.details  = inputOrDefault( argList[5],"-" )
    
    def makeAttrList(self): 
        attrList = list(self.__dict__.keys()) 
        return attrList
    
    def lenAttr(self):
        attrLength = len(list(self.__dict__.keys()))
        return attrLength

#SUB CLASS
class stockItem(Item):
    def __init__(self,*args):
        self.stock = "0"
        super().__init__(*args)
        
        # Dealing with the extra input of "stock", unique to the stockItem class
        if( len(args) > 1 ):
            self.stock = inputOrDefault( args[6], 0 )
        elif len(args) == 1:
            if isinstance( args[0], list):
                self.stock = inputOrDefault( args[0][6], 0 ) 

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
objectList = importObject('stock.csv',stockItem)
printObjectList( objectList )

############################################################################################################################
#TKinter
root = Tk()
Label(root, text='Stock list').grid(row = 0,column =3)

#For Labels
i = 0
while i < stockItemAttrLength:
    title = str(stockItemAttr[i]).capitalize() 
    Label(root,text=title).grid(row=1,column = i)
    Label(root,text=title).grid(row=3,column = i)
    i += 1

#For displaying stock

#For Entries
i = 0
boxes = []
while i < stockItemAttrLength:
    entry = Entry(root)
    entry.grid(row=4, column=i)
    istr = str(i)
    boxes.append(entry)
    i += 1

Button(root,text = "Input", command=storeInput).grid(row=5)

mainloop()
############################################################################################################################