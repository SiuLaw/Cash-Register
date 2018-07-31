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
    file = open( csvfile ,'r')
    spamreader = csv.reader( file ,delimiter = ",")
    table = []
    for line in spamreader:
        table.append(line)
    objectList = []
    col_title_passed = False
    for line in table:
        if( col_title_passed == False ):
            col_title_passed = True
            continue

        newObject = objectClass(line[0],line[1],line[2],line[3],line[4],line[5],line[6])
        objectList.append( newObject )
    file.close
    
    return objectList

def printObjectList( objectList ):
    for obj in objectList:
        print( obj.__dict__ )

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
            # When the args are input as individually ( i.e. 
            self.initializeFromArgs(*args)
            
    def initializeFromArgs(self,*args):
        self.seller   = args[0]
        self.fandom   = args[1]
        self.maintype = args[2]
        self.bundle   = args[3]
        self.price    = args[4]
        self.details  = args[5]
    
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
        
        if( len(args) == 7 ):
            self.stock = args[6]

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