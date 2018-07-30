#!/usr/bin/env python3
# Copyright 2009-2017 BHG http://bw.org/
import os
from tkinter import *
dir_path = os.path.dirname(__file__)
os.chdir(dir_path)

stockItemAttr = ["seller","fandom","maintype","bundle","price","details","stock"]

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
    
    def storeNewStock(self): #For excel to read
        if( os.path.isfile("stock.csv") == False ):
            file = open("stock.csv","a+")
            text = ""
            for i in range( stockItemAttrLength ) :
                text += stockItemAttr[i].capitalize() 
                if i < stockItemAttrLength - 1:
                    text += ","
            file.write(text)
            file.close
        
        file = open("stock.csv","a+")
        text = "\n{},{},{},{},{},{},{}".format(self.seller,self.fandom,self.maintype,self.bundle,self.price,self.details,self.stock)
        file.write(text)
        file.close

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

#For Entries
i = 0
boxes = []
while i < stockItemAttrLength:
    entry = Entry(root)
    entry.grid(row=4, column=i)
    istr = str(i)
    boxes.append(entry)
    i += 1

#For Input new item as an object
def storeInput():
    newStockAttr = []
    i = 0
    while i < stockItemAttrLength:
        newStockAttr.append(boxes[i].get() )
        i +=1
    newStock = stockItem(newStockAttr[0],newStockAttr[1],newStockAttr[2],newStockAttr[3],newStockAttr[4],newStockAttr[5],newStockAttr[6])
    newStock.storeNewStock()

Button(root,text = "Input", command=storeInput).grid(row=5)

mainloop()
############################################################################################################################