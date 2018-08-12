#!/usr/bin/env python3
# Copyright 2009-2017 BHG http://bw.org/
import os
import csv
import gc
import operator
from tkinter import *
import TkTreectrl as treectrl
import tkinter.font as tkFont
import tkinter.ttk as ttk
import sqlite3

dir_path = os.path.dirname( __file__ )
os.chdir( dir_path )

stockItemAttr = [ "seller", "fandom", "maintype","bundle","price","details","stock"]

############################################################################################################################
#NOTE

#lambda
    # one time code
    # BLUEPRINT >>> lambda argument: manipulation( argument )
    
############################################################################################################################
#FUNCTIONS

# Converting empty input into default value
def inputOrDefault( inp_val, def_val ):
    if inp_val == "":
        return def_val
    else:
        return inp_val

# Read csvfile -> list -> objects
def importObject( csvfile, objectClass ):
    # initialize the objectList for output
    objectList = [ ]
    
    # Stop the import if the csvfile does not exist
    if ( os.path.isfile( csvfile ) == False ):
        print( "There are no existing csv file named: " + csvfile )
        return objectList
    
    # Open csvfile, read and store everything into [table]
    file = open( csvfile, 'r')
    spamreader = csv.reader( file, delimiter = ",")
    table = [ ]
    for line in spamreader:
        table.append( line )
    
    # Create a list of objects
    col_title_passed = False
    for i in range( len( table ) ):
        line = table[ i ]
        if( col_title_passed == False ):
            col_title_passed = True
            continue
        newObject = objectClass( line )
        objectList.append( newObject )
        
    file.close
    
    return objectList

# Create list of objects
def objectintoList ( x, objectClass ):
    olist = [ ]
    for things in x:
        if isinstance( things, objectClass ):
            olist.append( things )
    olist = sortList( olist )
    return olist

# input stock + renew stockList
def stockInput( ):
    Input( 'stock.csv', stockItem, stockItemAttr )
    stockList = importObject( 'stock.csv', stockItem )
    MLB( root, stockList )

# Part of input
def listToCSVtxt( input_list ):
    output_text = ""
    length = len( input_list )
    for i in range( length ):
        output_text += input_list[ i ]
        if i < length - 1:
            output_text += ","
        else:
            output_text += "\n"
    return output_text 

# Input -> list -> stored into csv file
def Input( csvfile, objectClass, ItemAttr ): 
    newAttr = [ ]
    i = 0
    newObject = objectClass( )
    objectAttrLength = newObject.lenAttr( )
    
    #turning input into list
    while i < objectAttrLength:
        newAttr.append( boxes[ i ].get( ) )
        i +=1
    
    #turning storing list via listToCSVtxt
    if( os.path.isfile( csvfile ) == False ):
            file = open( csvfile, "a+" )
            text = listToCSVtxt( ItemAttr ) 
            file.write( text ) 
            file.close
            
    file = open( csvfile, "a+" )
    text = listToCSVtxt( newAttr )
    file.write( text )
    file.close

def sortList( objectList ):
    objectList_sorted = sorted( objectList, key = operator.attrgetter( 'maintype' ))
    objectList_sorted = sorted( objectList, key = operator.attrgetter( 'fandom' ))
    objectList_sorted = sorted( objectList, key = operator.attrgetter( 'seller' ))
    return objectList_sorted

def printObjectList( objectList ):
    for obj in objectList:
        print( obj.__dict__ )

############################################################################################################################
#GUI FUNCTION

# MLB function - Sort content when header is clicked on in MLB
def sortby( tree, col, descending ):
    # Making a list of [column,content]
        # tree.set = returns value of the specific column
        # tree.get_children = returns list of children belonging to items
    data = [( tree.set( child, col ), child ) for child in tree.get_children('')]
    
    # Sorting list
    data.sort( reverse = descending )
    for ix, item in enumerate( data ):
        tree.move( item[ 1 ], '', ix ) # tree.move(item,parent,index), move #item# to position #index# in #parent's# list of children
    
    # tree.heading(column, command = reversed sortby)
    tree.heading( col, command = lambda col = col: sortby( tree, col, int( not descending ) ) )

class MLB(object):
    # Container created in loop because for updating stocklist
    
    def __init__(self):
        self.tree = None
        self.titles = [ ]
        self.popup_menu = Menu(container, tearoff = 0 )
        
        # functions
        self.makeList()
        self.fillList()
        self.title()
        self.scroll()
        
        # popup
        self.popup_menu.add_command( label = "Delete", command = self.deleteStock )
        self.popup_menu.add_command( label = "Stock", command = self.changeStock )
        self.tree.bind( "<Button-2>", self.popup ) 
    
    # Constructing Tree
    def makeList(self):
        i = 0
        while i < stockItemAttrLength:
            self.titles.append( str( stockItemAttr[ i ] ).capitalize( ) ) 
            i += 1
        self.tree = ttk.Treeview( column = self.titles, show = "headings" )
        
    # Filling Tree
    def fillList(self):
        i = 0
        while i < len( stockList ): 
            q = 0
            while q < stockItemAttrLength: #
                stuff = [ ]
                for things in stockList:
                    stuff.append( stockList[ i ].switcher( q ) )
                    q += 1
                self.tree.insert( '', 'end', values = stuff )
            i += 1
        print( "stock display updated" )
    
    #Making title
        # col.title = assign headings
        # command = sortby(tree,column, descending = 0)
    def title(self):
        for col in self.titles:
            self.tree.heading( col, text = col.title(), command = lambda c = col: sortby( self.tree, c, 0 ) )
    
    def popup(self, event):
        self.popup_menu.post(event.x_root, event.y_root)
    
    def deleteStock(self):
        # for all items selected in tree
        for i in self.tree.selection():
            self.tree.delete(i)
    
    def changeStock(self):
        newWin = Toplevel()
        newWin.wm_title("Change Stock")
        Label(newWin, text = "Enter new stock number: \n").pack()
        stockEntry = Entry(newWin).pack()
        Button(newWin,text = "Input").pack()
    
    # Vertical scrollbar  
    def scroll(self):
        vsb = ttk.Scrollbar( orient="vertical", command = self.tree.yview )
        self.tree.configure( yscrollcommand = vsb.set )
        
        self.tree.grid( row = 0, column = 0, sticky = 'nsew', in_ = container )
        vsb.grid      ( row = 0, column = 1, sticky = 'ns'  , in_ = container )
    
        container.grid_columnconfigure( 0, weight = 1 )
        container.grid_rowconfigure   ( 0, weight = 1 )
        
def entries( root ):
    container = Frame ( bg = "white" )
    container.pack( fill = "both", expand = True )
    
    #Creating labels
    i = 0
    while i < stockItemAttrLength:
        title = str( stockItemAttr[ i ] ).capitalize( ) 
        Label( root, text = title ).grid( row = 0, column = i, in_ = container )
        Label( root, text = title ).grid( row = 0, column = i, in_ = container )
        i += 1
    
    #Creating entries boxes
    i = 0
    boxes = [ ]
    while i < stockItemAttrLength:
        entry = Entry( root )
        entry.grid( row = 1, column = i, in_ = container )
        istr = str( i )
        boxes.append( entry )
        i += 1
    return boxes

    print( "label display updated" )
    
############################################################################################################################
#MAIN CLASS
class Item:
    
    def __init__( self, *args ): #*args = for any number of arguments
        # DEFAULT VALUES
        self.seller   = "Unknown seller"
        self.fandom   = "Unknown fandom"
        self.maintype = "Unknown type"
        self.bundle   = "Unknown bundle"
        self.price    = 0
        self.details  = "-"
        
        if len( args ) >= 6:
            # When the args are input as individually ( i.e. Item( seller, fandom, maintype, bundle, price, details ) )
            self.initializeFromArgs( *args )
        elif len( args ) == 1:
            # When there is only one input, then check that it is a list
            if( isinstance( args[ 0 ], list ) ):
                self.initializeFromList( args[ 0 ] )
            else:
                print( "Only one input and not list" )
        else:
            pass
            
    # Set the attr values with the 6 arguments
    def initializeFromArgs( self, *args ):

        self.seller   = inputOrDefault( args[0], "Unknown seller" )
        self.fandom   = inputOrDefault( args[1], "Unknown fandom" )
        self.maintype = inputOrDefault( args[2], "Unknown type" )
        self.bundle   = inputOrDefault( args[3], "Unknown bundle" )
        self.price    = inputOrDefault( args[4], 0 ) 
        self.details  = inputOrDefault( args[5], "-" )
        
    # Set the attr values with the single "list" arguments
    def initializeFromList( self, argList ):
        self.seller   = inputOrDefault( argList[0], "Unknown seller" )
        self.fandom   = inputOrDefault( argList[1], "Unknown fandom" )
        self.maintype = inputOrDefault( argList[2], "Unknown type" )
        self.bundle   = inputOrDefault( argList[3], "Unknown bundle" )
        self.price    = inputOrDefault( argList[4], 0 ) 
        self.details  = inputOrDefault( argList[5], "-" )
    
    # Amount of attribute, for number of loops needed
    def lenAttr( self ):
        attrLength = len( list( self.__dict__.keys( ) ) )
        return attrLength
    
#SUB CLASS
class stockItem( Item ):
    
    def __init__( self, *args ):
        self.stock = "0"
        super( ).__init__( *args ) #inherit all arguments from class Item
        
        # Dealing with the extra input of "stock", unique to the stockItem class
        if( len( args ) == 7 ):
            self.stock = inputOrDefault( args[ 6 ], 0 )
        elif len( args ) == 1:
            if isinstance( args[ 0 ], list ):
                self.stock = inputOrDefault( args[ 0 ][ 6 ], 0 )
    
    #calling attributes with number
    def switcher( self, number ):
        switcher = {
            0: self.seller,
            1: self.fandom,
            2: self.maintype,
            3: self.bundle,
            4: self.price,
            5: self.details,
            6: self.stock
        }
        return switcher.get( number, 0 )
    
    def changestock (self, newStock ):
        pass
        
    def sales( self ):
        self.stock = int( self.stock ) - 1
        
class salesItem( Item ):
    
    def __init__( self, *args ):
        self.discount = False
        self.alternativePrice = 0
        super().__init__( *args )
        
    def switcher( self, number ):
        switcher = {
            0: self.seller,
            1: self.fandom,
            2: self.maintype,
            3: self.bundle,
            4: self.price,
            5: self.details,
            6: self.discount,
            7: self.alternativePrice
        }
        return switcher.get( number, 0 )

#For grabbing stuff from 
def readFile( x ):
    file = open( x , "r" )
  
############################################################################################################################
#DEFAULT ITEMS

#Deafult StockItem
defaultStockItem = stockItem( )
stockItemAttrLength = defaultStockItem.lenAttr( )
del defaultStockItem

############################################################################################################################
#OBJECT INPUT
#Object into list
objectList = importObject( 'stock.csv', stockItem )
allObject = gc.get_objects( )
stockList = objectintoList ( allObject, stockItem )
############################################################################################################################
#TKinter
root = Tk( )

Label( root, text = 'Stock list' ).pack( )

container = ttk.Frame( )
container.pack( fill = "both", expand = True )
MLB = MLB( )

LINE = Frame( root, height = 2, width = 5000, bg = "black" )
LINE.pack( )

Label( root, text = 'New Entries' ).pack( side = "left" )

boxes = entries( root )
Button( root, text = "Input", command = stockInput ).pack( )

mainloop( )
############################################################################################################################