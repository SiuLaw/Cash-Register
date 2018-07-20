from imported_functions import take_csv_return_table, find_match_in_table_with_index, file_initialization, get_time

import os

import tkinter as tk
import tkinter.messagebox as tkm



dir_path = os.path.dirname(__file__)
os.chdir(dir_path)

def update_price():
    pri_v.set( int( find_match_in_table_with_index( typ_v.get(), pri_table, 2 ) ))
    root.update()

record_file_name = file_initialization()
per_table = take_csv_return_table( 'PersonInput.txt' )
fan_table = take_csv_return_table( 'FandomInput.txt' )
pri_table = take_csv_return_table( 'PriceInput.txt' )





root = tk.Tk()

root.title("Cashier")
root.resizable(width=False, height=False) #do not let outer window be resized

row_names = ["Person","Fandom","Type","Detail","Price(GBP)"]
r = 0
for row_name in row_names:
    tk.Label(root, text=row_name,relief=tk.SUNKEN,width = 10).grid(row=r,column=0)
    r += 1
    
    

per_frame = tk.Frame(root)
fan_frame = tk.Frame(root)
typ_frame = tk.Frame(root)
pri_frame = tk.Frame(root)
sub_frame = tk.Frame(root)
ent_frame = tk.Frame(root)

per_v = tk.StringVar()
per_v.set(per_table[0][0])
fan_v = tk.StringVar()
fan_v.set(fan_table[0][0])
typ_v = tk.StringVar()
typ_v.set(pri_table[0][0])

pri_v = tk.IntVar()
pri_v.set(-1)

alt_v = tk.IntVar()
alt_v.set(1)




for short_name, long_name in per_table:
    tk.Radiobutton(per_frame, text=long_name, variable=per_v, value=short_name).pack(side=tk.LEFT)
    
tk.Radiobutton(per_frame, text="Other: ", variable=per_v, value="CUS").pack(side=tk.LEFT)
per_entry = tk.Entry(per_frame)
per_entry.pack(side=tk.LEFT)

def focus_per(event):
    per_v.set("CUS")
per_entry.bind("<Button-1>",focus_per)



for short_name, long_name in fan_table:
    tk.Radiobutton(fan_frame, text=long_name, variable=fan_v, value=short_name).pack(side=tk.LEFT)

for short_name, long_name, price in pri_table:
    tk.Radiobutton(typ_frame, text=long_name, variable=typ_v, value=short_name,command=update_price).pack(side=tk.LEFT)

def green_f1():
    f1.config(bg="green")
    pri_def.config(bg="green")
    pri_def_label.config(bg="green")
    
    f2.config(bg="white")
    pri_alt.config(bg="white")
    pri_alt_entry.config(bg="white")
    

def green_f2():
    f2.config(bg="green")
    pri_alt.config(bg="green")
    pri_alt_entry.config(bg="green")
    
    f1.config(bg="white")
    pri_def.config(bg="white")
    pri_def_label.config(bg="white")

f1 = tk.Frame(pri_frame,bg="green")
pri_def = tk.Radiobutton(f1,text="Default price:", variable=alt_v, value=1,bg="green",command=green_f1)
pri_def_label = tk.Label(f1,textvariable=pri_v,bg="green")
pri_def.pack(side=tk.LEFT)
pri_def_label.pack(side=tk.LEFT)

f2 = tk.Frame(pri_frame,bg="white")
pri_alt = tk.Radiobutton(f2,text="Alter. price:", variable=alt_v, value=2,command=green_f2,bg="white")
pri_alt_entry = tk.Entry(f2,bg="white")
pri_alt.pack(side=tk.LEFT)
pri_alt_entry.pack(side=tk.LEFT)

def focus_pri(event):
    alt_v.set(2)
    green_f2()
pri_alt_entry.bind("<Button-1>",focus_pri)



f3 = tk.Label(pri_frame, text="  /  ")

f1.grid(row=0,column=0)
f3.grid(row=0,column=1)
f2.grid(row=0,column=2)




detail_entry = tk.Entry(ent_frame)
detail_entry.pack()

def submit_record():
    this_time = get_time()
    
    if( per_v.get() != "CUS"):        
        person = find_match_in_table_with_index(per_v.get(), per_table, 1)
    else:
        person = per_entry.get()
        
    fandom = find_match_in_table_with_index(fan_v.get(), fan_table, 1)
    mertyp = find_match_in_table_with_index(typ_v.get(), pri_table, 1)
    if(alt_v.get() == 1):
        prices = pri_v.get()
    else:
        prices = pri_alt_entry.get()
        
    detail = detail_entry.get()
    output = this_time + ',' + person + ',' + fandom + ',' + mertyp + ',' + detail + ',' + str(prices)
    
    if tkm.askokcancel('Confirm?', output):
        file = open( record_file_name, "a")
        file.write( output + "\n" )
        file.close()

        tkm.showinfo('Submitted', 'Record submitted')
    

tk.Button(sub_frame,text="Submit",command=submit_record).pack()



per_frame.grid(row=0,column=1)
fan_frame.grid(row=1,column=1)
typ_frame.grid(row=2,column=1)
ent_frame.grid(row=3,column=1)
pri_frame.grid(row=4,column=1)
sub_frame.grid(row=5,column=1)

def ret(event):
    submit_record()

root.bind("<Return>", ret)

update_price()
root.mainloop()