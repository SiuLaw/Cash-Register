import os
import csv
import time
dir_path = os.path.dirname(__file__)
os.chdir(dir_path)
#os.chdir("/Users/Po/Desktop/Python/Convention")

####################################################################################################



def print_h_line( line_length ):
    print_string = ""
    for i in range(0, line_length):
        print_string += "-"
    print( print_string )
    
def print_v_line( string, x_max ):
    print_string = "| " + string
    while len(print_string) < x_max + 3:
        print_string += " "
    print_string += "|"
    print( print_string )
    
def contain_in_box( string_list ):
    y_max = len( string_list )
    x_max = 0
    for y in range(0, y_max ):
        x_max = max(x_max, len(string_list[y]) )
    
    print_h_line( x_max + 4 )
    for y in range(0, y_max ):
        print_v_line( string_list[y], x_max)
    print_h_line( x_max + 4 )
    
def make_double_digit( input_val ):
    if( input_val < 10 ):
        return "0" + str( input_val )
    else:
        return str( input_val )


####################################################################################################

this_time = time.localtime(time.time())
year = str(this_time[0])
mon = make_double_digit( this_time[1] )
day = make_double_digit( this_time[2] )

this_date = year + "-" + mon + "-" + day
record_file_name = "Report-" + this_date + ".csv"
record_file_name

####################################################################################################

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

####################################################################################################

while True:
    
    os.system("clear")
    file = open(record_file_name,'a+')
    
    print("\n" + "Starting from beginning")
    
####################################################################################################
    
#Who is the seller
    while True:
        PersonFile = open('PersonInput.txt','r')
        PersonInput = input(PersonFile.read())
        PersonFile.close()
        
        os.system("clear")
        
        if PersonInput == "F":
            PersonInput = "Fork"
            os.system("clear")
            break
            
        if PersonInput == "L":
            PersonInput = "Lee"
            os.system("clear")
            break
            
        if PersonInput == "O":
            PersonInput = input("Type in name:")
            os.system("clear")
            break
    
        print("Unrecognised person, type 'O' for others")
    
    
####################################################################################################
    
#What is the Fandom
    
    while True:
        try:
            contain_in_box( ["Person:  " + PersonInput] )
            
            FandomFile = open('FandomInput.txt','r')
            FandomInput = int(input(FandomFile.read())) -1
            FandomFile.close()
            
            FandomFile = open('FandomInput.txt','r')
            FandomTable = []
            FandomCSV = csv.reader(FandomFile, delimiter=",")
            for line in FandomCSV:
                FandomTable.append(line)
        
            Fandom = str(FandomTable[FandomInput][1])
            os.system("clear")
            break
            
        except ValueError:
            os.system("clear")
            print("Oops! Choose a number.  Try again...")
            
        except IndexError:
            os.system("clear")
            print("Oops! Choose a valid number. Try again...")
    

    
####################################################################################################
    
#What Price
    
    PriceFile = open('PriceInput.txt','r')
    PriceTable = []
    PriceCSV = csv.reader(PriceFile, delimiter=",")
    for line in PriceCSV:
        PriceTable.append(line)
    PriceFile.close()
    
    
    
    while True:
        try:
            contain_in_box( ["Person:  " + PersonInput, "Fandom:  " + Fandom] )
            
            PriceFile = open('PriceInput.txt','r')
            PriceInput = input(PriceFile.read()+ "\n" + "\n" + "Or type 'O' for alternative pricing (e.g. sales)" +"\n" + "\n" + "\n" + "INPUT: ")
            PriceFile.close()
            if PriceInput == "O":
                os.system("clear")
                while True: #protection for not numeric input for "alternated pricing"
                    try:
                        contain_in_box( ["Person:  " + PersonInput, "Fandom:  " + Fandom] )
                        
                        NewPrice = input("Type in alternated pricing:")
                        Price = int(NewPrice)
                        break
                    except ValueError:
                        os.system("clear")
                        print("Oops! Choose a number.  Try again...")
                    
                
                while True: #protection for AFTER choosing a alternatied pricing, THEN the second time choosing a merch type
                    try:
                        os.system("clear")
                        contain_in_box( ["Person:  " + PersonInput, "Fandom:  " + Fandom, "Price:   " + str(Price) ] )
                        
                        PriceFile = open('PriceInput.txt','r')                
                        PriceInput = int( input("RESELECT:" + "\n" + "\n" + PriceFile.read() + "\n" + "\n" + "INPUT: "   ) ) - 1
                        Type = str(PriceTable[PriceInput][1])                     
                        PriceFile.close()
                        break
                    except ValueError:
                        os.system("clear")
                        print("Oops! Choose a number.  Try again...")
                    except IndexError:
                        os.system("clear")
                        print("Oops! Choose a valid number. Try again...")
                        
            else:
                PriceInput = int(PriceInput) - 1
                Price = int(PriceTable[PriceInput][2])
                Type = str(PriceTable[PriceInput][1])
                        
            PriceFile.close()
            os.system("clear")
            contain_in_box( ["Person:  " + PersonInput, "Fandom:  " + Fandom, "Type:    " + Type, "Price:   " + str(Price) ] )
            break
            
        except ValueError:
            os.system("clear")
            print("Oops! Choose a number.  Try again...")
            
        except IndexError:
            os.system("clear")
            print("Oops! Choose a valid number. Try again...")
         

    
####################################################################################################
    
#Merch
    MerchInput = input("Input details, e.g. Persona characters name, if not leave blank: ")
    os.system("clear")
    
####################################################################################################
    
#Time
    localtime = time.localtime(time.time())
    hour = str(localtime[3])
    minute = make_double_digit( localtime[4] )

    this_time = hour + ":" + minute
    
    
    output = this_time + ',' + PersonInput + ',' + Fandom + ',' + Type + ',' + MerchInput + ',' + str(Price)
    os.system("clear")
    
####################################################################################################
    
# print(output)
    
    contain_in_box( [    "Time:    " + this_time,
                         "Person:  " + PersonInput,
                         "Fandom:  " + Fandom,
                         "Type:    " + Type,
                         "Details: " + MerchInput,
                         "Price:   " + str(Price) ] )

    submit = input("Confirm record sales? Y/N" + "\n")
    os.system("clear")
    if submit == "Y":
        file.write( output + "\n" )
        file.close()
    else:
        print("Sales not recorded, start again.")
        file.close()
    
    Check = input("Press Y to end, enter to continue" + "\n")
   
    if Check == "Y":
        os.system("clear")
        print("Cash register quitted successfully")
        break
    os.system("clear")
    
