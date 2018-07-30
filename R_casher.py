#!/usr/bin/env python3
# Copyright 2009-2017 BHG http://bw.org/
import os
from tkinter import *
dir_path = os.path.dirname(__file__)
os.chdir(dir_path)


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
    
    def makeAttributeList(self): 
        attributeList = list(self.__dict__.keys()) 
        return attributeList
    
    def lenAttribute(self):
        attributeLength = len(list(self.__dict__.keys()))
        return attributeLength

#SUB CLASS
class stockItem(Item):
    def __init__(self,seller = "Unknown seller", fandom="Unknown fandom",maintype = "Unknown type",bundle = "Unknown bundle",price = 0,details = "-",stock = "0"):
        super().__init__(seller,fandom,maintype,bundle,price,details)
        self.stock = stock
    
    def storeNewStock(self): #For excel to read
        file = open("stock.csv","a+")
        text = "\n{},{},{},{},{},{},{}".format(self.seller,self.fandom,self.maintype,self.bundle,self.price,self.details,self.stock)
        file.write(text)
        file.close
        
    def convertIntoList(self):
        listTemp = []
        listTemp = [self.seller,self.fandom,self.maintype,self.bundle,self.price,self.details,self.stock]
        return listTemp

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
stockItemAttribute = defaultStockItem.makeAttributeList()
stockItemAttributeLength = defaultStockItem.lenAttribute()

############################################################################################################################
#TKinter
root = Tk()
Label(root, text='Stock list').grid(row = 0,column =3)

#For Labels
i = 0
while i < stockItemAttributeLength:
    title = str(stockItemAttribute[i]).capitalize() 
    Label(root,text=title).grid(row=1,column = i)
    Label(root,text=title).grid(row=3,column = i)
    i += 1

#For Entries
i = 0
boxes = []
while i < stockItemAttributeLength:
    entry = Entry(root)
    entry.grid(row=4, column=i)
    istr = str(i)
    boxes.append(entry)
    i += 1

#For Input new item as an object
def storeInput():
    i = 0
    newStock = []
    while i < stockItemAttributeLength:
        newStock.append(boxes[i].get() )
        i +=1
    newStock = stockItem(newStock[0],newStock[1],newStock[2],newStock[3],newStock[4],newStock[5],newStock[6])
    newStock.storeNewStock()
    newStock.convertIntoList()


Button(root,text = "Input", command=storeInput).grid(row=5)

mainloop()
############################################################################################################################