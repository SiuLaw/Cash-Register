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

# def storeInput(): #for input->list->object
#     newStockAttr = []
#     i = 0
#     while i < stockItemAttrLength:
#         newStockAttr.append(boxes[i].get() )
#         i +=1
#     if( os.path.isfile("stock.csv") == False ):
#             file = open("stock.csv","a+")
#             text = listToCSVtxt( stockItemAttr ) 
#             file.write(text) 
#             file.close
#             
#     file = open("stock.csv","a+")
#     text = listToCSVtxt( newStockAttr )
#     file.write( text )
#     # file.write(str(newStockAttr))
#     file.close  

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
    def Input('stock.csv',stockItem,stockItemAttr)

def importObject( fileName,objectClass):
    file = open( fileName ,'r')
    spamreader = csv.reader( fileName ,delimiter = ",")
    table = []
    for line in spamreader:
        table.append(line)
    for line in table:
        newObject = objectClass(table[0],table[1],table[2],table[3],table[4],table[5],table[6])
    file.close

############################################################################################################################
#MAIN CLASS
class Item:
    def __init__(self,seller = "Unknown seller", fandom="Unknown fandom",maintype = "Unknown type",bundle = "Unknown bundle",price = 0,details = "-",stock = "0"):
        self.seller = seller
        self.fandom = fandom
        self.maintype = maintype
        self.bundle = bundle
        self.price = price
        self.details = details
    
    def makeAttrList(self): 
        attrList = list(self.__dict__.keys()) 
        return attrList
    
    def lenAttr(self):
        attrLength = len(list(self.__dict__.keys()))
        return attrLength

#SUB CLASS
class stockItem(Item):
    def __init__(self,seller = "Unknown seller", fandom="Unknown fandom",maintype = "Unknown type",bundle = "Unknown bundle",price = 0,details = "-",stock = "0"):
        super().__init__(seller,fandom,maintype,bundle,price,details)
        self.stock = stock

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
# stockItemAttr = defaultStockItem.makeAttrList()
stockItemAttrLength = defaultStockItem.lenAttr()

############################################################################################################################
#OBJECT INPUT
importObject('stock.csv',stockItem)

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
#Button(root,text = "Input", command=Input).grid(row=5)
#Salesinput button

mainloop()
############################################################################################################################