from tkinter import *
import report as rp
import time




root = Tk()

root.title("Cashier")
root.resizable(width=False, height=False) #do not let outer window be resized

row_names = ["Person","Fandom","Type","Price"]
r = 0
for row_name in row_names:
    Label(root, text=row_name,relief=SUNKEN,width = 10).grid(row=r,column=0)
    r += 1

per_frame = Frame(root)
fan_frame = Frame(root)
typ_frame = Frame(root)
pri_frame = Frame(root)
sub_frame = Frame(root)

per_v = StringVar()
fan_v = StringVar()
typ_v = StringVar()
pri_v = IntVar()





per_table = rp.take_csv_return_table( 'PersonInput.txt' )
per_v.set(per_table[0][0])
for short_name, long_name in per_table:
    Radiobutton(per_frame, text=long_name, variable=per_v, value=short_name).pack(side=LEFT)


fan_table = rp.take_csv_return_table( 'FandomInput.txt' )
fan_v.set(fan_table[0][0])
for short_name, long_name in fan_table:
    Radiobutton(fan_frame, text=long_name, variable=fan_v, value=short_name).pack(side=LEFT)

pri_table = rp.take_csv_return_table( 'PriceInput.txt' )
typ_v.set(pri_table[0][0])






def make_double_digit( input_val ):
    if( input_val < 10 ):
        return "0" + str( input_val )
    else:
        return str( input_val )

def find_match_in_table_with_index(match, table, offset_int):
    for row in table:
        if( row[0] == match ):
            return row[offset_int]
    return "ERR"

def get_time():
    localtime = time.localtime(time.time())
    hour = str(localtime[3])
    minute = make_double_digit( localtime[4] )

    this_time = hour + ":" + minute
    
    return this_time

def file_initialization():
    this_time = time.localtime(time.time())
    year = str(this_time[0])
    mon = rp.make_double_digit( this_time[1] )
    day = rp.make_double_digit( this_time[2] )
    
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

def update_price():
    pri_v.set( int( find_match_in_table_with_index( typ_v.get(), pri_table, 2 ) ))
    root.update()


for short_name, long_name, price in pri_table:
    rb = Radiobutton(typ_frame, text=long_name, variable=typ_v, value=short_name,command=update_price)
    rb.pack(side=LEFT)
    
pri_v.set(-1)
pri_label = Label(pri_frame,textvariable=pri_v).pack()




record_file_name = file_initialization()

def submit_record():
    print("record submitted")
    this_time = get_time()
    person = find_match_in_table_with_index(per_v.get(), per_table, 1)
    fandom = find_match_in_table_with_index(fan_v.get(), fan_table, 1)
    mertyp = find_match_in_table_with_index(typ_v.get(), pri_table, 1)
    prices = pri_v.get()
    detail = ""
    output = this_time + ',' + person + ',' + fandom + ',' + mertyp + ',' + detail + ',' + str(prices)
    
    file = open( record_file_name, "a")
    file.write( output + "\n" )
    file.close()
    


Button(sub_frame,text="Submit",command=submit_record).pack()


per_frame.grid(row=0,column=1)
fan_frame.grid(row=1,column=1)
typ_frame.grid(row=2,column=1)
pri_frame.grid(row=3,column=1)
sub_frame.grid(row=4,column=1)

update_price()
        
root.mainloop()