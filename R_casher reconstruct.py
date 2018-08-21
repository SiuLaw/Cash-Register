#!/usr/bin/env python3
# Copyright 2009-2017 BHG http://bw.org/
import os
import csv
import gc

import operator

from tkinter import *
import tkinter.font as tkFont
import tkinter.ttk as ttk

import sqlite3
from collections import OrderedDict

dir_path = os.path.dirname( __file__ )
os.chdir( dir_path )

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

# Import CSV into ObjectList
def importObject( csvfile, objectClass ):
    # initialize objectList for output
    objectList = [ ]
    
    # Check that csv exists
    if os.path.exists( csvfile ):
        # print( csvfile + " exist." )
        pass
    else:
        print( csvfile + " does not exist." )
        file = open( csvfile , 'w')
        file.close()
        return objectList # if the csv did not exist before, return a empty objectList
    
    # Open csvfile, read and store everything into [table]
    file = open( csvfile, 'r')
    spamreader = csv.reader( file, delimiter = ",")
    
    table = [ ]
    for line in spamreader:
        table.append( line )
        
    # Create a list of objects
    for i in range( len( table ) ):
        line = table[ i ]
        newObject = objectClass( line )
        objectList.append( newObject )
        
    file.close
    
    return objectList

def EntriesInput ( ):
    i = 0
    newList = [ ]
    while i < len( boxes ):
        newList.append( boxes[ i ].get( ) )
        i +=1
    return newList

# Input list -> stored into csv file
def Input( csvfile, objectClass, ItemAttr, newList ):
    newObject = objectClass( )
    objectAttrLength = newObject.lenAttr( )
    del newObject
            
    file = open( csvfile, "a+" )
    text = listToCSVtxt( newList )
    file.write( text )
    file.close

# List -> CSV txt
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

# Erase CSV -> Use ObjectList to restore CSV
def renewCSV ( csvfile, objectClass, ItemAttr, ObjectList, AttrLength):
    print( "Now attemping to renew CSV file" )
    file = open( csvfile , 'w')
    file.close()
    
    ObjectList.reverse()
    while 0 != len( ObjectList ):
        newList = [ ]
        i = 0
        popList = ObjectList.pop()
        while i < AttrLength:
            newList.append ( str( popList.switcher( i ) ) )
            i += 1
        Input( csvfile, objectClass, ItemAttr, newList )
    ObjectList = importObject( csvfile, objectClass )
    
    return ObjectList

    print( "csv is now rewrited." )

# Input entires into newList -> Store newList -> import from CSV -> renew CSV -> renew MLB
def stockInput( ):
    global stockList
    
    newList = EntriesInput( )
    Input ( 'stock.csv', stockItem, stockItemAttr, newList )
    stockList = importObject( 'stock.csv' , stockItem )
    stockList = renewCSV( 'stock.csv', stockItem, stockItemAttr, stockList, stockItemAttrLength )
    MLB( )
    print ( "Stock.csv updated. ")
    
############################################################################################################################
#GUI FUNCTION

# MLB function - Sort content when header is clicked on in MLB
def sortby( tree, col, descending ):
    # Making a list of [column,content]
        # tree.set = returns value of the specific column
        # tree.get_children = returns list of children belonging to items
    data = [ ( tree.set( child, col ), child ) for child in tree.get_children( '' ) ]
    
    # Sorting list
    data.sort( reverse = descending )
    for ix, item in enumerate( data ):
        tree.move( item[ 1 ], '', ix ) # tree.move(item,parent,index), move #item# to position #index# in #parent's# list of children
    
    # tree.heading(column, command = reversed sortby)
    tree.heading( col, command = lambda col = col: sortby( tree, col, int( not descending ) ) )

class MLB( object ):
    # Container created in loop because for updating stocklist
    
    def __init__( self ):
        self.tree = None
        self.titles = [ ]
        self.popup_menu = Menu(container, tearoff = 0 )
        
        # Functions
        self.makeList( )
        self.fillList( )
        self.title( )
        self.scroll( )
        
        # Change stock
        self.changeStockWIN = None
        self.alterStock = None
        self.alterStockBOX = None
        self.objectIndex = None
        
        # Popup window
        self.popup_menu.add_command( label = "Delete", command = self.deleteStock )
        self.popup_menu.add_command( label = "Change Stock", command = self.changeStock )
        self.tree.bind( "<Button-2>", self.popup ) # binding right click to popup window
    
    # Constructing Tree
    def makeList( self ):
        i = 0
        while i < stockItemAttrLength:
            self.titles.append( str( stockItemAttr[ i ] ).capitalize( ) ) 
            i += 1
        self.tree = ttk.Treeview( column = self.titles, show = "headings" )
        
    # Filling Tree
    def fillList( self ):
        global stockList
        global stockItemAttrLength
        
        i = 0
        while i < len( stockList ): 
            q = 0
            stuff = [ ]
            
            # stockList -> List of Object attributes
            while q < stockItemAttrLength: 
                stuff.append( stockList[ i ].switcher( q ) )
                q += 1
            
            # Adding tags
            stuff.append( stockList[ i ] )  # Tagging object name
            stuff.append( i )               # Tagging object index number in stockList
            
            # Insert list of object attributes into tree
            self.tree.insert( '', 'end', values = stuff )
            i += 1
            
        print( "stock display updated" )
    
    # Making title
    def title( self ):
        # col.title = assign headings
        # command = sortby(tree,column, descending = 0)
        
        for col in self.titles:
            self.tree.heading( col, text = col.title(), command = lambda c = col: sortby( self.tree, c, 0 ) )
    
    # Popup window when right clicked
    def popup( self, event ):
        self.popup_menu.post( event.x_root, event.y_root )
    
    # Delete stock
    def deleteStock( self ):
        global stockList
        del_List = [ ]
        
        #Identify selected object(s) index number(s)
        for i in self.tree.selection( ):
            del_objectIndex = int( self.tree.item( i )[ "values" ][ -1 ] )
            del_List.append(del_objectIndex)
            self.tree.delete( i )   # remove from tree
        
        # Remove from stockList
        i = 0
        del_List.reverse( )
        while i != len( del_List ):
            stockList.pop (del_List[i])   
            i += 1
                           
        #renew CSV + MLB
        stockList = renewCSV( 'stock.csv', stockItem, stockItemAttr, stockList, stockItemAttrLength )
        MLB( )
    
    # Change stock
    def changeStock( self ):
        
        # Identify selected object's index number
        i = self.tree.selection( )
        self.objectIndex = int( self.tree.item( i )[ "values" ][ -1 ] )   

        self.changeStockWIN = Tk( )
        
        # change stock WINDOW
        Label( self.changeStockWIN, text = "Now enter the new stock!").pack ( )
        self.alterStockBOX = Entry ( self.changeStockWIN )
        self.alterStockBOX.pack( )
        Button ( self.changeStockWIN, text = "Change Stock", command = self.fetch ).pack( )
    
    # Change stock Pt2 - Fetching new user input 
    def fetch( self ):
        global stockList
        
        # Take input from user and change stock in stockList
        self.alterStock = self.alterStockBOX.get( )
        stockList [ self.objectIndex ].stock = int( self.alterStock )
        
        # renew CSV + MLB
        stockList = renewCSV( 'stock.csv', stockItem, stockItemAttr, stockList, stockItemAttrLength )
        MLB( )
    
    # Vertical scrollbar  
    def scroll( self ):
        vsb = ttk.Scrollbar( orient="vertical", command = self.tree.yview )
        self.tree.configure( yscrollcommand = vsb.set )
        
        self.tree.grid( row = 0, column = 0, sticky = 'nsew', in_ = container )
        vsb.grid      ( row = 0, column = 1, sticky = 'ns'  , in_ = container )
    
        container.grid_columnconfigure( 0, weight = 1 )
        container.grid_rowconfigure   ( 0, weight = 1 )

class sINPUT ( object ):
    
    def __init__( self ):
        global stockList
        
        self.input = None
        self.output = [ ]   # for recording user input and write in CSV 
        self.tempList = [ ] # for .modifier( )    - storing and moving selected List
        self.tempAttr = [ ] # for .radioButton( ) - showing only uniqued attributes
        self.RBList = [ ]   # for storing all the RadioButtons
        self.RBCount = 0    # RadioButton set made
        self.gate = False
        self.v = None
        
        self.filter (0)
        self.modifier (0)
        self.RB(0)
    
    def regulator( self, i ):
        if self.input is True:
            self.gate = True
        else:
            self.gate = False
        print (self.gate)
        print(self.v.get())
        
      
    # Filter for only selected items
    def filter( self, i ):
        self.tempList = [ ]
        
        # Does not filter for Attr0
        if i == 0:
            global stockList
            self.tempList = stockList
            return
        
        # Filter so that only the selected attribute will remain on the list
        else:
            self.tempList = [ ]
            self.input = self.v.get ( )
            
            # Select objects that had the attribute at i location
            for items in self.input, items.switcher(i) == self.input:
                self.tempList.append( items )
 
    # Modify list for radioButton display
    def modifier( self, i):
        
        # Make a list of existing attributes
        self.tempAttr = [ ]
        
        for items in self.tempList:
            self.tempAttr.append( str( items.switcher( i ).capitalize( ) ) )
        
        # Delete duplication from Attr
        self.tempAttr = list(dict.fromkeys( self.tempAttr ) )
        
        # Change List into str + sort list
        for items in self.tempAttr:
            items = str(items)
        self.tempAttr.sort()
    
    def RB( self, i):
        
        self.gate = False
        
        # q = 0
        # for items in self.tempAttr:
        #     self.v = StringVar( )
        #     self.v.set( str(items) )
        #     self.RBList.append( self.v )
        #     Radiobutton(root2, text = str(items), padx = 20, variable = self.v, command = self.regulator( i ), value = q ).pack(side = LEFT)
        #     q += 1
        
        self.v = StringVar( )
        self.v.set( "no selection" )
        
        for displaytext,vv in self.tempAttr:
            Radiobutton( root2, text = displaytext, variable = self.v, value = vv).pack( )
            
# Entry boxes for input
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
    
    #Creating entry boxes
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
            7: self.alternativePrice,
            8: self.time
        }
        return switcher.get( number, 0 )

#For grabbing stuff from 
def readFile( x ):
    file = open( x , "r" )

############################################################################################################################
#BEFORE TKinter

# Deafult StockItem
defaultStockItem = stockItem( )
stockItemAttrLength = defaultStockItem.lenAttr( )
del defaultStockItem

# stockItem's Attributes
stockItemAttr = [ "seller", "fandom", "maintype","bundle","price","details","stock"]

# Importing stockList
stockList = importObject( 'stock.csv', stockItem )

############################################################################################################################
#TKinter

#STOCK TABLE
root = Tk( )

Label( root, text = 'Stock list' ).pack( )

container = ttk.Frame( )
container.pack( fill = "both", expand = True )
mlb = MLB( )

LINE = Frame( root, height = 2, width = 5000, bg = "black" )
LINE.pack( )

Label( root, text = 'New Entries' ).pack( side = "left" )

boxes = entries( root )
Button( root, text = "Input", command = stockInput ).pack( )

#SALES TABLE
root2 = Tk ()

Label (root2, text = "Sales Input").pack()

container2 = ttk.Frame( )
container2.pack()

salesInput = sINPUT( )

#
mainloop( )
############################################################################################################################
