import csv
import time

def foo():
    print("foo")

def take_csv_return_table( csv_name ):
    File = open( csv_name,'r')
    Table = []
    FileCSV = csv.reader(File, delimiter=",")
    for line in FileCSV:
        Table.append(line)
    File.close()
    return Table

def mdd( input_val ):
    output_val = "-1"
    if( input_val < 10 ):
        output_val = "0" + str( input_val )
    else:
        output_val = input_val
        
    return str(output_val)
    return input_val
    
def find_match_in_table_with_index(match, table, offset_int):
    for row in table:
        if( row[0] == match ):
            return row[offset_int]
    return "ERR"
    
def get_time():
    localtime = time.localtime(time.time())
    hour = str(localtime[3])
    minute = mdd( localtime[4] )

    this_time = hour + ":" + minute
    
    return this_time

def file_initialization():
    this_time = time.localtime(time.time())
    year = str(this_time[0])
    mon = mdd( this_time[1] )
    day = mdd( this_time[2] )
    
    this_date = year + "-" + mon + "-" + day
    record_file_name = "Report-" + this_date + ".csv"
    
    file = open(record_file_name,"a+")
    file.close()
    
    file = open(record_file_name,"r+")
    if file.read() == "":
        file.close()
        
        file = open(record_file_name,"a+")
        file.write( "Time" + "," + "Person" + "," + "Franchise" + "," + "Merch. Type" + "," + "Detail" + "," + "Price" + "\n" )
        file.close()
        
    else:
        file.close()
        
    return record_file_name